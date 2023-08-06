from setuptools import setup

setup(
    name='attrs-mek',
    version='0.0.0',
    author='Alex Rudolph',
    author_email='alex3rudolph@gmail.com',
    packages=['attrs-mek'],
    url='http://pypi.python.org/pypi/attrs-mek/',
    license='LICENSE',
    description='An awesome package that does something',
    long_description=open('README.md').read(),
    install_requires=[
        "attrs>=21.4.0",
        "pytest",
    ],
)