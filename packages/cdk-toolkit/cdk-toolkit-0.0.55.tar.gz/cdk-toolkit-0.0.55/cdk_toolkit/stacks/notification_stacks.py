from aws_cdk import (
    Stack,
    aws_pinpoint as pinpoint
) 
from constructs import Construct 


class NotificationStack(Stack): 
    '''
    This Stack ...
    '''
    def __init__(self, scope: Construct, construct_id: str, pinpoint_app_name: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pinpoint_app = pinpoint.CfnApp(self, pinpoint_app_name, name=pinpoint_app_name)

        cfn_aPNSSandbox_channel = pinpoint.CfnAPNSSandboxChannel(self, "{}-apns-sandbox".format(pinpoint_app_name),
            application_id=pinpoint_app.logical_id,

            # the properties below are optional
            bundle_id="bundleId",
            # certificate="certificate",
            default_authentication_method="certificate",
            enabled=False,
            # private_key="privateKey",
            # team_id="teamId",
            # token_key="tokenKey",
            # token_key_id="tokenKeyId"
        )