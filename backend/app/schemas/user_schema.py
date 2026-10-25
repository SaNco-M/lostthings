import phonenumbers
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: EmailStr | None = None
    phone: str | None = None
    password: str = Field(min_length=6, max_length=128)

    @model_validator(mode="after")
    def validate_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Укажите email или телефон")

        return self

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if value == "":
            return None

        try:
            parsed = phonenumbers.parse(value.strip(), None)
        except phonenumbers.NumberParseException:
            raise ValueError("Некорректный номер телефона")
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Некорректный номер телефона")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
