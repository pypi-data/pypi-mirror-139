from typing import List, Optional

from aws_cdk.aws_iam import (
    Effect, FederatedPrincipal, Policy, PolicyDocument, PolicyStatement, Role, ServicePrincipal
)
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Construct, Stack

from deltarescdk.utils import get_cluster_oidc_provider_arn, get_cluster_oidc_provider_url

class KubeBucket(Construct):
    """
    Creates:
        s3.Bucket
        iam.Role
        iam.Policy
    for use with a EKS OIDC setup, using a serviceaccount in a certain namespace.
    args:
        scope: construct scope,
        id: unique construct id, used for subresources in this construct
        bucket_name: name of the created bucket
        cluster_name: name of the eks cluster
        namespace: kubernetes namespace, defaults to "default"
        s3_actions: s3 actions allowed for the serviceaccount, defaults to [s3:*]
        sa_name: name of the serviceaccount in kubernetes, defaults to {bucket_name}-access
    """
    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket_name: str,
        cluster_name: str,
        bucket_prefix: Optional[str] = None,
        namespace: str = "default",
        s3_actions: Optional[List] = None,
        sa_name: Optional[str] = None
    ) -> None:
        super().__init__(scope, id)

        if not s3_actions:
            s3_actions = ["s3:*"]
        
        if not sa_name:
            sa_name = f"{bucket_name}-access"

        account_id: str = Stack.of(self).account

        oidc_provider_arn = get_cluster_oidc_provider_arn(cluster_name, account_id)
        oidc_provider_url = get_cluster_oidc_provider_url(cluster_name)

        self._bucket: Bucket = Bucket(
            self,
            "Bucket",
            bucket_name=bucket_name
        )

        s3_pol_statement_bucket_loc = PolicyStatement(
            actions=["s3:GetBucketLocation"],
            effect=Effect.ALLOW,
            resources=["arn:aws:s3:::*"],
        )
        s3_pol_statement_bucket_list = PolicyStatement(
            actions=["s3:ListBucket"],
            effect=Effect.ALLOW,
            resources=[f"arn:aws:s3:::{bucket_name}"]
        )
        if bucket_prefix:
            bucket_resources: List[str] = [f"{self._bucket.bucket_arn}/{bucket_prefix}/*"]
        else:
            bucket_resources: List[str] = [f"{self._bucket.bucket_arn}/*"]
        s3_pol_statement_bucket_access = PolicyStatement(
            actions=s3_actions,
            effect=Effect.ALLOW,
            resources=bucket_resources,
        )

        role_pol_statement_assume_role = PolicyStatement(
            actions=["sts:AssumeRoleWithWebIdentity"],
            effect=Effect.ALLOW,
            principals=[FederatedPrincipal(oidc_provider_arn, conditions={})],
            conditions={
                "StringLike": {
                    oidc_provider_url + ":sub":
                        f"system:serviceaccount:{namespace}:{sa_name}"
                },
                "StringEquals": {
                    oidc_provider_url + ":aud": "sts.amazonaws.com"
                }
            }
        )
        policy_document = PolicyDocument(
            statements=[
                s3_pol_statement_bucket_access,
                s3_pol_statement_bucket_list,
                s3_pol_statement_bucket_loc
            ]
        )

        self._policy = Policy(
            self,
            "Policy",
            document=policy_document,
            policy_name=f"{id}-policy"
        )

        self._role = Role(
            self,
            "Role",
            assumed_by=ServicePrincipal(service="ec2.amazonaws.com"),
            role_name=f"{id}-role",
            description=f"role used by EKS OIDC serviceaccounts access the {bucket_name} bucket"
        )

        self._policy.attach_to_role(self._role)
        # Set assume role policy
        self._role.assume_role_policy.add_statements(role_pol_statement_assume_role)
    
    @property
    def bucket(self):
        return self._bucket

    @property
    def policy(self):
        return self._policy

    @property
    def role(self):
        return self._role
