from django.contrib.auth.middleware import get_user
from django.http import HttpResponse
from messenger_backend.models import ReadStatus
from rest_framework.views import APIView


class ReadStatuses(APIView):
    """Mark all messages in the conversation as read"""

    def post(self, request, conversationId):
        try:
            user = get_user(request)
            
            if user.is_anonymous:
                return HttpResponse(status=401)
            
            ReadStatus.markAsRead(conversation=conversationId, user=user)
            
            return HttpResponse(status=200)
        except Exception as e:
            print(str(e))
            return HttpResponse(status=500)