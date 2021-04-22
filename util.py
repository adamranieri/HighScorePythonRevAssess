import pytest
import json
import base64
import requests
from os import path, remove, listdir, rmdir, mkdir
import shutil


def RevaTest(points=0, tier=0):
    def decorator_reva_test(func):
        def inner_reva_test(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                
                # Do logic to add to JSON if no exception is thrown
                add_to_json(func.__name__, points=points, isSuccessful=True, errorMessage="SUCCESS", tier=tier)
                
                return result
        
            except AssertionError as ae:

                # Do Logic to add to JSON is exception is thrown
                add_to_json(func.__name__, points=points, isSuccessful=False, errorMessage=str(ae), tier=tier)

                raise
        return inner_reva_test
    return decorator_reva_test


@pytest.fixture(scope="session", autouse=True)
def finish():
    # Start logic that starts at the beginning of the session
    start_json()

    yield
    
    # End logic goes at the end of all sessions
    data = load_result()
    requests.put(data['config']['serverLocation'], json=data)

def load_result():
    data = {}
    with open("TestResults.json") as f:
        tests = json.load(f)
    with open("RevAssessConfig.json") as f:
        config = json.load(f)

    zip()

    with open("main.zip", "rb") as f:
        main_bytes = f.read()
    
    remove("main.zip")
    
    base64_bytes = base64.b64encode(main_bytes)
    base64_main = base64_bytes.decode('ascii')

    data['config'] = config
    data['tests'] = tests
    data['base64EncodedResults'] = base64_main

    return data


def start_json():
    filename = "TestResults.json"

    if not path.exists(filename):
        data = []
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)


def add_to_json(testName, points, isSuccessful, errorMessage, tier):
    filename = "TestResults.json"
    with open(filename) as f:
        data = json.load(f)
    
    temp = {}
    temp['testName'] = testName
    temp['points'] = points
    temp['isSuccessful'] = isSuccessful
    temp['errorMessage'] = errorMessage
    temp['tier'] = tier

    index = -1
    for i in range(len(data)):
        if data[i]['testName'] == temp['testName']:
            index = i
            break
    
    if index == -1:
        data.append(temp)
    else:
        data[i] = temp

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def zip():
    if path.exists("main.zip"):
        remove("main.zip")
    
    dest = copytree()

    shutil.make_archive("main", 'zip', dest)

    shutil.rmtree(dest)


def copytree():

    src = "."
    dst = "to_zip"

    mkdir(dst)

    exclude = ['__pycache__', '.pytest_cache', '.git', 'to_zip']

    for item in listdir(src):
        if item in exclude:
            continue
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            shutil.copytree(s, d, True)
        else:
            shutil.copy2(s, d) 
    
    return dst