
from setuptools import setup
from setuptools import find_packages

VERSION = '0.1'
AUTHORS = 'Matthew Bourque'
DESCRIPTION = 'Calculates the Foo et al. parameterization for atmospheric sea-spray physics'

REQUIRES = [
    'pytest',
]

setup(
    name='foo_parameterization',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/bourque/foo_parameterization.git',
    author=AUTHORS,
    author_email='matthewkbourque@gmail.com',
    license='BSD 3-Clause',
    keywords=['python'],
    classifiers=['Programming Language :: Python'],
    packages=find_packages(),
    install_requires=REQUIRES
)
