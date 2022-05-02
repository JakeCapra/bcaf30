from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save

from . import utils
from .user import User
from .conversation import Conversation
from .message import Message


class ReadStatus(utils.CustomModel):
    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+",
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
        
    @receiver(post_save, sender=Conversation)
    def addUnread(sender, instance, **kwargs):
        user1ReadStatus = ReadStatus(userId=instance.user1, conversation=instance)
        user1ReadStatus.save()
        user2ReadStatus = ReadStatus(userId=instance.user2, conversation=instance)
        user2ReadStatus.save()