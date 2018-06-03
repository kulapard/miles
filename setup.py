import io
import os

from setuptools import find_packages, setup

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

requirements = []
with io.open(os.path.join(PROJECT_ROOT, 'requirements.txt')) as f:
    for line in f:
        requirements.append(line.strip())

setup(
    name='miles',
    version='0.0.1',
    license='BSD',
    maintainer='Taras Drapalyuk',
    maintainer_email='taras@drapalyuk.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    extras_require={
        'test': [
            'pytest',
        ],
    },
)
