from typing import Tuple, List, Dict, Iterable, Optional

import numpy as np
from numpy.typing import NDArray
from sklearn import metrics

from dldseval.utils import class_indices_from_confidences


def prepare_per_item_classification_predictions(data: Iterable[Tuple[Dict, List[int]]],
                                                evaluation_classes: List[int],
                                                multilabel: bool = False) -> Tuple[NDArray[float], NDArray[int],
                                                                                   NDArray[float]]:
    """
    Prepare the per item classification results based on the provided classes for evaluation. This method
    concatenates all predictions for further evaluation.

    :param data: Iterable of tuple containing classification predictions and ground truth labels per item.
    :param evaluation_classes: Only these classes are evaluated.
    :param multilabel: Return annotations with multiple labels (not yet implemented).
    :return: Prepared classification results for further evaluation (concatenated predictions and annotations).
    """

    predictions: List[List[float]] = []
    annotations: List[int] = []
    max_confidences_unevaluated_class: List[float] = []

    if multilabel:
        # TODO return 2-dimensional annotation array
        raise NotImplemented

    for d in data:
        prediction: Dict = d[0]
        annotation: List[int] = d[1]

        prediction_classes = prediction.get('classes')
        prediction_confidences = prediction.get('class_confidences')

        if not isinstance(prediction_classes, list) or not isinstance(prediction_confidences, list):
            continue

        prediction_classes = np.array([int(c) for c in prediction_classes])
        prediction_confidences = np.array(prediction_confidences)
        selected_confidences: List[float] = []
        for c in evaluation_classes:
            conf = prediction_confidences[prediction_classes == c]
            if len(conf) > 0:
                selected_confidences.append(float(conf[0]))
            else:
                selected_confidences.append(0.0)

        max_rest_confidence: float = 0
        for pred_conf, pred_class in zip(prediction_confidences, prediction_classes):
            if pred_class not in evaluation_classes:
                max_rest_confidence = max(max_rest_confidence, pred_conf)

        has_ground_truth_label = False
        for label in annotation:
            if label in evaluation_classes:
                has_ground_truth_label = True
                annotations.append(label)
                # we only add one label per item in the binary- and multiclass case
                break

        if has_ground_truth_label:
            predictions.append(selected_confidences)
            max_confidences_unevaluated_class.append(max_rest_confidence)

    predictions: np.ndarray = np.array(predictions).reshape((len(predictions), len(evaluation_classes)))
    annotations: np.ndarray = np.array(annotations)
    max_confidences_unevaluated_class: np.ndarray = np.array(max_confidences_unevaluated_class)

    return predictions, annotations, max_confidences_unevaluated_class


def evaluate_classification(predictions: NDArray, annotations: NDArray, evaluation_classes: List,
                            multilabel: bool = False) -> Dict:
    """
    Compute evaluation metrics for the provided classification predictions and annotations.

    :param predictions: 2-dimensional array containing confidences (n_items, n_classes).
    :param annotations: Array of ground truth classes per item (one class per item or, in case of multilabel,
                        2-dimensional array with one-hot-encoded labels).
    :param evaluation_classes: List of classes that should be evaluated.
    :param multilabel: Indicates the multilabel case.
    :return: Dictionary of classification metrics.
    """

    if multilabel:
        # TODO implement multilabel evaluation
        raise NotImplementedError

    if len(evaluation_classes) < 2:
        raise ValueError('Evaluated classes must contain at least two classes.')

    if multilabel and len(annotations.shape) != 2:
        raise ValueError('Classification annotations must be a 2-dimensional array in the case of '
                         'multiple labels per item (`multilabel`)')

    if multilabel and annotations.shape[1] != len(evaluation_classes):
        raise ValueError('Classification annotations must be a 2-dimensional with the same number of '
                         'classes as `evaluation_classes` array in the case of multiple labels per '
                         'item (`multilabel`)')

    if not multilabel and not len(annotations.shape) == 1:
        raise ValueError('Classification annotations must be a 1-dimensional array in the case of '
                         'one label per item.')

    if len(predictions.shape) != 2:
        raise ValueError('Classification predictions must be a 2-dimensional array.')

    if predictions.shape[0] != annotations.shape[0]:
        raise ValueError('Classification predictions and annotations must have the same length.')

    if predictions.shape[1] != len(evaluation_classes):
        raise ValueError('Classification predictions must have the same number of classes as `evaluated_classes`.')

    evaluation_results = {'evaluated_items': len(annotations), 'class_ids': evaluation_classes}

    pred_classes, confidences = class_indices_from_confidences(predictions, evaluation_classes)

    evaluation_results['confusion_matrix'] = {
        'absolute': metrics.confusion_matrix(annotations, pred_classes,
                                             labels=evaluation_classes).tolist(),
        'normalized_pred': metrics.confusion_matrix(annotations, pred_classes,
                                                    labels=evaluation_classes,
                                                    normalize='pred').tolist(),
        'normalized_true': metrics.confusion_matrix(annotations, pred_classes,
                                                    labels=evaluation_classes,
                                                    normalize='true').tolist()
    }

    evaluation_results['accuracy'] = {
        'absolute': metrics.accuracy_score(annotations, pred_classes),
        'normalized': metrics.accuracy_score(annotations, pred_classes)
    }

    evaluation_results['f1'] = {
        'micro': metrics.f1_score(annotations, pred_classes, labels=evaluation_classes, average='micro'),
        'macro': metrics.f1_score(annotations, pred_classes, labels=evaluation_classes, average='macro'),
        'weighted': metrics.f1_score(annotations, pred_classes, labels=evaluation_classes, average='weighted'),
        'per_class': metrics.f1_score(annotations, pred_classes, labels=evaluation_classes, average=None)
    }

    evaluation_results['precision'] = {
        'micro': metrics.precision_score(annotations, pred_classes, labels=evaluation_classes, average='micro'),
        'macro': metrics.precision_score(annotations, pred_classes, labels=evaluation_classes, average='macro'),
        'weighted': metrics.precision_score(annotations, pred_classes, labels=evaluation_classes, average='weighted'),
        'per_class': metrics.precision_score(annotations, pred_classes, labels=evaluation_classes, average=None)
    }

    evaluation_results['recall'] = {
        'micro': metrics.recall_score(annotations, pred_classes, labels=evaluation_classes, average='micro'),
        'macro': metrics.recall_score(annotations, pred_classes, labels=evaluation_classes, average='macro'),
        'weighted': metrics.recall_score(annotations, pred_classes, labels=evaluation_classes, average='weighted'),
        'per_class': metrics.recall_score(annotations, pred_classes, labels=evaluation_classes, average=None)
    }

    return evaluation_results
