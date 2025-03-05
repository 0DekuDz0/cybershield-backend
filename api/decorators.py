from functools import wraps
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime

def is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('CyberShieldToken')
        if not access_token:
            return Response({'error': 'You are not authorized to access this page'}, status=403)
        access_token_obj = AccessToken(access_token)
        now = datetime.now().timestamp()
        if access_token_obj['exp']< now:
             return Response({'error': 'You are not authorized to access this page'}, status=403)
        

        return view_func(request, *args, **kwargs)

    
    return _wrapped_view
