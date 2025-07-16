import unittest

from app import User, app, db


class FlaskAppTestCase(unittest.TestCase):

    # Set up the test environment
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = app.test_client()

        # Create the database in memory
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.drop_all()

    # Test case for the home page route
    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Test case for the login route
    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    # Test case for the register route
    def test_register_route(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    # Test case for the admin route (access denied if not logged in as admin)
    def test_admin_route(self):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 302)  # Redirects to login if not logged in

    # Test case for the sentiment analysis page route
    def test_sentiment_page_route(self):
        response = self.client.get('/sentiment')
        self.assertEqual(response.status_code, 200)

    # Test case for the sentiment prediction route
    def test_predict_route(self):
        input_data = {'text': 'I am so happy!'}
        response = self.client.post('/predict', json=input_data)
        self.assertEqual(response.status_code, 200)

    # Test case for the chat route
    def test_chat_route(self):
        input_data = {'message': 'Hello!'}
        response = self.client.post('/chat', json=input_data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
