from custom_resource_lambda_role import CustomResourcesLambdaRole
from typing import Any, Dict

from aws_cdk import (
    core,
    aws_iam as iam,
)
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.core import Stack
from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    AwsSdkCall,
    PhysicalResourceId,
)


class RoleAliasResource(core.Construct):
    """AWS IoT Role Alias construct that uses AWSCustomResource internally
    Arguments:
        :param role_alias - The role alias name that will point to a role ARN. This allows you to change the role without having to update the device
        :param role_arn - The role arn that this alias will point to
        :param credential_duration_seconds: How long (in seconds) the credentials will be valid
        :param log_retention: The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. 
                              Default: logs.RetentionDays.INFINITE
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)
    """
    def __init__(self, 
                 scope: core.Construct, 
                 id_: str, 
                 role_alias: str, 
                 role_arn: str, 
                 credential_duration_seconds: int, 
                 log_retention=None, 
                 timeout=None,) -> None:
        super().__init__(scope, id_)


        on_create = self.get_on_create(role_alias=role_alias, role_arn=role_arn, credential_duration_seconds=credential_duration_seconds)
        on_update = self.get_on_update(role_alias=role_alias, role_arn=role_arn, credential_duration_seconds=credential_duration_seconds)
        on_delete = self.get_on_delete(role_alias=role_alias)

        account_id = Stack.of(self).account
        region=Stack.of(self).region

        policy = AwsCustomResourcePolicy.from_sdk_calls(resources=[f'arn:aws:iot:{region}:{account_id}:rolealias/{role_alias}'])
        lambda_role_singleton = CustomResourcesLambdaRole(scope)
        lambda_role_singleton.add_to_policy(actions=["iam:PassRole"], resources=[role_arn])

        # lambda_role = self.get_provisioning_lambda_role(role_arn)

        AwsCustomResource(scope=self, id=f'CustomResource', policy=policy, log_retention=log_retention,
                          on_create=on_create, on_update=on_update, on_delete=on_delete, resource_type='Custom::AWS-IoT-Role-Alias',
                          role=lambda_role_singleton.role, timeout=timeout)

    def get_provisioning_lambda_role(self, role_arn: str):
        role = iam.Role(
            scope=self,
            id=f'LambdaRole',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")],
        )
        # role.add_to_policy(PolicyStatement(actions=["iam:PassRole"], resources=['*']))

        print(f'adding iam:PassRole to "role_arn"')
        role.add_to_policy(PolicyStatement(actions=["iam:PassRole"], resources=[role_arn]))
        return role

    def get_on_create(self, role_alias: str, role_arn: str, credential_duration_seconds: int):
        create_params = {
            "roleAlias": role_alias,
            "roleArn": role_arn,
            "credentialDurationSeconds": credential_duration_seconds,
        }
        return self.get_sdk_operation(resource_id=role_alias, create_params=create_params, action_name='createRoleAlias')

    def get_on_update(self, role_alias: str, role_arn: str, credential_duration_seconds: int):
        create_params = {
            "roleAlias": role_alias,
            "roleArn": role_arn,
            "credentialDurationSeconds": credential_duration_seconds,
        }
        return self.get_sdk_operation(resource_id=role_alias, create_params=create_params, action_name='updateRoleAlias')

    def get_on_delete(self, role_alias: str,):
        create_params = {
            "roleAlias": role_alias
        }
        return self.get_sdk_operation(resource_id=role_alias, create_params=create_params, action_name='deleteRoleAlias')


    def get_sdk_operation(self, resource_id: str, create_params: Dict[str, Any], action_name: str):
        #api_version=None uses the latest api
        action = AwsSdkCall(
            action=action_name,
            service='Iot',
            parameters=create_params,
            # Must keep the same physical resource id, otherwise resource is deleted by CF
            physical_resource_id=PhysicalResourceId.of(id=resource_id),
        )
        return action
