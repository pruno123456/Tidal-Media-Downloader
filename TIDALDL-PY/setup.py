from setuptools import setup, find_packages
from tidal_dl.printf import VERSION

setup(
    name='pruno-dl',
    version=VERSION,
    license="Apache2",
    description="Pruno custom TIDAL downloader.",

    author='Oli',
    author_email="",

    packages=find_packages(exclude=['tidal_gui*']),
    include_package_data=False,
    platforms="any",
    install_requires=[
        "aigpy>=2022.7.8.1",
        "requests>=2.22.0",
        "pycryptodome",
        "pydub",
        "prettytable",
        "lxml",
    ],
    entry_points={
        'console_scripts': [
            'pruno-dl = tidal_dl:main',
        ]
    }
)
