namespace
=========

`namespace` is a Python translation of JSON files. It is fundamentaly a dictionary with attribute access to its keys.


Features:
---------
* saving to and loading from text files.
* value access via attributes (`x = obj.attr`) and keys (`x = obj['attr']`).
* pretty printed via print() function.
* for sake of simplicity, values loaded from files MUST be builtin types.
