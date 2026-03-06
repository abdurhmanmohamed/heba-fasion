from flask import Flask
from flask import render_template, url_for, redirect, request
app= Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/shoping')
def shop():
    return render_template('shop.html')

@app.route('/shoping-cart')
def shoping_cart():
    return render_template('shoping-cart.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/checkout')
def check_out():
    return render_template('checkout.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

