# Flask Mail Template Tester
This package provides a faster way to inject data into flask mail templates and send them to a recipient for testing.

# Setup
- `pip install flask-mail-template-tester`
- `pip freeze > requirements.txt`

### using environment variables (recommended)
- `export TEMPLATE_DATA_FILE="path/to/some/data.py"`
	- note: the default data file is set to look at the current working directory + /templates/test_data.py. This is meant to allow you to write a script to test all your templates with one central and standard set of data.
- `export TEMPLATE_EMAIL="my-email@gmail.com"`
- `flask template-test name-of-template.html`

### using cli arguments
- `flask template-test name-of-template.html -d "path/to/some/data.py" -e "my-email@gmail.com"`
