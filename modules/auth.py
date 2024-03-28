"""Module for all relate auth"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
import jwt
from modules.aws_handler import get_secret_from_str

# Extract from: https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/


class UnauthorizedException(HTTPException):
    """Class for unauthorized exceeption"""

    def __init__(self, detail: str, **_):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    """Class for unauthenticated exceeption"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self):
        self.secrets = get_secret_from_str(
            secret_name="quote-values-auth0"
        )
        self.domain = self.secrets["AUTH0_DOMAIN"]
        self.audience = self.secrets["AUTH0_API_AUDIENCE"]
        self.alg = self.secrets["AUTH0_ALGORITHMS"]
        self.issuer = self.secrets["AUTH0_ISSUER"]

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(self,
                     _: SecurityScopes,
                     token: Optional[HTTPAuthorizationCredentials] = Depends(
                         HTTPBearer())
                     ):
        """Verify the scope"""
        if token is None:
            raise UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error)) from error
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error)) from error

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.alg,
                audience=self.audience,
                issuer=self.issuer,
            )
        except Exception as error:
            raise UnauthorizedException(str(error)) from error

        return payload
