from flask import Flask, request, jsonify, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
# app.debug = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)



boggle_game = Boggle()


@app.route('/')
def display_board():
    """Get board from Boggle instance"""

    board = boggle_game.make_board()
    session["board"] = board
    high_score = session.get('high_score', 0)
    n_plays = session.get('n_plays', 0)

    return render_template('game.html', board=board, high_score=high_score, n_plays=n_plays)


@app.route('/check-word')
def check_word():
    """check if word is valid"""
    
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})
    # jsonify is not actually necessary as of Flask 1.1.0, you can directly return a python dictionary and flask jsonifys behind the scenes
    # return {"result":response}

@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json['score']
    # import pdb; pdb.set_trace()
    high_score = session.get('high_score', 0)
    n_plays = session.get('n_plays', 0)

    session['n_plays'] = n_plays + 1
    session['high_score'] = max(score, high_score)

    return jsonify(brokeRecord=score > high_score)
