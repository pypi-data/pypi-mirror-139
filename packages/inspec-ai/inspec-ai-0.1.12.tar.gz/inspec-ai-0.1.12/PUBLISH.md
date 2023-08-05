# Publishing Instructions

To create a package and publish, ensure the following:

- In file `inspec/__init__.py` ensure that `__version__` has the expected value.
- In file `setup.py` ensure that `version` is updated to the same value.
- Folders `dist/`, `build/` and `inspec.egg-info/` are deleted.

Then, run the following command in the project folder:

```
python setup.py sdist bdist_wheel
```

This will create the `dist/` folder that will contain the output with the correct version. You can verify
that the package was built correctly with the following *twine* command:

NOTE: You need to install manually with `pip install twine` before running the following commands.

```
twine check dist/*
```

To publish to Pypi's test to make sure everything is working correctly, you can run the following command:

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

To publish to Pypi live, use this command:

```
twine upload dist/*
```