from rest_framework.response import Response
from rest_framework.views import APIView


class ViewAPIAccountUserDrinkStatus(APIView):
    """
    This api check the user drink status and subscription  status.
    """

    def get(self, *args, **kwargs):

        data = {}

        try:
            data['plan_id'] = self.request.user.subscription.plan.id
        except AttributeError:
            data['plan_id'] = None

        if self.request.user.is_today_order_allowed:
            data["today_order"] = True
        else:
            data["today_order"] = False

        return Response(data)
