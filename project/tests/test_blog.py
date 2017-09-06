# project/test.py

import unittest
from project import app

class ProjectTests(unittest.TestCase):
    # setup and teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.assertEquals(app.debug, False)

    def tearDown(self):
       pass

    # tests

    def test_blog_page(self):
        response = self.app.get('/blog/', follow_redirects=True)
        self.assertIn(b'Hello Blog', response.data)

if __name__ == "__main__":
    unittest.main()
