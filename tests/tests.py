from django.test import TestCase
import requests,json
import datetime
from django.utils import timezone
from .models import Test

class TestTests(TestCase):


# # =========== Test endpoint ======================

    """
    Test the endpoint GET list of all available tests
    expected result 200
    """
    def test_gettestlist(self): #200
        r = requests.get("http://127.0.0.1/api/v1/test/")
        self.assertEqual(r.status_code, 200)


    """
    Test the endpoint with incorrect name
    expected result 404 - don't have such page
    """
    def test_gettestlist(self): #404
        r = requests.get("http://127.0.0.1/api/v1/testssdsf/")
        self.assertEqual(r.status_code, 404)


# # =========== TestLogs endpoint ======================
    """
    Test the endpoint GET list of testlogs by PIN
    given PIN in DB and the test doesn't have any teslogs
    expected result number of testlogs == 0

    """
    def test_gettestlogslist_PINinDB(self): #200
        r = requests.get("http://127.0.0.1/api/v1/testlog/bypin/135126531/")
        self.assertEqual(len(json.loads(r.text)) == 0, True)

    """
    Test the endpoint GET list of testlogs by PIN
    given PIN in DB and the test has testlogs 
    expected result number of testlogs> 0

    """
    def test_gettestlogslist_PINinDB(self): #200
        r = requests.get("http://127.0.0.1/api/v1/testlog/bypin/147483647/")
        self.assertEqual(len(json.loads(r.text))>0, True)

    """
    Test the endpoint GET list of testlogsby PIN
    given PIN not in DB
    expected result 404

    """
    def test_gettestloglist_PINnotinDB(self): #404
        r = requests.get("http://127.0.0.1/api/v1/testlog/bypin/11111210/")
        self.assertEqual(r.status_code, 404)

