import setuptools
from setuptools import find_packages

# Load the README and requirements
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'LoraLogger',
    version = '0.1.1',
    description = 'Custom LORA logger.',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://asklora.ai',
    author = 'LORA Tech',
    author_email = 'asklora@loratechai.com',
    package_dir = {
            '': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    zip_safe = False
)
