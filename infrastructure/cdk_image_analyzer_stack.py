import os

import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_lambda_event_sources as lambda_event_sources
import aws_cdk.aws_s3 as s3
from aws_cdk import core

from lambda_bundler import build_lambda_package, build_layer_package

class CdkImageAnalyzerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        input_bucket = s3.Bucket(
            self,
            "input-bucket"
        )

        metadata_table = dynamodb.Table(
            self,
            "metadata-table",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(name="PK",type=dynamodb.AttributeType.STRING)
        )

        dependency_layer_path = build_layer_package(
            requirement_files=[os.path.join(os.path.dirname(__file__), "..", "src", "requirements.txt")]
        )

        dependency_layer = _lambda.LayerVersion(
            self,
            "dependency-layer",
            code=_lambda.Code.from_asset(path=dependency_layer_path),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_7, _lambda.Runtime.PYTHON_3_8]
        )

        lambda_package_path = build_lambda_package(
            code_directories=[os.path.join(os.path.dirname(__file__), "..", "src")],
        )

        processing_lambda = _lambda.Function(
            self,
            "processing-lambda",
            code=_lambda.Code.from_asset(path=lambda_package_path),
            handler="src.processing_lambda.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(30),
            environment={
                "METADATA_TABLE_NAME": metadata_table.table_name
            },
            layers=[dependency_layer],
            description="Triggers object recognition on an S3 object and stores the metadata",
            tracing=_lambda.Tracing.ACTIVE
        )

        # Allow Lambda to talk to Rekognition
        processing_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["rekognition:DetectLabels"],
                resources=["*"]
            )
        )

        # Create the S3 Event Trigger for Lambda
        processing_lambda.add_event_source(
            lambda_event_sources.S3EventSource(
                input_bucket,
                events=[s3.EventType.OBJECT_CREATED]
            )
        )

        input_bucket.grant_read(processing_lambda)
        metadata_table.grant_read_write_data(processing_lambda)
