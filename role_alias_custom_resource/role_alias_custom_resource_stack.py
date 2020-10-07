from aws_cdk import (
    core,
    aws_iam as iam,
)

from role_alias_resource import RoleAliasResource

class RoleAliasCustomResourceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role = iam.Role(scope=self, id="MyRole",
            assumed_by=iam.ServicePrincipal("credentials.iot.amazonaws.com")
        )

        role_alias = RoleAliasResource(scope=self, 
                                       id_=f'{id}-RoleAlias', 
                                       role_alias="my-role-alias", 
                                       role_arn=role.role_arn, 
                                       credential_duration_seconds="3600")
