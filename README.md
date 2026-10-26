# pydantic-serializable

[![PyPI](https://img.shields.io/pypi/v/pydantic-serializable)](https://pypi.org/project/pydantic-serializable/)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A small, type-safe base class that saves a Pydantic model to a JSON file and loads it back, falling back to the model's defaults when the file does not exist yet.

## Installation

```bash
pip install pydantic-serializable
```

## Usage

1. Define a Pydantic model whose fields all have defaults.
2. Subclass `Serializable[YourModel]` and implement `_save_path()`.

```python
from pathlib import Path

from pydantic import BaseModel
from pydantic_serializable import Serializable


class SettingsModel(BaseModel):
    theme: str = "light"
    font_size: int = 14


class Settings(Serializable[SettingsModel]):
    def _save_path(self) -> Path:
        return Path("settings.json")


settings = Settings()          # loads settings.json, or uses defaults if it is missing
settings.data.font_size = 16
settings.save_data()           # writes settings.json (parent folders are created)
```

## API

| Member                          | Description                                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| `data`                          | The model instance, loaded on creation                                              |
| `save_path`                     | Path returned by `_save_path()`                                                     |
| `save_data(overwrite=True)`     | Write `data` as indented JSON; with `overwrite=False`, raise `FileExistsError` if the file exists |
| `load_data()`                   | Read the file again; raises pydantic's `ValidationError` if its contents are invalid |
| `load_from_json` (class attr)   | Set to `False` to always start from the model's defaults                            |

A fuller example lives in [`examples/user-info-example`](examples/user-info-example/main.py).

## License

MIT
