# coding: utf-8
import os
import re

import boto3
import pandas as pd
from tqdm import tqdm

s3 = boto3.resource("s3")

m = re.search(r"s3://([^/]+)/(.*?([^/]+)/?)", os.environ["AWS_S3_URI"])

bucket = s3.Bucket(m.group(1))
objects = bucket.objects.filter(Prefix=m.group(2))

df = pd.DataFrame()

for obj in tqdm(objects):
    try:
        tempdf = pd.read_json(
            obj.get()["Body"], lines=True, compression="gzip", encoding="utf-8"
        )
        props = pd.json_normalize(tempdf["properties"])
        tempdf.drop(columns=["properties"])
        df = pd.concat([df, tempdf, props])
    except Exception as e:
        print(e)
