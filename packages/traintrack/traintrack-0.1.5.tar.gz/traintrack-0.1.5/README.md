<div align="center">

<figure>
    <img src="https://raw.githubusercontent.com/murnanedaniel/train-track/master/docs/media/logo.png" width="250"/>
</figure>
    
# TrainTrack ML
### Quickly run stages of an ML pipeline from the command line

[Documentation](https://hsf-reco-and-software-triggers.github.io/Tracking-ML-Exa.TrkX/)

[![ci](https://github.com/murnanedaniel/train-track/actions/workflows/ci.yml/badge.svg)](https://github.com/murnanedaniel/train-track/actions/workflows/ci.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


</div>

Welcome to repository and documentation the TrainTrack library. Detailed documentation coming very soon! See [here](https://hsf-reco-and-software-triggers.github.io/Tracking-ML-Exa.TrkX/) for the documentation of the examples of this library. 

## Install

TrainTrack is most easily installed with pip:
```
pip install traintrack
```

## Objective

The aim of TrainTrack is simple: Given any set of self-contained [Pytorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning) modules, run them in a serial and trackable way. 

At its heart, TrainTrack is nothing more than a loop over the stages defined in a `pipeline.yaml` configuration file. However, it can also handle data processing steps (i.e. non-trainable modules), automatically creates grid scans over combinations of hyperparameters, logs training with (currently) either Tensorboard or Weights & Biases, and can run separate, dependent Slurm batch jobs. It also has an opinionated approach to how data is passed from stage to stage, via Lightning callbacks. In this way, the only code that needs to be written is Lightning modules, all other boilerplate and tracking is handled by TrainTrack. 

## Example

`traintrack` uses two ingredients to run and track your training pipeline: 
1. A project configuration file
2. A pipeline configuration file

It also makes one or two assumptions about the structure of your project. For project `MyFirstMNIST`, we should structure it as
```
📦 MyFirstMNIST
┣ 📂 architectures
┣ 📂 notebooks
┣ 📂 configs
┃ ┣ 📜 project_config.yaml
┃ ┗ 📜 my_first_pipeline.yaml
┗ 📂 logs
```
**Note:** Only `configs/project_config.yaml` is a required file. All else is configurable. An example `project_config.yaml`:
```
# project_config.yaml

# Location of libraries
libraries:
    model_library: architectures
    artifact_library: /my/checkpoint/directory
    

# The lines you would like/need in a batch script before the call to pipeline.py
custom_batch_setup:
    - conda activate my-favorite-environment
    
# If you need to set up some environment before a batch is submitted, define it here in order of commands to run
command_line_setup:
    - module load cuda
    
# If you need to run jobs serially, set to true
serial: False

# Which logger to use - options are Weights & Biases [wandb], TensorBoard [tb], or [None]
logger: wandb
```

We can launch a vanilla run of TrainTrack with 
```
traintrack configs/my_first_pipeline.yaml
```
This trains and performs inference callbacks in the terminal. 


## A Pipeline

The pipeline config file defines a pipeline, for example:
```
# my_first_pipeline.yaml

stages:
    - {set: CNN, name: ResNet50, config: test_train.yaml}

```

which presumes a directory structure of:

```
📦 MyFirstMNIST
┣ 📂 architectures
┃ ┗ 📂 CNN
┃ ┃ ┣ 📜 cnn_base.py
┃ ┃ ┣ 📜 test_train.yaml
┃ ┃ ┗ 📂 Models
┃ ┃ ┃ ┗ 📜 resnet.py

```

Again, see [this repository](https://hsf-reco-and-software-triggers.github.io/Tracking-ML-Exa.TrkX/tree/master/Pipelines/Common_Tracking_Example) for example pipelines in action.
