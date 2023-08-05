#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemethod.py
An abstract class which implements the basic structure for creating methods.
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
from functools import update_wrapper
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..types_ import AnyCallable, GetObjectMethod
from .baseobject import BaseObject, search_sentinel
from .singlekwargdispatchmethod import singlekwargdispatchmethod


# Definitions #
# Classes #
class BaseMethod(BaseObject):
    """An abstract class which implements the basic structure for creating methods.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _selected_get_method: The __get__ method to use as a Callable or a string.
        _get_method_: The method that will be used as the __get__ method.
        _instances: Copies of this object for specific owner instances.

    Args:
        func: The function to wrap.
        get_method: The method that will be used for the __get__ method.
        init: Determines if this object will construct.
    """

    sentinel = search_sentinel

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        get_method: GetObjectMethod | str | None = None,
        init: bool | None = True,
    ):
        # Special Attributes #
        self.__func__: AnyCallable | None = None
        self.__self__: Any = None

        # Attributes #
        self._selected_get_method: GetObjectMethod | str = "get_self_bind"
        self._get_method_: GetObjectMethod = self.get_self_bind
        self._instances: dict[Any, "BaseMethod"] = {}

        # Object Construction #
        if init:
            self.construct(func=func, get_method=get_method)

    @property
    def _get_method(self) -> GetObjectMethod:
        """The method that will be used for the __get__ method.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._get_method_

    @_get_method.setter
    def _get_method(self, value: GetObjectMethod | str) -> None:
        self.set_get_method(value)

    # Descriptors
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> "BaseMethod":
        """When this object is requested by another object as an attribute.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            The bound BaseMethod which can either self or a new BaseMethod.
        """
        return self._get_method_(instance, owner=owner)

    # Callable
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """The call magic method for this object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The results of the wrapped function.
        """
        return self.__func__(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        get_method: GetObjectMethod | str | None = None,
    ) -> None:
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            get_method: The method that will be used for the __get__ method.
        """
        if func is not None:
            self.__func__ = func
            update_wrapper(self, self.__func__)

        if get_method is not None:
            self.set_get_method(get_method)

    # Descriptor
    @singlekwargdispatchmethod("method")
    def set_get_method(self, method: GetObjectMethod | str) -> None:
        """Sets the __get__ method to another function or a method name within this object can be given to select it.

        Args:
            method: The function to set the __get__ method to.
        """
        raise NotImplementedError(f"A {type(method)} cannot be used to set a {type(self)} get_method.")

    @set_get_method.register(Callable)
    def _(self, method: GetObjectMethod) -> None:
        """Sets the __get__ method to another function.

        Args:
            method: The function to set the __get__ method to.
        """
        self._selected_get_method = method
        self._get_method_ = method

    @set_get_method.register
    def _(self, method: str) -> None:
        """Sets the __get__ method to a method within this object based on name.

        Args:
            method: The method name to set the __get__ method to.
        """
        self._selected_get_method = method
        self._get_method_ = getattr(self, method)

    def get_self(self, instance: Any, owner: type[Any] | None = None) -> "BaseMethod":
        """The __get__ method where it returns itself.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            This object.
        """
        return self

    def get_self_bind(self, instance: Any, owner: type[Any] | None = None) -> "BaseMethod":
        """The __get__ method where it binds itself to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            This object.
        """
        if instance is not None and self.__self__ is not instance:
            self.bind(instance)
        return self

    def get_new_bind(
        self,
        instance: Any,
        owner: type[Any] | None = None,
        new_binding: GetObjectMethod | str = "get_self_bind",
    ) -> "BaseMethod":
        """The __get__ method where it binds a new copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
            new_binding: The binding method the new object will use.

        Returns:
            Either bound self or a new BaseMethod bound to the instance.
        """
        if instance is None:
            return self
        else:
            bound = self.bind_to_new(instance=instance)
            bound.set_get_method(new_binding)
            setattr(instance, self.__func__.__name__, bound)
            return bound

    def get_subinstance(self, instance: Any, owner: type[Any] | None = None) -> "BaseMethod":
        """The __get__ method where it binds a registered copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            Either bound self or a BaseMethod bound to the instance.
        """
        if instance is None:
            return self
        else:
            bound = self._instances.get(instance, search_sentinel)
            if bound is search_sentinel:
                self._instances[instance] = bound = self.bind_to_new(instance=instance)
            return bound

    # Binding
    def bind(self, instance: Any, name: str | None = None, set_attr: bool = True) -> None:
        """Binds this object to another object to give this object method functionality.

        Args:
            instance: The object to bing this object to.
            name: The name of the attribute this object will bind to in the other object.
            set_attr: Determines if this object will be set as an attribute in the object.
        """
        self.__self__ = instance
        if name is not None:
            setattr(instance, name, self)
        elif set_attr:
            setattr(instance, self.__func__.__name__, self)

    def bind_to_new(self, instance: Any, name: str | None = None, set_attr: bool = True) -> Any:
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.
            set_attr: Determines if this object will be set as an attribute in the object.

        Returns:
            The new bound deepcopy of this object.
        """
        new_obj = type(self)(func=self.__func__, get_method=self._selected_get_method)
        new_obj.bind(instance=instance, name=name, set_attr=set_attr)
        return new_obj
