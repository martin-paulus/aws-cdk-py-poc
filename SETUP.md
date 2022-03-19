# AWS CDK setup

## Boostrap CDK in AWS account

* read [boostrap guide](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)
* look up aws account id,
  [instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html#FindingYourAWSId)
* bootstrap cdk in relevant account+region combinations:
  `cdk bootstrap aws://${account_id}/${region_name}`

## Initialize stack

* read [cdk intro](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html)
* execute in a new directory: `cdk init app --language python`
* activate the new virtualenv: `source .venvbin/activate`
* install default dependencies: `pip install -r requirements.txt`

## Provision resources

* add resource definitions to `${project_name}/${project_name}_stack.py`
* if stack is new, add entry to `app.py`
* optional: synthesize the CloudFormation template to preview changes:
  `cdk synth`
* optional: list defined stacks: `cdk list`
* deploy the stack: `cdk deploy ${stack_name}`
