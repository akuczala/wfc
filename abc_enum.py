import abc
import enum


# source: https://stackoverflow.com/questions/54893595/abstract-enum-class-using-abcmeta-and-enummeta
class ABCEnumMeta(abc.ABCMeta, enum.EnumMeta):

    def __new__(mcls, *args, **kw):
        cls = super().__new__(mcls, *args, **kw)
        if issubclass(cls, enum.Enum) and getattr(cls, "__abstractmethods__", None):
            raise TypeError("...")
        return cls

    def __call__(cls, *args, **kw):
        if getattr(cls, "__abstractmethods__", None):
            raise TypeError(f"Can't instantiate abstract class {cls.__name__} "
                            f"with frozen methods {set(cls.__abstractmethods__)}")
        return super().__call__(*args, **kw)
