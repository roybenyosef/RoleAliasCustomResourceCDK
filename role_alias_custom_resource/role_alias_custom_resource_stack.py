from aws_cdk import (
    core,
    aws_iam as iam,
)

from role_alias_resource import RoleAliasResource

class RoleAliasCustomResourceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role1 = iam.Role(scope=self, id="MyRole1",
            assumed_by=iam.ServicePrincipal("credentials.iot.amazonaws.com")
        )

        role2 = iam.Role(scope=self, id="MyRole2",
            assumed_by=iam.ServicePrincipal("credentials.iot.amazonaws.com")
        )
 
        role_alias1 = RoleAliasResource(scope=self, 
                                       id_='RoleAlias1', 
                                       role_alias="my-role-alias1", 
                                       role_arn=role1.role_arn,
                                       credential_duration_seconds="3600")

        role_alias2 = RoleAliasResource(scope=self, 
                                       id_='RoleAlias2', 
                                       role_alias="my-role-alias2", 
                                       role_arn=role2.role_arn,
                                       credential_duration_seconds="3600")
