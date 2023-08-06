from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
    name='topsis_bhuvnesh_101903607',
    version='0.0.1',
    description='Topsis package by Bhuvnesh Jindal-101903607-3CO23',
    author= 'Bhuvnesh Jindal',
    #url = '',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['bhuvnesh jindal', 'tiet', 'topsis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['topsis_bhuvnesh_101903607'],
    package_dir={'':'src'},
    install_requires = [
        'pandas'
    ]
)