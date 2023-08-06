import os

from setuptools import find_namespace_packages, setup

package_version = os.environ.get("CI_COMMIT_TAG") or "0.dev0"

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

title = "kontur-unp1c"
author = "korotovskih"
email = "korotovskih@kontur.ru"
url = "https://git.skbkontur.ru/python-libs/unp1c"

requires_dev = [
    "black",
    "flake8==4.0.1; python_version < '3.7'",
    "flake8; python_version >= '3.7'",
    "pytest",
    "pytest-cov",
    "pytest-runner",
]

tests_require = [
    "pytest",
    "pytest-cov",
    "pytest-runner",
]

setup(
    name=title,
    version=package_version,
    description="Сбор/разбор бинарей 1С:Предприятие",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=["dataclasses; python_version < '3.7'"],
    setup_requires=tests_require,
    tests_require=tests_require,
    url=url,
    packages=find_namespace_packages(include=["kontur.*"]),
    entry_points={},
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
