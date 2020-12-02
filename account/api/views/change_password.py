from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from cheers.apps.account.api.serializers.change_password import SerializerAccountChangePassword
from cheers.apps.account.models import ModelAccountUser
from django.utils.translation import ugettext_lazy as _

class ViewAPIAccountChangePassword(UpdateAPIView):
        """
        An endpoint for changing password.
        """

        serializer_class = SerializerAccountChangePassword
        model = ModelAccountUser


        def get_object(self, queryset=None):

            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            """
            Update the password
            """

            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password":_("Wrong password.")}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": _("your password changed successfully please login again")},
                            status=HTTP_200_OK)
