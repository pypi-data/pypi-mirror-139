# toontown.py
A simple Python API wrapper for the Toontown Rewritten API (https://github.com/ToontownRewritten/api-doc/)

## Features
- Asynchronous and synchronous
- API complete

## Installing
**Python 3.8 or higher is required**

```zsh
# Linux/macOS
python3 -m pip install -U toontown.py

# Windows
py -3 -m pip install -U toontown.py
```

## About

All methods return a tuple-like wrapper class with all the response data wrapped in objects

e.g. This will print all the current doodles in Toontown Rewritten

```py
async with toontown.AsyncToontownClient() as client:
    doodles = await client.doodles()

    for doodle in doodles:
        print(doodle.district, doodle.playground, doodle.dna, doodle.rendition, doodle.traits, doodle.cost)
```
