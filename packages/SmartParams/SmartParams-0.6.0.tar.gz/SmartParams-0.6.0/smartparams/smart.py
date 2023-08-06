import inspect
import re
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from smartparams.cli import Print, parse_arguments
from smartparams.io import load_data, print_data, save_data
from smartparams.utils import (
    check_key_override,
    check_missing_values,
    check_params_name_override,
    check_params_type,
    convert_to_primitive_types,
    flatten_keys,
    get_class_name,
    get_nested_dictionary_and_key,
    import_class,
    join_class,
    join_key,
    parse_class,
    parse_param,
)

_T = TypeVar('_T')


class Smart(Generic[_T]):
    def __init__(
        self,
        _class: Optional[Type[_T]] = None,
        /,
        **params: Any,
    ) -> None:
        self._class: Optional[Type[_T]] = _class
        self._params: Dict[str, Any] = dict()

        self._keyword = 'class'
        self._missing_value = '???'

        self._location = ''

        self._check_missings = True
        self._check_typings = True
        self._check_overrides = True

        self._allow_only_registered = False

        self._aliases: Dict[str, str] = dict()
        self._origins: Dict[str, str] = dict()

        for k, v in params.items():
            self.set(k, v)

    @property
    def type(self) -> Optional[Type[_T]]:
        return self._class

    @property
    def params(self) -> Dict[str, Any]:
        return self._params.copy()

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> _T:
        if self._class is None:
            raise AttributeError("Class is not set.")

        params = self._instantiate_dict(
            dictionary=self._params,
            location=self._location,
        )

        if self._check_overrides:
            check_params_name_override(
                params=params,
                kwargs=kwargs,
                location=join_class(self._location, get_class_name(self._class)),
            )

        params.update(kwargs)

        return self._instantiate_class(
            location=self._location,
            cls=self._class,
            args=args,
            kwargs=params,
        )

    def __str__(self) -> str:
        cls_str = "" if self._class is None else f"[{get_class_name(self._class)}]"
        params_str = ", ".join((f"{k}={v}" for k, v in self._params.items()))
        return f"{self.__class__.__name__}{cls_str}({params_str})"

    def __repr__(self) -> str:
        return str(self)

    def keys(
        self,
        flatten: bool = False,
        pattern: Optional[str] = None,
    ) -> Tuple[str, ...]:
        keys = flatten_keys(self._params) if flatten else self._params
        if pattern is not None:
            return tuple(key for key in keys if re.fullmatch(pattern, key))
        return tuple(keys)

    def items(
        self,
        flatten: bool = False,
        pattern: Optional[str] = None,
    ) -> Tuple[Tuple[str, Any], ...]:
        return tuple((k, self.get(k)) for k in self.keys(flatten, pattern))

    def get(
        self,
        name: str,
        default: Optional[Any] = None,
        required: bool = False,
    ) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
            required=required,
        )
        return dictionary.get(key, default)

    def set(
        self,
        name: str,
        value: Any,
    ) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
            set_mode=True,
        )
        dictionary[key] = value
        return value

    def pop(
        self,
        name: str,
        default: Optional[Any] = None,
        required: bool = False,
    ) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
            required=required,
        )
        return dictionary.pop(key, default)

    def map(
        self,
        name: str,
        function: Callable,
    ) -> Any:
        dictionary, key = get_nested_dictionary_and_key(
            dictionary=self._params,
            name=name,
            required=True,
        )
        dictionary[key] = value = function(dictionary[key])
        return value

    def update_from(
        self,
        source: Union['Smart', Dict[str, Any], List[str], Path],
        name: Optional[str] = None,
        override: bool = True,
        required: bool = True,
    ) -> 'Smart':
        smart: Smart
        if isinstance(source, Smart):
            smart = source
        elif isinstance(source, dict):
            smart = Smart(**source)
        elif isinstance(source, list):
            smart = Smart(**dict(map(parse_param, source)))
        elif isinstance(source, Path):
            smart = Smart(**load_data(source))
        else:
            raise TypeError(f"Source type '{type(source)}' is not supported.")

        if name is None:
            _flatten_keys = self.keys(flatten=True)
            for key in smart.keys(flatten=True):
                if override or not check_key_override(key, _flatten_keys):
                    self.set(key, smart.get(key, required=True))
        else:
            try:
                self.update_from(
                    source=smart.get(name, default=dict(), required=required),
                    override=override,
                )
            except Exception as e:
                raise RuntimeError(f"Cannot update with source name '{name}'. " + ' '.join(e.args))

        return self

    def instantiate(
        self,
        name: Optional[str] = None,
        persist: bool = True,
    ) -> Any:
        obj = self._instantiate(
            obj=self.params if name is None else self.get(name),
            location=self._location,
        )

        if persist and name is not None:
            return self.set(name, obj)

        return obj

    def representation(
        self,
        skip_defaults: bool = False,
        merge_params: bool = False,
    ) -> Dict[str, Any]:
        smart: Smart = Smart()

        if merge_params:
            smart.update_from(self)

        smart.update_from(
            source=self._representation(
                obj=self._class,
                skip_default=skip_defaults,
            ),
            override=False,
        )

        return convert_to_primitive_types(
            obj=smart.params,
            missing_value=self._missing_value,
        )

    def register(
        self,
        classes: Union[
            Sequence[Union[str, Type[Any]]],
            Mapping[str, str],
            Mapping[Type[Any], str],
            Mapping[Union[str, Type[Any]], str],
        ],
        prefix: str = '',
    ) -> 'Smart':
        if self._location:
            msg = f"Classes can only be registered in root Smart object, not in {self._location}."
            raise AttributeError(msg)

        if isinstance(classes, Sequence):
            self._register_classes(
                classes=classes,
                prefix=prefix,
            )
        elif isinstance(classes, Mapping):
            self._register_aliases(
                aliases=classes,
                prefix=prefix,
            )
        else:
            raise TypeError(f"Register classes type '{type(classes)}' is not supported.")

        return self

    def run(
        self,
        function: Callable[['Smart'], Any],
        path: Path = Path('params.yaml'),
    ) -> 'Smart':
        args = parse_arguments(default_path=path)

        if args.path.is_file():
            self.update_from(args.path)

        self.update_from(args.params)

        if args.dump:
            save_data(
                data=self.representation(
                    skip_defaults=args.skip_defaults,
                    merge_params=args.merge_params,
                ),
                path=args.path,
            )
        elif args.print:
            if args.print == Print.PARAMS:
                print_data(
                    data=self.representation(
                        skip_defaults=args.skip_defaults,
                        merge_params=args.merge_params,
                    ),
                    fmt=args.format,
                )
            elif args.print == Print.KEYS:
                print_data(
                    data=self.keys(flatten=True),
                    fmt=args.format,
                )
            else:
                raise NotImplementedError(f"Print '{args.print}' has not been implemented yet.")
        else:
            function(self)

        return self

    def copy(self) -> 'Smart[Type[_T]]':
        return Smart(self.type, **self.params).setup(smart=self)

    def setup(
        self,
        smart: Optional['Smart'] = None,
        *,
        keyword: Optional[str] = None,
        missing_value: Optional[str] = None,
        location: Optional[str] = None,
        check_missings: Optional[bool] = None,
        check_typings: Optional[bool] = None,
        check_overrides: Optional[bool] = None,
        allow_only_registered: Optional[bool] = None,
    ) -> 'Smart':
        if keyword is not None:
            self._keyword = keyword
        elif smart is not None:
            self._keyword = smart._keyword

        if missing_value is not None:
            self._missing_value = missing_value
        elif smart is not None:
            self._missing_value = smart._missing_value

        if location is not None:
            self._location = location
        elif smart is not None:
            self._location = smart._location

        if check_missings is not None:
            self._check_missings = check_missings
        elif smart is not None:
            self._check_missings = smart._check_missings

        if check_typings is not None:
            self._check_typings = check_typings
        elif smart is not None:
            self._check_typings = smart._check_typings

        if check_overrides is not None:
            self._check_overrides = check_overrides
        elif smart is not None:
            self._check_overrides = smart._check_overrides

        if allow_only_registered is not None:
            if allow_only_registered:
                self._allow_only_registered = True
            elif self._allow_only_registered:
                raise AttributeError("Cannot disallow only registered classes if already allowed.")
        elif smart is not None:
            self._allow_only_registered = smart._allow_only_registered

        if smart is not None:
            self._aliases = smart._aliases
            self._origins = smart._origins

        return self

    def _instantiate(self, obj: Any, location: str) -> Any:
        if isinstance(obj, dict):
            if self._keyword in obj:
                return self._instantiate_class_from_dict(
                    dictionary=obj,
                    location=location,
                )

            return self._instantiate_dict(
                dictionary=obj,
                location=location,
            )

        if isinstance(obj, list):
            return self._instantiate_list(
                lst=obj,
                location=location,
            )

        return obj

    def _instantiate_dict(self, dictionary: Dict[str, Any], location: str) -> Dict[str, Any]:
        return {
            key: self._instantiate(
                obj=value,
                location=join_key(location, key),
            )
            for key, value in dictionary.items()
        }

    def _instantiate_list(self, lst: List[Any], location: str) -> List[Any]:
        return [
            self._instantiate(
                obj=element,
                location=join_key(location, str(index)),
            )
            for index, element in enumerate(lst)
        ]

    def _instantiate_class_from_dict(
        self,
        dictionary: Dict[str, Any],
        location: str,
    ) -> Any:
        kwargs, class_name, option = parse_class(
            dictionary=dictionary,
            keyword=self._keyword,
        )

        if class_name == self.__class__.__name__:
            return self._instantiate_class(
                location=location,
                cls=Smart,
                kwargs=kwargs,
            )

        if class_name in self._origins:
            class_name = self._origins[class_name]
        elif self._allow_only_registered:
            raise ImportError(f"Class '{class_name}' is not registered.")

        cls = cast(Type[_T], import_class(class_name))

        if option:
            if option == self.__class__.__name__:
                return self._instantiate_class(
                    location=location,
                    cls=Smart,
                    args=(cls,),
                    kwargs=kwargs,
                )
            else:
                raise ValueError(f"Option '{option}' is not supported.")
        else:
            return self._instantiate_class(
                location=location,
                cls=cls,
                kwargs=kwargs,
            )

    def _instantiate_class(
        self,
        location: str,
        cls: Type[Any],
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        class_location = join_class(location, get_class_name(cls))
        args = args or tuple()
        kwargs = kwargs or dict()

        if self._check_missings:
            check_missing_values(
                location=class_location,
                kwargs=kwargs,
                missing_value=self._missing_value,
            )

        if self._check_typings:
            check_params_type(
                cls=cls,
                args=args,
                kwargs=kwargs,
                location=class_location,
            )

        try:
            obj = cls(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Error during instantiate {class_location} class.") from e
        else:
            if isinstance(obj, Smart):
                obj.setup(
                    smart=self,
                    location=location,
                )

            return obj

    def _representation(
        self,
        obj: Any,
        skip_default: bool = False,
    ) -> Dict[str, Any]:
        representation: Dict[str, Any] = dict()
        signature = inspect.signature(obj)

        for name, param in signature.parameters.items():
            if name != 'self' and param.kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                annotation = param.annotation
                default = param.default

                if annotation is Smart or isinstance(default, Smart) and default.type is None:
                    representation[name] = {
                        self._keyword: self.__class__.__name__,
                    }
                elif get_origin(annotation) is Smart or isinstance(default, Smart):
                    if isinstance(default, Smart):
                        param_type = default.type
                    else:
                        param_type, *_ = get_args(annotation)

                    keyword = inspect.formatannotation(param_type)
                    keyword = self._aliases.get(keyword, keyword)
                    keyword = join_class(keyword, get_class_name(self))

                    representation[name] = {
                        self._keyword: keyword,
                        **self._representation(
                            obj=param_type,
                            skip_default=skip_default,
                        ),
                    }
                elif default is not inspect.Parameter.empty and skip_default:
                    continue
                elif default is None or isinstance(default, (bool, float, int, str)):
                    representation[name] = default
                elif annotation is not inspect.Parameter.empty and isinstance(annotation, type):
                    if annotation in (bool, float, int, str):
                        representation[name] = annotation.__name__ + self._missing_value
                    else:
                        keyword = inspect.formatannotation(annotation)
                        keyword = self._aliases.get(keyword, keyword)
                        representation[name] = {
                            self._keyword: keyword,
                            **self._representation(
                                obj=annotation,
                                skip_default=skip_default,
                            ),
                        }
                else:
                    representation[name] = self._missing_value

        return representation

    def _register_classes(
        self,
        classes: Sequence[Union[str, Type[Any]]],
        prefix: str = '',
    ) -> None:
        self._register_aliases(
            aliases={cls: cls if isinstance(cls, str) else get_class_name(cls) for cls in classes},
            prefix=prefix,
        )

    def _register_aliases(
        self,
        aliases: Union[
            Mapping[str, str],
            Mapping[Type[Any], str],
            Mapping[Union[str, Type[Any]], str],
        ],
        prefix: str = '',
    ) -> None:
        for origin, alias in aliases.items():
            origin = origin if isinstance(origin, str) else inspect.formatannotation(origin)

            if origin in self._aliases:
                raise ValueError(f"Origin '{origin}' has been overridden.")

            if alias in self._origins:
                raise ValueError(f"Alias '{alias}' has been overridden.")

            alias = join_key(prefix, alias)

            self._aliases[origin] = alias
            self._origins[alias] = origin
