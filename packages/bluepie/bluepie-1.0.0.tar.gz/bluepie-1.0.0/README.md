# Irnas Bluepie Software

This repository contains often used BLE wrappers around [bleak](https://github.com/hbldh/bleak).

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BluePie like below.
Rerun this command to check for and install  updates.
```bash
pip install bluepie
```

## Developing

For development and testing the use of `virtualenv` is suggested.

Install `virtualenv`:
```bash
pip install virtualenv
```

Create and activate `virtualenv`, run this from project root:

```bash
virtualenv venv
. /venv/bin/activate
```

To make development of the python package more smooth you can run below command from the project root directory.
Changes that you make in the source code will be automatically available instead of running `pip install .` all time.
```bash
pip install --editable .
```

## Creating a PyPi package

Important: bump version in `setup.py` file.

Twine package is needed:
```bash
pip install twine
```

Create a wheel:
```bash
python3 setup.py sdist bdist_wheel
```

Check if everything is ok:
```bash
twine check dist/*
```

Upload to Test PyPi:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

After you made sure that everything is ok you can upload to PyPi:
```bash
twine upload dist/*
```

# License

Firmware and software originating from this repository is licensed under the [GNU General Public License v2.0](./LICENSE).

Open-source licensing means the hardware, firmware, software and documentation may be used without paying a royalty, and knowing one will be able to use their version forever. One is also free to make changes, but if one shares these changes, they have to do so under the same conditions they are using themselves. The name IRNAS is a mark of IRNAS LTD. This name and term may only be used to attribute the appropriate entity as required by the Open Licence referred to above. The names and marks may not be used in any other way, and in particular may not be used to imply endorsement or authorization of any hardware one is designing, making or selling.
