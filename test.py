from main import *
from util import *

# run your flask server on the default port of 5000 then run pytest test.py
# if this test passes then it is working correctly
@RevaTest(points=0, tier= 0)
def test_hello():
    response = requests.get('http://localhost:5000/hello')
    assert response.text == 'hello'




great_score = {"scoreId" : 0, "initials" : 'JRR','points': 9999}
medium_score = {"scoreId" : 0 ,"initials": 'MEH','points': 5000}
bad_score = {"scoreId" : 0 ,"initials" : 'KIM' , 'points' : 1000}

#Example URI: POST /scores   body: {"scoreId":0, "initials":"THV", "points":6000}
@RevaTest(points=10, tier= 1)
def test_post_scores():
    response = requests.post('http://localhost:5000/scores',  json = great_score)
    body = response.json()
    great_score["scoreId"] = body["scoreId"]
    assert body["scoreId"] != 0

    response = requests.post('http://localhost:5000/scores',  json = medium_score)
    body = response.json()
    medium_score["scoreId"] = body["scoreId"]
    assert body["scoreId"] != 0

    response = requests.post('http://localhost:5000/scores',  json = bad_score)
    body = response.json()
    bad_score["scoreId"] = body["scoreId"]
    assert body["scoreId"] != 0


#Example URI: GET  /scores/45
@RevaTest(points=10, tier= 1)
def test_get_score_by_id():
    response = requests.get(f'http://localhost:5000/scores/{great_score["scoreId"]}')
    body = response.json()
    assert body == great_score

#Example URI: GET  /scores
@RevaTest(points=10, tier= 1)
def test_get_scores():
    response = requests.get(f'http://localhost:5000/scores')
    body = response.json()
    assert len(body) > 2

#Example URI: PUT /scores/65
@RevaTest(points=10, tier= 1)
def test_update_score():
    updated_score = great_score
    updated_score["points"] = 0
    requests.put(f'http://localhost:5000/scores/{great_score["scoreId"]}',  json = updated_score)
    response = requests.get(f'http://localhost:5000/scores/{great_score["scoreId"]}')
    body = response.json()
    assert body["points"] == 0
#Example URI: DELETE /scores/54
@RevaTest(points=10, tier= 1)
def test_delete_score_204():
    response = requests.delete(f'http://localhost:5000/scores/{great_score["scoreId"]}')
    assert response.status_code == 204

@RevaTest(points=10, tier= 1)
def test_delete_score_404():
    response = requests.delete(f'http://localhost:5000/scores/{great_score["scoreId"]}')
    assert response.status_code == 404

#Example URI: GET /scores?ordered=descending
@RevaTest(points=10, tier= 1)
def test_scores_ordered_by_points_descending():
    pass


#Example URI: GET /scores?ordered=ascending
@RevaTest(points=10, tier= 1)
def test_scores_ordered_by_points_ascending():
    pass

#Example URI: GET /scores?initals=JTR
@RevaTest(points=10, tier= 1)
def test_scores_by_intials():
    pass

