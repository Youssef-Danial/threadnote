from django.contrib import admin
from .models import User, Friendship, Thread, Note, Notification, Access
# Register your models here.
admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Thread)
admin.site.register(Note)
admin.site.register(Notification)
admin.site.register(Access)