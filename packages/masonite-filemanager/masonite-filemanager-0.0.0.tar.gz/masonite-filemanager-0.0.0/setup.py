from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="masonite-filemanager",
    version="0.0.0",
    author="Yubaraj Shrestha",
    author_email="companion.krish@outlook.com",
    description="File management solution for Masonite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yubarajshrestha/masonite-filemanager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Masonite",
    ],
    packages=[
        'filemanager',
        'filemanager.assets',
        'filemanager.config',
        'filemanager.controllers',
        'filemanager.drivers',
        'filemanager.providers',
        'filemanager.routes',
        'filemanager.views',
    ],

    package_dir={"": "src"},
    install_requires=[
        "masonite>=4.0,<5.0",
    ],
    license="MIT",
    include_package_data=True,
    keywords=["masonite", "storage", "filemanager", "masonite-filemanager"],
)
