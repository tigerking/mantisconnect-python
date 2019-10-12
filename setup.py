from setuptools import setup
from setuptools import find_packages
import mantisconnect2

setup(
    name=mantisconnect2.__module_name__,
    version=mantisconnect2.__version__,
    description=mantisconnect2.__doc__.strip(),
    author='Ji Haijun',
    author_email='tigerking1218@gmail.com',
    url='https://github.com/tigerking/mantisconnect2',
    license=mantisconnect2.__license__,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
