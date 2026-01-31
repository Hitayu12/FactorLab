from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel

from app.services.factors.base import BaseFactor
from app.services.factors.lowvol import LowVolFactor
from app.services.factors.trend import TrendFactor
from app.services.factors.xsmom import XsMomFactor


_REGISTRY: dict[str, Type[BaseFactor]] = {
    TrendFactor.name: TrendFactor,
    XsMomFactor.name: XsMomFactor,
    LowVolFactor.name: LowVolFactor,
}


def _schema_fields(schema: Type[BaseModel]) -> list[dict[str, Any]]:
    fields = []
    for name, field in schema.model_fields.items():
        fields.append(
            {
                "name": name,
                "type": str(field.annotation),
                "default": field.default,
                "description": field.description,
            }
        )
    return fields


def list_factors() -> list[dict[str, Any]]:
    output = []
    for name, factor_cls in _REGISTRY.items():
        output.append(
            {
                "name": name,
                "params": _schema_fields(factor_cls.param_schema),
            }
        )
    return sorted(output, key=lambda x: x["name"])
