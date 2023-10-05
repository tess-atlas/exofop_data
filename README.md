# ExoFOP data for TESS-Atlas
[![Update ExoFOP data](https://github.com/tess-atlas/exofop_data/actions/workflows/update_dataset.yml/badge.svg)](https://github.com/tess-atlas/exofop_data/actions/workflows/update_dataset.yml)

This repo contains the code to query and save the [ExFOP](https://exofop.ipac.caltech.edu/tess/) candidate data for
TESS-Atlas. The data is saved as a CSV table in the `data` directory. It contains a column indicating if 2-minute cadence data is available for the candidate.


## Workflow

```bash

python update_exofop_data.py
git commit -am "Update exofop data"
git push
```
This will update the data in the `data` directory and upload the new data to the repo.
