from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from cheers.apps.account.models import ModelAccountReference
from cheers.apps.bar.models import ModelBarProduct


class SerializerAccountReference(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # ---------------------------------------------------------------------------
    # Meta
    # ---------------------------------------------------------------------------
    class Meta:
        model = ModelAccountReference
        fields = ('id', 'name', "image")


    def get_image(self, obj):
        request = self.context.get("request")

        if obj.referrer_to.preview_image and not obj.referrer_to.facebook_id:
            return request.build_absolute_uri(obj.referrer_to.preview_image)
        return obj.referrer_to.preview_image

    def get_name(self, obj):
        return obj.referrer_to.get_name
