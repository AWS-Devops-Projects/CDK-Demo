#!/usr/bin/env python3

from aws_cdk import core

from infrastructure.cdk_image_analyzer_stack import CdkImageAnalyzerStack


app = core.App()
CdkImageAnalyzerStack(app, "cdk-image-analyzer")

app.synth()
