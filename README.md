# segment-logs

Load and process Segment logs from S3.

## Getting started

### Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Run the notebook

```bash
AWS_S3_URI=s3://<bucket>/segment-logs/<path> \
AWS_PROFILE=<profile name> \
jupyter notebook load.ipynb
```

## Development

### Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements-dev.txt
```

### Run checks
```bash
tox -e linters
```