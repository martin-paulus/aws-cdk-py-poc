#!/usr/bin/env python3
''' module that instantiates cdk stacks '''
import os

import aws_cdk as cdk

from no_ops.no_ops_stack import NoOpsStack
from no_ops.cdn_stack import CdnStack


app = cdk.App()
NoOpsStack(app, "NoOpsStack", env=cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region='eu-central-1'
))
CdnStack(app, "CdnStack", env=cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region='us-east-1'
))

app.synth()
