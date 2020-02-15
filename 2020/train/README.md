# Training module

This module contains a package for model training

## Requirements

## Setup

## Usage

1. Setup the training parameters, by copying `conf/train-conf.yml.dist` into `conf/train-conf.yml` and editing the
parameters to your taste

2. Run the training job:
```bash
conda activate ${your_env_name}
python train/run.py data/artefacts data/${dataset_filename} conf/train-conf.yml
```
