#!/bin/bash
for ((i=0; i<1000; i++)); do
    python /home/ethan/d2.cattle/infer_net.py --num-gpus 1 --config-file configs/CattleKeypoints/keypoints_rcnn_R_50_FPN.yaml  MODEL.WEIGHTS data/train_outputs/test/model_final.pth OUTPUT_DIR data/train_outputs/test/   DATASETS.TEST "('keypoints_test_infer',)"
done
