"""
Abstract base wrappers:
- k8s model object wrapper to allow defining methods for k8s objects
- k8s model object with metadata
- list of k8s objects which allows search by name, index or regex
"""
import inspect
from re import Pattern

import kubernetes


class KubernetesObjectWrapper:
    """
    Wraps k8s client model classes, adding:
    * k8s client
    * a way to implement any DSL-like methods on objects
    """

    def __init__(self, k8s: kubernetes.client.CoreV1Api, model_object) -> None:
        self.k8s: kubernetes.client.CoreV1Api = k8s
        init_args = {}
        for arg in inspect.getfullargspec(type(model_object).__init__).args:
            if arg != "self":
                init_args[arg] = getattr(model_object, arg)
        type(model_object).__init__(self, **init_args)

    def __repr__(self) -> str:
        type_name = type(self).__name__
        return f"{type_name}(name='{self.name}')"

    def __str__(self) -> str:
        return self.to_str()


class KubernetesMetadataObjectWrapper(KubernetesObjectWrapper):
    """
    Wraps k8s client model classes with metadata, adding uid and name properties
    """

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def uid(self) -> str:
        return self.metadata.uid

    def __repr__(self) -> str:
        type_name = type(self).__name__
        return f"{type_name}(name='{self.name}', uid='{self.uid}')"


class KubernetesObjectList:
    """
    Wraps lists of k8s entites, adding:
    * lookuping by name, index and regex
    * converting raw model objects to wrapped ones
    """

    def __init__(
        self, k8s: kubernetes.client.CoreV1Api, raw_list: list, item_type: type
    ):
        self.k8s = k8s
        self._item_type = item_type
        self._list = [self.item(raw_item) for raw_item in raw_list]

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self._list[item]
        if isinstance(item, Pattern):
            if res := [i for i in self._list if item.match(i.name)]:
                return res
            raise KeyError(item)
        try:
            return next((i for i in self._list if i.name == item))
        except StopIteration:
            raise KeyError(item)

    def __iter__(self):
        return iter(self._list)

    def __contains__(self, item_name):
        if isinstance(item_name, Pattern):
            return any((item for item in self._list if item_name.match(item.name)))
        return any((item for item in self._list if item.name == item_name))

    def __len__(self) -> int:
        return len(self._list)

    def item(self, raw_item_data: any):
        return self._item_type(self.k8s, raw_item_data)

    def __repr__(self) -> str:
        name = self._item_type.__name__
        items = ", ".join((repr(i) for i in self))
        return f"{name}List([{items}])"

    def __str__(self) -> str:
        return str(self._list)

    def names(self) -> list[str]:
        return [i.name for i in self._list]
