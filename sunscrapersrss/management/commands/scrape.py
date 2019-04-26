from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
import untangle
import datetime
from xml.parsers.expat import ExpatError
from xml.sax._exceptions import SAXParseException

from sunscrapersrss.models import CurrencyRate
from sunscrapers import settings

class Command(BaseCommand):
    help = 'Scrapes data from target endpoint. '

    def scrape_for_currency(self, currency_code):
        req = requests.get('https://www.ecb.europa.eu/rss/fxref-%s.html' % (currency_code, ))
        try:
            obj = untangle.parse(req.text)
        except (ExpatError, SAXParseException):
            return

        for obj in obj.rdf_RDF.item:
            date = obj.dc_date.cdata
            price = obj.cb_statistics.cb_exchangeRate.cb_value.cdata
            base_currency = obj.cb_statistics.cb_exchangeRate.cb_baseCurrency.cdata
            target_currency = obj.cb_statistics.cb_exchangeRate.cb_targetCurrency.cdata

            date = date[:22] + date[23:]
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
            date = datetime.date(year=date.year, month=date.month, day=date.day)

            try:
                currency_rate = CurrencyRate.objects.get(currency_from=base_currency, currency_to=target_currency, currency_date=date)
            except CurrencyRate.DoesNotExist:
                currency_rate = CurrencyRate(currency_from=base_currency, currency_to=target_currency, currency_date=date)
            currency_rate.currency_rate = float(price)
            currency_rate.save()

    def handle(self, *args, **kwargs):
        for currency in settings.CURRENCIES_TO_SCRAPE_FOR:
            self.scrape_for_currency(currency)
