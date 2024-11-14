import asyncio
import aiofiles
import httpx
import os
from typing import Union, Optional

class AsyncUnwater:
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

    async def remove_watermark(self, image_input: Union[str, bytes]) -> Optional[str]:
        async with httpx.AsyncClient(http2=True) as client:
            files = await self._prepare_files(image_input, client)
            response = await client.post(
                "https://api.unwatermark.ai/api/unwatermark/v4/ai-remove-auto/create-job",
                files=files,
                headers=self.headers_water
            )
            response_data = response.json()
            job_id = response_data['result']['job_id']

            while True:
                result = await client.get(
                    f"https://api.unwatermark.ai/api/unwatermark/v4/ai-remove-auto/get-job/{job_id}"
                )
                status = result.json()
                if status['result'] is not None:
                    return status['result']['output_image_url'][0]
                await asyncio.sleep(1)

    async def _prepare_files(self, image_input: Union[str, bytes], client: httpx.AsyncClient) -> dict:
        if isinstance(image_input, bytes):
            return {"original_image_file": image_input}
        elif isinstance(image_input, str):
            if image_input.startswith("http://") or image_input.startswith("https://"):
                response = await client.get(image_input)
                return {"original_image_file": response.content}
            elif os.path.isfile(image_input):
                async with aiofiles.open(image_input, "rb") as f:
                    file_content = await f.read()
                return {"original_image_file": file_content}
        raise ValueError("Invalid input format: must be file path, URL, or bytes.")
