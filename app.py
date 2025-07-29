from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Replace this with your actual API key from exchangerate-api
API_KEY = "ebf6804c32dc16f376e25cad"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Save to users.txt file
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # If no users file exists yet
        if not os.path.exists('users.txt'):
            return "<h1>No users found. Please sign up first.</h1><br><a href='/signup'>Sign Up</a>"

        with open('users.txt', 'r') as file:
            for line in file:
                stored_user, stored_pass = line.strip().split(',')
                if stored_user == username and stored_pass == password:
                    return redirect(url_for('convert'))
        return "<h1>Invalid credentials</h1><br><a href='/login'>Try again</a>"
    
    return render_template('login.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    currency_list = ['USD', 'NGN', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'ZAR', 'KES', 'GHS']

    result = None
    from_currency = to_currency = amount = ''
    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
        response = requests.get(url)
        data = response.json()

        if data['result'] == 'success':
            result = data['conversion_result']
        else:
            result = "Error fetching conversion."

    return render_template('convert.html', result=result, currency_list=currency_list,
                           from_currency=from_currency, to_currency=to_currency, amount=amount)

if __name__ == '__main__':
    app.run(debug=True)

