import json
import os
import typing

from decimal import Decimal
from urllib.parse import unquote

import boto3
from aws_xray_sdk.core import patch_all

ENV_METADATA_TABLE_NAME = "METADATA_TABLE_NAME"

patch_all()

def parse_s3_event(event) -> typing.Iterable[typing.Tuple[str, str]]:
    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]
        object_key = unquote(object_key)
        yield bucket_name, object_key

def lambda_handler(event: dict, context: "LambdaContext") -> None:
    
    print(json.dumps(event))

    # Initialize the boto3 client to talk to rekognition
    rekognition_client = boto3.client("rekognition")

    # Initialize a boto3 resource as an abstraction of the dynamo db table
    table = boto3.resource("dynamodb").Table(
        os.environ.get(ENV_METADATA_TABLE_NAME)
    )
    
    # Parse the s3 event, see above
    for bucket_name, object_key in parse_s3_event(event):
        
        response = rekognition_client.detect_labels(
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": object_key
                }
            }
        )
        
        print("Rekognition response:", json.dumps(response))
        
        # Flatten the response structure
        labels = []
        for item in response["Labels"]:
            labels.append({
                "Name": item["Name"],
                "Confidence": Decimal(str(item["Confidence"])),
                "Parents": item["Parents"]

            })

        # Store the item in the metadata table
        table.put_item(
            Item={
                "PK": object_key,
                "Labels": labels
            }
        )
