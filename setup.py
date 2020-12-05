from setuptools import find_packages, setup

setup(
    name='aoc',
    version='1.0',
    url='https://github.com/RazerM/advent-of-code-2019',
    author='Frazer McLean',
    author_email='frazer@frazermclean.co.uk',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'arpeggio ~= 1.10',
        'attrs ~= 20.3',
        'click ~= 7.1',
        'more-itertools ~= 8.0',
        'python-dotenv >= 0.15',
        'requests ~= 2.25',
        'sortedcontainers ~= 2.3',
    ],
    extras_require={
        'test': [
            'pytest ~= 6.0',
        ],
    },
    zip_safe=False,
)
