from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class UsersTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        User.query.delete()
        user = User(first_name="Aaron", last_name="Andreson")
        if not user.image_url:
            user.image_url = "google.com"
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Aaron', html)
    
    def test_create_user(self):
        with app.test_client() as client:
            data = {'first_name': "Eragon", 'last_name': "Shadeslayer", "url": "google.com"}
            resp = client.post("/create_user", data=data , follow_redirects= True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Eragon Shadeslayer", html)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {'first_name': "Miranda", 'last_name': "Andreson", "url": "google.com"}
            resp = client.post("/edit_user/1", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Aaron Andreson", html)
            self.assertIn("Miranda Andreson", html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get("/delete_user/1", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Aaron Andreson", html)
