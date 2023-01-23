from importlib import metadata
from typing import List

from tei_transform.abstract_node_observer import AbstractNodeObserver


class ObserverConstructor:
    """
    Check if a observer matches a valid observer plugin and load
    plugins from entry points.
    """

    def __init__(self) -> None:
        self.entry_points = metadata.entry_points()["node_observer"]
        self.plugins_by_name = {plugin.name: plugin for plugin in self.entry_points}

    def construct_observers(
        self, observer_strings: List[str]
    ) -> List[AbstractNodeObserver]:
        observer_list = []
        for observer_name in self._sort_plugins(observer_strings):
            observer = self._load_observer(observer_name)
            if not self._is_valid_observer(observer):
                raise InvalidObserver(
                    f"{observer_name} is not an instance of AbstractNodeObserver."
                )
            observer_list.append(observer)
        return observer_list

    def _load_observer(self, observer: str) -> AbstractNodeObserver:
        if observer not in self.plugins_by_name:
            raise InvalidObserver(f" No plugin '{observer}' found.")
        return self.plugins_by_name[observer].load()()

    def _is_valid_observer(self, observer: AbstractNodeObserver) -> bool:
        return isinstance(observer, AbstractNodeObserver)

    def _sort_plugins(self, observer_strings: List[str]) -> List[str]:
        observer_strings = self._move_div_parent_to_front(observer_strings)
        return self._move_p_div_sibling_to_end(observer_strings)

    def _move_p_div_sibling_to_end(self, observer_strings: List[str]) -> List[str]:
        return sorted(observer_strings, key=lambda x: x == "p-div-sibling")

    def _move_div_parent_to_front(self, observer_strings: List[str]) -> List[str]:
        return sorted(observer_strings, key=lambda x: x == "div-parent", reverse=True)


class InvalidObserver(Exception):
    pass
