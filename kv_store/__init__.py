from importlib import metadata

# https://github.com/python-poetry/poetry/issues/273#issuecomment-1103812336
__version__ = metadata.version(__package__)

del metadata  # optional, avoids polluting the results of dir(__package__)
