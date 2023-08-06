from setuptools import setup, find_packages

setup(
    name="PyBark",
    version="0.1",
    keywords=("pip", "PyBark", "Bark"),
    description="A simple Bark application for notification",
    long_description="A simple application to send a message push via Bark",
    license="MIT License",
    url="https://github.com/MrReochen/PyBark",
    author="Reo Chen",
    author_email="reo@pku.edu.cn",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
)