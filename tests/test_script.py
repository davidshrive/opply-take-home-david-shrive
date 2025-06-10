import runpy
import json
from script import *

def test_script():
    runpy.run_path("script.py")

def test_find_value_found():
    testCompany = {"key1": "exists"}
    assert find_value(testCompany,["key1","key2"]) == "exists"

def test_find_value_not_found():
    testCompany = {"key3": "exists"}
    assert find_value(testCompany,["key1","key2"]) == "unknown"

def test_calc_score_no_product():
    testCompany = {"labels": ["exists"]}
    assert calc_score(testCompany, ["label1"]) == 0

def test_calc_score_no_labels():
    testCompany = json.loads('{"products":[{"name":"cake","ingredients":["flour","sugar","eggs"]},{"name":"biscuits"},{"name":"chips"}]}')
    assert calc_score(testCompany, ["label1"]) == 0

def test_calc_score_nothing():
    testCompany = {"key1": "exists"}
    assert calc_score(testCompany, ["label1"]) == 0

def test_calc_score_ingredient_match():
    testCompany = json.loads('{"products":[{"name":"cake","ingredients":["flour","sugar","eggs"]},{"name":"biscuits"},{"name":"chips"}]}')
    assert calc_score(testCompany, ["eggs"]) == 5

def test_calc_score_no_product():
    testCompany = {"labels": ["exists"]}
    assert calc_score(testCompany, ["exists"]) == 10