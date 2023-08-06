# facial-extractor

PyPi: [flare-face-extractor](https://pypi.org/project/flare-face-extractor/)

## API
* `locate_faces`
  * Calculates the location of all the faces in a given image.

* `outline_faces`
  * Opens a window displaying the image provided and outlines the faces present in the photo. 
    Should be used purely for interactive purposes.

* `count`
  * Returns the number of faces present in the given image.

## Publishing the package
1. Install packages in `requirements.txt`
2. Bump the version number in [setup.cfg](/setup.cfg)
3. Building (Now run this command from the same directory where [pyproject.toml](pyproject.toml) is located): 
   `python3 -m build`
4. Get the PyPI API token
5. Run Twine to upload all the archives under `dist`: 
   `python3 -m twine upload dist/*`
  1. username: `__token__`
  2. password: the PyPi token  including the `pypi-` prefix

## Helpful links 
* [Instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/)