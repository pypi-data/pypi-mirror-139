from typing import Literal, Optional

from pydantic import BaseModel, Field

from .logistics import CvsMapSubTypeOptions


class CvsMapRequestModel(BaseModel):
    logistics_type: Literal["CVS"] = Field(default="CVS", alias="LogisticsType")
    logistics_subtype: CvsMapSubTypeOptions = Field(
        default="FAMIC2C", alias="LogisticsSubType"
    )
    is_collection: Literal["Y", "N"] = Field(
        default="N", alias="IsCollection", description="是否收款"
    )
    device: Literal["0", "1"] = Field(
        default="0", alias="Device", description="PC:0; MOBILE:1"
    )
    redirect_url: Optional[str] = Field(default=None, alias="redirect_url")
