from collections.abc import Callable
from dataclasses import dataclass

from pandas import DataFrame, Timedelta
from pandas._typing import Renamer as DSColumns

from src.shared.enums import BaseEnum
from src.settings import Settings


__all__ = [
    "DatasetType",
    "PreprocessedDataPeriod",
    "PreprocessedData",
    "PreprocessedDataWithDownSamples",
    "PreprocessLogicFunction",
    "PreprocessLogicFunctionArgs",
    "DSColumns",
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
    columns: DSColumns
    output_dir: str


type PreprocessLogicFunction = Callable[[PreprocessLogicFunctionArgs], PreprocessedData]


@dataclass
class PreprocessedDataWithDownSamples(PreprocessedData):
    downsamples: list[DataFrame] | None
