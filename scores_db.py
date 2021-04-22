from typing import TypedDict

class Score(TypedDict):
    scoreId: int
    initials: str
    points: int


class ScoreDAO:

    counter = 0
    scores = {}

    @classmethod
    def add_score(cls, score: Score):
        cls.counter += 1
        score["scoreId"] = cls.counter
        cls.scores[cls.counter] = score

    @classmethod
    def get_score_by_id(cls, id: int):
        return cls.scores[id]

    @classmethod
    def get_scores(cls):
        return cls.scores.values()

