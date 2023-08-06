import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="recallai",
    version="0.0.1",
    description="recall.ai Python SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/recall-ai/recallai-python",
    author="Recall.ai",
    author_email="hello@recall.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["recallai"],
    include_package_data=True,
)