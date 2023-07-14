import os
import re
import cv2
import sys
import glob
import json
import math
import pickle
import random
import numpy as np
from PIL import Image
from tqdm import tqdm
from pathlib import Path 
import matplotlib.pyplot as plt
from collections import defaultdict

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset
import torchvision.transforms as transforms

jsons = ['train_raw.json', 'test_raw.json']
root_dir = 'datasets/keypoints/coco_format/annotations'
for json_ in jsons:
    with open(os.path.join(root_dir, json_)) as f:
        data = json.load(f)
    for i in range(len(data['annotations'])):
        for j in range(len(data['annotations'][i]['keypoints'])):
            if j % 3 == 2:
                data['annotations'][i]['keypoints'][j] = 2 if data['annotations'][i]['keypoints'][j] >= 2 else 1
    with open(os.path.join(root_dir, json_.replace('_raw', '')), 'w') as f:
        json.dump(data, f, indent=4)
