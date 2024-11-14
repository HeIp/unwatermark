from setuptools import setup, find_packages

setup(
    name="unwatermark",
    version="1.2.0",
    author="FSystem88",
    author_email="ivan@fsystem88.ru",
    description="A library for asynchronous and synchronous watermark removal from images using Unwatermark.ai",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FSystem88/unwatermark",
    packages=find_packages(),
    install_requires=["httpx", "aiofiles"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
