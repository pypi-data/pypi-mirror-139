#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import setuptools
from Strings2 import strings

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Strings2',
    version=strings.__version__,
    author=strings.__name__,
    author_email='121116728@qq.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/CountChangye/Strings2',
    packages=setuptools.find_packages(),
    license='LICENSE',
    description='Some operations on strings',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
