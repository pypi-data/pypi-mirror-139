from .DataSet import DataSet
from . import CIFAR
from . import MNIST
from . import SVHN
from . import flowers


def get_dataset(name: str):
    return DataSet.get_dataset(name)


def list_datasets():
    return DataSet.list_datasets()