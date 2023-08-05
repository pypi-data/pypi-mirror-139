#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cachingobject.py
An abstract class which creates properties for this class automatically.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Callable
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..types_ import AnyCallable
from ..bases import BaseObject
from .metaclasses import CachingObjectMeta
from .caches import TimedSingleCache, TimedKeylessCache, TimedCache, BaseTimedCache


# Definitions #
# Classes #
class CachingObjectMethod(BaseTimedCache):
    """A timed cache wrapper for a method which includes extra control from the object."""

    # Instance Methods #
    # Object Calling
    def caching_call(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the caching function, clears the cache at certain time, and allows the owning object to override.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        # Get the object to operate on.
        if self.__self__ is not None:
            obj = self.__self__
        else:
            obj = args[0]

        # Clear cache if condition is met or not caching.
        if self.clear_condition() or not obj.is_cache:
            self.clear_cache()

        # Use caching method if allowed.
        if obj.is_cache:
            return self.caching_method(obj, *args, **kwargs)
        # Run normal method if not allowed.
        else:
            return self.__func__(obj, *args, **kwargs)

    def clearing_call(self, *args: Any, **kwargs: Any) -> Any:
        """Clears the cache then calls the caching function and allows the owning object to override.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        # Get the object to operate on.
        if self.__self__ is not None:
            obj = self.__self__
        else:
            obj = args[0]

        # Clear Cache
        self.clear_cache()

        # Use caching method if allowed.
        if obj.is_cache:
            return self.caching_method(obj, *args, **kwargs)
        # Run normal method if not allowed.
        else:
            return self.__func__(obj, *args, **kwargs)


class TimedSingleCacheMethod(TimedSingleCache, CachingObjectMethod):
    """A mixin class that implements both TimedSingleCache and CachingObjectMethod"""

    pass


class TimedKeylessCacheMethod(TimedKeylessCache, CachingObjectMethod):
    """A mixin class that implements both TimedKeylessCache and CachingObjectMethod"""

    pass


class TimedCacheMethod(TimedCache, CachingObjectMethod):
    """A mixin class that implements both TimedCache and CachingObjectMethod"""

    pass


class CachingObject(BaseObject, metaclass=CachingObjectMeta):
    """An abstract class which is has functionality for methods that are caching.

    Attributes:
        is_cache: Determines if the caching methods of this object will cache.
        _caches: All the caches within this object.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self) -> None:
        # Attributes #
        self.is_cache: bool = True

        self._caches: set[str] = self._caches_.copy()

    # Instance Methods #
    # Caches Operators
    def get_caches(self) -> set[str]:
        """Get all the caches in this object.

        Returns:
            All the cache objects within this object.
        """
        for name in dir(self):
            attribute = getattr(type(self), name, None)
            if isinstance(attribute, BaseTimedCache) or (
                attribute is None and isinstance(getattr(self, name), BaseTimedCache)
            ):
                self._caches.add(name)

        return self._caches

    def enable_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Enables all caches to cache.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if not self._caches or get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Enable caches in the set.
        for name in caches:
            getattr(self, name).set_caching_method()

    def disable_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Disables all caches to cache.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if not self._caches or get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Disable caches in the set.
        for name in caches:
            getattr(self, name).set_caching_method(method="no_cache")

    def timeless_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Sets all caches to have no expiration time.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if not self._caches or get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Disable expiration all caches in set.
        for name in caches:
            getattr(self, name).is_timed = False

    def timed_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Sets all caches to have an expiration time.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if not self._caches or get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Enable expiration for all caches in the set.
        for name in caches:
            getattr(self, name).is_timed = True

    def clear_caches(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Clears all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if not self._caches or get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Clear caches in the set.
        for name in caches:
            getattr(self, name).clear_cache()


# Functions #
def timed_single_cache_method(
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: AnyCallable | str = "caching_call",
    collective: bool = True,
) -> Callable[[AnyCallable], TimedSingleCacheMethod]:
    """A factory to be used a decorator that sets the parameters of timed single cache method factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed single cache method factory.
    """

    def timed_cache_method_factory(func: AnyCallable) -> TimedSingleCacheMethod:
        """A factory for wrapping a method with a TimedSingleCacheMethod object.

        Args:
            func: The function to wrap with a TimedSingleCacheMethod.

        Returns:
            The TimeSingleCacheMethod object which wraps the given function.
        """
        return TimedSingleCacheMethod(
            func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            collective=collective,
        )

    return timed_cache_method_factory


def timed_keyless_cache_method(
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: AnyCallable | str = "caching_call",
    collective: bool = True,
) -> Callable[[AnyCallable], TimedKeylessCacheMethod]:
    """A factory to be used a decorator that sets the parameters of timed keyless cache method factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed keyless cache method factory.
    """

    def timed_cache_method_factory(func: AnyCallable) -> TimedKeylessCacheMethod:
        """A factory for wrapping a method with a TimedKeylessCacheMethod object.

        Args:
            func: The function to wrap with a TimedKeylessCacheMethod.

        Returns:
            The TimeKeylessCacheMethod object which wraps the given function.
        """
        return TimedKeylessCacheMethod(
            func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            collective=collective,
        )

    return timed_cache_method_factory


def timed_cache_method(
    maxsize: int | None = None,
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: AnyCallable | str = "caching_call",
    collective: bool = True,
) -> Callable[[AnyCallable], TimedCacheMethod]:
    """A factory to be used a decorator that sets the parameters of timed cache method factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed cache method factory.
    """

    def timed_cache_method_factory(func: AnyCallable) -> TimedCacheMethod:
        """A factory for wrapping a method with a TimedCacheMethod object.

        Args:
            func: The function to wrap with a TimedCacheMethod.

        Returns:
            The TimeCacheMethod object which wraps the given function.
        """
        return TimedCacheMethod(
            func,
            maxsize=maxsize,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            collective=collective,
        )

    return timed_cache_method_factory
