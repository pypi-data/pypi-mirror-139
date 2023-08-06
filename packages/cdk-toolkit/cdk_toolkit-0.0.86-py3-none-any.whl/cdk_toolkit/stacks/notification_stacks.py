from aws_cdk import (
    Stack,
    aws_pinpoint as pinpoint,
    aws_s3_assets as Asset
) 
from constructs import Construct 

from OpenSSL import crypto
import base64





def get_apns_certificate(cert_path, cert_pw):
    p12 = crypto.load_pkcs12(open(cert_path, 'rb').read(), cert_pw)
    pem = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())   
    return pem

def get_apns_private_key(cert_path, cert_pw):
    p12 = crypto.load_pkcs12(open(cert_path, 'rb').read(), cert_pw)
    pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())   
    return pem


class NotificationStack(Stack): 
    '''
    This Stack ...
    '''
    def __init__(self, scope: Construct, construct_id: str, pinpoint_app_name: str, apns_certificate_path: str, apns_private_key_path: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pinpoint_app = pinpoint.CfnApp(self, pinpoint_app_name, name=pinpoint_app_name)  


        cfn_aPNSSandbox_channel = pinpoint.CfnAPNSSandboxChannel(self, "{}-apns-sandbox".format(pinpoint_app_name),
            application_id=pinpoint_app.ref,

            # the properties below are optional
            # bundle_id=apns_bundle_id,
            certificate=open(apns_certificate_path).read(),
            default_authentication_method="CERTIFICATE", 
            enabled=False,
            private_key=open(apns_private_key_path).read(),
            # team_id="teamId",
            # token_key="tokenKey",
            # token_key_id="tokenKeyId"
        )