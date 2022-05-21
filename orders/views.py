from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PlacingOrder

# Create your views here.

def create_order(request):
    if request.method == 'POST':
        form = PlacingOrder(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Successfully Created')
            return redirect(reverse('accounts:home'))
    # form = PlacingOrder(initial={'seller':request.user.seller})
    form = PlacingOrder()
    return render(request, 'create_order.html', {'form': form})