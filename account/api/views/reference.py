from rest_framework.generics import ListAPIView

from cheers.apps.account.api.serializers.reference import SerializerAccountReference
from cheers.apps.account.models import ModelAccountReference


class ViewAPIAccountReference(ListAPIView):
    """
    This class handle the user references.
    """

    model = ModelAccountReference
    serializer_class = SerializerAccountReference
    queryset = model.objects.all()
    pagination_class = None


    def get_queryset(self):
        return self.queryset.filter(referrer_from=self.request.user)



