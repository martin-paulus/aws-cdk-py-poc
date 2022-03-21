# Deploy Content

The No-Ops portal page is comprised of a single index file. The portal content is stored in an AWS S3 bucket named **no-ops-portal** in the `portal_content/` path. In order to extend or update the content the new file(s) need to be uploaded to the S3 bucket.

## AWS CLI

Update a single file: `aws s3 cp index.html s3://no-ops-portal/portal_content/`

Note: Read the help section to synchronize multiple files instead: `aws s3 sync help`

## AWS Management Console

Navigate to the *S3* service, open the **no-ops-portal** bucket, then navigate to the `portal_content/` path. Next, click the *Upload* button followed by the *Add files* button. Finally, click the *Upload* button on the bottom right.
