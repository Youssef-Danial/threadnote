from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
#from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
# Create your models here.

class User(AbstractUser):
    friends = models.ManyToManyField("self", through="Friendship")
    # unique=True the name should be unique
    def __str__(self):
        return self.username
    
    def get_friends(self):
        friendshiplist=Friendship.objects.filter(Q(friend_a=self)|Q(friend_b=self))
        friendslist = []
        for friendship in friendshiplist:
            friendslist.append(friendship.friend_a)
            friendslist.append(friendship.friend_b)
        return set(friendslist)

    def get_threads(self):
        # Get threads created by the user or threads where the user has access
        return Thread.objects.filter(Q(creator=self) | Q(users=self) | Q(privacy="p")).distinct().order_by("-modify_date")
    
class Friendship(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    friend_a = models.ForeignKey(User, related_name='friendship_set_a', on_delete=models.CASCADE, db_index=True)
    friend_b = models.ForeignKey(User, related_name='friendship_set_b', on_delete=models.CASCADE, db_index=True)
    class Meta:
        unique_together = ['friend_a', 'friend_b']
class Tnbase(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    pin = models.BooleanField(db_default=False)
    is_active = models.BooleanField(db_default=True)
    class Meta:
        abstract = True

class Thread(Tnbase):
    creator = models.ForeignKey("User", related_name="threads", on_delete=models.CASCADE)
    title = models.CharField(max_length = 30,blank=False)
    description = models.TextField(max_length = 256, blank=True)
    users = models.ManyToManyField('User', through = "Access")
    privacy_options = {
        "p": "Public",
        "a": "Access only",
    }
    privacy = models.CharField(max_length=1,choices=privacy_options, db_default="a")

    def __str__(self):
        return self.title
    
    def get_notes(self):
        return self.notes.all().order_by("-modify_date")

class Access(models.Model):
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_type_options = {
        "v" : "Access View",
        "e" : "Access Edit"
    }
    access_type = models.CharField(max_length=1,choices=access_type_options, db_default="e")
    class Meta:
        unique_together = ['user', 'thread']

class Note(Tnbase):
    creator = models.ForeignKey("User", related_name="notes",on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", related_name="notes", on_delete=models.CASCADE)
    content = HTMLField(blank=True)
    #last_user = models.ForeignKey("User", on_delete=models.do_nothing)
    def __str__(self):
        return self.content[:20]

class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}: {self.message}"


