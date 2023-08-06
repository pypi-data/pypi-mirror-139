#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 17 March, 2020
"""
from setuptools import setup

setup(
    name = "GMarkdownViewer",
    version = "0.0.1",
    author = "Ben Knisley",
    author_email = "benknisley@gmail.com",
    description = ("An application for viewing Markdown files."),
    url = "https://benknisley.com",
    license = "MIT",
    keywords = "markdown",
    install_requires=['Markdown==3.3.6', 'PyGObject==3.40.1'],
    packages=["MarkdownViewer",],
    long_description="A simple Markdown viewer, made with Python, GTK, and Webkit.",
    
    ## Set up bin files
    entry_points = {
        'console_scripts': [
            'MarkdownViewer = MarkdownViewer:main',                  
        ],              
    },

    ## Include aux package files (in MarkdownViewer folder)
    include_package_data=True,
    package_data={'MarkdownViewer': ['highlight_js.html', 'place_holder.md']},

    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)

