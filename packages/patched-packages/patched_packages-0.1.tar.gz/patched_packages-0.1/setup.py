from setuptools import setup, find_packages 

VERSION = '0.1'
DESCRIPTION = 'This package contains patched packages for specific graphene_django, graphql_jwt and jwt versions to work with pyhton 3.9'

#Setting up 
setup(
    name="patched_packages",
    version=VERSION,
    author="Tinashe Chiraya",
    author_email="<shattyadrenal1@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent'  
    ],
    zip_safe=False
)