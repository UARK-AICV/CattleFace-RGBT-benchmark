import os

from detectron2.data import MetadataCatalog
from detectron2.data.datasets.coco import register_coco_instances

RED = (255,0,0)

def register_keypoints_dataset(root):
    root = os.path.join(root, 'keypoints/coco_format')
    splits = ['train', 'test']
    for split in splits:
        register_coco_instances("keypoints_{}".format(split), {}, 
            os.path.join(root, "annotations/{}.json".format(split)),
            os.path.join(root, "{}_imgs".format(split))
        )
    
        meta = MetadataCatalog.get('keypoints_{}'.format(split))
        meta.thing_classes = ['cattle']
        meta.keypoint_names =  ['p1','p2','p3','p4','p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13']
        meta.keypoint_flip_map = [['p1','p1'],['p2', 'p3'],['p4','p5']]
        meta.keypoint_connection_rules = [['p1','p2',RED], ['p1','p3',RED],['p2','p4',RED],['p3','p5',RED]]



_root = os.getenv("CATTLE_DATASETS", "datasets")
register_keypoints_dataset(_root)