from typing import Optional
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class TechCompany(BaseModel):
    name: str = Field(
        default=None, description="The full name of the technology company"
    )
    location: Optional[str] = Field(
        default=None,
        description="City and state/province/country/planet where the company is headquartered",
    )
    employee_count: Optional[int] = Field(
        default=None, description="Total number of employees"
    )
    founding_year: Optional[int] = Field(
        default=None, description="Year the company was established"
    )
    is_public: Optional[bool] = Field(
        default=None,
        description="Whether the company is publicly traded (True) or privately held (False)",
    )
    valuation: Optional[float] = Field(
        default=None, description="Company's valuation in billions of dollars"
    )
    primary_focus: Optional[str] = Field(
        default=None,
        description="Main area of technology or industry the company focuses on",
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, value,  info: ValidationInfo):
        context = info.context
        if context:
            haystack = context.get('data', '')
            if value not in haystack:
                raise ValueError(f"Company name: '{value}' is not found in context given to you. Do not use examples. Use only context.")
            else:
                print(f"[DEBUG]: Company name: '{value}' is found.")
        return value
