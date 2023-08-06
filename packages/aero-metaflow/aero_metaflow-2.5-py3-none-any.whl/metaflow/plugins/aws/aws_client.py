# File modified under the Apache Licence 2.0 spec. Modified by Aero Technologies.
# Altered how profile is set based on local/remote execution
from .auth import AWSRequestsAuth
import os
import time
import random

from metaflow.metaflow_config import AERO_REFRESH_TOKEN, AERO_IDENTITY_POOL, AERO_PROVIDER, USER_POOL_CLIENT_ID

class CredentialsExpiredException(Exception):
    
    def __init__(self) -> None:
        super().__init__("Credentials have expired, please run 'aero account login' again")

def get_aws_credentials():
    import boto3

    # Retry, as we may get errors with RateLimit from Cognito
    for _ in range(0, 2):

        try:

            client = boto3.client('cognito-identity', region_name='eu-west-1')
            idp_client = boto3.client('cognito-idp', region_name='eu-west-1')

            try:                
                tokens = idp_client.initiate_auth(
                    ClientId=USER_POOL_CLIENT_ID,
                    AuthFlow='REFRESH_TOKEN_AUTH',
                    AuthParameters={
                        "REFRESH_TOKEN": AERO_REFRESH_TOKEN
                    }
                )
                aero_id_token = tokens['AuthenticationResult']['IdToken']

                identity_response = client.get_id(
                    IdentityPoolId=AERO_IDENTITY_POOL,
                    Logins={AERO_PROVIDER: aero_id_token})
            except:
                raise CredentialsExpiredException()

            identity_id = identity_response['IdentityId']

            resp = client.get_credentials_for_identity(
                IdentityId=identity_id,
                Logins={AERO_PROVIDER: aero_id_token})

            secret_key = resp['Credentials']['SecretKey']
            access_key = resp['Credentials']['AccessKeyId']
            session_token = resp['Credentials']['SessionToken']
            expiry = resp['Credentials']['Expiration']

            return {
                "access_key": access_key,
                "secret_key": secret_key,
                "token": session_token,
                "expiry_time": expiry.isoformat()
            }
        except CredentialsExpiredException:
            raise CredentialsExpiredException()
        except Exception:
            time.sleep(random.randint(1, 4))

    raise CredentialsExpiredException()

def create_client_credentials():
    import boto3
    from botocore.credentials import RefreshableCredentials
    from botocore.session import get_session

    # Catch if running on Batch
    if 'METAFLOW_INPUT_PATHS_0' in os.environ or 'MANAGED_BY_AWS' in os.environ:
        return boto3.session.Session(
            region_name='eu-west-1'
        )

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=get_aws_credentials(),
        refresh_using=get_aws_credentials,
        method='sts-assume-role'
    )

    session = get_session()
    session._credentials = session_credentials
    autorefresh_session = boto3.Session(
        botocore_session=session,
        region_name='eu-west-1'
    )

    try:
        sts = autorefresh_session.client('sts')
        sts.get_caller_identity()
    except:
        raise CredentialsExpiredException()

    return autorefresh_session


AWS_SESSION = create_client_credentials()


def get_aws_client(module, with_error=False, params={}):
    from metaflow.exception import MetaflowException

    try:
        import boto3
        from botocore.exceptions import ClientError
    except (NameError, ImportError):
        raise MetaflowException(
            "Could not import module 'boto3'. Install boto3 first.")

    if with_error:
        return AWS_SESSION.client(module, **params), ClientError
    return AWS_SESSION.client(module, **params)


class Boto3ClientProvider(object):
    name = "boto3"

    @staticmethod
    def get_client(module, with_error=False, params={}):
        from metaflow.exception import MetaflowException

        try:
            import boto3
            from botocore.exceptions import ClientError
        except (NameError, ImportError):
            raise MetaflowException(
                "Could not import module 'boto3'. Install boto3 first.")

        if with_error:
            return AWS_SESSION.client(module, **params), ClientError
        return AWS_SESSION.client(module, **params)

class AeroAWSRequestsAuth(AWSRequestsAuth):

    def __init__(self, aws_host, aws_region, aws_service, session):

        super(AeroAWSRequestsAuth, self).__init__(None, None, aws_host, aws_region, aws_service)
        self._refreshable_credentials = session.get_credentials()

    def get_aws_request_headers_handler(self, r):
        # provide credentials explicitly during each __call__, to take advantage
        # of botocore's underlying logic to refresh expired credentials
        frozen_credentials = self._refreshable_credentials.get_frozen_credentials()
        credentials = {
            'aws_access_key': frozen_credentials.access_key,
            'aws_secret_access_key': frozen_credentials.secret_key,
            'aws_token': frozen_credentials.token,
        }

        return self.get_aws_request_headers(r, **credentials)

def get_auth_object(
    url: str,
    region: str = 'eu-west-1',
    service: str = 'execute-api'
):
    split_url = url.split("/")
    endpoint = split_url[2] # Just the domain
    return AeroAWSRequestsAuth(
        endpoint, region, service, AWS_SESSION
    )