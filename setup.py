from setuptools import setup, find_packages

setup(
    name="backend-academy-2024-python-template",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "analyzer=src.main:main",
        ],
    },
)
