import json
import os



dir = "datasets/keypoints/coco_format/Frames"
out = "datasets/keypoints/coco_format/image_jsons"

for folder in os.listdir(dir):
    images = []
    annotations = []
    categories = [{"supercategory": "cow", "id": 1, "name": "cattle", "keypoints": ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13"], "skeleton": [[1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 8], [7, 9], [8, 10], [9, 11], [10, 12], [11, 13], [12, 13]]}]
    id = 0
    image_folder = os.path.join(dir, folder)



    for image in os.listdir(image_folder):
        images.append({"license": None, "file_name": image,"coco_url": None, "height": 1440, "width": 2560, "id": id})
        annotations.append({"segm)entation": None, "num_keypoints": 13, "area": 0, "iscrowd": 0, "keypoints": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "image_id": id, "bbox": [0, 0, 0, 0], "category_id": 1, "id": id, "inmodal_bbox": None, "inmodal_seg": None})
        id += 1

    data = {"images": images, "annotations": annotations, "categories" : categories}

    output_dir = os.path.join(out, folder)
    output_dir += ".json"
    with open(output_dir, 'w') as f:
        json.dump(data, f, indent = 4)