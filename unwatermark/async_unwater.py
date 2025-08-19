import httpx
import os
from asyncio import sleep
import aiofiles
from typing import Union, Optional

from unwatermark.models import ResponseData
from .common import HEADERS, CREATE_JOB_URL, GET_JOB_URL_TEMPLATE


class AsyncUnwater:
    async def remove_watermark(self, image_input: Union[str, bytes]) -> Optional[ResponseData]:
        async with httpx.AsyncClient(http2=True) as client:
            files = await self._prepare_files_async(image_input, client)
            response = await client.post(
                CREATE_JOB_URL,
                files=files,
                headers=HEADERS
            )

            response_data = ResponseData.parse_obj(response.json())
            job_id = response_data.result.job_id

            while True:
                result = await client.get(
                    GET_JOB_URL_TEMPLATE.format(job_id=job_id)
                )
                status = ResponseData.parse_obj(result.json())
                if status.result and status.result.output_image_url:
                    return status
                await sleep(1)

    async def _prepare_files_async(self, image_input: Union[str, bytes], client: httpx.AsyncClient) -> dict:
        if isinstance(image_input, bytes):
            return {"original_image_file": image_input}
        elif isinstance(image_input, str):
            if image_input.startswith("http://") or image_input.startswith("https://"):
                response = await client.get(image_input)
                return {"original_image_file": response.content}
            elif os.path.isfile(image_input):
                async with aiofiles.open(image_input, "rb") as f:
                    return {"original_image_file": await f.read()}
        raise ValueError("Invalid input format: must be file path, URL, or bytes.")
