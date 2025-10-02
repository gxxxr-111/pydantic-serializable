from pathlib import Path
from typing import TypeVar, Generic, Type

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Serializable(Generic[T]):
    data_type: Type[T]

    data: T
    save_path: Path

    def __init__(self):
        self.save_path = self._save_path()
        self.data = self.load_data()

    def _default_data(self) -> T:
        raise NotImplementedError("Serializable.default_data is not implemented")

    def _save_path(self) -> Path:
        raise NotImplementedError("Serializable.default_save_path is not implemented")

    def save_data(self, overwrite: bool = True) -> None:
        json_data: str = self.data.model_dump_json(indent=2)
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        if self.save_path.exists() and not overwrite:
            raise FileExistsError(f"File {self.save_path} already exists and overwrite is False.")

        self.save_path.write_text(json_data)

    def load_data(self) -> T:
        if not self.save_path.exists():
            return self._default_data()
        return self.data_type.model_validate_json(self.save_path.read_text())
