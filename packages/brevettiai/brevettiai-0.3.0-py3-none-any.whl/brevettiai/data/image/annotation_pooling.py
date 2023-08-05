import tensorflow as tf

import brevettiai.interfaces.vue_schema_utils as vue
from brevettiai.platform.models import JobSettings
from pydantic import Field, PrivateAttr
from typing_extensions import Literal
from typing import Union, Tuple, List

class AnnotationPooling(JobSettings):
    """pydantic module for average pooling"""
    pooling_method: Literal["max", "average"] = Field(default="max")
    input_key: str = Field(default="segmentation")
    output_key: str = Field(default=None)
    pool_size: Union[Tuple[int, int], List[int]] = Field(default=None)

    _pooling_algorithms: dict = PrivateAttr(default_factory=dict)
    def __init__(self, **data):
        super().__init__(**data)

        if self.output_key is None:
            self.output_key = self.input_key

        self._pooling_algorithms = {"max": tf.keras.layers.MaxPool2D,
                                   "average": tf.keras.layers.AveragePooling2D}

    def __call__(self, x, *args, **kwargs):
        inp = x[self.input_key]
        x[self.output_key] = self._pooling_algorithms[self.pooling_method](
            pool_size=self.pool_size)(inp)
        return x
