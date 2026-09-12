from django.shortcuts import render
from quotes.models import Quote
from discussions.models import DiscussionThread


def home(request):
    """
    Главная страница.
    Показывает последние цитаты и темы обсуждений.
    """
    latest_quotes = Quote.objects.all().order_by('-created_at')[:5]
    latest_threads = DiscussionThread.objects.all().order_by('-created_at')[:5]
    
    context = {
        'latest_quotes': latest_quotes,
        'latest_threads': latest_threads,
    }
    return render(request, 'index.html', context)