## Opply Take Home Challenge - Part 2

##
This is my python script for the Opply take home challenge, it can be ran via...

`python script.py`

And the tests can be ran via...

`pytest`


It loads the json file located within the input directory, normalises all fields into a consistant format, deduplicates (via merging) any duplicate companies and then applies a basic scoring system using a list of values we are interested in.

* +10pts for each value found in a companies label list
* +5pts for each value found in the ingredient list of a companies products
* +10pts for each value found in the company description

The full list of companies is then exported into the csv file in the output directory.


## Further Improvements
* Make Dynamic - Input json file, output csv file and values used in the scoring system are hardcoded, these could be updated to be arguments, environment variables or config values.
* Extend test suite - I added some basic tests but they are mostly happy path and bugs tend to be around the edge cases so this is definetly any area for improvement.