# imports
from flask import Flask, render_template, redirect, request
import re

# create app var
app = Flask(__name__)
app.config['DEBUG'] = True

# create view for sign up page
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():

    # pull err_msg vars, fields to be preserved from query parameters on
    # redirect from /welcome
    user_err_msg = request.args.get('user_err')
    email_err_msg = request.args.get('email_err')
    pass_err_msg = request.args.get('pass_err')
    username = request.args.get('username')
    email = request.args.get('email')

    # if no username or email, don't pass them as vars to sign up template
    # (i.e., create initial, blank sign up form)
    if username == None and email == None:
        return render_template('sign-up.html', user_err=user_err_msg,
            email_err=email_err_msg, pass_err=pass_err_msg)

    # else, keep the username and email entered in first attempt and pass to
    # sign up template (i.e., create second attempt form after errors)
    return render_template('sign-up.html', user_err=user_err_msg,
        email_err=email_err_msg, pass_err=pass_err_msg, username=username,
        email=email)

# process/validate form data from sign up, render welcome page or redirect
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():

    # pull data from form for validation
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    # initiaulize err_msg vars so later test for errs works (no use before
    # assignment error)
    user_err_msg = ''
    email_err_msg = ''
    pass_err_msg = ''

    # username validation using regexs (where sensible)
    if not re.search(r"\S", username):
        user_err_msg = "Username is required."

    elif len(username) < 3 or len(username) > 20:
        user_err_msg = "Usernames must 3--20 characters long."

    elif re.search(r"\s", username):
        user_err_msg = "Usernames cannot contain a space."

    # password validation using regexs (where sensible)
    if not re.search(r"\S", password):
        pass_err_msg = "Password is required."

    elif 3 > len(password) or len(password) > 20:
        pass_err_msg = "Passwords must be 3--20 characters long."

    elif re.search(r"\s", password):
        pass_err_msg = "Passwords cannot contain a space."

    elif password != password2:
        pass_err_msg = "Passwords don't match."

    elif not re.search(r"\S", password2):
        pass_err_msg = "Password must be confirmed."

    # email validation using regexs (where sensible)
    if re.search(r"\S", email):

        if not re.search(r".*@.*\..*", email):
            email_err_msg = 'Email format invalid (must be "____@___.___" format).'

        elif 3 > len(email) or len(email) > 20:
            email_err_msg = "Email must be 3--20 characters long."

    # if no errors, render welcome template
    if user_err_msg == '' and email_err_msg == '' and pass_err_msg == '':
        return render_template('welcome.html', user=username)

    # if errors, reroute back to sign up with relevant error msgs
    else:
        return redirect('''/sign-up?user_err={0}
        &email_err={1}&pass_err={2}&username={3}&email={4}'''.format(
        user_err_msg, email_err_msg, pass_err_msg, username, email))

if __name__ == "__main__":
    app.run()
