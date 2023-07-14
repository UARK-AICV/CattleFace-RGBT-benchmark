import os

from detectron2.data import MetadataCatalog
from detectron2.data.datasets.coco import register_coco_instances

RED = (0,255,0)

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
        meta.keypoint_flip_map = [['p1','p1'],['p2', 'p3'],['p4','p5'],['p6','p7'],['p8','p9'],['p10','p11'],['p12','p13']]
        # meta.keypoint_connection_rules = [['p1','p2',RED], ['p1','p3',RED],['p2','p4',RED],['p4','p5',RED], ['p5','p6',RED],['p6','p7',RED],['p7','p8',RED],['p7','p11',RED],['p11','p13',RED],['p11','p10',RED],
                                        #   ['p10','p12',RED],['p12','p13',RED],['p3','p12',RED],['p3','p9',RED]]



_root = os.getenv("CATTLE_DATASETS", "datasets")
register_keypoints_dataset(_root)