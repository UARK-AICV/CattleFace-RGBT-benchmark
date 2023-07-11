from detectron2.config import CfgNode as CN

def add_custom_config(cfg):
    cfg.MODEL.ROI_KEYPOINT_HEAD.CONSTRAINED_TYPE = "mask"
