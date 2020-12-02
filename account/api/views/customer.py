from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cheers.apps.account.api.serializers.user import SerializerAccountUser, SerializerAccountUserUpdate
from cheers.apps.account.models import ModelAccountUser


# -------------------------------------------------------------------------------
# ViewAPIAccountManageUser
# -------------------------------------------------------------------------------
from cheers.apps.base.utility.oauth_token import generate_oauth2_access_token


class ViewAPIAccountManageUser(ModelViewSet):
    """
    API endpoint that allows Actors to be viewed by authenticated users.

    Instance Update works with POST and PATCH both requests.
    """

    model = ModelAccountUser
    serializer_class = SerializerAccountUser
    update_serializer_class = SerializerAccountUserUpdate
    authentication_classes = ()
    permission_classes = ()

    queryset = model.objects.all()
    http_method_names = ['put', 'post', 'get', 'patch']

    def dispatch(self, request, *args, **kwargs):
        """
        overriding dispatch to have all endpoints authenticated except 'POST'
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.method.lower() != 'post':
            self.authentication_classes = (OAuth2Authentication,)
            self.permission_classes = (IsAuthenticated,)

        return super(ViewAPIAccountManageUser, self).dispatch(
            request, *args, **kwargs)

    def get_serializer_class(self):
        """
        Return different serializer for different kind of http requests.
        :return: serializer class
        """
        if self.request.method.lower() in ["put", "patch"]:
            return self.update_serializer_class

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:

        :param kwargs:
        :return: Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Prepare data
        data = serializer.data
        user = ModelAccountUser.objects.get(email=data['email'])
        data['plan_id'] = None
        data['cancellation'] = False

        token_data = generate_oauth2_access_token(request, user)
        token_data.update(data)

        return Response(token_data, status=status.HTTP_201_CREATED, headers=headers)
