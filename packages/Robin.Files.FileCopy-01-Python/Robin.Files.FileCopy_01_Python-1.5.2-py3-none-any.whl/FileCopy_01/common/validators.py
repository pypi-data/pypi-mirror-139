import os

from pathlib import Path

from typing import Union, Any

import platform

import string

from time import sleep

from EngineActionInterface.RobinExceptions import ActionException

StrPath = Union[Path, str]

OS_NAME = platform.system().lower()


class Validator:
    OS_NAME = platform.system().lower()

    @classmethod
    def is_windows(cls) -> bool:
        return cls.OS_NAME == 'windows'

    @classmethod
    def is_linux(cls) -> bool:
        return cls.OS_NAME == 'linux'

    @classmethod
    def validate_path_len(cls, p: StrPath) -> bool:
        if cls.is_windows:
            # Actually 260 up to Windows 10, 
            # the value 247 copied from .NET implementation for actions
            return len(str(p)) <= 247
        if cls.is_linux:
            return len(str(p)) <= 4096

    @classmethod
    def validate_filename_len(cls, p: StrPath) -> bool:
        if cls.is_windows:
            # Actually limitation exists for entire path
            return len(str(p)) <= 247
        if cls.is_linux:
            return len(str(p)) <= 255
    
    @classmethod
    def validate_path_chars(cls, p: StrPath) -> bool:
        # Включена по аналогии с .NET, 
        # делает отбраковку символов которые в принципе недопустимы в пути,
        # не учитывает особенности ОС,
        # встроенные функции .NET также не гарантируют 
        # окончательную проверку валидности символов
        def validate_char(c) -> bool:
            return c in '*?"<>|\t\n\r\x0b\x0c' or c not in string.printable
        return not any(map(validate_char, str(p)))

    @classmethod
    def check_read_access(cls, p: StrPath) -> bool:
        return os.access(str(p), os.R_OK)


    @classmethod
    def check_write_access(cls, p: StrPath) -> bool:
        return os.access(str(p), os.W_OK)

    @classmethod
    def check_exec_access(cls, p: StrPath) -> bool:
        return os.access(str(p), os.X_OK)

    @classmethod
    def check_file_locked(cls, p: StrPath) -> bool:
        # See also idea from: https://blogs.blumetech.com/blumetechs-tech-blog/2011/05/python-file-locking-in-windows.html
        file_path = str(p)
        if not (os.path.exists(file_path)):
            return False
        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            return True
        return False

 

class DirectoryValidator(Validator):
    # Для того, чтобы импорты Robin-исключений были сконцентрированы
    # в одном модуле action.py, испольуем вставку зависимостей (dependency injection):
    def __init__(self, 
            DirectoryNotFound: 'ActionException',
            DirectoryNotAvailable: 'ActionException',
        ) -> None:

        super().__init__()
        self.DirectoryNotFound = DirectoryNotFound
        self.DirectoryNotAvailable = DirectoryNotAvailable


    def validate_directory_path(self, p: StrPath) -> None:
        """Проверка валидности имени ресурса без проверки существования
        """
        folder_path = str(p)

        if not self.validate_path_len(folder_path):
            raise self.DirectoryNotAvailable(
                file_path=folder_path, 
                message=f'Превышено ограничение на длину имени "{folder_path}"')
        
        # check valid symbols
        if not self.validate_path_chars(p):
            raise self.DirectoryNotAvailable(
                file_path=folder_path, 
                message=f'Недопустимые символы в имени пути')
        
    def validate_directory_resource(self, p: StrPath, *, check_write: bool=False, check_read: bool=False) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории и вложенным файлам
        """
        folder_path = str(p)

        if not os.path.exists(folder_path):
            raise self.DirectoryNotFound(
                file_path=folder_path, 
                message=f'Директория "{folder_path}" не найдена')

        if not os.path.isdir(folder_path):
            raise self.DirectoryNotFound(
                file_path=folder_path, 
                message=f'Ресурс "{folder_path}" не является директорией')
        
        if check_read and not self.check_read_access(folder_path):
            raise self.DirectoryNotAvailable(
                file_path=folder_path, 
                message=f'Ошибка доступа к "{folder_path}" для чтения')

        if check_write and not self.check_write_access(folder_path):
            raise self.DirectoryNotAvailable(
                file_path=folder_path, 
                message=f'Ошибка доступа к "{folder_path}" для записи')



class DirectoryTreeValidator(DirectoryValidator):

    # Для того, чтобы импорты Robin-исключений были сконцентрированы
    # в одном модуле action.py, испольуем вставку зависимостей (dependency injection):
    def __init__(self, 
            FileNotFound: 'ActionException',
            DirectoryNotFound: 'ActionException',
            FileNotAvailable: 'ActionException',
            DirectoryNotAvailable: 'ActionException',
        ) -> None:

        super().__init__(
            DirectoryNotFound=DirectoryNotFound,
            DirectoryNotAvailable=DirectoryNotAvailable
        )
        # Внимание: этот валидатор должен содержать полный набор исключений файловой системы,
        # так как валидатор также используется как контейнер вставки зависимостей импортированных исключений
        self.FileNotFound = FileNotFound
        self.FileNotAvailable = FileNotAvailable


    def validate_file_path(self, p: StrPath) -> None:
        """Проверка валидности имени ресурса без проверки существования
        """
        file_path = str(p)

        if not self.validate_path_len(file_path):
            raise self.FileNotAvailable(
                file_path=file_path, 
                message=f'Превышено ограничение на длину имени "{file_path}"')
        
        # check valid symbols
        if not self.validate_path_chars(p):
            raise self.FileNotAvailable(
                file_path=file_path, 
                message=f'Недопустимые символы в имени пути')
        
    def validate_file_resource(self, p: StrPath, *, check_write: bool=False, check_read: bool=False) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к файлу
        """
        file_path = str(p)

        if not os.path.exists(file_path):
            raise self.FileNotFound(
                file_path=file_path, 
                message=f'Файл "{file_path}" не найден')

        if not os.path.isfile(file_path):
            raise self.FileNotFound(
                file_path=file_path, 
                message=f'Ресурс "{file_path}" не является файлом')
        
        if check_read and not self.check_read_access(file_path):
            raise self.FileNotAvailable(
                file_path=file_path, 
                message=f'Ошибка доступа к "{file_path}" для чтения')

        if check_write and not self.check_write_access(file_path):
            raise self.FileNotAvailable(
                file_path=file_path, 
                message=f'Ошибка доступа к "{file_path}" для записи')


    def validate_directory_resource(self, p: StrPath, *, check_write: bool=False, check_read: bool=False) -> None:
        """Проверка отсутствия блокировок и наличия прав доступа к директории и вложенным файлам
        """
        folder_path = str(p)

        super().validate_directory_resource(p, check_read=check_read, check_write=check_write)

        for root, _, files in os.walk(folder_path, topdown=False):
            for name in files:
                fpath = os.path.join(root, name)

                if check_write and not self.check_write_access(fpath):
                    raise self.FileNotAvailable(file_path=fpath, 
                        message=f'Недостаточно прав для записи "{fpath}"')

                if check_read and not self.check_read_access(fpath):
                        raise self.FileNotAvailable(file_path=fpath, 
                            message=f'Недостаточно прав для чтения "{fpath}"')

                # Важно: проверка блокировки должна проводиться после проверки доступа
                if self.check_file_locked(fpath):
                    raise self.DirectoryNotAvailable(
                        file_path=fpath, 
                        message='Невозможно совершить операцию,' + \
                            f' файл используется другим процессом: "{fpath}"')
