from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "secret123"   # session key

ADMIN_PASSWORD = "1234"        # yaha apna password set karo

user_data = {}
results = {}

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        crush = request.form['crush']
        user_data[name] = crush
        return redirect(f"/waiting/{name}")
    return render_template("index.html")

@app.route('/waiting/<name>')
def waiting(name):
    return render_template("waiting.html", name=name)

@app.route('/result/<name>')
def result(name):
    percent = results.get(name, "Pending")
    return render_template("result.html",percent=percent)

# ---------- ADMIN LOGIN ----------
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
    return """
    <h2>Admin Login</h2>
    <form method='post'>
        Password: <input name='password' type='password'>
        <button>Login</button>
    </form>
    """

# ---------- ADMIN PANEL ----------
@app.route('/admin', methods=['GET','POST'])
def admin():
    if not session.get('admin'):
        return redirect('/admin_login')

    if request.method == 'POST':
        name = request.form['name']
        percent = request.form['percent']
        results[name] = percent

    return render_template("admin.html", users=user_data)


@app.route('/get_users')
def get_users():
    return jsonify(user_data)

@app.route('/check_result/<name>')
def check_result(name):
    return results.get(name, "Pending")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)