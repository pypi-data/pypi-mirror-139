# setup.py
from setuptools import setup
setup(
    name='mlchen', 
    setup_requires=['pillow'],
    packages=['mlchen'],
    data_files=['mlchen/drawing.jpg']
)