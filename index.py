from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form


@app.route('/')
def form():
    return render_template('form.html')

# define a route for the action of the form, for example '/usuario/'

if __name__ == "__main__":
    app.run(debug=True)
