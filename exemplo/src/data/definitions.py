from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, make_dataclass

from pandas import DataFrame, Timedelta
from pandas._typing import Renamer

from src.shared.enums import BaseEnum
from src.settings import Settings


__all__ = [
    "DatasetType",
    "PreprocessedDataPeriod",
    "PreprocessedData",
    "PreprocessLogicFunction",
    "PreprocessLogicFunctionArgs",
    "make_preprocessed_data",
]


class DatasetType(BaseEnum):
    MIRIS = "miris"
    POWER_QUALITY = "power_quality"
    RYE_GENERATION_LOAD = "rye_generation_load"


@dataclass
class PreprocessedDataPeriod:
    period: Timedelta
    total_seconds: float


@dataclass
class PreprocessedData:
    preprocessed_period: PreprocessedDataPeriod


@dataclass
class PreprocessLogicFunctionArgs:
    settings: Settings
    data_length: int
    ds_filepath: str
    columns: Renamer
    output_dir: str


type PreprocessLogicFunction = Callable[[PreprocessLogicFunctionArgs], PreprocessedData]


def make_preprocessed_data(
    period: PreprocessedDataPeriod, downsamples: list[DataFrame] | None = None
) -> PreprocessedData:
    """Create a preprocessed data object and its type dynamically."""

    ppdata = PreprocessedData(preprocessed_period=period)
    ppdata_has_downsamples = downsamples is not None and len(downsamples) > 0

    make_dataclass_args = {
        **{
            "fields": [(f"downsample{i}", DataFrame) for i in range(len(downsamples))]
            if ppdata_has_downsamples
            else {}
        },
        "bases": (PreprocessedData,),
    }

    ppdata.__class__ = make_dataclass(
        PreprocessedData.__class__.__name__, **make_dataclass_args
    )

    if ppdata_has_downsamples:
        for i, ds in enumerate(downsamples):
            ppdata.__dict__.__setattr__(f"downsample{i}", ds)

    return ppdata
