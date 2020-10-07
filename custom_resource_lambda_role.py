from typing import List
from aws_cdk import (
    core,
    aws_iam as iam,
)
from aws_cdk.aws_iam import PolicyStatement

"""When doing Custom Resources in CDK, according to the docs:
This role will apply to all AwsCustomResource instances in the stack. 
Therefore, this class is implemented as a singleton, so that all custom resource lambda needs can be fulfilled by it.
(https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_custom-resources.AwsCustomResource.html#role)
"""

class CustomResourcesLambdaRole:
    class __CustomResourcesLambdaRole:
        def __init__(self, scope):
            self.role = iam.Role(
                scope=scope,
                id=f'LambdaRole',
                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
                managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")],
            )

        def __str__(self):
            return repr(self) + self.val
    
    instance = None

    def __init__(self, scope):
        if not CustomResourcesLambdaRole.instance:
            CustomResourcesLambdaRole.instance = CustomResourcesLambdaRole.__CustomResourcesLambdaRole(scope)
        else:
            CustomResourcesLambdaRole.instance.scope = scope
    def __getattr__(self, name):
        return getattr(self.instance, name)


    def add_to_policy(self, actions: List[str], resources=List[str]):
        self.role.add_to_policy(PolicyStatement(actions=actions, resources=resources))

    def lambda_role(self) -> iam.Role:
        return self.role
