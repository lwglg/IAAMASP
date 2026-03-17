from dataclasses import dataclass


__all__ = [
    "Settings",
]


@dataclass
class Settings:
    # Setup for analysis
    dataset: int
    horizon: int
    epochs: int
    data_split: float  # Test (%)
    epochs_h: int
    max_evals: int
    k_fold: int
    k_scalable: int

    save_images: bool
    fixed_samples: bool

    # General analysis
    analysis_downsample: bool
    analysis_filters: bool
    analysis_horizon: bool
    analysis_hypertuning: bool
    analysis_opt_model_k_fold: bool
    analysis_statistics: bool

    # To evaluate our model step by step
    analysis_our_model_steps: bool
    cnn_use: bool
    attention_use: bool
    filter_use_std: bool
    filter_use_scalable: bool

    # For benchmarking
    analysis_benchmarking: bool
    analysis_our_model: bool
    filter_use: bool
