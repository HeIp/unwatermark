import httpx
import os
import time
from typing import Union

from unwatermark.models import ResponseData
from .common import HEADERS, CREATE_JOB_URL, GET_JOB_URL_TEMPLATE
from .exceptions import UnwatermarkError


class Unwater:
    def remove_watermark(
        self,
        image_input: Union[str, bytes],
        timeout: int = 60,
        poll_interval: int = 2,
    ) -> ResponseData:
        """Removes a watermark from an image using the unwatermark.ai service.

        This is a synchronous operation that will block until the job is complete
        or the timeout is reached.

        Args:
            image_input: The image to process. Can be a file path (str),
                a public URL (str), or raw image data (bytes).
            timeout: The maximum time in seconds to wait for the job to complete.
                Defaults to 60.
            poll_interval: The time in seconds to wait between checking the
                job status. Defaults to 2.

        Returns:
            A ResponseData object containing the result, including the URL
            of the unwatermarked image.

        Raises:
            UnwatermarkError: If the job fails, the API returns an error,
                or the timeout is exceeded.
        """
        start_time = time.time()
        with httpx.Client(http2=True) as client:
            files = self._prepare_files_sync(image_input, client)
            try:
                response = client.post(
                    CREATE_JOB_URL, files=files, headers=HEADERS, timeout=10
                )
                response.raise_for_status()
            except httpx.RequestError as e:
                raise UnwatermarkError(f"Failed to create job: {e}") from e

            response_data = ResponseData.parse_obj(response.json())
            if response_data.code != 0 or not response_data.result or not response_data.result.job_id:
                raise UnwatermarkError(f"API Error creating job: {response_data.message.en}")

            job_id = response_data.result.job_id

            while time.time() - start_time < timeout:
                try:
                    result_response = client.get(
                        GET_JOB_URL_TEMPLATE.format(job_id=job_id), timeout=10
                    )
                    result_response.raise_for_status()
                except httpx.RequestError as e:
                    raise UnwatermarkError(f"Failed to poll job status: {e}") from e

                status = ResponseData.parse_obj(result_response.json())
                if status.code != 0:
                    raise UnwatermarkError(f"API Error polling job: {status.message.en}")

                if status.result and status.result.output_image_url:
                    return status
                time.sleep(poll_interval)

            raise UnwatermarkError(f"Timeout of {timeout}s exceeded while waiting for job {job_id}")

    def _prepare_files_sync(self, image_input: Union[str, bytes], client: httpx.Client) -> dict:
        try:
            if isinstance(image_input, bytes):
                return {"original_image_file": image_input}
            elif isinstance(image_input, str):
                if image_input.startswith("http://") or image_input.startswith("https://"):
                    response = client.get(image_input)
                    response.raise_for_status()
                    return {"original_image_file": response.content}
                elif os.path.isfile(image_input):
                    with open(image_input, "rb") as f:
                        return {"original_image_file": f.read()}
            raise ValueError("Invalid input format: must be file path, URL, or bytes.")
        except (httpx.RequestError, IOError, ValueError) as e:
            raise UnwatermarkError(f"Failed to read image input: {e}") from e
