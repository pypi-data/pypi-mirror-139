import re
from typing import Any, Dict, List

from aws_cdk.core import Stack
import boto3


def get_cluster_oidc_provider_arn(cluster_name: str, account_id: str) -> str:
    return "".join([
        "arn:aws:iam::",
        account_id,
        ":oidc-provider/",
        get_cluster_oidc_provider_url(cluster_name)
    ])

def get_cluster_oidc_provider_url(cluster_name: str) -> str:
    eks = boto3.client("eks")
    return re.sub(
        "https://", "",
        eks.describe_cluster(name=cluster_name)["cluster"]["identity"]["oidc"]["issuer"]
    )

def get_cluster_vpc_id(cluster_name: str) -> str:
    eks = boto3.client("eks")
    return eks.describe_cluster(name=cluster_name)["cluster"]["resourcesVpcConfig"]["vpcId"]

def get_kwargs_from_context(args: List[str], stack: Stack) -> Dict[str, Any]:
    return {arg: stack.node.try_get_context(arg) for arg in args}
