# segment-logs

Load and process Segment logs from S3.

## Getting started

### Local processing using Spark

#### Install dependencies

```bash
brew install parallel

python -m venv .venv
source .venv/bin/activate
pip install pyspark
```

#### Fetch data
```bash
aws configure --profile lightspeed-telemetry
export AWS_PROFILE=lightspeed-telemetry
export AWS_S3_URL=s3://host/prefix
aws s3 sync $AWS_S3_URL data/raw
```

#### (Optional) Extract local data and cache (for better local performance)
```bash
find data/raw -type f | parallel --bar 'gzcat {} | jq -c "."' > data/all.jsonl
```

#### Start PySpark
```bash
pyspark
```

#### Process data in PySpark
```python
spark.conf.set("spark.sql.debug.maxToStringFields", 1000)
df_all = spark.read.json("./data/all.jsonl")
```

#### Example query
```python
from pyspark.sql.functions import col

completions = df_all.alias("completions").alias("completions")
feedback = df_all.filter("event == 'inlineSuggestionFeedback'").alias("feedback")

top = completions.join(feedback, col("completions.properties.metadata.activityId") == col("feedback.properties.activityId")) \
    .where(col("feedback.properties.action") == 0) \
    .groupBy(col("completions.properties.request.prompt")) \
    .count() \
    .orderBy("count", ascending=False)

top.show()
```

### Remote processing using Jupyter

#### Run the notebook

```bash
AWS_S3_URI=s3://<bucket>/segment-logs/<path> \
AWS_PROFILE=<profile name> \
jupyter notebook load.ipynb
```

## Development

#### Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements-dev.txt
```

#### Run checks
```bash
tox -e linters
```
