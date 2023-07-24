import os

from detectron2.data import MetadataCatalog
from detectron2.data.datasets.coco import register_coco_instances

RED = (0,255,0)

def make_test_infer(root, target_folder='test_imgs', sample_annotation_path='annotations/test.json'):
    infer_annotation_path = os.path.join(root, 'annotations/test_infer.json')
    if os.path.exists(infer_annotation_path):
        return
    import json
    test_infer_path = os.path.join(root, target_folder)
    with open(os.path.join(root, sample_annotation_path)) as f:
        test_annotation = json.load(f)
    infer_annotation = test_annotation.copy()
    infer_annotation['images'] = []
    infer_annotation['annotations'] = []
    all_images_target = os.listdir(test_infer_path)
    for image_id, image in enumerate(all_images_target):
        infer_annotation['images'].append({
            'license': None,
            'file_name': image,
            'coco_url': None,
            "height": 1440,
            "width": 2560,
            'id': image_id
        })
        infer_annotation['annotations'].append({
            'segmentation': None,
            'num_keypoints': 13,
            'area': 0,
            'iscrowd': 0,
            'keypoints': [0,0,0]*13,
            'image_id': image_id,
            'bbox': [0,0,0,0],
            'category_id': 1,
            'id': image_id,
            'inmodal_bbox': None,
            'inmodal_seg': None
        })
    with open(infer_annotation_path, 'w') as f:
        json.dump(infer_annotation, f)


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

    make_test_infer(root, target_folder='test_imgs', sample_annotation_path='annotations/test.json')
    register_coco_instances("keypoints_test_infer", {},
        os.path.join(root, "annotations/test_infer.json"),
        os.path.join(root, "test_imgs")   
    )
    meta = MetadataCatalog.get('keypoints_test_infer')
    meta.thing_classes = ['cattle']
    meta.keypoint_names =  ['p1','p2','p3','p4','p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13']
    meta.keypoint_flip_map = [['p1','p1'],['p2', 'p3'],['p4','p5'],['p6','p7'],['p8','p9'],['p10','p11'],['p12','p13']]


_root = os.getenv("CATTLE_DATASETS", "datasets")
register_keypoints_dataset(_root)