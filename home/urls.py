from django.urls import path,include
from . import views
app_name = "home"
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("thread/<int:id>", views.show_thread, name="show_thread"),
    path("get_threads", views.get_threads, name="get_threads"),
    path("create_thread", views.create_thread, name="create_thread"),
    path("get_threadform", views.get_threadform, name="get_threadform"),
    path("create_note/<int:thread_id>",views.create_note, name="create_note"),
    path("show_note/<int:id>", views.show_note,name="show_note"),
    path("delete_note/<int:note_id>", views.delete_note, name="delete_note"),
    path("show_thread_settings/<int:id>",views.show_thread_settings, name="show_thread_settings"),
    path("access/<int:id>", views.thread_access,name="access"),
    path("threadaccess/<int:id>",views.thread_accestype, name="threadaccess")
]
