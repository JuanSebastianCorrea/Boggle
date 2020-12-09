from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
         with app.test_client() as client:
            #  import pdb; pdb.set_trace()
            response =  client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-4 text-center">Boggle</h1>', html) 
            self.assertIn('<div class="h3 text-center">High Score', html)
            self.assertIn('<div class="h3 text-center">Score', html)
            self.assertIn('<div class="h3 text-center timer-container">Time left', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('n_plays'))


    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as sesh:
                sesh['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]

            response = client.get('/check-word?word=cat')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

            
    def test_word_on_board(self):
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=hippopotamus')
            
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_english_word(self):
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=lkjdj')
            
            self.assertEqual(response.json['result'], 'not-word')


    # def test_post_score(self):
    #     with app.test_client() as client:
            
    #         response = client.post('/post-score', data={'score': 20})
    #         import pdb; pdb.set_trace()
        