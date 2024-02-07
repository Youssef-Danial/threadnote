from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import Threadform, Noteform, Threadsetting
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Note, Thread, User, Access

def is_authorized(user_id, thread_id):
    user = get_object_or_404(User, id=user_id)
    thread = get_object_or_404(Thread, id=thread_id)
    access = Access.objects.filter(thread= thread, user=user).first()
    if user == thread.creator or access.access_type == "e":
        return True
    else:
        return False

# Create your views here.
@login_required
def homepage(request):
    threads = request.user.get_threads()
    paginator = Paginator(threads,9)
    if "page" in request.GET:
        pagenumber = int(request.GET["page"])
        page = paginator.get_page(pagenumber)
        content = {"user":request.user, "threadform":Threadform(), "page":page}
        return render(request,"home/threads.html",content)
    else:
        page = paginator.get_page(1)
    content = {"user":request.user, "threadform":Threadform(), "page":page}
    return render(request, "home/index.html",content)

@login_required
def show_thread(request, id):
    thread = get_object_or_404(Thread, id=id)
    content={"thread":thread, "user": request.user}
    return render(request, "home/thread.html", content)

@login_required
def get_threads(request):
    user = request.user
    threads = request.user.get_threads()
    paginator = Paginator(threads,9)
    if "page" in request.GET:
        pagenumber = int(request.GET["page"])
        page = paginator.get_page(pagenumber)
    else:
        page = paginator.get_page(1)
    content = {"user":user,"page":page}
    return render(request,"home/threads.html",content)

@login_required
def get_threadform(request):
    content = {"threadform":Threadform()}
    return render(request, "home/threadform.html", content)

@login_required
def create_thread(request):
    print("you are creating a thread")
    print(request.POST)
    user = request.user
    if request.method == "POST":
        form = Threadform(request.POST)
        if form.is_valid():
            # creating the form
            form.instance.creator = user
            form.save()
            return show_thread(request, form.instance.pk)
        return HttpResponse("404")
    return HttpResponse("404")


@login_required
def show_note(request,id):
    user = request.user
    note = get_object_or_404(Note, id=id)
    if request.method == "POST" and is_authorized(user.id, note.thread.id):
        print(request.POST)
        form = Noteform(request.POST,instance=note)
        #print(request.POST)
        if form.is_valid():
            form.save()
            print("Saved")
            return render(request, "home/toast.html", {"message":"Note Updated Successfully","alert":"success"})
        return HttpResponse("404")
    form = Noteform(instance = note)
    content = {"Noteform":form, "note":note, "user":user}
    return render(request, "home/note.html", content)
    #return HttpResponse("Not Authorized") 

@login_required
def create_note(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if is_authorized(request.user.id, thread.id):
        user = request.user
        note = Note()
        note.creator = user
        note.thread = thread
        note.save()
        request.method="None"
        return show_note(request,note.pk)
    return HttpResponse("404")
    

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    notethread = note.thread
    if request.method == "DELETE" and is_authorized(request.user.id, notethread.id):
        note.delete()
        return show_thread(request, notethread.pk)
    return HttpResponse("404")

@login_required
def thread_access(request, id):
    thread = get_object_or_404(Thread, id=id)
    content={"thread":thread}
    return render(request,'home/access.html',content)

@login_required
def thread_accestype(request, id):
    user = request.user
    thread = get_object_or_404(Thread, id=id)
    if thread.creator == user:
        # we do our access stuff here
        if request.method == "POST":
            content = request.POST
            if "username" in content.keys():
                username = content["username"]
                access_type = content["accesstype"]
                access_user = User.objects.filter(username=username).first()
                print(thread.creator.get_friends())
                print(access_user in thread.creator.get_friends())
                if access_user!=None and access_user!= thread.creator and (access_user not in thread.users.all()) and (access_user in thread.creator.get_friends()):
                    access = Access(thread=thread, user=access_user, access_type=access_type)
                    access.save()
                    #return render(request, "home/toast.html", {"message":"User Added Successfully","alert":"success"})
                    return render(request, "home/access_item.html",{"aces":access,"message":"User Added Successfully","alert":"success"})
                return render(request, "home/toast.html", {"message":"Wrong User Name or User is not your friend","alert":"error"})
            return HttpResponse("404")
        if request.method == "DELETE":
            access_id = request.GET.get("access_id")
            access_id = int(access_id)
            access = get_object_or_404(Access, id=access_id)
            if access.thread == thread:
               access.delete()
            return render(request, "home/toast.html", {"message":"User Deleted Successfully","alert":"success"})
        return HttpResponse("404")
    return HttpResponse("404")

@login_required
def show_thread_settings(request,id):
    thread = get_object_or_404(Thread, id=id)
    if request.method == "POST" and is_authorized(request.user.id, thread.id):
        # here we update the Settings
        settingsform = Threadsetting(request.POST,instance=thread)
        if settingsform.is_valid():
            settingsform.save()
            return render(request, "home/toast.html", {"message":"Settings Updated Successfully","alert":"success"})

    if request.method == "DELETE"and is_authorized(request.user.id, thread.id):
        thread.delete()
        return get_threads(request)
    settingsform = Threadsetting(instance = thread)
    content = {"thread":thread, "settingsform":settingsform}
    return render(request, "home/thread_settings.html", content)


