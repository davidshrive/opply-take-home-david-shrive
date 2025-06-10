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
	labels = list(map(lambda label:label.strip(), labels.split(";")))
	company["labels"] = labels

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

	# Dedupe by company name, if multiple found labels & products are merged.
	# Can cause issues with duplicate products
	if name not in companies.keys():
		companies[name] = company
	else:
		companies[name]["labels"].extend(labels)
		companies[name]["products"].extend(products)

## Score
for companyName in companies:

	score = 0
	## Check labels, +10 for each
	labels = ['corn-starch', 'corn starch']
	for label in labels:
		if label in companies[companyName]['labels']:
			score += 10

	## Check ingredients, +5 for each
	for product in companies[companyName]['products']:
		if "ingredients" in product.keys():
			for ingredient in product["ingredients"]:
				if ingredient in label:
					score += 5
	companies[companyName]['score'] = score

## Export