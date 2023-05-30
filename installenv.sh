#!/bin/bash
eval "$(conda shell.bash hook)"
rm -rf d2cattle/
conda create --prefix d2cattle/ python=3.8 -y
conda activate d2cattle/
conda install pytorch==1.10.0 torchvision==0.11.0 cudatoolkit=11.3 -c pytorch -y

# coco api
pip install pycocotools

# detectron2
python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html

# cv2
pip install opencv-python

# setuptools
pip install setuptools==59.5.0