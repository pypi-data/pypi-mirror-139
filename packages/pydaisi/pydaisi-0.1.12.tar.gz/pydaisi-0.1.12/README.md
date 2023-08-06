# Simples Steps for PyDaisi SDK

## Preliminary Steps

Install with PIP:

- `pip install pydaisi`

Create your personal access token:

- https://dev3.daisi.io/settings/personal-access-tokens

## Using PyDaisi

Set your Personal Access Token:

- `import os`
- `os.environ["ACCESS_TOKEN"] = "L5d5r4p8zzWIvBx7RtkES4d0xnlB3bms"`

Import the Daisi Class:

- `from pydaisi import Daisi`

Connect to a Daisi:

- `daisi = Daisi("Titanic Service")`

Check the schema of a Daisi:

- `daisi.schema()`

Compute a Daisi:

- `daisi.compute(func="raw", rows=5)`
