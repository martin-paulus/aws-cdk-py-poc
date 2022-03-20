''' module for managing the no-ops.nl platform  '''
from aws_cdk import (
    aws_certificatemanager as certificatemanager,
    aws_route53 as route53,
    aws_s3 as s3,
    Stack
)
from constructs import Construct

PORTAL_DOMAIN = 'portal.no-ops.nl'


class NoOpsStack(Stack):
    ''' resource definitions for the main stack '''

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.public_zone = self.provision_dns_zone()
        self.bucket = self.provision_bucket()
        self.alb_cert = self.provision_alb_cert()

    def provision_alb_cert(self):
        ''' provision alb certificate '''
        cert_validation = certificatemanager.CertificateValidation.from_dns(
            self.public_zone
        )
        alb_cert = certificatemanager.Certificate(
            self, 'no-ops_nl', domain_name='*.no-ops.nl',
            validation=cert_validation
        )
        return alb_cert

    def provision_bucket(self):
        ''' provision static web resources  '''
        bucket = s3.Bucket(
            self, 'no-ops_portal',
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            bucket_name='no-ops-portal',
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            public_read_access=False
        )
        return bucket

    def provision_dns_zone(self):
        ''' provision dns public zone '''
        public_zone = self.public_zone = route53.PublicHostedZone(
            self, 'no-ops', caa_amazon=True, zone_name='no-ops.nl'
        )
        return public_zone
