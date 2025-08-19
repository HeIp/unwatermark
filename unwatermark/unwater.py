import httpx
import os
from time import sleep
from typing import Union, Optional

from unwatermark.models import ResponseData
from .common import HEADERS, CREATE_JOB_URL, GET_JOB_URL_TEMPLATE


class Unwater:
    def remove_watermark(self, image_input: Union[str, bytes]) -> Optional[ResponseData]:
        with httpx.Client(http2=True) as client:
            files = self._prepare_files_sync(image_input, client)
            response = client.post(
                CREATE_JOB_URL,
                files=files,
                headers=HEADERS
            )
            response_data = ResponseData.parse_obj(response.json())
            job_id = response_data.result.job_id

            while True:
                result = client.get(
                    GET_JOB_URL_TEMPLATE.format(job_id=job_id)
                )
                status = ResponseData.parse_obj(result.json())
                if status.result and status.result.output_image_url:
                    return status
                sleep(1)

    def _prepare_files_sync(self, image_input: Union[str, bytes], client: httpx.Client) -> dict:
        if isinstance(image_input, bytes):
            return {"original_image_file": image_input}
        elif isinstance(image_input, str):
            if image_input.startswith("http://") or image_input.startswith("https://"):
                response = client.get(image_input)
                return {"original_image_file": response.content}
            elif os.path.isfile(image_input):
                with open(image_input, "rb") as f:
                    return {"original_image_file": f.read()}
        raise ValueError("Invalid input format: must be file path, URL, or bytes.")
