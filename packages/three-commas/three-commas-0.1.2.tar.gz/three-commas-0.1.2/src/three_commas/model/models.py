from __future__ import annotations
from typing import List, Union, Callable, TypeVar, Any, Generic, Optional
import datetime
import functools
import logging
from .. import configuration


logger = logging.getLogger(__name__)

T = TypeVar('T')


class ThreeCommasParser:
    DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S.%fZ'

    @staticmethod
    def parsed_timestamp(func: Callable[[Any], Any]) -> Callable[[Any], Union[None, str, datetime.datetime]]:
        @functools.wraps(func)
        def wrapper(*args, parsed: bool = None, **kwargs) -> Union[None, str, datetime.datetime]:
            timestamp = func(*args, **kwargs)
            if timestamp is None:
                return None
            if parsed is None:
                parsed = configuration.THREE_COMMAS_AUTO_PARSE_DATETIME_DEFAULT
            return datetime.datetime.strptime(timestamp, ThreeCommasParser.DATETIME_PATTERN) if parsed else timestamp
        return wrapper

    @staticmethod
    def parsed(t: T):
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any],  Union[T, None]]:
            @functools.wraps(func)
            def wrapper(*args, parsed: bool = None, **kwargs) -> Union[T, str, None]:
                result = func(*args, **kwargs)
                if result is None:
                    return None
                if parsed is None:
                    parsed = configuration.THREE_COMMAS_AUTO_PARSE_DEFAULT
                return t(result) if parsed else result
            return wrapper
        return decorator

    @staticmethod
    def get_setter_with_getter(getter: Callable) -> Callable:
        """
        this assumes that the setter exists and has the same name convention. the 'g' is replaces with 's'
        """
        getter_name: str = getter.__name__
        setter_name = 's' + getter_name[1:]

        print()
        print(getter)
        print(getter.__globals__)
        print(dir(getter))
        print(getter.__dict__)

        instance_of_getter: dict = getter.__self__
        setter = dir(instance_of_getter)[setter_name]
        return setter
        # setting the result back
        # instance_of_method: dict = func.__self__
        # parameter = None
        # if len(args) == 1:
        #     parameter = args[0]
        # elif len(kwargs) == 1:
        #     parameter = kwargs.popitem()[1]
        #
        # if not isinstance(instance_of_method, dict):
        #     logger.warning(f'Enclosing instance is not a dict, cant set the lazy parsed result back')
        # elif not parameter:
        #     logger.warning(f'Could not determine the parameter from {args=}, {kwargs=}')
        # elif parameter not in instance_of_method:
        #     logger.warning(f'{parameter} was not found in the instance {instance_of_method}')
        # else:
        #     instance_of_method[parameter] = parsed_result

    @staticmethod
    def lazy_parsed_wip(t: Union[type, List]):
        def decorator(getter: Callable) -> Callable:
            was_parsed = False

            @functools.wraps(getter)
            def wrapper(*args, parsed: bool = True, **kwargs):
                nonlocal was_parsed
                if was_parsed or not parsed:
                    return getter(*args, **kwargs)

                result = getter(*args, **kwargs)
                was_parsed = True
                if result is None:
                    return None

                if str(t).startswith('typing.List['):
                    elem_type = t.__args__[0]
                    # TODO probably should not use the __init__ of the type
                    parsed_result = [elem_type(elem) for elem in result]
                else:
                    parsed_result = t(result)

                # setter = ThreeCommasParser.get_setter_with_getter(getter=getter)
                # setter(parsed_result)

                return parsed_result
            return wrapper
        return decorator

    @staticmethod
    def lazy_parsed(t: Union[type, List]):
        def decorator(getter: Callable) -> Callable:
            @functools.wraps(getter)
            def wrapper(*args, parsed: bool = True, **kwargs):
                result = getter(*args, **kwargs)
                if result is None:
                    return None
                if not parsed:
                    return result
                if str(t).startswith('typing.List['):
                    elem_type = t.__args__[0]
                    parsed_result = [elem_type(elem) for elem in result]
                else:
                    parsed_result = t(result)
                return parsed_result
            return wrapper
        return decorator


class ThreeCommasDict(dict):
    def __init__(self, d: dict = None):
        if d is None:
            return
        super().__init__(d)

    @classmethod
    def of(cls, d: dict) -> Union[None, cls]:
        if d is None:
            return None
        return cls(d)

    @classmethod
    def of_list(cls, list_of_d: List[dict]) -> List[cls]:
        if list_of_d is None:
            return None
        return [cls(d) for d in list_of_d]

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'


class ThreeCommasModel(ThreeCommasDict):
    def __getattr__(self, name):
        proxy_type = self.__class__.parsing_map.get(name)
        if proxy_type is QuestionMarkProxy:
            return self.get(name + '?')
        item = self.get(name)
        if item is None:
            return None
        if proxy_type is None:
            return item
        try:
            return proxy_type(item)
        except ValueError:
            return item

    def __setattr__(self, key, value):
        self[key] = value


class StrIntProxy(int):
    def parsed(self, parsed: bool) -> Union[str, int]:
        return self if parsed else str(self)


class StrFloatProxy(float):
    def parsed(self, parsed: bool) -> Union[str, float]:
        return self if parsed else str(self)


class StrDatetimeProxy(str):
    DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S.%fZ'

    def parsed(self, parsed: bool) -> Union[str, datetime]:
        return datetime.datetime.strptime(self, StrDatetimeProxy.DATETIME_PATTERN) if parsed else self


class QuestionMarkProxy:
    pass
