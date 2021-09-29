from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import PlacingOrder

# Create your views here.

def create_order(request, id):

    form = PlacingOrder()
    if request.method == 'POST':
        # question = get_object_or_404(Order, pk=id)
        form = PlacingOrder(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Account Successfully Create')
            return redirect(reverse('accounts:home'))
    return render(request, 'create_order.html', {'form': form})