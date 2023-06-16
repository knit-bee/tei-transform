from __future__ import annotations

import configparser
import sys
from importlib import metadata
from typing import List, Optional, Tuple, Union

from tei_transform.abstract_node_observer import AbstractNodeObserver


class ObserverConstructor:
    """
    Check if a observer matches a valid observer plugin and load
    plugins from entry points.
    """

    def __init__(self) -> None:
        self.entry_points = self._get_node_observer_entry_points()
        self.plugins_by_name = {plugin.name: plugin for plugin in self.entry_points}

    @classmethod
    def _get_node_observer_entry_points(
        cls,
    ) -> Union[Tuple[metadata.EntryPoint], metadata.EntryPoints]:
        if sys.version_info < (3, 10):
            entry_points = metadata.entry_points()["node_observer"]
        else:
            entry_points = metadata.entry_points().select(group="node_observer")
        return entry_points

    def construct_observers(
        self,
        observer_strings: List[str],
        config: Optional[configparser.ConfigParser] = None,
    ) -> Tuple[List[AbstractNodeObserver], List[AbstractNodeObserver]]:
        first_pass_observers = []
        second_pass_observers = []
        for observer_name in self._sort_plugins(observer_strings):
            observer = self._load_observer(observer_name)
            if getattr(observer, "config_required", False) and (
                config is None or observer_name not in config
            ):
                raise MissingConfiguration(
                    f"Configuration required for {observer_name} plugin."
                )
            if not self._is_valid_observer(observer):
                raise InvalidObserver(
                    f"{observer_name} is not an instance of AbstractNodeObserver."
                )
            if config is not None:
                self._configure_observer(observer, config, observer_name)
            if observer_name in {"div-sibling", "unfinished-elem"}:
                second_pass_observers.append(observer)
                continue
            first_pass_observers.append(observer)
        return first_pass_observers, second_pass_observers

    def _load_observer(self, observer: str) -> AbstractNodeObserver:
        if observer not in self.plugins_by_name:
            raise InvalidObserver(f" No plugin '{observer}' found.")
        return self.plugins_by_name[observer].load()()

    def _is_valid_observer(self, observer: AbstractNodeObserver) -> bool:
        return isinstance(observer, AbstractNodeObserver)

    def _sort_plugins(self, observer_strings: List[str]) -> List[str]:
        observer_strings = self._move_lb_text_to_front(observer_strings)
        observer_strings = self._move_div_parent_to_front(observer_strings)
        observer_strings = self._move_p_parent_to_end(observer_strings)
        return self._move_double_plike_to_end(observer_strings)

    def _move_double_plike_to_end(self, observer_strings: List[str]) -> List[str]:
        return sorted(observer_strings, key=lambda x: x == "double-plike")

    def _move_p_parent_to_end(self, observer_strings: List[str]) -> List[str]:
        return sorted(observer_strings, key=lambda x: x == "p-parent")

    def _move_div_parent_to_front(self, observer_strings: List[str]) -> List[str]:
        return sorted(observer_strings, key=lambda x: x == "div-parent", reverse=True)

    def _move_lb_text_to_front(self, observer_strings: List[str]) -> List[str]:
        return sorted(observer_strings, key=lambda x: x == "lb-text", reverse=True)

    def _configure_observer(
        self,
        observer: AbstractNodeObserver,
        config: configparser.ConfigParser,
        plugin_name: str,
    ) -> None:
        if hasattr(observer, "configure") and plugin_name in config:
            observer.configure(config[plugin_name])


class InvalidObserver(Exception):
    pass


class MissingConfiguration(Exception):
    pass
