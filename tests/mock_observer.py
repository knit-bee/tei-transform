from importlib import metadata

from lxml import etree

from tei_transform.abstract_node_observer import AbstractNodeObserver


class MockConfigurableObserver(AbstractNodeObserver):
    def __init__(self, attribute=None):
        self.configurable = True
        self.attribute = attribute

    def observe(self, node: etree._Element) -> None:
        pass

    def transform_node(self, node):
        pass

    def configure(self, config):
        allowed_actions = {"setattr": setattr}
        action = config["action"]
        if action in allowed_actions:
            allowed_actions[action](self, "attribute", config["attribute"])


class MockObserverConfigRequired(AbstractNodeObserver):
    def __init__(self, attribute=None):
        self.config_required = True

    def observe(self):
        pass

    def transform_node(self, node):
        pass


def add_mock_plugin_entry_point(observer_constructor, plugin_name, plugin_path):
    mock_entry_point = metadata.EntryPoint(
        name=plugin_name,
        value=plugin_path,
        group="node_observer",
    )
    observer_constructor.entry_points += mock_entry_point
    observer_constructor.plugins_by_name[plugin_name] = mock_entry_point
