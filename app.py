from flask import Flask, render_template, request, url_for, redirect, flash, render_template_string

app = Flask(__name__)


@app.route('/')
def fun():
    return render_template("index.html")


@app.route('/ten-minute-pitch')
def pitch():
    title = "Ten Minute Pitch: Write a Query Letter"

    return render_template('pitch.html', title=title)


@app.route('/invitation')
def invite():
    title = "Huge Impossible Word Search"

    return render_template('invite.html', title=title)



if __name__ == '__main__':
    app.run(debug=False)
