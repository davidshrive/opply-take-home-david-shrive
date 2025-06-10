import json
import csv

## Load file
with open('input/processed_buyer_leads.json', 'r') as inputFile:
	inputData = json.load(inputFile)

## Normalise 
def find_value(company, possible_keys):
	for key in possible_keys:
		if key in company.keys():
			return company[key]
	return "unknown"

companies = {}

for inputCompany in inputData:
	company = {}
	company['name'] 			= find_value(inputCompany, ['company_name', 'company', 'name'])
	company['description'] 		= find_value(inputCompany, ['info', 'desc', 'description'])
	company['labels'] 			= list(map(lambda label:label.strip(), find_value(inputCompany, ['labels', 'keywords', 'tags']).split(";")))
	company['website'] 			= find_value(inputCompany, ['website', 'site', 'url'])
	company['products'] 		= find_value(inputCompany, ['products', 'product_list', 'items'])

	# Dedupe by company name, if multiple found labels & products are merged.
	# Can cause issues with duplicate products
	if company['name'] not in companies.keys():
		companies[company['name']] = company
	else:
		companies[company['name']]["labels"].extend(company["labels"])
		companies[company['name']]["products"].extend(company["products"])

## Score
def calc_score(company, labels):
	score = 0
	## Check labels, +10 for each
	for label in labels:
		if label in company['labels']:
			score += 10

	## Check ingredients, +5 for each
	for product in company['products']:
		if "ingredients" in product.keys():
			for ingredient in product["ingredients"]:
				if ingredient in label:
					score += 5
	return score

# These are the values we are looking for to increase a companies score
labels = ['corn-starch','corn starch']

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
