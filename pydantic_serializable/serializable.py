from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar, Generic, get_args, get_origin

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Serializable(Generic[T], ABC):
    data: T
    save_path: Path

    load_from_json: bool = True

    @abstractmethod
    def _save_path(self) -> Path:
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # Take the model type from `Serializable[Model]`; subclasses of a
        # concrete subclass inherit it.
        for base in cls.__dict__.get("__orig_bases__", ()):
            if get_origin(base) is Serializable:
                arg = get_args(base)[0]
                if isinstance(arg, type) and issubclass(arg, BaseModel):
                    cls._type_T = arg
                    return
        if not hasattr(cls, "_type_T"):
            raise TypeError(f"{cls.__name__} must subclass Serializable[YourModel].")

    def __init__(self):
        self.save_path = self._save_path()
        self.data = self.load_data()

    def save_data(self, overwrite: bool = True) -> None:
        json_data: str = self.data.model_dump_json(indent=2)
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        if self.save_path.exists() and not overwrite:
            raise FileExistsError(f"File {self.save_path} already exists and overwrite is False.")

        self.save_path.write_text(json_data)

    def load_data(self) -> T:
        if not self.load_from_json or not self.save_path.exists():
            return self._type_T()
        # Let pydantic's ValidationError surface so a bad JSON file is easy to diagnose.
        return self._type_T.model_validate_json(self.save_path.read_text())
