#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages
from reportWaysonQi123 import HTMLTestRunner
# python setup.py sdist
# python setup.py bdist
# python setup.py bdist_egg
# python setup.py bdist_wheel
# twine upload dist/*0.1.4*
setup(
    name="reportWaysonQi123",
    version='1.0.1',
    keywords=("test report", "python unit testing"),
    url="",
    author="",
    author_email="",
    package_dir={'reportWaysonQi123': 'reportWaysonQi123'},
    packages=['reportWaysonQi123'],
    include_package_data=True,
    package_data={'reportWaysonQQQ': ['static/*', 'templates/*']},
    py_modules=[],
    data_files=[
        'reportWaysonQi123/static/js/capture.js',
        'reportWaysonQi123/templates/default.html',
        'reportWaysonQi123/static/css/default.css',
        'reportWaysonQi123/static/js/default.js',
        'reportWaysonQi123/templates/legency.html',
        'reportWaysonQi123/static/css/legency.css',
        'reportWaysonQi123/static/js/legency.js'
    ],
    platforms="any",
    install_requires=[
        'Jinja2==2.10',
        'Flask==1.0.2'
    ],
    scripts=[],
    entry_points={
        'console_scripts': [
            'reportWaysonQi123.shell = reportWaysonQi123:shell',
            'reportWaysonQi123.web = reportWaysonQi123:web'
        ], "pytest11": ["reportWaysonQi123 = reportWaysonQi123.PyTestReportPlug"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest"
    ],
    zip_safe=False
)
