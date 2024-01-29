from pydantic import BaseModel, Field


class GetDeviceMeasurementResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    type: str = Field(..., description="Type of measurement")
    value: str = Field(..., description="Value of of measurement")
    device_id: int = Field(..., description="Device id")

    class Config:
        from_attributes = True
