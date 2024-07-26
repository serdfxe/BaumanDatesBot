from pydantic import BaseModel, Field


class FillProfileSchema(BaseModel):
    name: str = Field(None, description="Name")
    age: int = Field(None, description="Age")
    description: str = Field(None, description="Description")
    sex: str = Field(None, description="Sex")

    class Config:
        from_attributes = True