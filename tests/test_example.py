from app import server
from nose.tools import ok_

def setup_module():
    global app_client 
    app_client = server.test_client()

def test_index():
    res = app_client.get('/')
    ok_(res.status_code == 200)
