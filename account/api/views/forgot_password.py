from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from cheers.apps.account.api.serializers.forgot_password import SerializerAccounForgotPassword
from cheers.apps.account.models import ModelAccountUser, ModelAccountVerification
from django.utils.translation import ugettext_lazy as _


class ViewAPIAccountForgotPassword(APIView):
    """
    This class is used for handle the forgot password functionality
    """

    serializer_class = SerializerAccounForgotPassword
    authentication_classes = ()
    permission_classes = ()


    def post(self, request):
        """
        This method used to post the url for forgot password functionality.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = ModelAccountUser.objects.get(email=serializer.data.get("email"))
        except ModelAccountUser.DoesNotExist:
            return Response({"email":_("This email does not exist in our database")}, status=status.HTTP_400_BAD_REQUEST)

        ModelAccountVerification.objects.send_verification_email(user,
                                                                 verification_type=ModelAccountVerification.VERIFICATION_TYPES[1][0])

        message =_("Email sent successfully to the {0}").format(user.email)
        return Response({"message": message}, status=HTTP_200_OK)