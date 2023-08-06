import importlib.util
from hashlib import sha256
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Optional


def sha256sum(path_file: str):
    """
    Получить хеш сумму файла
    @param path_file: Путь к файлу
    """
    h = sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(path_file, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def read_file_by_module(infile: str) -> ModuleType:
    """
    Импортировать файл как модуль `python`

    :param infile: Путь к `python` файлу
    :return: Модуль `python`
    """
    # указать модуль, который должен быть импортируется относительно пути модуль
    spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location("my_module", infile)
    # создает новый модуль на основе спецификации
    __module: ModuleType = importlib.util.module_from_spec(spec)
    # выполняет модуль в своем собственном пространстве имен,
    # когда модуль импортируется или перезагружается.
    spec.loader.exec_module(__module)
    return __module


def concat_absolute_dir_path(_file: str, _path: str) -> str:
    """
    Получить абсолютный путь папки и объединить с другим путем

    :param _file:
    :param _path:
    :return:
    """
    return str(Path(_file).resolve().parent / _path)


def absolute_path_dir(_file: str, back: int = 1) -> Path:
    """
    Получить абсолютный путь к своей директории

    :param _file: Путь
    :param back: Сколько отступить назад
    """
    res = Path(_file).resolve()
    for _ in range(back):
        res = res.parent
    return res
