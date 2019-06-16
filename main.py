from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["POST", "GET"])
def validate_form():
    if request.method == "POST":
        name = request.form["user_name"]
        pswd = request.form["password"]
        pswd_chk = request.form["ver_pass"]
        email = request.form['email']
        tested = validate_check(name, pswd, pswd_chk, email)

        if tested[0]:
            return render_template("welcome.html", name=name)
        else:
            return render_template("index.html", user_name=name, email=email, 
                                    name_error=tested[1], pass_error=tested[2],
                                    ver_pass_error=tested[3], email_error=tested[4])

    return render_template("index.html")


def validate_check(name, pswd, pswd_chk, email):
    error = "* Invalid "
    user_error = ""
    pswd_error = ""
    pswd_chk_error = ""
    mail_error = ""
    valid = True

    if not validate_name_pass(name):
        user_error = error + "username"
        valid = False
    if not validate_name_pass(pswd):
        pswd_error = error + "password"
        valid = False
    if pswd != pswd_chk:
        pswd_chk_error = "* Passwords do not match"
        valid = False
    if not validate_email(email):
        mail_error = error + "email"
        valid = False
        
    return [valid, user_error, pswd_error, pswd_chk_error, mail_error]


def validate_name_pass(name_pass):
    if len(name_pass) < 3 or len(name_pass) > 20 or name_pass.count(" ") != 0:
        return False
    else:
        return True


def validate_email(email):
    if len(email) == 0:
        return True
    else:
        if len(email) < 3 or len(email) > 20:
            return False
        else:
            if email.count(" ") == 0 and email.count(".") == 1 and email.count("@") == 1:
                return True
            else:
                return False


app.run()