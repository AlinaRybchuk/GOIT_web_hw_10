from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .utils import get_mogngodb
from .models import Author, Quote, Tag

def main(request, page=1):
    db = get_mogngodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

@login_required
def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        Author.objects.create(name=name, url=url)
        return redirect('author_list')
    return render(request, 'quotes/add_author.html')

@login_required
def add_quote(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        author_name = request.POST.get('author')
        tags = request.POST.getlist('tags')
        
        author, created = Author.objects.get_or_create(name=author_name)
        quote = Quote.objects.create(text=text, author=author)
        
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

        return redirect('quote_list')
    authors = Author.objects.all()
    return render(request, 'quotes/add_quote.html', {'authors': authors})