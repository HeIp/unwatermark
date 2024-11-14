Unwatermark
==============

**Unwatermark** is a Python library for removing watermarks from images, supporting both asynchronous and synchronous operations via the Unwatermark API (Unwatermark.ai).

Installation
------------

Install the package using pip:

    pip install unwatermark -U

Usage
-----

This library includes two main classes: `AsyncUnwater` for asynchronous operations and `Unwater` for synchronous operations.

### Example Usage

#### Asynchronous

Using the `AsyncUnwater` class to remove a watermark asynchronously:

    import asyncio
    from unwatermark import AsyncUnwater
    
    async def main():
        async_unwater = AsyncUnwater()
        result_url = await async_unwater.remove_watermark("path, url or bytes")
        print(f"Watermark removed image URL: {result_url}")
    
    asyncio.run(main())
    

#### Synchronous

Using the `Unwater` class to remove a watermark synchronously:

    from unwatermark import Unwater
    
    unwater = Unwater()
    result_url = unwater.remove_watermark("path, url or bytes")
    print(f"Watermark removed image URL: {result_url}")
    

Project Details
---------------

*   **Version:** 1.1.0
*   **Author:** FSystem88
*   **Author Email:** ivan@fsystem88.ru
*   **Repository URL:** [GitHub](https://github.com/FSystem88/unwatermark)
*   **Repository URL:** [GitHub](https://Unwatermark.ai)

Dependencies
------------

This package depends on:

*   `httpx`
*   `aiofiles`

Requirements
------------

Python 3.6 or higher

License
-------

Unwatermark is licensed under the MIT License. See the LICENSE file for more details.

Classifiers
-----------

*   Programming Language :: Python :: 3
*   License :: OSI Approved :: MIT License
*   Operating System :: OS Independent