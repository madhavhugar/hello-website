from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='aiven-poc',
    version='1',
    description='Proof of concept for kafka and postgres using aiven',
    long_description='',
    author='Madhav Hugar',
    author_email='madhav.hugar@gmail.com',
    license='Apache Software License',
    packages=find_packages(),
    zip_safe=False,
    install_requires=REQUIREMENTS,
)
