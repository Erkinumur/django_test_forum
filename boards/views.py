from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from boards.models import Board, Topic, Post
from boards.forms import TopicForm, PostForm


def index_page_view(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})


def board_details_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-created_at').annotate(replies=Count('posts') - 1)
    return render(request, 'board_details.html', {'board': board, 'topics': topics})


@login_required
def new_topic_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.user =request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                authored_by=request.user,
            )
        return redirect('topic_posts', board_pk=board.pk, topic_pk=topic.pk)
    form = TopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    topic.views_count += 1
    topic.save(update_fields=['views_count', ])
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def new_post_view(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.authored_by = request.user
            post.save()
            return redirect('topic_posts', board_pk=board_pk, topic_pk=topic.pk)
    form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})    