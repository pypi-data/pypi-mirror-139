from setuptools import setup

setup(
    name='PyLambdaTest',
    url='https://github.com/deino475/PyLambdaTest',
    author='Nile Dixon',
    author_email='niledixon475@gmail.com',
    packages=['pylambdatest'],
    install_requires=[],
    version='0.2.1',
    license='GNU GPL-V2',
    description='A simple Python library for testing AWS Lambda functions.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    python_requires=">=3.6"
)