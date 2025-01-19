from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.middleware.csrf import get_token
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
from src.backend.accounts.serializers.auth import (
    LoginSerializer,
    UserAuthSerializer,
    AuthResponseSerializer
)
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from src.backend.organization.serializers.membership_serializer import MembershipSerializer

@extend_schema(tags=['Authentication'])
@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token for session authentication."""
    return Response({'csrfToken': get_token(request)})

@extend_schema(tags=['Authentication'])
@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: AuthResponseSerializer}
    )
    def post(self, request):
        print("Login attempt with data:", request.data)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        if user.is_authenticated:
            print("User logged in:", user.username)
            return Response({
                'user': UserAuthSerializer(user).data
            })
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(tags=['Authentication'])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={204: None}
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Authentication'])
class SessionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: AuthResponseSerializer}
    )
    def get(self, request):
        return Response({
            'user': UserAuthSerializer(request.user).data,
            'membership': MembershipSerializer(self.request.session.get('membership', None)).data
        })
    
    @extend_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        print(request.data)
        membership = request.data

        if not membership:
            return Response(
                {"membership": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.session['membership'] = membership

        return Response(
            {"message": "Session updated", "membership": membership},
            status=status.HTTP_200_OK
        )