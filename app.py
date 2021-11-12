#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from remedy_delete_default_vpcs.remedy_delete_default_vpcs_stack import RemedyDeleteDefaultVpcsStack

app = cdk.App()

RemedyDeleteDefaultVpcsStack(
    app, 'RemedyDeleteDefaultVpcsStack',
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('delete-default-vpcs','delete-default-vpcs')

app.synth()
