import datetime
import subprocess

from selenium import webdriver
from django.core.management.base import BaseCommand

from oneliner.models import Service


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        domLoadTimes = []
        loadTimes = []
        requests = 10

        print Service.objects.all()

        for idx in range(0, requests):
            driver = webdriver.Firefox()
            driver.get('http://oneliner.inn.org/')
            timing = driver.execute_script('return performance.timing')
            driver.close()

            """
            Time between domLoading and domComplete
            """
            domLoadTimes.append(self.get_domcomplete(timing))

            """
            Time between requestStart and loadEventEnd
            """
            loadTimes.append(self.get_load(timing))

        """
        Print average load and domComplete times
        """
        print "For %s requests..." % requests
        print "Average load time: %s sec" % self.get_average(loadTimes)
        print "Average domComplete time: %s sec" % self.get_average(domLoadTimes)

    def start_webserver(self):
        self.webserver = subprocess.Popen([
            './manage.py', 'runserver', '0.0.0.0:8000', '--nothreading', '--noreload'
        ])

    def stop_webserver(self):
        self.webserver.terminate()

    def get_load(self, timing):
        delta = (
            datetime.datetime.fromtimestamp(float(timing.get('loadEventEnd')) / 1000.00) -
            datetime.datetime.fromtimestamp(float(timing.get('requestStart')) / 1000.00)
        )
        return delta.total_seconds()

    def get_domcomplete(self, timing):
        delta = (
            datetime.datetime.fromtimestamp(float(timing.get('domComplete')) / 1000.00) -
            datetime.datetime.fromtimestamp(float(timing.get('domLoading')) / 1000.00)
        )
        return delta.total_seconds()

    def get_average(self, list):
        return sum(list) / len(list)
