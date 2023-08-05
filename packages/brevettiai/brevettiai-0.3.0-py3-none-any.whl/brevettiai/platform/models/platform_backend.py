import os
import logging
import numpy as np
import urllib
import requests
from brevettiai.io import path as path_utils
from .tag import Tag
from pydantic import Field, BaseModel
from typing import Union, List
from uuid import UUID

log = logging.getLogger(__name__)


class PlatformBackend(BaseModel):
    host: str = Field(default_factory=lambda: os.getenv("BREVETTIAI_HOST_NAME", "https://platform.brevetti.ai"))
    output_segmentation_dir: str = Field(default="output_segmentations")
    bucket_region: str = Field(default_factory=lambda: os.getenv("AWS_REGION", "eu-west-1"))
    data_bucket: str = Field(default_factory=lambda: os.getenv("BREVETTIAI_DATA_BUCKET", "s3://data.criterion.ai"))
    custom_job_id: str = Field(default="a0aaad69-c032-41c1-a68c-e9a15a5fb18c",
                               description="uuid of model type to use for custom jobs")

    @property
    def s3_endpoint(self):
        return f"s3.{self.bucket_region}.amazonaws.com"

    def resource_path(self, uuid: Union[str, UUID]) -> str:
        """
        Get location of a resource
        """
        return path_utils.join(self.data_bucket, str(uuid))

    def prepare_runtime(self):
        # Determine runtime
        on_sagemaker = os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI") is not None

        # Initialize services
        if on_sagemaker:
            from brevettiai.interfaces import sagemaker
            sagemaker.load_hyperparameters_cmd_args()

    def get_download_link(self, path):
        if path.startswith("s3://"):
            target = path[5:].split("/", 1)[1]
            return f"{self.host}/download?path={urllib.parse.quote(target, safe='')}"
        else:
            raise ValueError("Can only provide download links on s3")

    def get_root_tags(self, id, api_key) -> List[Tag]:
        r = requests.get(f"{self.host}/api/resources/roottags?key={api_key}&id={id}")
        if r.ok:
            return [Tag.parse_obj(x) for x in r.json()]
        else:
            log.warning("Could not get root tags")
            return []

    @property
    def custom_model_type(self):
        from .web_api_types import ModelType
        return ModelType(id=self.custom_job_id, name="custom job")


backend = PlatformBackend()
