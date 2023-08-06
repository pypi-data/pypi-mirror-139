from typing import Tuple
from .. import log


class DataSet:
    _datasets = {}

    def __init__(self, name: str, alias: Tuple[str, ...] = ()):
        self.name = name
        self.alias = alias

    def __call__(self, function):
        if self._datasets.get(self.name):
            log.warn(f"数据集{self.name}已存在")
        else:
            self._datasets[self.name] = function
        for alias in self.alias:
            if self._datasets.get(alias):
                log.warn(f"数据集别名{alias}已存在")
            else:
                self._datasets[alias] = function

    @staticmethod
    def get_dataset(name: str):
        if DataSet._datasets.get(name):
            return DataSet._datasets.get(name)
        else:
            log.critical(f"数据集{name}不存在")

    @staticmethod
    def list_datasets():
        for k, v in DataSet._datasets.items():
            print(f"{k}: {v}")
