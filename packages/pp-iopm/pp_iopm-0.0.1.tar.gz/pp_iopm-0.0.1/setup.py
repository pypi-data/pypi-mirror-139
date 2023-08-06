import setuptools

import pp_iopm

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name=pp_iopm.__name__,
    version=pp_iopm.__version__,
    author=pp_iopm.__author__,
    author_email=pp_iopm.__author_email__,
    description="An Abstraction-Based Approach for Privacy-Aware Inter-Organizational Process Mining",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m4jidRafiei/pp-iopm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pm4py >= 2.2.18'
    ],
    project_urls={
        'Source': 'https://github.com/m4jidRafiei/pp-iopm'
    }
)