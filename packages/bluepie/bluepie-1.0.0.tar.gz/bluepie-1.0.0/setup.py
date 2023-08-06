import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="bluepie",
    version="1.0.0",
    author="Irnas",
    author_email="iot@irnas.eu",
    description="This repository contains often used BLE wrappers around bleak.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IRNAS/irnas-bluepie-software",
    project_urls={
        "Bug Tracker": "https://github.com/IRNAS/irnas-bluepie-software/issues"
    },
    license="GPLv2",
    packages=["bluepie"],
    install_requires=["bleak >= 0.14.2", "rich >= 11.2.0"],
    classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Operating System :: POSIX :: Linux",
        ],
)
