from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    # Works at all?
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Redirects on inexistent board?
    def test_redirect_inexistent_board(self):
        tester = app.test_client(self)
        response = tester.get('/foo', follow_redirects = True)
        self.assertIn(b'board foo does not exist', response.data)

if __name__ == '__main__':
    unittest.main()
