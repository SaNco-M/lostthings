from typing import Annotated

from pydantic import Field

from app.schemas import AnimalAdCreateSchema, ItemAdCreateSchema

AnyAdCreateSchema = Annotated[
    AnimalAdCreateSchema | ItemAdCreateSchema, Field(discriminator="type_ad")
]
