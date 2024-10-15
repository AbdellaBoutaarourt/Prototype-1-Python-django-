from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import ArticleForm
from .models import Article
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm



@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Assign the current user as the author
            article.save()
            messages.success(request, 'Article added successfully!')
            return redirect('articles:article_list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.author:
        article.delete()
        messages.success(request, 'Article deleted successfully.')
    else:
        messages.error(request, 'You are not allowed to delete this article.')

    return redirect('articles:article_list')


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})

def my_article(request):
    if request.user.is_authenticated:
        articles = Article.objects.filter(author=request.user)
    else:
        articles = []

    return render(request, 'my_articles.html', {'articles': articles})

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, author=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:my_article')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Password1 is used to log in
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                messages.success(request, 'Your account has been created and you are now logged in!')
                return redirect('articles:article_list')  # Redirect to the article list page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('articles:article_list')  # Redirect to articles list after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

