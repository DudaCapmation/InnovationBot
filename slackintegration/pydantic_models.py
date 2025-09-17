from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class Initiative(BaseModel):
    id: int = Field(..., alias="Id")
    status_id: int = Field(..., alias="StatusId")
    name: str = Field(..., alias="Name")
    start_date: Optional[date] = Field(None, alias="StartDate")
    end_date: Optional[date] = Field(None, alias="EndDate")
    target_end_date: Optional[date] = Field(None, alias="TargetEndDate")
    description: Optional[str] = Field(None, alias="Description")
    created_on: Optional[date] = Field(None, alias="CreatedOn")
    modified_on: Optional[date] = Field(None, alias="ModifiedOn")

    # Converts empty strings to None
    @field_validator("*", mode="before")
    def _empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

class Config:
    # Allows constructing the model by field names (snake_case) or by aliases (PascalCase)
    allow_population_by_field_name = True
    # ISO date strings when serializing
    json_encoders = {date: lambda v: v.isoformat()}