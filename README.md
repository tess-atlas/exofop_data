# ExoFOP data for TESS-Atlas

This repo contains the code to query and save the [ExFOP](https://exofop.ipac.caltech.edu/tess/) candidate data for
TESS-Atlas. The data is saved in the `data` directory as a CSV table. It contains a column indicating if 2-minute cadence data is available for the candidate.


## Workflow

```bash

python update_exofop_data.py
git commit -am "Update exofop data"
git push
```
This will update the data in the `data` directory and upload the new data to the repo.
