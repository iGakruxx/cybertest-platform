from typing import Literal
from pydantic import BaseModel, Field, field_validator

class AuditCreate(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    client: str | None = Field(default=None, max_length=200)
    operator: str = Field(min_length=2, max_length=200)
    mode: Literal["white_box", "grey_box", "black_box"]
    authorization_ref: str = Field(min_length=3, max_length=500)
    notes: str | None = None

class ScopeCreate(BaseModel):
    cidr: str
    allow_active_discovery: bool = False
    allow_offensive_validation: bool = False
    exclusions: list[str] = Field(default_factory=list)
    justification: str = Field(min_length=8, max_length=1000)

class JobCreate(BaseModel):
    kind: Literal["local_reconnaissance", "nmap_discovery"]
    scope_id: str | None = None
    interface: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_.:-]{1,32}$")
