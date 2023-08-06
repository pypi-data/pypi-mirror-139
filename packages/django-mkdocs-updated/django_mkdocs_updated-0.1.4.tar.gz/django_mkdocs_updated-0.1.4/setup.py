import os
from setuptools import find_packages, setup

with open('README.md') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_mkdocs_updated',
    version='0.1.4',
    include_package_data=True,
    license='LGPL',
    description='MkDocs served by Django for permissioned access',
    author='Ali moradi',
    author_email='ali.mrd318@gmail.com',
    packages=['django_mkdocs'],
    install_requires=[
        'mkdocs',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.1",
)
