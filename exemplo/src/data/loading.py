from typing import cast
import pandas as pd
import matplotlib.pyplot as plt

from src.settings import Settings
from .definitions import (
    DatasetType,
    DSColumns,
    PreprocessedData,
    PreprocessedDataPeriod,
    PreprocessLogicFunction,
    PreprocessLogicFunctionArgs,
    PreprocessedDataWithDownSamples,
)


def get_data_length(settings: Settings, ds_type: str) -> int | None:
    """Determine the length of the dataset, given a valid type."""

    sanitized_ds_type = ds_type.strip().lower()

    if sanitized_ds_type not in DatasetType.values():
        raise ValueError(
            f"Tipo de dataset inválido. Tipos suportados são: {','.join(DatasetType.values())}"
        )

    # For a fixed data length
    if settings.fixed_samples:
        return 1000

    ds_type_length_map: dict[str, int] = {
        DatasetType.MIRIS.value: 12
        * 60
        * 24
        * 30,  # Sample every 5 sec (12*60*24*30 = 1 month)
        DatasetType.POWER_QUALITY.value: 60
        * 24
        * 30,  # Sample every 1 min (60*24*30 = 1 month)
        DatasetType.RYE_GENERATION_LOAD.value: 24
        * 30,  # Sample every 1 h (24*30 = 1 month)
    }

    # For one-month data length
    return ds_type_length_map[sanitized_ds_type]


def plot_dataset(
    df: pd.DataFrame,
    out_filepath: str,
    df_series: str = "Load",
    xlabel: str = "Time",
    ylabel: str = "Load [kW]",
    show_plot: bool = True,
    xticks_rotation: int | float | None = None,
    yticks_rotation: int | float | None = None,
) -> None:
    """Perform time series plotting and save output figure into file."""

    plt.figure(figsize=(8, 3))
    plt.plot(df[df_series], "k", zorder=2)
    plt.xlabel(xlabel)

    if xticks_rotation is not None:
        plt.xticks(rotation=xticks_rotation)

    plt.ylabel(ylabel)

    if yticks_rotation is not None:
        plt.yticks(rotation=yticks_rotation)

    plt.grid(linestyle="--", linewidth=0.5, zorder=0)
    plt.savefig(out_filepath, bbox_inches="tight")

    if show_plot:
        plt.show()


def preprocess_miris_ds(params: PreprocessLogicFunctionArgs) -> PreprocessedData:
    """Time series preprocessing dataset 1."""

    df = pd.read_csv(params.ds_filepath, parse_dates=["DateTime"])
    df = df.rename(columns=params.columns)
    df.set_index("DateTime", inplace=True)

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/preprocessed1.pdf"
        plot_dataset(df, out_filepath=output_filepath)

    preprocessed = df[
        0 : params.data_length
    ]  # sample every 5 sec (12*60*24*30 = 1 month)

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/preprocessed1.pdf"
        plot_dataset(preprocessed, out_filepath=output_filepath)

    preprocessed_d = df[0 : 12 * 60 * 24 * 3]
    p_downsample1 = preprocessed_d[::12]
    p_downsample2 = preprocessed_d[:: 12 * 30]
    p_downsample3 = preprocessed_d[:: 12 * 60]

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/downsample1.pdf"
        plot_dataset(p_downsample1, out_filepath=output_filepath)

    # Measure the period of each time series
    preprocessed_period: pd.Timedelta = preprocessed.index[1] - preprocessed.index[0]

    return PreprocessedDataWithDownSamples(
        preprocessed_period=PreprocessedDataPeriod(
            period=preprocessed_period,
            total_seconds=preprocessed_period.total_seconds(),
        ),
        downsamples=[
            p_downsample1,
            p_downsample2,
            p_downsample3,
        ],
    )


def preprocess_power_quality_ds(
    params: PreprocessLogicFunctionArgs,
) -> PreprocessedData:
    """# Time series preprocessing dataset 2."""

    df = pd.read_excel(params.ds_filepath, skiprows=2)
    df = df.rename(columns=params.columns)
    df.set_index("DateTime", inplace=True)

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/original2.pdf"
        plot_dataset(df, xticks_rotation=45, out_filepath=output_filepath)

    preprocessed = df[0 : params.data_length]  # sample every 1 min (60*24 = 1 day)

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/preprocessed2.pdf"
        plot_dataset(preprocessed, xticks_rotation=45, out_filepath=output_filepath)

    # Measure the period of each time series
    preprocessed_period: pd.Timedelta = preprocessed.index[1] - preprocessed.index[0]

    return PreprocessedData(
        preprocessed_period=PreprocessedDataPeriod(
            period=preprocessed_period,
            total_seconds=preprocessed_period.total_seconds(),
        )
    )


def preprocess_rye_generation_load_ds(
    params: PreprocessLogicFunctionArgs,
) -> PreprocessedData:
    """Time series preprocessing dataset 3."""

    df = pd.read_csv(params.ds_filepath, parse_dates=["index"])
    df = df.rename(columns=params.columns)
    df.set_index("DateTime", inplace=True)

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/original3.pdf"
        plot_dataset(df, out_filepath=output_filepath)

    preprocessed = df[0 : params.data_length]  # sample every 1h (24 = 1 day)

    if params.settings.save_images:
        output_filepath = f"./{params.output_dir}/preprocessed3.pdf"
        plot_dataset(preprocessed, out_filepath=output_filepath)

    # Measure the period of each time series
    preprocessed_period: pd.Timedelta = preprocessed.index[1] - preprocessed.index[0]

    return PreprocessedData(
        preprocessed_period=PreprocessedDataPeriod(
            period=preprocessed_period,
            total_seconds=preprocessed_period.total_seconds(),
        )
    )


def load_dataset(
    settings: Settings,
    ds_type: str,
    input_dir: str = "datasets",
    output_dir: str = "results",
) -> PreprocessedData:
    """Perform the loading of a dataset of a specific type."""

    sanitized_ds_type = ds_type.strip().lower()

    if ds_type not in DatasetType.values():
        raise ValueError(
            f"Tipo de dataset inválido. Tipos suportados são: {','.join(DatasetType.values())}"
        )

    type Args = dict[str, str | DSColumns]
    # type Mapper = dict[str, PreprocessLogicFunction | Args]

    ds_type_preprocessing_logic_map = {
        DatasetType.MIRIS.value: {
            "args": {
                "ds_filepath": f"./{input_dir}/miris_load.csv",
                "columns": {"Conso": "Load"},
            },
            "callable": preprocess_miris_ds,
        },
        DatasetType.POWER_QUALITY.value: {
            "args": {
                "ds_filepath": f"./{input_dir}/miris_load.csv",
                "columns": {"record time[s]": "DateTime", "avg.Pfh1[kW]": "Load"},
            },
            "callable": preprocess_power_quality_ds,
        },
        DatasetType.RYE_GENERATION_LOAD.value: {
            "args": {
                "ds_filepath": f"./{input_dir}/rye_generation_and_load.csv",
                "columns": {"index": "DateTime", "Consumption": "Load"},
            },
            "callable": preprocess_rye_generation_load_ds,
        },
    }

    preprocessing_logic = ds_type_preprocessing_logic_map[sanitized_ds_type]
    preprocessing_function = cast(
        PreprocessLogicFunction, preprocessing_logic["callable"]
    )
    preprocessing_func_args = cast(Args, preprocessing_logic["args"])
    data_length = get_data_length(settings, ds_type)

    if data_length is None or (isinstance(data_length, int) and data_length == 0):
        raise ValueError(
            f"The data length for dataset '{sanitized_ds_type}' must be a positive integer"
        )

    args = PreprocessLogicFunctionArgs(
        settings=settings,
        data_length=data_length,
        ds_filepath=cast(str, preprocessing_func_args["ds_filepath"]),
        columns=cast(DSColumns, preprocessing_func_args["columns"]),
        output_dir=output_dir,
    )

    return preprocessing_function(args)
