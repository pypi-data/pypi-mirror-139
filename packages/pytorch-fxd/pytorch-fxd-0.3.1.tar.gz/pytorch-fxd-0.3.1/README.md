[![PyPI](https://img.shields.io/pypi/v/pytorch-fxd.svg)](https://pypi.org/project/pytorch-fxd/)

# FXD score for PyTorch

## An Improved Metric for Evaluating Chest X-Ray Generation Methods

This is a port of the official implementation of FXD Score to PyTorch.

Generative models are widely used to augment data to improve machine learning models trained on insufficient data. The quality of generated data plays a significant role in the model’s performance. Evaluating a quality of the generative models used a challenging problem. Many sample-based evaluation metrics like Fréchet Inception Distance (FID) compare the distributions of real and generated images in a latent space of models trained on the ImageNet dataset. Such metrics work well in evaluating quality of images of common entities but generally fail in case of images from niche domains not present in the ImageNet dataset like chest x-rays. In this work we propose the FXD score which computes Fréchet distance over the latent space of the pretrained TorchXrayVision model. We perform a series of carefully designed experiments to test for necessary conditions for a meaningful metric. Through these experiments we show that the proposed metric shows more discriminability robustness to transformations and is more sensitive to, mode dropping, mode collapsing and overfitting compared to metrics based on ImageNet weights. Which also proves the importance of choosing domain specific representations in evaluating the quality of generative models. We believe that the proposed FXD score will enable researchers in building generation models efficiently which will in turn aid in building better models to analyze patients more accurately.

![pipeline](https://user-images.githubusercontent.com/32260534/154482892-4947a4ad-3022-4b05-8991-31c657ad8c21.png)

FXD Score is calculated by computing the [Fréchet distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance) between two Gaussians fitted to feature representations of the Inception network. 

## Installation
All the codes have been tested on Linux (ubuntu)

Install from [pip](https://pypi.org/project/pytorch-fxd/):

```
pip install pytorch-fxd
```

Requirements:
- python3
- pytorch
- torchvision
- pillow
- numpy
- scipy
- pytorch-fid
- torchxrayvision
- scikit-image

## Usage

To compute the FXD score between two datasets, where images of each dataset are contained in an individual folder:
```
pytorch-fxd --dataroot path/to/dataset
```
path/to/dataset must contain two folders: setA and setB

To run the evaluation on GPU, use the flag `--cuda`  

To compute other metric scores, use the flag `--all` 

The scores are by default calculated using Torchxrayvision's pretrained model. To calculate using Inception v3 instead, use the flag `--metric fid`

To view other optional arguments:
```
pytorch-fxd --help
```


## License

This implementation is licensed under the MIT License.
