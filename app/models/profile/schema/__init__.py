from pydantic import BaseModel, Field


class FillProfileSchema(BaseModel):
    name: str = Field(None, description="Name")
    age: int = Field(None, description="Age")
    description: str = Field(None, description="Description")
    sex: str = Field(None, description="Sex")

    class Config:
        from_attributes = True
        

class FlowProfileSchema(BaseModel):
    user_id: int = Field(None, description="ID")
    name: str = Field(None, description="Name")
    description: str = Field(None, description="Description")
    
    class Config:
        from_attributes = True
