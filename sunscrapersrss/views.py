# Create your views here.
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CurrencyRate


@api_view(['GET'])
def get_for_date(request):
    """
    Return a request for given date.

    Accepts a optional parameter date, which is a ISO8601-encoded part up to day part including, ie. '2019-04-25' would be fine. An optional day
    to get the data for. By default, is today.
    """
    date = request.GET.get('date', datetime.date.today().isoformat())
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = datetime.date(year=date.year, month=date.month, day=date.day)

    output = {'data': []}
    for currency_rate in CurrencyRate.objects.filter(currency_date=date):
        output['data'].append({'currency_from': currency_rate.currency_from,
                               'currency_to': currency_rate.currency_to,
                               'currency_date': currency_rate.currency_date.isoformat(),
                               'currency_rate': currency_rate.currency_rate})

    return Response(output)
