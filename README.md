# Tagcounter

#### version 0.5.0 no GUI

### Installation

    python -m pip install .

### Usage

    python -m tagcounter command [command arguments] [--OPTIONS]
#### Example
Count tags on the default site `docs.python.org/3/`:

    python -m tagcounter synthetic

Create custom DB with the specific directory and fill with info:

    python -m tagcounter exec --website www.yahoo.com --uri /search?q=github+Forbea/tagcounter
