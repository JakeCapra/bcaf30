from django.utils import timezone
from django.db import models
from django.db.models import Q


from . import utils
from .user import User
from .conversation import Conversation
from .message import Message


class ReadStatus(utils.CustomModel):
    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+"
    )   
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        db_column="conversationId",
        related_name="readStatuses",
        related_query_name="readStatus"
    )
    lastReadMessage = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        db_column="lastReadMessageId",
        null=True,
        blank=True,
        default=None,
    )
    readAt = models.DateTimeField(null=True, blank=True, default=None)
    
    @staticmethod
    def markAsRead(conversation, user):
        readStatus = ReadStatus.objects.filter(conversation=conversation, userId=user).first()
        latestMessage = Conversation.objects.filter(id=conversation).first().messages.filter(~Q(senderId=user.id)).all().last();
        readStatus.lastReadMessage = latestMessage
        readStatus.readAt = timezone.now()
        
        readStatus.save()