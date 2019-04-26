from rest_framework.test import APITestCase

from .models import CurrencyRate


class TestAPI(APITestCase):

    def test_getdata(self):
        cr = CurrencyRate(currency_from='EUR', currency_to='PLN',
                          currency_date='2019-04-26',
                          currency_rate=4.2950)
        cr.save()

        data = self.client.get('/rates/?date=2019-04-26')
        self.assertEquals(data.data, {'data': [{'currency_from': 'EUR',
                                                'currency_to': 'PLN',
                                                'currency_rate': 4.2950,
                                                'currency_date': '2019-04-26'}]})

    def test_scraping(self):
        from sunscrapersrss.management.commands import scrape
        bc = scrape.Command()
        bc.handle()

        self.assertGreater(CurrencyRate.objects.count(), 0)
