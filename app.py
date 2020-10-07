#!/usr/bin/env python3

from aws_cdk import core

from role_alias_custom_resource.role_alias_custom_resource_stack import RoleAliasCustomResourceStack


app = core.App()
RoleAliasCustomResourceStack(app, "role-alias-custom-resource")

app.synth()
