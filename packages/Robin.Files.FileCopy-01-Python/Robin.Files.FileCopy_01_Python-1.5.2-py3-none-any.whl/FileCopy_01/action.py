import shutil
import os

from ActionSDK import BaseRobinAction
from ActionSDK.Utils import check_parameters

from RobinFilePath.RobinFilePath import RobinFilePath
from RobinFolderPath.RobinFolderPath import RobinFolderPath

from FileCopy_01.exceptions import \
    RobinFileNotFoundException, \
    RobinFileNotAvailableException, \
    RobinDirectoryNotFoundException

from FileCopy_01.common.mixins import InOutMixin

from typing import Any, Optional, Mapping


class FileCopy_01(BaseRobinAction, InOutMixin):

    # "Протокол" действия, свойство класса
    Parameters = dict(
        filePath=(True, RobinFilePath),
        targetPath=(True, RobinFolderPath),
        newFileName=(False, str),
        overwrite=(False, bool))

    Defaults = dict(
        newFileName='',
        overwrite=False,
    )
    Results = dict(
        result=RobinFilePath
    )

    @check_parameters(**Parameters)
    def run_action(self) -> Mapping[str, Any]:
        # Именованные аттрибуты, скалярные типы Python:
        params = self.get_params()        
        # Вызов ядра действия:
        result = self.file_copy(**params)

        results = dict()
        self.set_result_attribute(results, 'result', result)
        return results


    def file_copy(self, *,
            filePath: str, 
            targetPath: str, 
            newFileName: str, 
            overwrite: bool) -> str:

        if not os.path.exists(filePath):
            raise RobinFileNotFoundException(
                file_path=filePath)
        
        if not newFileName:
            newFileName = os.path.basename(filePath)

        if targetPath.endswith(os.path.sep):
            targetPath = targetPath[:-1]

        if not os.path.exists(targetPath):
            raise RobinDirectoryNotFoundException(file_path=targetPath)

        new_file_path = os.path.join(targetPath, newFileName)

        if not overwrite and os.path.exists(new_file_path):
            raise RobinFileNotAvailableException(file_path=new_file_path)
        
        try:
            shutil.copy2(filePath, new_file_path)
        except Exception as ex:
            raise RobinFileNotAvailableException(
                file_path=new_file_path, 
                message=f'Невозможно получить доступ к файлу: {str(ex)}')

        return str(new_file_path)
