#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Quote

def index(request):
    latest_quote_list = Quote.objects.order_by('-pub_date')[:5]
    context = {'latest_quote_list': latest_quote_list}
    return render(request, 'daily_digest/index.html', context)

def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'daily_digest/detail.html', {'quote': quote})

def results(request, quote_id):
    response = "You're looking at the results of quote {}."
    return HttpResponse(response.format(quote_id))

def vote(request, quote_id):
    return HttpResponse("You're voting on quote {}.".format(quote_id))
    
