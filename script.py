import json
import csv

## Load file
with open('input/processed_buyer_leads.json', 'r') as inputFile:
	inputData = json.load(inputFile)

## Normalise 
companies = {}

for inputCompany in inputData:
	company = {}
	keys = list(inputCompany.keys())

	name = "unknown"
	if "company_name" in keys:
		name = inputCompany["company_name"]
	elif "company" in keys:
		name = inputCompany["company"]
	elif "name" in keys:
		name = inputCompany["name"]
	company["name"] =  name

	description = "unknown"
	if "info" in keys:
		description = inputCompany["info"]
	elif "desc" in keys:
		description = inputCompany["desc"]
	elif "description" in keys:
		description = inputCompany["description"]
	company["description"] =  description

	labels = "unknown"
	if "labels" in keys:
		labels = inputCompany["labels"]
	elif "keywords" in keys:
		labels = inputCompany["keywords"]
	elif "tags" in keys:
		labels = inputCompany["tags"]
	company["labels"] = list(map(lambda label:label.strip(), labels.split(";")))

	website = "unknown"
	if "website" in keys:
		website = inputCompany["website"]
	elif "site" in keys:
		website = inputCompany["site"]
	elif "url" in keys:
		website = inputCompany["url"]
	company["website"] =  website

	products = "unknown"
	if "products" in keys:
		products = inputCompany["products"]
	elif "items" in keys:
		products = inputCompany["items"]
	elif "product_list" in keys:
		products = inputCompany["product_list"]
	company["products"] =  products

	# Lots of duplication here, can I add function?

	# Dedupe by company name
	companies[company["name"]] = company

print(companies)

## Score

## Export