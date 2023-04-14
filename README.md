# d24chicken
detectron2 for chicken

## Installation
```
conda create -n d24chicken python=3.8 -y
conda activate aistron
conda install pytorch==1.10.0 torchvision==0.11.0 cudatoolkit=11.3 -c pytorch

# coco api
pip install pycocotools

# detectron2
python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html

# cv2
pip install opencv-python
```

## Usage
### 1. Visualize datasets
```bash
export CHICKEN_DATASETS=../data/datasets/ # the path to the root folder contain the datasets

python visualize_data.py --dataset-name back_chicken_keypoints_test \ # the dataset name
                         --output-dir ../data/outtest/viz_back_kp_test/ \ # the output dir of visualize images
                         --source annotation \ # source of annotation
```
