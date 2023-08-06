import re

from setuptools import find_packages, setup

with open("requirements.txt", encoding="utf-8") as f:
    install_requires = [x.strip() for x in f.readlines()]

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("tsvkit/__init__.py", encoding="utf-8") as f:
    version = re.search(r'__version__\s*=\s*"(.*)"', f.read()).group(1)

setup(
    name="tsvkit",
    license="MIT",
    version=version,
    description="TSV toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="singchen",
    author_email="xhqsm@qq.com",
    url="https://github.com/5xc/tsvkit/",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={"console_scripts": ["tsvkit=tsvkit:main"]},
)
