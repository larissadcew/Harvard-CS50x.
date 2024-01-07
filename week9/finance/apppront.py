import os
import json
from sqlalchemy import create_engine, MetaData, Table

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import pytz
import sqlite3
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash



from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Attempts to convert the input string to an integer.
def try_perse_int(sting_value):
    try:
        int_value = int(sting_value)
        return int_value
    except ValueError:
        return None

# checking if and an integer
def is_integer(value):
    try:
        int_value = int(value)
        return True
    except ValueError:
        return False

def get_cash(user_id):
    cash = db.execute("SELECT cash FROM users WHERE id = ?",user_id)[0]["cash"]
    if cash is None:
        print("Not is posible ckeck the cash user")
    else:
        return cash

def convert_time_NY():
    pass

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # Selecting all stocks information
    stocks = db.execute("SELECT symbol,name,price, SUM(shares) as totalSheres FROM transactions WHERE user_id = ? GROUP BY symbol",user_id)

    # Money available to the user
    cash = get_cash(user_id)

    total = cash

    # calculated on total money that a stock
    for stock in stocks:
        total =+ stock["price"] * stock["totalSheres"]

    return render_template("index.html",stocks=stocks,cash=cash,usd=usd,total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        # picking up how many shares and how much
        symbol = request.form.get("symbol").upper()

        # checking if the symbol exists
        stock_info = lookup(symbol)

        if not stock_info:
            return apology("Invalid symbol",400)

        # checking if the user has chosen a symbol
        if not symbol:
            return apology("Pleas inter a symbol!",400)

        # checking if symbol and an integer
        symbol_valid = is_integer(symbol)

        if symbol_valid:
            return apology("Not be number",400)

        # trying to convert the selected amount
        sheres_a = try_perse_int(request.form.get("shares"))

        # shares se for less than zero
        if sheres_a is None or sheres_a <= 0:
            return apology("Shares must be a positive integer!", 400)

        # converting hoary
        time = datetime.now()
        time_usa = pytz.timezone('America/New_York')
        time_now = time.astimezone(time_usa)

        user_id = session["user_id"]

        # taking all the money in the user's box
        cash =  get_cash(user_id)

        # taking stock information in lookup
        stock_info_name = stock_info["name"]
        stock_info_price = stock_info["price"]
        stock_total_price = stock_info_price * sheres_a

        # if the user has less money than the total
        if cash < stock_total_price:
            return apology("Not enough cash!",400)
        else:
            # Corrected the UPDATE statement
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - stock_total_price, user_id)
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", user_id, stock_info_name, sheres_a , stock_info_price, 'buy', symbol)

        return redirect("/")

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]

    transaction = db.execute("SELECT type,symbol,price,shares,time FROM transactions WHERE user_id = ?",user_id)

    return render_template("history.html",transactions=transaction,usd=usd)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":

        # taking the symbol input
        symbol = request.form.get("symbol")

        # Getting quotes using lookup function
        quotes = lookup(symbol)

         # checking if the input is empty
        if not symbol:
            return apology("please enter a valid symbol", 400)

        # checking if the function returns nothing
        if quotes is None:
            return apology("This symbol does not exist!", 400)

        # taking price and dictionary symbol
        quote_prices = quotes["price"]
        quote_symbol = quotes["symbol"]

        return render_template("values.html", quote_prices=quote_prices,quote_name=quote_symbol,usd_function=usd)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("/register.html")

    elif request.method == "POST":
        # Taking the form inputs
        name = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # Checking if any of the entries are blank
        if not name or not password or not confirm:
            return apology("blank space!", 400)


        # if the passwords are not the same
        if password != confirm:
            return apology("passwords are not the same!", 400)

        hash_value = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users(username,hash) VALUES (?,?)",name,hash_value)
            return redirect("/")
        except:
            return apology("Username has already been registerd!",400)

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        user_id = session["user_id"]

        symbol = request.form.get("symbol")
        sheres = try_perse_int(request.form.get("shares"))

        if sheres is None or sheres <= 0:
            return apology("sheres most be a positive number",400)

        price_item = lookup(symbol)["price"]
        name_item = lookup(symbol)["name"]
        price = sheres * price_item


        sheres_owned = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",user_id,symbol)[0]["shares"]
        if sheres_owned < sheres:
            return apology("You don't have enougth sheres!",400)


        current_cash = get_cash(user_id)
        db.execute("UPDATE users SET cash = ? WHERE id = ?",current_cash + price,user_id)
        db.execute("INSERT INTO transactions (user_id,name,shares,price,type,symbol) VALUES(?,?,?,?,?,?)",user_id,name_item,-sheres,price_item,"sell",symbol)
        return redirect("/")
    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol",user_id)
        return render_template("sell.html",symbols=symbols)