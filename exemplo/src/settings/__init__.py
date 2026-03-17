from .definitions import *  ## noqa: F403


EXAMPLE_SETTINGS = Settings(  ## noqa: F405
    dataset=1,
    horizon=10,
    epochs=100,
    data_split=0.2,
    epochs_h=20,
    max_evals=50,
    k_fold=5,
    k_scalable=20,
    save_images=True,
    fixed_samples=True,
    analysis_downsample=False,
    analysis_filters=False,
    analysis_horizon=False,
    analysis_hypertuning=False,
    analysis_opt_model_k_fold=False,
    analysis_statistics=False,
    analysis_our_model_steps=False,
    cnn_use=False,
    attention_use=False,
    filter_use_std=False,
    filter_use_scalable=False,
    analysis_benchmarking=True,
    analysis_our_model=False,
    filter_use=False,
)
