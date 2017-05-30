from django.test import TestCase
import requests
import datetime
from django.utils import timezone
from .models import Test

class TestTests(TestCase):

# =========== Test that PIN processed properly ======================

    """
    Test the endpoint with PIN that is not in the DB
    expected result 404 (object not found) - we don't have a test with such PIN

    """
    def test_addtestlog_to_PINnotinDB(self): #404
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/aa65", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 404)

    """
    Test endpoint with PIN that starts from valid PIN that is in the DB
    and ends with extra 0
    expected result 404 (object not found) - we don't have a test with such PIN

    """
    def test_addtestlog_to_PINcorrectPIN_extra0(self): #404
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/aa658687911607b3efb0389060af6a210", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 404)

    """
    Test the endpoint with empty PIN
    Important this request should be routed properly
    expected result 404 (object not found) - we don't have a test without PIN (because PIN is generated automatically,
                when we save the test to DB for first time)  and the request routed to proper endpoint

    """
    def test_addtestlog_to_emptyPIN(self): #404
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 404)

    """
    Test the endpoint with PIN strings that includes incorrect symbols "bad"
    expected result 404 (object not found) - we don't have a test with such PIN

    """
    def test_addtestlog_to_PINincludesbadcharts(self): #404
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/b4970e8 efc1$f745c407a2e59b720%2", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 404)

# =========== Test that isactive and test dates processed properly ======================
    """
    Test the endpoint with correct PIN from DB but the test is inactive
    expected result 499

    """
    def test_addtestlog_to_correctPIN_inactiveTEST(self): #499
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/b4970e8efc1f745c407a2e59b7201892", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 499)

    """
    Test the endpoint with correct PIN from DB and the test is inactive but
        now < test.date_from (too early)
    expected result 499

    """
    def test_addtestlog_to_correctPIN_wrongdateofTESTtooearly(self): #499
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/ba638b02b57b5a75246a6c535f1b0aa3", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 499)

    """
    Test the endpoint with correct PIN from DB and the test is inactive but
        now > test.date_till (too late)
    expected result 499

    """
    def test_addtestlog_to_correctPIN_wrongdateofTESTtoolate(self): #499
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/aa658687911607b3efb0389060af6a21", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 499)

    """
    Test the endpoint with correct PIN from DB and the test active 
    expected result 200

    """
    def test_addtestlog_to_correctPIN_activeTEST(self): #200
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/6118249081e022fb041c49edac1f03cf",
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 200)

    """
    Test the endpoint with correct PIN from DB and the test active but PIN is typed in upper case 
    expected result 499 - PIN is case sensitive

    """
    def test_addtestlog_to_correctPIN_UPPERCASE_activeTEST(self): #200
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/AA658687911607b3efb0389060Af6A21", 
                files={'screenshot':open('/home/screenshot1495418189067.jpeg', 'rb'), 'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 499)


# =========== Test that isactive and dates are correct but we send not all needed fields in the request ======================
# ===========     We need to think about this becaus some students may not have web cam, or the app has troubles with some modules ...
# ===========          so the app cannot send full request. THe backend should save at least fields that presents in the request
    """
    Test the endpoint with correct PIN from DB and the test active
         but request doesn't include screenshot field
    expected result 200

    """
    def test_addtestlog_to_correctPIN_noscreenshot(self): #200
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/6118249081e022fb041c49edac1f03cf", 
                files={'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 200)

    """
    Test the endpoint with correct PIN from DB and the test active
         but request doesn't include photo field
    expected result 200

    """
    def test_addtestlog_to_correctPIN_nophoto(self): #200
        r = requests.post("http://127.0.0.1/api/v1/testlog/bypin/6118249081e022fb041c49edac1f03cf", 
                files={'photo': open('/home/photo1495270562238.jpeg', 'rb')},
                data={'text': "Example text"})
        self.assertEqual(r.status_code, 200)
