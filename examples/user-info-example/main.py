from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_serializable import Serializable


class UserModel(BaseModel):
    id: int = Field(default=1, ge=0)
    name: str = Field(default="user")
    email: str = Field(default="email@example.com")

    model_config = {
        "validate_default": True,
        "validate_assignment": True,
    }


class User(Serializable[UserModel]):
    # load_from_json = False

    def _save_path(self) -> Path:
        return Path(__file__).parent / "my_info.json"

    def __repr__(self):
        return f"User Information:\n- ID: {self.data.id}\n- Name: {self.data.name}\n- Email: {self.data.email}"


user = User()
user.save_data()
# pprint(user.data.model_dump())
print(user)
