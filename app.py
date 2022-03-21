#!/usr/bin/env python3
''' module that instantiates cdk stacks '''
import os

import aws_cdk as cdk

from no_ops.no_ops_stack import NoOpsStack


app = cdk.App()
NoOpsStack(app, "NoOpsStack", env=cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region='eu-central-1'
))

app.synth()
