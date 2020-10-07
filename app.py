#!/usr/bin/env python3

from aws_cdk import core

from role_alias_custom_resource.role_alias_custom_resource_stack import RoleAliasCustomResourceStack


app = core.App()

# env_neo = core.Environment(account="450676674096", region="eu-west-1")
# env_everest = core.Environment(account="450676674096", region="eu-west-1")

# RoleAliasCustomResourceStack(app, "role-alias-custom-resource-stack", env=env_neo)
RoleAliasCustomResourceStack(app, "role-alias-custom-resource-stack")

app.synth()
