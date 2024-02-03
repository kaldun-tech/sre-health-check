# sre-health-check
Script reads REST endpoints from YAML file, queries them repeatedly, computes and reports the percent uptime for domain.

An endpoint is considered UP if response is 200-299 and latency is less than 500 milliseconds.

#### Install dependencies
pip install -r requirements.txt

#### Run main script
python main.py

Exit with CTRL + C

#### Run test cases
python -m unittest testcase.test_availability

python -m unittest testcase.test_endpoint_reader

python -m unittest testcase.test_http_requests

#### Run pylint

pylint --fail-under 9 **/*.py

#### TODO list:

Confirm code accurately determines uptime of endpoints
