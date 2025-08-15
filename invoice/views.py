from django.shortcuts import render, redirect
from .forms import InvoiceForm

def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/invoice/success')  # يجب تعريف URL باسم 'invoice_success'
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form})

def invoice_success(request):
    return render(request, 'invoice_success.html')