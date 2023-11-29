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
python visualize_data.py --dataset-name keypoints_train --output-dir data/outtest/viz_back_kp_test/ --source annotation 
```
### 2. Training
Example of training keypoints dectection on back cattle dataset, using R50 FPN as backbone.
```bash
python train_net.py --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN.yaml
```

### 3. Testing
Example of testing keypoints dectection on back cattle dataset, using R50 FPN as backbone.
```bash
python train_net.py --num-gpus 1 --config-file configs/cattleKeypoints/keypoints_rcnn_R_50_FPN.yaml --eval-only MODEL.WEIGHTS data/train_outputs/test/model_final.pth OUTPUT_DIR data/train_outputs/test/ 
```

### 3.5. Inference
```bash
python infer_net.py --num-gpus 1 --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN.yaml  MODEL.WEIGHTS data/train_outputs/test/model_final.pth OUTPUT_DIR data/train_outputs/test/   DATASETS.TEST "('keypoints_test_infer',)"
python infer_net.py --num-gpus 1 --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN.yaml  MODEL.WEIGHTS data/train_outputs/test/model_final.pth OUTPUT_DIR data/train_outputs/train/   DATASETS.TEST "('keypoints_train',)"

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

### 5. Visualize results
```bash
# For set with annotations
python visualize_json_results.py --input /home/ptthang/d2.cattle/data/train_outputs/test/inference/coco_instances_results.json --output data/inference/vis --dataset keypoints_test

# For set without annotations
python visualize_json_results_infer.py --input /home/ethan/d2.cattle/data/train_outputs/test/inference/coco_instances_results.json --output data/inference/vis_test --dataset keypoints_test_infer
python visualize_json_results_infer.py --input /home/ptthang/d2.cattle/data/train_outputs/train/inference/coco_instances_results.json --output data/inference/vis_train --dataset keypoints_train

# to merge into videos (with consecutive frames)
python visualize_json_results_infer_merge_video.py --output data/inference/vis_test
python visualize_json_results_infer_merge_video.py --output data/inference/vis_train
```


### New data
- download the json annotation file for each folder
- merge them into one json file, and split into train and test json
- split them into train and test images

The final structure must be
```
data/
  train_imgs/
    *.jpg
  test_imgs/
    *.jpg
  annotations/
    *.json
```
Before doing this, you should backup the old data folder. Then run the original script like normal. Or you can create new data, but remember to change all the config and python scripts too. 

You can use the notebook `make_new_data.ipynb` to convert any new data into the required format.
Then you should run step 1 to make sure the folder can be visualized correctly.
Then you can train it.

visualize
```bash
python train_net.py --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN.yaml
python train_net.py --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN_withaligned.yaml


python infer_net.py --num-gpus 1 --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN_withaligned.yaml  MODEL.WEIGHTS data/train_outputs/test/model_final.pth OUTPUT_DIR data/train_outputs/test/   DATASETS.TEST "('keypoints_test_infer',)"
python infer_net.py --num-gpus 1 --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN_withaligned.yaml  MODEL.WEIGHTS data/train_outputs/test/model_final.pth OUTPUT_DIR data/train_outputs/train/   DATASETS.TEST "('keypoints_train',)"

python visualize_json_results_infer.py --input /home/ptthang/d2.cattle/data/train_outputs/test/inference/coco_instances_results.json --output data/inference3/vis_test --dataset keypoints_test_infer
python visualize_json_results_infer.py --input /home/ptthang/d2.cattle/data/train_outputs/train/inference/coco_instances_results.json --output data/inference3/vis_train --dataset keypoints_train


python visualize_json_results_infer_merge_video.py --output data/inference2/vis_test
python visualize_json_results_infer_merge_video.py --output data/inference3/vis_test

```