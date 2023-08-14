#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates.

import argparse
import glob
import json
import numpy as np
import os
from collections import defaultdict
import cv2
import tqdm

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.structures import Boxes, BoxMode, Instances, Keypoints
from detectron2.utils.file_io import PathManager
from detectron2.utils.logger import setup_logger
from visualizer import Visualizer
import register_cattle_datasets




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script that visualizes the json predictions from COCO or LVIS dataset."
    )
    parser.add_argument("--output", required=True, help="output directory")
    args = parser.parse_args()

    _saved_dir = args.output + '_video'
    os.makedirs(_saved_dir, exist_ok=True)
    all_files = glob.glob(args.output + '/*.jpg')
    all_files.sort()
    all_idx = [int(os.path.basename(f).split('.')[0].split('_')[-1]) for f in all_files]
    all_prefix = ["_".join(os.path.basename(f).split('.')[0].split('_')[:-1]) for f in all_files]
    map_idx_prefix = defaultdict(list)
    for idx, prefix in zip(all_idx, all_prefix):
        map_idx_prefix[prefix].append(idx)
    all_prefix = list(map_idx_prefix.keys())
    for prefix in all_prefix:
        all_idx_chunk_consecutive = []
        tmp_cons = []
        for idx in map_idx_prefix[prefix]:
            if len(tmp_cons) == 0:
                tmp_cons.append(idx)
            elif idx == tmp_cons[-1] + 1:
                tmp_cons.append(idx)
            else:
                all_idx_chunk_consecutive.append(tmp_cons)
                tmp_cons = [idx]
        for idx_chunk in tqdm.tqdm(all_idx_chunk_consecutive):
            start_index = idx_chunk[0]
            os.system(f'ffmpeg -y -framerate 30 -start_number {start_index} -i {args.output}/{prefix}_%09d.jpg  {_saved_dir}/{prefix}_{start_index}.mp4')