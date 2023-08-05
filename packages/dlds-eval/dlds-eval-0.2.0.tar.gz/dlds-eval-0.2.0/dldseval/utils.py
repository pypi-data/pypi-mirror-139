from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray, ArrayLike


def class_indices_from_confidences(confidences: NDArray[np.float_],
                                   evaluated_classes: Optional[ArrayLike] = None) -> Tuple[NDArray[np.int_],
                                                                                           NDArray[np.int_]]:
    """
    Get class indices from an array of confidences.

    :param confidences: Array containing the confidence for each instance. One row per instance and
                        one column per class.
    :param evaluated_classes: Array containing the class IDs that describe the columns of the confidence array.
                              If not provided, class IDs are [0, 1, 2, ...].
    :return: Array containing class indices.
    """
    if confidences.shape[0] == 0 or confidences.shape[1] == 0:
        return np.empty((0,), dtype=np.int_), np.empty((0,), dtype=np.int_)

    max_classes = np.argmax(confidences, axis=1)
    max_confidences = np.take_along_axis(confidences, np.expand_dims(max_classes, axis=1), axis=1).reshape(
        (confidences.shape[0]))
    if evaluated_classes is not None:
        evaluated_classes = np.array(evaluated_classes)
        return evaluated_classes[max_classes], max_confidences
    return max_classes, max_confidences
