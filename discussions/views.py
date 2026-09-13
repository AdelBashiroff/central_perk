from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DiscussionThread, Comment
from .forms import DiscussionThreadForm, CommentForm
from notifications.utils import send_notification


def thread_list(request):
    """
    Список всех тем обсуждений.
    """
    threads = DiscussionThread.objects.all().order_by('-created_at')
    context = {'threads': threads}
    return render(request, 'discussions/thread_list.html', context)


def thread_detail(request, pk):
    """
    Детальная страница темы обсуждения.
    Показывает тему и все комментарии.
    """
    thread = get_object_or_404(DiscussionThread, pk=pk)
    
    # Увеличиваем счетчик просмотров
    thread.views += 1
    thread.save(update_fields=['views'])
    
    # Получаем корневые комментарии (не ответы)
    comments = thread.comments.filter(parent=None).order_by('created_at')
    
    # Форма для комментария
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.user = request.user
            comment.save()
            
            # Уведомление автору темы
            if thread.user != request.user:
                send_notification(
                    user=thread.user,
                    notification_type='new_comment',
                    message=f'{request.user.username} прокомментировал вашу тему',
                    link=f'/discussions/{thread.pk}/'
                )
            
            return redirect('discussions:detail', pk=thread.pk)
    else:
        form = CommentForm()
    
    context = {
        'thread': thread,
        'comments': comments,
        'form': form,
    }
    return render(request, 'discussions/thread_detail.html', context)


@login_required
def thread_create(request):
    """
    Создание новой темы обсуждения.
    """
    if request.method == 'POST':
        form = DiscussionThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            messages.success(request, 'Тема создана!')
            return redirect('discussions:detail', pk=thread.pk)
    else:
        form = DiscussionThreadForm()
    
    context = {'form': form}
    return render(request, 'discussions/thread_form.html', context)


@login_required
def thread_edit(request, pk):
    """
    Редактирование темы обсуждения.
    Только автор может редактировать.
    """
    thread = get_object_or_404(DiscussionThread, pk=pk)
    
    if thread.user != request.user:
        messages.error(request, 'Вы не можете редактировать эту тему!')
        return redirect('discussions:detail', pk=pk)
    
    if request.method == 'POST':
        form = DiscussionThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тема обновлена!')
            return redirect('discussions:detail', pk=thread.pk)
    else:
        form = DiscussionThreadForm(instance=thread)
    
    context = {'form': form, 'thread': thread}
    return render(request, 'discussions/thread_form.html', context)


@login_required
def thread_delete(request, pk):
    """
    Удаление темы обсуждения.
    Только автор может удалить.
    """
    thread = get_object_or_404(DiscussionThread, pk=pk)
    
    if thread.user != request.user:
        messages.error(request, 'Вы не можете удалить эту тему!')
        return redirect('discussions:detail', pk=pk)
    
    if request.method == 'POST':
        thread.delete()
        messages.success(request, 'Тема удалена!')
        return redirect('discussions:list')
    
    context = {'thread': thread}
    return render(request, 'discussions/thread_confirm_delete.html', context)


@login_required
def comment_delete(request, pk):
    """
    Удаление комментария.
    Только автор может удалить.
    """
    comment = get_object_or_404(Comment, pk=pk)
    thread_pk = comment.thread.pk
    
    if comment.user != request.user:
        messages.error(request, 'Вы не можете удалить этот комментарий!')
        return redirect('discussions:detail', pk=thread_pk)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('discussions:detail', pk=thread_pk)
    
    context = {'comment': comment}
    return render(request, 'discussions/comment_confirm_delete.html', context)