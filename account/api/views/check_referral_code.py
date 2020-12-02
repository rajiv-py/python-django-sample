from rest_framework.response import Response
from rest_framework.views import APIView

from cheers.apps.account.api.serializers.referral_code import SerializerAccountReferralCode


class ViewAPIAccountCheckReferralCode(APIView):

    serializer_class = SerializerAccountReferralCode

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={"request":self.request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)







