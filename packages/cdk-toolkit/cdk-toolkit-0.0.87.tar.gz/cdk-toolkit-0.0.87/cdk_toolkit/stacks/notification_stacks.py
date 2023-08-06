from aws_cdk import (
    Stack,
    aws_pinpoint as pinpoint,
    aws_lambda,
    aws_s3_assets as Asset
) 
from constructs import Construct 

from OpenSSL import crypto
import base64

# https://gist.github.com/ejdoh1/fde1a611e0ab4de2f32a6beba30a44f0



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
    def __init__(self, scope: Construct, construct_id: str, pinpoint_app_name: str, apns_certificate_path: str, apns_private_key_path: str, push_notification_lambda_code_dir: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pinpoint_app = pinpoint.CfnApp(self, pinpoint_app_name, name=pinpoint_app_name)  


        # APNS Sandbox Channel
        cfn_aPNSSandbox_channel = pinpoint.CfnAPNSSandboxChannel(self, "{}-apns-sandbox".format(pinpoint_app_name),
            application_id=pinpoint_app.ref, 
            certificate=open(apns_certificate_path).read(),
            default_authentication_method="CERTIFICATE", 
            enabled=False,
            private_key=open(apns_private_key_path).read(), 
        )

        # Push Notification - Send Message
        push_notifications_lambda = aws_lambda.Function(self,'push-notification-lambda',
            handler='lambda_function.lambda_handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            architecture=aws_lambda.Architecture.ARM_64,
            code=aws_lambda.Code.from_asset(push_notification_lambda_code_dir),
        )