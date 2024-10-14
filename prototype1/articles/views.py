from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import ArticleForm
from .models import Article

@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles:article_list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article_detail.html', {'article': article})

