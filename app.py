#!/usr/bin/env python3
import os

import aws_cdk as cdk

from remedy_delete_default_vpcs.remedy_delete_default_vpcs_stack import RemedyDeleteDefaultVpcsStack

app = cdk.App()

RemedyDeleteDefaultVpcsStack(
    app, 'RemedyDeleteDefaultVpcsStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = os.getenv('CDK_DEFAULT_REGION')
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('delete-default-vpcs','delete-default-vpcs')

app.synth()
