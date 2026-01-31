from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Type

from pydantic import BaseModel

if TYPE_CHECKING:
    import pandas as pd


class BaseFactor(ABC):
    name: ClassVar[str]
    param_schema: ClassVar[Type[BaseModel]]

    @abstractmethod
    def compute_signal(
        self, px_m: pd.DataFrame, ret_m: pd.DataFrame, **params: Any
    ) -> pd.DataFrame:
        """Return a cross-sectional signal matrix (aligned to monthly data)."""

    @staticmethod
    def _lag_signal(signal: pd.DataFrame) -> pd.DataFrame:
        """Shift signals by one period to avoid lookahead."""
        return signal.shift(1)
