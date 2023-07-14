# Copyright (c) Facebook, Inc. and its affiliates.
from typing import List
import torch
from torch import nn
from torch.nn import functional as F

from detectron2.config import configurable
from detectron2.layers import Conv2d, ConvTranspose2d, cat, interpolate
from detectron2.structures import Instances, heatmaps_to_keypoints
from detectron2.utils.events import get_event_storage
from detectron2.utils.registry import Registry
from detectron2.modeling.roi_heads.keypoint_head import keypoint_rcnn_inference

from detectron2.modeling.roi_heads import KRCNNConvDeconvUpsampleHead
from detectron2.modeling.roi_heads.keypoint_head import ROI_KEYPOINT_HEAD_REGISTRY



def constrained_keypoint_rcnn_loss(pred_keypoint_logits, instances, normalizer, constrained_type='mask'):
    """
    inherit from det2 keypoint head
    """
    heatmaps = []
    gt_masks = []
    valid = []

    keypoint_side_len = pred_keypoint_logits.shape[2]
    for instances_per_image in instances:
        if len(instances_per_image) == 0:
            continue
        keypoints = instances_per_image.gt_keypoints
        heatmaps_per_image, valid_per_image = keypoints.to_heatmap(
            instances_per_image.proposal_boxes.tensor, keypoint_side_len
        )
        gt_masks_per_image = instances_per_image.gt_masks.crop_and_resize(
            instances_per_image.proposal_boxes.tensor, keypoint_side_len
        )
        heatmaps.append(heatmaps_per_image.view(-1))
        valid.append(valid_per_image.view(-1))
        gt_masks.append(gt_masks_per_image)

    if len(heatmaps):
        keypoint_targets = cat(heatmaps, dim=0)
        gt_masks = cat(gt_masks, dim=0)
        valid = cat(valid, dim=0).to(dtype=torch.uint8)
        valid = torch.nonzero(valid).squeeze(1)

    # torch.mean (in binary_cross_entropy_with_logits) doesn't
    # accept empty tensors, so handle it separately
    if len(heatmaps) == 0 or valid.numel() == 0:
        global _TOTAL_SKIPPED
        _TOTAL_SKIPPED += 1
        storage = get_event_storage()
        storage.put_scalar("kpts_num_skipped_batches", _TOTAL_SKIPPED, smoothing_hint=False)
        return pred_keypoint_logits.sum() * 0

    N, K, H, W = pred_keypoint_logits.shape
    pred_keypoint_logits = pred_keypoint_logits.view(N * K, H * W)
    gt_masks =  gt_masks.unsqueeze(1).repeat(1,K,1,1).view(N * K, H * W)

    valid_pred_keypoint_logits = pred_keypoint_logits[valid]
    valid_keypoint_targets = keypoint_targets[valid]
    valid_gt_masks = gt_masks[valid]

    if constrained_type == 'mask':
        tmp = valid_pred_keypoint_logits.clone()
        valid_pred_keypoint_logits[valid_gt_masks == False] = -100

        # # find where the keypoint heat map is set to -100 but the location is where the ground
        # # truth keypoint is located. Set this back to the original value so it doesn't affect the loss.
        valid_pred_keypoint_logits[torch.arange(len(valid)), valid_keypoint_targets] = \
                tmp[torch.arange(len(valid)), valid_keypoint_targets]

    keypoint_loss = F.cross_entropy(
        valid_pred_keypoint_logits, valid_keypoint_targets, reduction="sum"
    )

    # If a normalizer isn't specified, normalize by the number of visible keypoints in the minibatch
    if normalizer is None:
        normalizer = valid.numel()
    keypoint_loss /= normalizer

    return keypoint_loss




@ROI_KEYPOINT_HEAD_REGISTRY.register()
class ConstrainedKRCNNConvDeconvUpsampleHead(KRCNNConvDeconvUpsampleHead):
    """
    A constrained standard keypoint head containing a series of 3x3 convs, followed by
    a transpose convolution and bilinear interpolation for upsampling.
    """

    @configurable
    def __init__(self, input_shape, *, num_keypoints, conv_dims, constrained_type, **kwargs):
        """
        Args:
            input_shape (ShapeSpec): shape of the input feature
            conv_dims: an iterable of output channel counts for each conv in the head
                         e.g. (512, 512, 512) for three convs outputting 512 channels.
        """
        super().__init__(input_shape=input_shape, num_keypoints=num_keypoints, conv_dims=conv_dims, **kwargs)
        self.constrained_type = constrained_type

    @classmethod
    def from_config(cls, cfg, input_shape):
        ret = super().from_config(cfg, input_shape)
        ret["constrained_type"] = cfg.MODEL.ROI_KEYPOINT_HEAD.CONSTRAINED_TYPE
        return ret

    def forward(self, x, instances: List[Instances]):
        """
        inherit from det2 keypoint head
        """
        x = self.layers(x)
        if self.training:
            num_images = len(instances)
            normalizer = (
                None if self.loss_normalizer == "visible" else num_images * self.loss_normalizer
            )
            return {
                "loss_keypoint": constrained_keypoint_rcnn_loss(x, instances, normalizer=normalizer,
                                                                constrained_type=self.constrained_type)
                * self.loss_weight
            }
        else:
            keypoint_rcnn_inference(x, instances)
            return instances
