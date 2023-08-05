from typing import Tuple, List, Dict, Iterable, Any

import numpy as np
from numpy.typing import NDArray

from dldseval.utils import class_indices_from_confidences

IOU_THRESHOLDS = (0.05, 0.5, 0.7, 0.95)


def intersection_over_union(boxes1: NDArray[np.float_], boxes2: NDArray[np.float_], rotation_factor: float = 1.0):
    """
    Compute the IoU of the two given boxes.

    :param boxes1: Array containing boxes.
    :param boxes2: Array containing boxes.
    :param rotation_factor: multiplier for rotation matching
    :return: Intersection over union (IoU) between all `boxes1` and all `boxes2`. The resulting array has
             the shape `(len(boxes1), len(boxes2))`.
    """
    if boxes1.shape[0] == 0 or boxes2.shape[0] == 0:
        return np.empty((boxes1.shape[0], boxes2.shape[0]))

    if boxes1.ndim == 1:
        boxes1_n = np.expand_dims(boxes1, 0)
    else:
        boxes1_n = boxes1

    x1 = np.expand_dims(boxes1_n[:, 0], 0)
    y1 = np.expand_dims(boxes1_n[:, 1], 0)
    w1 = np.expand_dims(boxes1_n[:, 2], 0)
    h1 = np.expand_dims(boxes1_n[:, 3], 0)

    if boxes2.ndim == 1:
        boxes2_n = np.expand_dims(boxes2, 0)
    else:
        boxes2_n = boxes2

    x2 = np.expand_dims(boxes2_n[:, 0], 0)
    y2 = np.expand_dims(boxes2_n[:, 1], 0)
    w2 = np.expand_dims(boxes2_n[:, 2], 0)
    h2 = np.expand_dims(boxes2_n[:, 3], 0)

    dx = np.abs(x1 - x2.T)
    dy = np.abs(y1 - y2.T)

    w_intersect = np.minimum(np.maximum(0.0, 0.5 * w1 + 0.5 * w2.T - dx), np.minimum(w1, w2.T))
    h_intersect = np.minimum(np.maximum(0.0, 0.5 * h1 + 0.5 * h2.T - dy), np.minimum(h1, h2.T))

    area1 = np.multiply(w1, h1)
    area2 = np.multiply(w2, h2)
    area_intersect = np.multiply(w_intersect, h_intersect)

    area_union = area1 + area2.T - area_intersect

    iou = np.divide(area_intersect, area_union, out=np.zeros_like(area_intersect),
                    where=area_union != 0).T

    # todo: multiply with (1- rotation difference) für pseudo rotIoU
    iou *= rotation_factor
    return np.array(iou)


def determine_tp_fp_fn(gt_boxes: NDArray[np.float_],
                       gt_classes: NDArray[np.int_],
                       boxes: NDArray[np.float_],
                       classes: NDArray[np.int_],
                       evaluated_classes: NDArray[np.int_],
                       iou_threshold: float = 0.5) -> Tuple[List[List[bool]], List[List[bool]]]:
    """
    Determine true positives, false positives, and false negatives.

    :param gt_boxes: 2-dimensional array with one row per ground truth object.
                     Columns: [x, y, width, height, orientation].
    :param gt_classes: 1-dimensional array containing the class of each ground truth object.
    :param boxes: 2-dimensional array with one row per predicted box. Columns: [x, y, width, height, orientation].
    :param classes: 1-dimensional array containing the class of each predicted object.
    :param evaluated_classes: 1-dimensional array containing the class IDs that should be evaluated.
    :param iou_threshold: Threshold for the intersection over union that is used for matching detections to ground truth
                          objects.
    :return: Tuple with two arrays: The first array contains one boolean per detection indicating
                                    as true/false positive.
                                    The second array contains one boolean per ground truth object
                                    and indicates if it was matched with a detection (true positive)
                                    or not (false negative).
    """

    #  array indicating tp/fp for each predicted object for each class
    is_tp_or_fp = []

    #  array indicating tp/fn for each ground truth object for each class
    is_tp_or_fn = []

    for c in evaluated_classes:
        gt_boxes_class_i = gt_boxes[gt_classes == c]
        n_gt_boxes_class_i = gt_boxes_class_i.shape[0]
        no_gt = (n_gt_boxes_class_i == 0)

        class_i_indices = classes == c
        no_detections = class_i_indices.shape[0] == 0

        boxes_class_i = boxes[class_i_indices]
        n_detections_class_i = boxes_class_i.shape[0]

        if no_detections or no_gt:
            # add all gt as false negatives
            is_tp_or_fn.append([False for _ in range(n_gt_boxes_class_i)])

            # add all detections as false positives
            is_tp_or_fp.append([False for _ in range(n_detections_class_i)])
            continue

        is_tp_or_fn_class_i = [False for _ in range(len(gt_boxes_class_i))]

        # TODO compute IoU of rotated boxes
        iou = intersection_over_union(gt_boxes_class_i, boxes_class_i)
        matched_gt_indices = np.argmax(iou, axis=0)

        is_tp_or_fp_class_i = []
        for j in range(n_detections_class_i):
            gt_idx = matched_gt_indices[j]
            is_true_positive = bool((iou[gt_idx, j] >= iou_threshold) and (not is_tp_or_fn_class_i[gt_idx]))
            if is_true_positive:
                is_tp_or_fn_class_i[gt_idx] = True
            is_tp_or_fp_class_i.append(is_true_positive)

        is_tp_or_fp.append(is_tp_or_fp_class_i)
        is_tp_or_fn.append(is_tp_or_fn_class_i)

    return is_tp_or_fp, is_tp_or_fn


def compute_per_item_detection_metrics(detection_results: Dict, objects: List,
                                       iou_thresholds=IOU_THRESHOLDS) -> Dict:
    """
    Compute (intermediate) detection metrics for one item (image). The intermediate results can be stored for later
    evaluation.

    :param detection_results: Detection results containing 'boxes' and 'confidences'.
    :param objects: Ground truth object labels.
    :param iou_thresholds: IoU thresholds for which to compute the metrics.
    :return: Intermediate detection metrics containing 'tp_fp, 'tp_fn', and 'confidences' per class for
             multiple IoU thresholds.
    """
    detection_metrics = dict()

    gt_boxes = np.array([[o['x'], o['y'], o['width'], o['height'], o['orientation']] for o in objects])
    gt_classes = np.array([o['label'] for o in objects])
    boxes = np.array(detection_results.get('boxes', []))
    confidences = np.array(detection_results.get('class_confidences', []))
    evaluated_classes = detection_results.get('classes')
    if evaluated_classes is None or len(evaluated_classes) == 0:
        raise ValueError('Detection classes not available.')

    pred_classes, max_confidences = class_indices_from_confidences(confidences, evaluated_classes)

    detection_metrics['gt'] = {
        'per_class': {f'{c}': int(np.sum(gt_classes == c)) for c in evaluated_classes}
    }
    detection_metrics['gt']['total'] = int(sum(detection_metrics['gt']['per_class'].values()))

    for iou_threshold in iou_thresholds:
        is_tp_or_fp, is_tp_or_fn = determine_tp_fp_fn(gt_boxes,
                                                      gt_classes,
                                                      boxes,
                                                      pred_classes,
                                                      evaluated_classes,
                                                      iou_threshold=iou_threshold)

        iou_key = f'iou_{iou_threshold:.2f}'
        detection_metrics[iou_key] = dict()
        for i, c in enumerate(evaluated_classes):
            detection_metrics[iou_key][str(c)] = {
                'tp_fp': is_tp_or_fp[i],
                'tp_fn': is_tp_or_fn[i],
                'confidences': (max_confidences[pred_classes == c]).tolist()
            }

    return detection_metrics


def prepare_per_item_detection_metrics(metrics: Iterable[Dict], evaluation_classes: List,
                                       iou_thresholds=IOU_THRESHOLDS) -> Tuple:
    """
    Prepare the per item detection metrics based on the provided classes for evaluation.

    :param metrics: Detection metrics obtained via `compute_per_item_detection_metrics`.
    :param evaluation_classes: Only these classes are evaluated.
    :param iou_thresholds: IoU thresholds for which to compute the metrics.
    :return: Prepared detection metrics for further evaluation.
    """

    prepared_metrics = {
        f'iou_{iou_th:.2f}': {
            f'{class_id}': {
                'confidences': [],  # sorted confidences of all objects
                'tp_fp': [],  # array indicating true positive / false positive (sorted as confidences)
            } for class_id in evaluation_classes
        } for iou_th in iou_thresholds
    }

    gt = {f'{class_id}': 0 for class_id in evaluation_classes}

    evaluated_items = 0
    for m in metrics:
        detection_metrics = m.get('detection')

        # skip if no detection metrics are given
        if detection_metrics is None:
            continue

        # skip if ground truth information are not provided
        if 'gt' not in detection_metrics:
            continue

        # check if all necessary iou_keys are available (otherwise, this item will be skipped)
        is_invalid = False
        for iou_key in prepared_metrics.keys():
            if iou_key not in detection_metrics:
                is_invalid = True
                break
        if is_invalid:
            continue

        for iou_key in prepared_metrics.keys():
            for i, class_id in enumerate(evaluation_classes):
                class_key = f'{class_id}'

                confidences = detection_metrics[iou_key][class_key]['confidences']
                prepared_metrics[iou_key][class_key]['confidences'].extend(confidences)

                tp_fp = detection_metrics[iou_key][class_key]['tp_fp']
                prepared_metrics[iou_key][class_key]['tp_fp'].extend(tp_fp)

        for class_id in evaluation_classes:
            gt[f'{class_id}'] += detection_metrics['gt']['per_class'][f'{class_id}']

        evaluated_items += 1

    return prepared_metrics, gt, evaluated_items


def evaluate_detection(prepared_metrics, gt) -> Dict:
    """
    Compute evaluation metrics for all given intermediate results.

    :param prepared_metrics: Prepared detection metrics obtained from `prepare_per_item_detection_metrics`.
    :param gt: Prepared ground truth counts obtained from `prepare_per_item_detection_metrics`.
    :return: Evaluation results for multiple IoU thresholds. Includes average precision (`ap`),
             and precision-recall curve (`pr_curve`) per evaluated class as well as mean average precision ('map').
    """
    evaluation_results = {}

    for iou_key, per_class_ir in prepared_metrics.items():
        evaluation_results[iou_key]: Dict[Any] = dict(per_class=dict(), map=0.0)
        aps = []

        for class_key, ir in per_class_ir.items():
            confidences = np.array(ir['confidences'])
            tp_fp = np.array(ir['tp_fp'])

            n_interpolates = 101
            r_interpolate = np.linspace(0.0, 1.0, n_interpolates)
            p_interpolate = np.zeros_like(r_interpolate)
            average_precision = 0

            if len(confidences) > 0:
                sorted_indices = np.argsort(confidences)[::-1]
                true_positives = np.cumsum(tp_fp[sorted_indices]).astype(np.float64)
                n_detections = len(confidences)

                # precision = TP / (TP + FP) = TP / n_detections
                precision = true_positives / np.arange(1, n_detections + 1)

                # recall = TP / (TP + FN) = TP / n_gt_boxes
                recall = np.divide(true_positives, gt[class_key],
                                   out=np.zeros_like(true_positives),
                                   where=gt[class_key] != 0)

                precision = np.expand_dims(precision, 1)
                for j in range(r_interpolate.shape[0]):
                    valid_precisions = precision[recall >= r_interpolate[j]]
                    if valid_precisions.shape[0] > 0:
                        p_interpolate[j] = np.max(valid_precisions, axis=0)
                    else:
                        p_interpolate[j] = 0.0

                average_precision = np.mean(p_interpolate)

            aps.append(average_precision)
            evaluation_results[iou_key]['per_class'][class_key] = {
                'ap': average_precision,
                'pr_curve': {
                    'r': list(r_interpolate),
                    'p': list(p_interpolate)
                }
            }

        if len(aps) > 0:
            mean_ap = float(np.mean(aps))
        else:
            mean_ap = 0.0
        evaluation_results[iou_key]['map'] = mean_ap

    return evaluation_results
