from pydantic import BaseModel, Field


class GetDeviceListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    name: str = Field(..., description="Name")
    description: str = Field(..., description="Description")
    is_in: bool = Field(..., description="Is in")
    is_active: bool = Field(..., description="Is active")
    user_id: int = Field(..., description="User ID")

    class Config:
        orm_mode = True


class CreateDeviceRequestSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: str = Field(..., description="Description")
    is_active: bool = Field(..., description="Is active")
