from flask import (
    Flask,
    render_template, redirect, url_for,
    flash, request, session
)
import os
from email_verify import VerifyEmail
from Database.user import MyDB
from forms import SignupForm, LoginForm
from Summarization.summary_app import app_summary
from QA.qa_app import app_qa

# Connect the database
db = MyDB()

# Use the Framework
app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_a_secret_key"

app.register_blueprint(app_summary, url_prefix="/summarize")
app.register_blueprint(app_qa, url_prefix="/question_answering")

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of each request."""
    if hasattr(db, 'close_connection'):
        db.close_connection()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        em = form.email.data
        gender = form.gender.data
        dob = form.dob.data
        pw = form.password.data

        v = VerifyEmail()

        if em:  # Ensure the email is not None
            if v.email_verify_smtp(em):
                flash("Email Validated Successfully!", "success")
                response = db.insert_one_data(username, em, gender, dob, pw)
                flash(f"Successfully Registered {form.username.data}, {response}!", "success")
            else:
                flash("Invalid email address!", "error")

            return redirect(url_for("home"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Ensure form is submitted and valid
        em = form.email.data
        pw = form.password.data

        if em:
            if db.search(email=em, password=pw):
                flash("Logged In successfully!", "success")
                # Redirect to the options page after successful login
                return redirect(url_for('select_option'))
            else:
                flash("Email or password is incorrect!", "error")
        else:
            flash("Email is required!", "error")

        return redirect(url_for("home"))

    return render_template("login.html", form=form)

@app.route("/select_option", methods=["GET", "POST"])
def select_option():
    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option == "qa_system":
            return redirect(url_for("app_qa.index"))  # Redirect to QA System
        elif selected_option == "summarization":
            return redirect(url_for("app_summary.index"))  # Redirect to Summarization

    return render_template("select_option.html")


@app.route("/generate_text", methods=["GET", "POST"])
def generate_text():
    if 'history' not in session:
        session['history'] = []

    if request.method == "POST":
        pdf_file = request.files.get('pdf_file')
        input_text = request.form.get('input_text')
        # Here you would generate text and add it to the session history
        generated_text = "Sample Generated Text"  # Replace with actual generation logic
        session['history'].append(generated_text)

    return render_template("generate_text.html", history=session['history'])


if __name__ == "__main__":
    app.run(debug=True,port=7000)
