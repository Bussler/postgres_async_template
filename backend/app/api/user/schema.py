from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    surname: str

    model_config = ConfigDict(from_attributes=True)
