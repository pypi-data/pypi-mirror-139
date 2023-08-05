"""
End-to-End Multi-Lingual Optical Character Recognition (OCR) Solution
"""

from setuptools import setup
from io import open

with open('Z:/_My Downloads/EasyOCR-master/EALOCR/EasyOCR-master/EasyOCR-master/requirements.txt', encoding="utf-8-sig") as f:
    requirements = f.readlines()

def readme():
    with open('Z:/_My Downloads/EasyOCR-master/EALOCR/EasyOCR-master/EasyOCR-master/README.md', encoding="utf-8-sig") as f:
        README = f.read()
    return README

setup(
    name='ealocr',
    packages=['ealocr'],
    include_package_data=True,
    version='1.4.4',
    install_requires=requirements,
    entry_points={"console_scripts": ["easyocr= easyocr.cli:main"]},
    license='Apache License 2.0',
    description='EasyAimLock forked edition / End-to-End Multi-Lingual Optical Character Recognition (OCR) Solution',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Rakpong Kittinaradorn',
    author_email='r.kittinaradorn@gmail.com',
    url='https://github.com/easyaimlock/easyocr',
    download_url='https://github.com/easyaimlock/easyocr.git',
    keywords=['ocr optical character recognition deep learning neural network eal easyaimlock'],
    classifiers=[
        'Development Status :: 5 - Production/Stable'
    ],
)
