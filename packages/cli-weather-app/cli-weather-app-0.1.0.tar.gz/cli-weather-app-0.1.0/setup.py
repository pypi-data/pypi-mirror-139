import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cli-weather-app",
    version="0.1.0",
    description="A CLI app used to check the current weather condition of cities around the world",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/smith2eric/weather-app",
    author="Eric Alaribe",
    author_email="ericsmithsonian2@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    py_modules=['cli-weather-app'],

    entry_points={
        'console_scripts': ['cli-weather-app=weather:weather'],
    },
)