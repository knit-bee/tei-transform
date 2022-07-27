from importlib import metadata

from tei_transform.abstract_node_observer import AbstractNodeObserver


class ObserverConstructor:
    def __init__(self) -> None:
        self.entry_points = metadata.entry_points()["node_observer"]
        self.plugins_by_name = {plugin.name: plugin for plugin in self.entry_points}

    def construct_observers(self, observer_strings: list) -> list:
        observer_list = []
        for observer_name in observer_strings:
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


class InvalidObserver(Exception):
    pass
