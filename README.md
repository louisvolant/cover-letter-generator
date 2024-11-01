# cover-letter-generator
Generate a cover-letter from a CV, a job opening and some sample of cover letter that you've produced in the past.

## Requirements

1. First install the required packages

Python3

````
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
# When finished, desactivate the venv using "deactivate"
````

2. You need to have an OpenAI Api Key

````
export OPENAI_API_KEY='your-api-key'
````

## How to execute

You run it like the following

````
$ python3 main.py -cv mon_cv.tex -of job-opening-position.txt -cl Lettre-de-Motivation-Entreprise-A.txt Lettre-de-Motivation-Entreprise-B.txt
````
