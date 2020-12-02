from django.core.exceptions import ObjectDoesNotExist
from oauth2_provider.admin import AccessToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
import facebook
from rest_framework_social_oauth2.views import ConvertTokenView

from cheers.apps.account.api.serializers.facebook_login import SerializerFacebookLogin
from cheers.apps.account.api.serializers.user import SerializerAccountUser
from cheers.apps.account.models import ModelAccountUser
from dateutil.parser import parse


class ViewAPIFacebookLogin(ConvertTokenView):
    """
    This class is used for login the user through facebook.
    """

    # serializer_class = SerializerFacebookLogin
    # authentication_classes = ()
    # permission_classes = ()

    def post(self, request, *args, **kwargs):
        response = super(ViewAPIFacebookLogin, self).post(request, *args, **kwargs)
        data  = response.data
        if response.status_code == 400:
            return Response({"error": data['error']})
        token_obj = AccessToken.objects.get(token=data['access_token'])
        user = SerializerAccountUser(token_obj.user).data
        data.update(user)

        try:
            data['plan_id'] = token_obj.user.subscription.plan.id
        except AttributeError:
            data['plan_id'] = None

        return Response(data)


# class ViewAPIFacebookLogins(APIView):
#     """
#     This class is used for login the user through facebook.
#     """
#
#     serializer_class = SerializerFacebookLogin
#     authentication_classes = ()
#     permission_classes = ()
#
#     def post(self, request):
#         """
#         This method post the user credentials and looged in.
#         """
#
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         access_token = serializer.data['access_token']
#
#         try:
#             graph = facebook.GraphAPI(access_token=access_token)
#             user_info = graph.get_object(
#                 id='me',
#                 fields='first_name, middle_name, last_name, id, '
#                        'currency, hometown, location, locale, '
#                        'email, gender, interested_in, picture.type(large),'
#                        ' birthday, cover')
#         except facebook.GraphAPIError:
#             return Response({'error': 'Invalid data'}, status=HTTP_400_BAD_REQUEST)
#
#         try:
#             #check and get existing facebook user # 1
#             ModelAccountUser.objects.get(email=user_info.get('email'), facebook_id=user_info.get('id'))
#         except ObjectDoesNotExist:
#             try:
#                 existing_user = ModelAccountUser.objects.get(email=user_info.get('email')) # check for existing email in DB, use .exists() # 2
#                 if existing_user:
#                     return Response({'email': "Looks like you have already registered using your email."
#                                               "You can try another facebook account, or use your email, password to login."},
#                                     status=HTTP_400_BAD_REQUEST)
#             except:
#                 pass
#
#         # # no existing fb account in our DB found and no email found, means it's fresh login.
#         # update data # 3
#         # do normal login # 4
#         # return success # last step
#
#         try:
#             user = ModelAccountUser.objects.get(facebook_id=user_info.get('id'))
#         except ModelAccountUser.DoesNotExist:
#             password = ModelAccountUser.objects.make_random_password()
#
#             first_name = user_info.get('first_name')
#             last_name = user_info.get('last_name')
#             birthday = user_info.get("birthday")
#             if birthday:
#                 birthday = parse(birthday)
#                 birthday_format = birthday.strftime('%Y-%m-%d')
#             else:
#                 birthday_format = None
#             user = ModelAccountUser(
#                 first_name = first_name,
#                 surname = last_name,
#                 email=user_info.get('email'),
#                 facebook_id=user_info.get('id'),
#                 avatar=user_info.get('picture')['data']['url'],
#                 date_of_birth=birthday_format,
#                 is_active=True)
#             user.set_password(password)
#             user.save()
#
#         data = SerializerAccountUser(user).data
#
#         token, created = Token.objects.get_or_create(user=user)
#         data['token'] = token.key
#
#         try:
#             data['plan_id'] = user.subscription.plan.id
#         except AttributeError:
#             data['plan_id'] = None
#
#         # Always send absolute url for avatar
#         if user.avatar:
#             data['avatar'] = user_info.get('picture')['data']['url']
#
#
#         if token:
#             return Response(data, status=HTTP_200_OK)
#         else:
#
#             return Response({'error': 'Invalid Token'}, status=HTTP_400_BAD_REQUEST)
