from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ftpbr',
    version='0.0.1',
    description='A basic  installer',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='',
    author='em',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='ftpbr',
    packages=find_packages()
)
