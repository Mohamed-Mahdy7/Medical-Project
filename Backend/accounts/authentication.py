from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        
        token = request.COOKIES.get("access_token")
        
        if token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token
        except (InvalidToken, TokenError):
            return None