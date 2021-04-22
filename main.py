from flask import Flask, jsonify, request
from scores_db import ScoreDAO, Score

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "hello"

@app.route('/scores', methods=['POST'])
def post_score():
    score: Score = request.json
    ScoreDAO.add_score(score)
    return jsonify(score)

@app.route('/scores', methods=['GET'])
def get_scores():
    return jsonify(list(ScoreDAO.get_scores()))

@app.route('/scores/<scoreId>', methods=['GET'])
def get_score_by_id(scoreId: str):
    return jsonify(ScoreDAO.get_score_by_id(int(scoreId)))


@app.route('/scores/<scoreId>', methods=['PUT'])
def put_score(scoreId: str):
    score: Score = request.json
    ScoreDAO.scores[int(scoreId)] = score
    return jsonify(score)

if __name__ == '__main__':
    app.run()
