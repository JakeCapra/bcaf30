from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save


from . import utils
from .user import User

class Conversation(utils.CustomModel):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="user1Id", related_name="+"
    )   
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="user2Id", related_name="+", 
    )
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # find conversation given two user Ids
    def find_conversation(user1Id, user2Id):
        # return conversation or None if it doesn't exist
        try:
            return Conversation.objects.get(
                (Q(user1__id=user1Id) | Q(user1__id=user2Id)),
                (Q(user2__id=user1Id) | Q(user2__id=user2Id)),
            )
        except Conversation.DoesNotExist:
            return None

from .readStatus import ReadStatus        

@receiver(post_save, sender=Conversation)
def addUnread(sender, instance, **kwargs):
    user1ReadStatus = ReadStatus(userId=instance.user1, conversation=instance)
    user1ReadStatus.save()
    user2ReadStatus = ReadStatus(userId=instance.user2, conversation=instance)
    user2ReadStatus.save()