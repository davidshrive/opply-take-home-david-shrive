import json
import csv

## Functions
def find_value(company, possible_keys, default_value="unknown"):
	for key in possible_keys:
		if key in company.keys():
			return company[key]
	return default_value

def normalise_company(inputCompany):
	company = {}
	company['name'] 		= find_value(inputCompany, ['company_name', 'company', 'name'])
	company['description'] 	= find_value(inputCompany, ['info', 'desc', 'description'])
	company['labels'] 		= list(map(lambda label:label.strip(), find_value(inputCompany, ['labels', 'keywords', 'tags']).split(";")))
	company['website'] 		= find_value(inputCompany, ['website', 'site', 'url'])
	company['products'] 	= normalise_products(find_value(inputCompany, ['products', 'product_list', 'items'], []))
	return company

def normalise_products(products):
	output = {}
	for product in products:
		output[product["name"]] = find_value(product,['ingredients'],['unknown'])
	return output

def merge_companies(companyA, companyB):
	# Merge and dedupe labels
	if "labels" in companyA.keys():
		companyA["labels"].extend(companyB["labels"])
		companyA["labels"] = list(set(companyA["labels"]))

	# Merge product ingredients and dedupe
	for product in companyB["products"]:
		companyA['products'][product].extend(companyB['products'][product])
		companyA['products'][product] = list(set(companyA['products'][product]))

	return companyA

def calc_score(company, labels):
	score = 0
	## Check labels, +10 for each
	if "labels" in company.keys():
		for label in labels:
			if label in company['labels']:
				score += 10

	## Check ingredients, +5 for each
	if "products" in company.keys():
		for product in company['products']:
				for ingredient in company['products'][product]:
					if ingredient in labels:
						score += 5
	
	## Check description, +10 for each
	if "description" in company.keys():
		for label in labels:
			if label in company['description']:
				score += 10

	return score


## Load file
with open('input/processed_buyer_leads.json', 'r') as inputFile:
	inputData = json.load(inputFile)

## Normalise
companies = {}
for inputCompany in inputData:

	company = normalise_company(inputCompany)

	# Dedupe by company name, if already exists companies are merged
	if company['name'] not in companies.keys():
		companies[company['name']] = company
	else:
		companies[company['name']] = merge_companies(companies[company['name']], company)

## Score
# These are the values we are looking for to increase a companies score
labels = ['corn-starch','corn starch','corn','starch']
for companyName in companies:
	companies[companyName]['score'] = calc_score(companies[companyName],labels)

## Export
with open("output/export.csv", "w") as outputFile:
	# Write headers
	writer = csv.DictWriter(outputFile, companies["Company 1"].keys())
	writer.writeheader()

	# Write data
	for companyName in companies:
		writer.writerow(companies[companyName])

	# Bit messy atm, labels and products written as json
