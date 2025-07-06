from abc import ABC, abstractmethod

class ScanModuleBase(ABC):
    name: str = ""
    description: str = ""
    platforms: list = []

    @property
    @abstractmethod
    def params(self) -> dict:
        """Параметры запуска: {имя: {type, default, description}}"""
        pass

    @abstractmethod
    def run(self, log=None, **kwargs) -> dict:
        """Запуск модуля. Возвращает результат в виде словаря. log -- функция для логирования (опционально)"""
        pass 