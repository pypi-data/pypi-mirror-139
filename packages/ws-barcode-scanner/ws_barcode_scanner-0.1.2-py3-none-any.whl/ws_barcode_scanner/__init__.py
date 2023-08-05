import sys

if sys.version_info[:2] < (3, 8):
    import importlib_metadata as metadata
else:
    from importlib import metadata

from .barcode_scanner import BarcodeScanner

__version__ = metadata.version("ws-barcode-scanner")

__all__ = ["__version__", "BarcodeScanner"]
