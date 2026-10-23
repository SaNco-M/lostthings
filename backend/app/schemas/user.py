from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


class UserCreateSchema(BaseModel):
    name: str
    contact_info: str

    @field_validator("contact_info")
    @classmethod
    def validate_contact(cls, value):
        if "@" not in value and "+" not in value:
            raise ValueError("Добавьте + или @")

        return value


class UserResponseSchema(BaseModel):
    id: int
    name: str
    contact_info: str
    role: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def display_name(self) -> str:
        return f"User: {self.name} (ID: {self.id})"
