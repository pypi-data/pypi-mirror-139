# image-hashing

# facial-extractor

PyPi: [flare-image-hashing](https://pypi.org/project/flare-image-hashing/)

## API
* `hash_image`
  * Average Hash computation of the given image.

* `are_similar`
  * Returns True if two images are relatively similar.

## Publishing the package
1. Install packages in `requirements.txt`
2. Bump the version number in [setup.cfg](/setup.cfg)
3. Building (Now run this command from the same directory where pyproject.toml is located): 
   `python3 -m build`
4. Get the PyPI API token
5. Run Twine to upload all the archives under `dist`: 
   `python3 -m twine upload dist/*`
  1. username: `__token__`
  2. password: the PyPi token  including the `pypi-` prefix

### Shortcut
```shell
python3 -m build && python3 -m twine upload dist/*
```
## Helpful links 
* [Instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/)