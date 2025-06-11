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
    testCompany = json.loads('{"products":{"cream":["milk","fat","emulsifier"]}}')
    assert calc_score(testCompany, ["label1"]) == 0

def test_calc_score_nothing():
    testCompany = {"key1": "exists"}
    assert calc_score(testCompany, ["label1"]) == 0

def test_calc_score_ingredient_match():
    testCompany = json.loads('{"products":{"cream":["milk","fat","emulsifier"]}}')
    assert calc_score(testCompany, ["milk"]) == 5

def test_calc_score_mult_ingredient_match():
    testCompany = json.loads('{"products":{"cream":["milk","fat","emulsifier"],"anothercream":["milk","fat","emulsifier"]}}')
    assert calc_score(testCompany, ["milk"]) == 10

def test_calc_score_no_product():
    testCompany = {"labels": ["exists"]}
    assert calc_score(testCompany, ["exists"]) == 10

def test_calc_score_description_full_match():
    testCompany = {"description": "exists"}
    assert calc_score(testCompany, ["exists"]) == 10

def test_calc_score_description_partial_match():
    testCompany = {"description": "blablaexists"}
    assert calc_score(testCompany, ["exists"]) == 10

def test_calc_score_description_not_match():
    testCompany = {"description": "exists"}
    assert calc_score(testCompany, ["not-exists"]) == 0

def test_normalise_name_found_1():
    testCompany = {"company_name": "exists"}
    print(normalise_company(testCompany)['name'])    
    assert normalise_company(testCompany)['name'] == "exists"

def test_normalise_name_found_2():
    testCompany = {"company": "exists"}    
    assert normalise_company(testCompany)['name'] == "exists"

def test_normalise_name_found_3():
    testCompany = {"name": "exists"}    
    assert normalise_company(testCompany)['name'] == "exists"

def test_normalise_name_not_found():
    testCompany = {"noname": "exists"}    
    assert normalise_company(testCompany)['name'] == "unknown"

def test_merge_companies():
    testCompany = json.loads('{"products":{"cream":["milk","fat"]}}')
    testCompany2 = json.loads('{"products":{"cream":["fat","emulsifier"]}}')
    assert set(merge_companies(testCompany, testCompany2)['products']['cream']) == set(['emulsifier', 'fat', 'milk'])