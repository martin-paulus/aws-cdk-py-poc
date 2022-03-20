# AWS CDK setup

## Boostrap CDK in AWS account

* read [boostrap guide](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)
* look up aws account id,
  [instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html#FindingYourAWSId)
* bootstrap cdk in relevant account+region combinations:
  `cdk bootstrap aws://${account_id}/${region_name}`

### De-Bootstrap CDK in a region

* read [cdk bootstrap - no destroy option](https://github.com/aws/aws-cdk/issues/986)
* look up cdk staging bucket name: `aws s3 ls`
* empty cdk staging bucket:
  * capture object delete markers and versions: `markers_versions=$(aws --query "[DeleteMarkers,Versions][].{key: Key, version: VersionId}" s3api list-object-versions --bucket ${bucket_name})`
  * determine number of markers and versions: `count=$(echo "$markers_versions" | jq length)`
  * iterate over captured markers/versions and remove every item:
    `for item in $(seq 0 $((count-1))); do key=$(echo "$markers_versions" | jq -r ".[$item].key"); version=$(echo "$markers_versions" | jq -r ".[$item].version"); aws s3api delete-object --bucket "${bucket_name}" --key "$key" --version-id "$version"; done`
* look up cdk cloudformation stack name: `aws --query "StackSummaries[?StackStatus!='DELETE_COMPLETE'] | [].{name: StackName, description: TemplateDescription}" --region $region_name} cloudformation list-stacks`
* delete cloudformation stack: `aws --region ${region_name} cloudformation delete-stack --stack-name ${stack_name}`
* remove cdk staging bucket (if skipped by cloudformation): `aws s3 rb s3://${bucket_name}`

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
