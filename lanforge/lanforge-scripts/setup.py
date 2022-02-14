#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="lanforge_scripts",
    version="0.0.1",
    author="Candela Technologies",
    description="Automate LANforge devices",
    license='BSD 3-clause license',
    url='https://github.com/greearb/lanforge-scripts',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'plotly',
        'numpy',
        'cryptography',
        'paramiko',
        'bokeh',
        'pyarrow',
        'websocket-client',
        'xlsxwriter',
        'pyshark',
        'influxdb',
        'influxdb-client',
        'matplotlib',
        'pdfkit',
        'pip-search',
        'pyserial',
        'pexpect-serial',
        'scp',
        'dash',
        'pyjwt'],
    python_requires='>=3.6, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Homepage': 'https://www.candelatech.com'
    }
)
