from django.shortcuts import render
from django.shortcuts import redirect, render
from .models import Message
# Create your views here.


def seller_join(request):
    return render(request, 'company/sell_withUs.html')


def delivery_join(request):
    return render(request, 'company/delivery_providers.html')


def send_message(request):
    if request.method == 'POST':
        # Get the message content from the form
        message_content = request.POST.get('content')
        # Create a new Message instance
        Message.objects.create(
            content=message_content, status="New"
        )
        # Redirect to a success page or return a response
        return redirect('home')
