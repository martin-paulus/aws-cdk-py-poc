''' module for managing the no-ops.nl cdn resources '''
from aws_cdk import (
    aws_certificatemanager as certificatemanager,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_s3 as s3,
    Stack
)
from constructs import Construct

BUCKET_NAME = 'no-ops-portal'
CDN_DOMAIN = 'portal.no-ops.nl'


class CdnStack(Stack):
    ''' resource definitions for the cdn stack  '''

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.public_zone = self.refer_dns_zone()
        self.cdn_cert = self.provision_cdn_cert()
        self.bucket = self.refer_bucket()
        self.cdn = self.provision_cdn()
        self.provision_cdn_dns()

    def provision_cdn(self):
        ''' provision cdn resources '''
        cdn = cloudfront.Distribution(
            self, 'no-ops_cdn', certificate=self.cdn_cert,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(
                    # self.bucket, origin_access_identity=origin_id,
                    self.bucket,
                    origin_path='/portal_content'
                ),
                viewer_protocol_policy=(
                    cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
                )
            ),
            default_root_object='index.html',
            domain_names=[CDN_DOMAIN],
            minimum_protocol_version=(
                cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021
            ),
            price_class=cloudfront.PriceClass.PRICE_CLASS_100
        )
        return cdn

    def provision_cdn_cert(self):
        ''' provision cdn certificate '''
        cert_validation = certificatemanager.CertificateValidation.from_dns(
            self.public_zone
        )
        cdn_cert = certificatemanager.Certificate(
            self, 'no-ops_nl_cdn', domain_name='*.no-ops.nl',
            validation=cert_validation
        )
        return cdn_cert

    def provision_cdn_dns(self):
        ''' provision cdn dns record  '''
        cdn_record = route53.RecordSet(
            self, 'portal_no-ops_nl', record_name=CDN_DOMAIN,
            record_type=route53.RecordType.A,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.cdn)
            ),
            zone=self.public_zone
        )
        return cdn_record

    def refer_bucket(self):
        ''' reference existing bucket '''
        bucket = s3.Bucket.from_bucket_attributes(
            self, 'no-ops_portal', bucket_name=BUCKET_NAME,
            region='eu-central-1'
        )
        # initialize policy on imported s3.Bucket
        # cloudfront.Distribution requires this for origin access id grant
        bucket.policy = s3.BucketPolicy(
            self, 'no-ops_portal_policy', bucket=bucket
        )
        # add statement from s3.Bucket(enforce_ssl=True)
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=['s3:*'],
                conditions={'Bool': {'aws:SecureTransport': 'false'}},
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                resources=[bucket.bucket_arn, bucket.arn_for_objects('*')]
            )
        )
        return bucket

    def refer_dns_zone(self):
        ''' reference existing dns zone '''
        public_zone = route53.PublicHostedZone.from_lookup(
            self, 'no-ops', domain_name='no-ops.nl', private_zone=False
        )
        return public_zone
