from pydantic import BaseModel, Field


class RegisterUserSchema(BaseModel):
    id: int = Field(None, description="ID")
    first_name: str = Field(None, description="First Name")
    last_name: str = Field(None, description="Last Name")
    username: str = Field(None, description="Username")

    class Config:
        from_attributes = True