# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

with open("README.md",'r',encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Morse-ruxia-TJY',
    version='0.0.1',
    keywords='Morse encode decode',
    description='Morse encode/decode',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ruxia-TJY",
    author_email="ruxia.tjy@qq.com",
    url="https://github.com/ruxia-TJY/Morse",
    download_url="https://github.com/ruxia-TJY/Morse",
    project_urls={
        "Bug Tracker":"https://github.com/ruxia-TJY/Morse/issues",
    },
    install_requires=[],
    packages=find_packages(),
    license='BSD 3-Clause',
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: BSD License'
    ]


)
