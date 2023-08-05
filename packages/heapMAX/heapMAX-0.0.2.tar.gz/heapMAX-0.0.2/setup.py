from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with open("C:/Users/user/Desktop/Max Heap Package/README.txt",'r') as fh:
    long_description =  fh.read()
    print(long_description)
VERSION = '0.0.2'
DESCRIPTION = 'implement max heap'
LONG_DESCRIPTION = 'A package that allows to implement Max Heap Data Structure and the related and relevant operations '

# Setting up
setup(
    name = "heapMAX",
    version = VERSION,
    author = "Mriganka Saikia",
    author_email = "mrigankas2001@gmail.com",
    packages=find_packages(),
    description = DESCRIPTION,
    LONG_DESCRIPTION = long_description,
    
    long_description_content_type = "text/markdown",
    keywords=['python', 'algorithm', 'heap', 'max heap'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
