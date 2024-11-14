import httpx
import os
from time import sleep
from typing import Union, Optional
from models import ResponseData

class Unwater:
    def __init__(self):
        self.headers_water = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru,en;q=0.9",
            "authorization": "",
            "origin": "https://unwatermark.ai",
            "product-code": "067003",
            "product-serial": "5806ba128e7d0d881cfea62b1cff0e86",
            "referer": "https://unwatermark.ai/",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0"
        }

    def remove_watermark(self, image_input: Union[str, bytes]) -> Optional[str]:
        with httpx.Client(http2=True) as client:
            files = self._prepare_files_sync(image_input, client)
            response = client.post(
                "https://api.unwatermark.ai/api/unwatermark/v4/ai-remove-auto/create-job",
                files=files,
                headers=self.headers_water
            )
            response_data = ResponseData.parse_obj(response.json())
            job_id = response_data.result.job_id

            while True:
                result = client.get(
                    f"https://api.unwatermark.ai/api/unwatermark/v4/ai-remove-auto/get-job/{job_id}"
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
