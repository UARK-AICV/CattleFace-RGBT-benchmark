# d2.cattle
detectron2 for cattle (boxes, masks, and keypoints)

## Installation
```
conda create -n d2.cattle python=3.8 -y
conda activate d2.cattle 
conda install pytorch==1.10.0 torchvision==0.11.0 cudatoolkit=11.3 -c pytorch

# coco api
pip install pycocotools

# detectron2
python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html

# cv2
pip install opencv-python

# setuptools
pip install setuptools==59.5.0
```

## Usage
### 1. Visualize datasets
```bash
export CATTLE_DATASETS=../data/datasets/ # the path to the root folder contain the datasets

python visualize_data.py --dataset-name keypoints_test --output-dir data/outtest/viz_back_kp_test/ --source annotation 
```
### 2. Training
Example of training keypoints dectection on back cattle dataset, using R50 FPN as backbone.
```bash
export CATTLE_DATASETS=../data/datasets/ # the path to the root folder contain the datasets
export CUDA_VISIBLE_DEVICES=0 # specify your gpu if needed

python train_net.py --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN.yaml
```

### 3. Testing
Example of testing keypoints dectection on back cattle dataset, using R50 FPN as backbone.
```bash
export CUDA_VISIBLE_DEVICES=0
export CATTLE_DATASETS=../data/datasets/

python3 train_net.py --num-gpus 1 \
        --config-file configs/cattleKeypoints/keypoints_rcnn_R_50_FPN.yaml \
        --eval-only MODEL.WEIGHTS data/train_outputs/test/model_final.pth \
        OUTPUT_DIR data/train_outputs/test/ 
```
### 4. Demoing
```bash
cd demo/
python demo.py --config-file ${config_file_path} \
  --input ${img_path}/*jpg \
  --output ${output_path} \
  --confidence-threshold 0.9 \
  --opts MODEL.WEIGHTS ${model_path}
```




python visualize_json_results.py --input /home/ptthang/d2.cattle/data/train_outputs/test/inference/coco_instances_results.json --output data/inference/vis --dataset keypoints_test
