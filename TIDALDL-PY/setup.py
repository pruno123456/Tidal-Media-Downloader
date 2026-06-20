from setuptools import setup, find_packages

VERSION = "0.1.0"

setup(
    name='pruno-dl',
    version=VERSION,
    license="Apache2",
    description="Custom TIDAL downloader for tagged library workflows.",

    author='YaronH',
    author_email="yaronhuang@foxmail.com",

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
