from __future__ import absolute_import, division, print_function
import os
import click
from flask import render_template
from flask.cli import with_appcontext
from flask_mail import Mail, Message

@click.command('template-test')
@click.argument('templatename')
@click.option('-d', '--data', 'dataFile', help="data file must set a template_data object to be given to the template. $TEMPLATE_DATA_FILE or cwd()/templates/test_data.py")
@click.option('-e', '--email', help="test recipient email. $TEMPLATE_EMAIL")
@with_appcontext
def test_template(templatename, dataFile, email):
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    mail = Mail(app)

    # data file directory or default to a data.py file
    dataFile = dataFile or os.getenv('TEMPLATE_DATA_FILE') or os.path.join(os.getcwd(), 'templates', 'test_data.py')
    email = email or os.getenv('TEMPLATE_EMAIL')
    if not email:
        raise "Email not provided to template tester. Pass -e or use TEMPLATE_EMAIL environment variable"

    # expect dataFile to define `template_data` variable with our template data
    # because this exec is within a function, variables defined here are in locals()
    with open(dataFile) as reader:
        exec(reader.read())

    template = render_template(templatename, **locals().get('template_data', {}))
    msg = Message('Template test', recipients=[email], html=template)
    mail.send(msg)
