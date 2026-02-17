from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"   # session key

ADMIN_PASSWORD = "1234"        # yaha apna password set karo

user_data = {}
results = {}

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        first = request.form['first']
        last = request.form['last']
        user_data[name] = (first, last)
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

    users = "".join([f"<li>{u}</li>" for u in user_data])
    return f"""
    <h2>Admin Panel</h2>
    <ul>{users}</ul>
    <form method='post'>
        Name: <input name='name'>
        Percentage: <input name='percent'>
        <button>Submit</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)