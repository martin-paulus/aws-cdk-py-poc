import aws_cdk as core
import aws_cdk.assertions as assertions

from no_ops.no_ops_stack import NoOpsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in no_ops/no_ops_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NoOpsStack(app, "no-ops")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
