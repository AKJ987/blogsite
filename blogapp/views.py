from django.shortcuts import render, redirect
from django.views.generic import View,CreateView, FormView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blogapp.forms import UserRegistrationForm, LoginForm, ProfileCreationForm, PasswordResetForm, BlogForm, CommentForm
from blogapp.models import UserProfile, Blogs, Comments
from django.contrib import messages

class UserRegistrationView(CreateView):
    form_class=UserRegistrationForm
    template_name='reg.html'
    model=User
    success_url = reverse_lazy("signin")

class LoginView(FormView):
    form_class=LoginForm
    template_name='login.html'
    model=User

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                messages.success(request, 'login success')
                return redirect('home')
            else:
                messages.error(request, 'login error')
                return render(request, self.template_name, {'form': form})

def signout(request, *args, **kwargs):
    logout(request)
    return redirect('signin')


class IndexView(FormView):
    template_name = 'home.html'
    form_class = BlogForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all().order_by('-posted_date')
        context['blogs']=blogs
        comment_form=CommentForm
        context['commentform']=comment_form
        return context

class ProfileCreationView(CreateView):
    form_class = ProfileCreationForm
    template_name = 'profile.html'
    model = UserProfile
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'profile has been created')
        self.object = form.save()
        return super().form_valid(form)

class ViewMyProfileView(FormView):
    template_name = 'viewprofile.html'
    form_class = ProfileCreationForm

class PasswordResetView(FormView):
    template_name = 'pass_reset.html'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpass=form.cleaned_data.get('old_password')
            newpass=form.cleaned_data.get('new_password')
            confpass=form.cleaned_data.get('confirm_password')
            user=authenticate(request,username=request.user.username, password=oldpass)
            if user:
                user.set_password(confpass)
                user.save()
                messages.success(request, 'password changed succesfully')
                return redirect('signin')
            else:
                messages.error(request, 'password not chnaged')
                return render(request, 'pass_reset.html', {'form':form})

class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = ProfileCreationForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        messages.success(self.request, 'profile has been successfully updated')
        self.object = form.save()
        return super().form_valid(form)

class BlogCreateView(CreateView):
    model = Blogs
    template_name = 'blogcreate.html'
    form_class = BlogForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request, 'Blog has succesfully created')
        self.object = form.save()
        return super().form_valid(form)

def add_comment(request, *args, **kwargs):
    if request.method == 'POST':
        blog_id=kwargs.get('post_id')
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get('comment')
        Comments.objects.create(blog=blog, comment=comment, user=user)
        messages.success(request, 'comment has been posted')
        return redirect('home')

def add_like(request, *args, **kwargs):
    blog_id=kwargs.get('post_id')
    blog=Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect('home')








