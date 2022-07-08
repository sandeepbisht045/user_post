from django.shortcuts import redirect, render
from django.http import JsonResponse
from . models import User, Post, Upvotes
from django.forms.models import model_to_dict
from pytz import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

# VIEWS TO REGISTER USER


def register(request):
    if not request.session.get("id"):
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                User.objects.get(email=email)
                return render(request, "register.html", {"email_alert": "exists", "username": username, "email": email})
            except:
                id = User.objects.create(
                    username=username, email=email, password=make_password(password))
            request.session["id"] = id.pk
            request.session["user"] = id.username

            return redirect("/posts")

        return render(request, "register.html")
    return redirect("/login")


# VIEWS TO LOGIN USER
def login(request):

    if not request.session.get("id"):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user_data = User.objects.get(email=email)
                is_valid = check_password(password, user_data.password)
                if is_valid:
                    request.session["id"] = user_data.id
                    request.session["user"] = user_data.username
                    return redirect("/posts")
                return render(request, "login.html", {"alert": "invalid", "email": email})

            except:
                return render(request, "login.html", {"alert": "invalid", "email": email})

        return render(request, "login.html")
    return redirect("/posts")

#  VIEWS TO LOGOUT USER


def logout(request):
    if request.session.get("id"):
        request.session.clear()
        return redirect("/login")
    return redirect("/login")

# VIEWS TO CREATE AND RENDER POSTS


def posts(request):
    if request.session.get("id"):

        if request.method == "POST":
            post = request.POST.get("post").strip()
            if post.replace(" ", "").isalnum():
                Post.objects.create(text=post, user=User.objects.get(
                    id=request.session.get("id")))
                return render(request, "posts.html", {"all_posts": Post.objects.all().order_by('-id')})
            return render(request, "posts.html", {"all_posts": Post.objects.all().order_by('-id'), "text": post, "alert": "invalid"})

        all_posts = Post.objects.all().order_by('-id')
        if all_posts.exists():
            return render(request, "posts.html", {"all_posts": all_posts})
        return render(request, "posts.html", {"null": "null"})
    return redirect("/login")

# VIEWS TO UPVOTE USER


def upvotes(request, id):
    if request.session.get("id"):
        if request.method == "POST":
            
            post_info = Post.objects.get(id=id)

            query = Upvotes.objects.filter(post_upvote__in=Post.objects.filter(id=id),
                                           user_upvote__in=User.objects.filter(id=request.session.get("id")))

            
            if not query:
                Upvotes.objects.create(user_upvote=User.objects.get(id=request.session.get(
                    "id")), upvote_bool=True, post_upvote=Post.objects.get(id=id))
                Post.objects.filter(id=id).update(
                    upvotes_count=post_info.upvotes_count+1)
                
                

                

            else:
                for data in query:
                    upvote_id = data.id
                    _bool = data.upvote_bool
                if not _bool:
                    Upvotes.objects.filter(
                        id=upvote_id).update(upvote_bool=True)
                    Post.objects.filter(id=id).update(
                        upvotes_count=post_info.upvotes_count+1)

                else:
                    Upvotes.objects.filter(
                        id=upvote_id).update(upvote_bool=False)
                    Post.objects.filter(id=id).update(
                        upvotes_count=post_info.upvotes_count-1)
            query_set = Post.objects.all().order_by('-id')
            data_list = []


            for data in query_set:
                query_to_dict = model_to_dict(data)
                now_asia = data.date_time.astimezone(timezone('Asia/Kolkata'))
                query_to_dict.update(
                    {"username": data.user.username, "date_time": now_asia.strftime("%B %d, %Y, %I:%M %P")})

                data_list.append(query_to_dict)

            return JsonResponse(data_list, safe=False)
        return redirect("/posts")
    return redirect("/login")
