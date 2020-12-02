from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import authentication
from django.contrib.auth import authenticate
from cheers.apps.account.api.serializers.login import SerializerAccountLogin
from cheers.apps.account.api.serializers.user import SerializerAccountUser
from django.utils.translation import ugettext_lazy as _

from cheers.apps.base.utility.oauth_token import generate_oauth2_access_token


class ViewAPIAccountLogin(APIView):
    """
    This class is used for login the user.
    """

    serializer_class = SerializerAccountLogin
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        This method post the user credentials and looged in.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['email']
        password = serializer.data["password"]
        device_token = serializer.data["device_token"]

        user = authenticate(username=username, password=password)

        if user:
            if device_token:
                user.device_token = device_token
                user.save()

            data = SerializerAccountUser(user).data

            # Always send absolute url for avatar
            if user.avatar:
                data['avatar'] = self.request.build_absolute_uri(user.avatar.url)

            try:
                data['plan_id'] = user.subscription.plan.id
                data['cancellation'] = user.subscription.cancellation
            except AttributeError:
                data['plan_id'] = None
                data['cancellation'] = False

            token_data = generate_oauth2_access_token(request, user)
            token_data.update(data)

            return Response(token_data, status=HTTP_200_OK)

        return Response({'error': _('Bad email or password. Please enter the correct information')}, status=HTTP_400_BAD_REQUEST)