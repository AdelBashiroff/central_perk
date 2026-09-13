from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Quote
from .forms import QuoteForm
from discussions.models import Comment
from discussions.forms import CommentForm


def quote_list(request):
    """
    Список всех цитат.
    Поддерживает поиск по тексту и фильтрацию по персонажу.
    """
    quotes = Quote.objects.all().order_by('-created_at')
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        quotes = quotes.filter(
            Q(text__icontains=search_query) |
            Q(character__name__icontains=search_query)
        )
    
    # Фильтр по персонажу
    character_id = request.GET.get('character', '')
    if character_id:
        quotes = quotes.filter(character_id=character_id)
    
    context = {
        'quotes': quotes,
        'search_query': search_query,
        'character_id': character_id,
    }
    return render(request, 'quotes/quote_list.html', context)


def quote_detail(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    
    context = {
        'quote': quote,
    }
    return render(request, 'quotes/quote_detail.html', context)


@login_required
def quote_create(request):
    """
    Создание новой цитаты.
    Доступно только авторизованным пользователям.
    """
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.author = request.user
            quote.save()
            
            # Отправляем уведомления всем (кроме автора)
            for user in User.objects.exclude(id=request.user.id)[:10]:
                send_notification(
                    user=user,
                    notification_type='new_quote',
                    message=f'{request.user.username} добавил новую цитату!',
                    link=f'/quotes/{quote.pk}/'
                )
            
            return redirect('quotes:detail', pk=quote.pk)
    else:
        form = QuoteForm()
    
    context = {'form': form}
    return render(request, 'quotes/quote_form.html', context)


@login_required
def quote_edit(request, pk):
    """
    Редактирование цитаты.
    Только автор может редактировать свою цитату.
    """
    quote = get_object_or_404(Quote, pk=pk)
    
    # Проверяем, что пользователь - автор
    if quote.author != request.user:
        messages.error(request, 'Вы не можете редактировать эту цитату!')
        return redirect('quotes:detail', pk=pk)
    
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цитата обновлена!')
            return redirect('quotes:detail', pk=quote.pk)
    else:
        form = QuoteForm(instance=quote)
    
    context = {'form': form, 'quote': quote}
    return render(request, 'quotes/quote_form.html', context)


@login_required
def quote_delete(request, pk):
    """
    Удаление цитаты.
    Только автор может удалить свою цитату.
    """
    quote = get_object_or_404(Quote, pk=pk)
    
    # Проверяем, что пользователь - автор
    if quote.author != request.user:
        messages.error(request, 'Вы не можете удалить эту цитату!')
        return redirect('quotes:detail', pk=pk)
    
    if request.method == 'POST':
        quote.delete()
        messages.success(request, 'Цитата удалена!')
        return redirect('quotes:list')
    
    context = {'quote': quote}
    return render(request, 'quotes/quote_confirm_delete.html', context)


@login_required
def quote_like(request, pk):
    """
    Лайк/дизлайк цитаты.
    Переключает состояние лайка.
    """
    quote = get_object_or_404(Quote, pk=pk)
    
    if request.user in quote.likes.all():
        quote.likes.remove(request.user)
        messages.info(request, 'Вы убрали лайк')
    else:
        quote.likes.add(request.user)
        messages.success(request, 'Вы поставили лайк!')
    
    return redirect('quotes:detail', pk=quote.pk)