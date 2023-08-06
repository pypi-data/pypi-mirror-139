import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="wsnasa",
    version="0.0.2beta",
    description="Library for use nasa.api",
    url="https://github.com/anikolaev82/nasaapi",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Artem Nikolaev",
    author_email="anikolaev82@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    packages=["wsnasa",
              "wsnasa/services/",
              "wsnasa/services/apod",
              "wsnasa/services/rovers",
              "wsnasa/entity",
              "wsnasa/entity/abclass",
              "wsnasa/utils"
            ],
    include_package_data=True,
    install_requires=["requests", "sqlalchemy", "psycopg2-binary"]
)
