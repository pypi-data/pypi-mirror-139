from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name="priceit",                     # This is the name of the package
    version="0.1.6",                        # The initial release version
    author="David WANG",                     # Full name of the author
    description="Data extractor in financial market, including realtime price, history price, financial statements and more. Besides stocks, cryptocurrency is also covered.",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["priceit"],
    package_dir={'':'priceit/src'}, # Name of the python package
    # package_dir={'':'src'},     # Directory of the source code of the package
    install_requires=[
        'requests'
    ]                     # Install other dependencies if any
)