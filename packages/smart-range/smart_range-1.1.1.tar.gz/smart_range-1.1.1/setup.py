from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='smart_range',
    version='1.1.1',
    packages=['smart_range'],
    url='https://github.com/PythonCoderAS/SmartRange',
    license='MIT',
    author='PythonCoderAS',
    author_email='sarkaraoyan@gmail.com',
    description='A class to easily deal with ranges.',
    extras_require={"docs": ["sphinx"]},
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6'
)
