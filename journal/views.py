from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """Index of Journal"""
    return render(request, 'journal/index.html')

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404


#list of topics
@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics" : topics}
    return render(request, "journal/topics.html", context)

#individual topic
@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {"topic": topic, "entries": entries}
    return render(request, "journal/topic.html", context)

@login_required
def new_topic(request):
    """Add a new topic."""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('journal:topics'))

    context = {"form" : form }
    return render(request, "journal/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry"""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('journal:topic',
            args=[topic_id]))

    context = {"topic": topic, "form": form}
    return render(request, 'journal/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an entry"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != "POST":
        #fill the form with the current info of the post
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('journal:topic',
            args=[topic.id]))

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, 'journal/edit_entry.html', context)
