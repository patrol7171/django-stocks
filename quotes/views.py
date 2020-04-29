from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json


def home(request):
    tickers = Stock.objects.all()
    symbols = []
    for ticker_item in tickers:
        symbols.append(str(ticker_item))
    ticker_str_list = (','.join([str(x) for x in symbols])).upper()
    api_request = requests.get("https://cloud.iexapis.com/v1/stock/market/batch?types=quote&symbols=" + ticker_str_list + "&token=pk_82c56903bd66444f888d1e6382138ee3")
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "error"
    return render(request, 'home.html', {'tickers':tickers, 'api':api})
    

def about(request):
    return render(request, 'about.html', {})


def update_stock(request):
    if request.method == 'POST':
       form = StockForm(request.POST or None)
       if form.is_valid():
           form.save()
           messages.success(request, "Stock symbol has been added!")
           return redirect('update_stock')
    else:
        tickers = Stock.objects.all()
        symbols = []
        for ticker_item in tickers:
            symbols.append(str(ticker_item))
        ticker_str_list = (','.join([str(x) for x in symbols])).upper()
        api_request = requests.get("https://cloud.iexapis.com/v1/stock/market/batch?types=quote&symbols=" + ticker_str_list + "&token=pk_82c56903bd66444f888d1e6382138ee3")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "error"
        return render(request, 'update_stock.html', {'tickers':tickers, 'api':api})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock symbol has been deleted!")
    return redirect('update_stock')


def lookup_stock(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_82c56903bd66444f888d1e6382138ee3")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "error"
        return render(request, 'lookup_stock.html', {'api':api})
    else:
        return render(request, 'lookup_stock.html', {'ticker':"Enter a symbol above to get started..."})