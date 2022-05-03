from django.contrib.auth.middleware import get_user
from django.http import HttpResponse
from messenger_backend.models import ReadStatus, Conversation
from rest_framework.views import APIView


class ReadStatuses(APIView):
    """Mark all messages in the conversation as read"""

    def put(self, request, conversationId):
        try:
            user = get_user(request)
            
            if user.is_anonymous:
                return HttpResponse(status=401)
            
            conversation = Conversation.objects.filter(id=conversationId).first()
            if conversation.user1_id != user.id and conversation.user2_id != user.id:
                return HttpResponse(status=403)
            
            ReadStatus.markAsRead(conversation=conversationId, user=user)
            
            return HttpResponse(status=204)
        except Exception as e:
            return HttpResponse(status=500)
