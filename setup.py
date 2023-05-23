from setuptools import setup, find_packages

setup(
    name='astrocat',
    version='0.1',
    packages=find_packages(),
    description='Crossmatching catalogs in astrophysics',
    author='Bruno Arsioli',
    author_email='bruno.arsioli@proton.me',
    license='MIT',
    install_requires=[
        'astropy',
        'numpy',
        'pandas',
    ],
)
