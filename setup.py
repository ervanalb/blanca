from setuptools import setup

setup(
    name='blanca',
    packages=['blanca'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
)
