from django.shortcuts import render
from django.core.context_processors import csrf


def chat(request):
    """
    """
    c = {"chat_id": "public"}
    c.update(csrf(request))
    return render(request, "django_chat/chat.html", c)
