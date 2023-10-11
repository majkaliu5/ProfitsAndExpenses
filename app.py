from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from helpers import login_required, usd

# configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Custom filter
app.jinja_env.filters["usd"] = usd

@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # if request is GET
    if request.method == "GET":
            # display register.html
            return render_template("register.html")

    # if request is POST
    if request.method == "POST":
        # insert user info
        db.execute(
            "INSERT INTO users (name, hash) VALUES (?, ?)",
            request.form.get("name"),
            generate_password_hash(request.form.get("password"), "pbkdf2", 15)
        )

        # display login page
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # if request is get
    if request.method == "GET":
        #display login page
        return render_template("login.html")

    # if request is post
    if request.method == "POST":
        # get user id
        user_id = db.execute("SELECT id FROM users WHERE name = (?)",
                request.form.get("name")
        )

        # Remember which user has logged in
        session["user_id"] = user_id[0]["id"]

        # show home
        return redirect("/")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # if request is get
    if request.method == "GET":
        # get date
        date = db.execute("SELECT CURRENT_DATE")

        # get the profits of the current date
        profits = db.execute("SELECT * FROM history WHERE history = (?) AND date = (?) AND id = (?)",
                "profit",
                date[0]["CURRENT_DATE"],
                session["user_id"]
        )

        # get total of profits
        totalProfits = 0

        # go through every row of profits
        for row in profits:
            # in each row get the product's price
            totalProfits += row["price"] * row["quantity"]

        # get the expenses of the current date
        expenses = db.execute("SELECT * FROM history WHERE history = (?) AND date = (?) AND id = (?)",
                 "expense",
                 date[0]["CURRENT_DATE"],
                 session["user_id"]
        )

        # get total of expenses
        totalExpenses = 0

        # go through every row of profits
        for row in expenses:
            # in each row get the product's price
            totalExpenses += row["price"] * row["quantity"]

        # get all daily history
        history = db.execute("SELECT * FROM history WHERE date = (?) AND id = (?)",
                date[0]["CURRENT_DATE"],
                session["user_id"]
        )

        # display homepage
        return render_template("index.html", totalProfits=totalProfits, totalExpenses=totalExpenses, history=history);

    # if request is post
    if request.method == "POST":

         # get current date
         date = db.execute("SELECT CURRENT_DATE")

         # get current week
         week = db.execute("SELECT strftime('%W','now') AS Week")

         weekValue = week[0]["Week"]

         # get current month
         month = db.execute("SELECT strftime('%m','now') AS Month")

         monthValue = month[0]["Month"]

         # get current year
         year = db.execute("SELECT strftime('%Y','now') AS Year")

         yearValue = year[0]["Year"]

         # get the input from the dropdown list
         display = request.form.get("display")

         # if display is day
         if display == "day":

              # get the profits of the current date
              profits = db.execute("SELECT * FROM history WHERE history = (?) AND date = (?) AND id = (?)",
                      "profit",
                      date[0]["CURRENT_DATE"],
                      session["user_id"]
              )

              # get total of profits
              totalProfits = 0

              # go through every row of profits
              for row in profits:
                # in each row get the product's price
                totalProfits += row["price"] * row["quantity"]

              # get the expenses of the current date
              expenses = db.execute("SELECT * FROM history WHERE history = (?) AND date = (?) AND id = (?)",
                       "expense",
                       date[0]["CURRENT_DATE"],
                       session["user_id"]
              )

              # get total of expenses
              totalExpenses = 0

              # go through every row of expenses
              for row in expenses:
                # in each row get the product's price
                totalExpenses += row["price"] * row["quantity"]

              # get all daily history
              history = db.execute("SELECT * FROM history WHERE date = (?) AND id = (?)",
                      date[0]["CURRENT_DATE"],
                      session["user_id"]
              )

              return render_template("index.html", history=history, totalProfits=totalProfits, totalExpenses=totalExpenses)

         # if display is week
         if display == "week":

             # get profits of current week
             weeklyProfits = db.execute("SELECT * FROM history WHERE history = (?) AND week = (?) AND id = (?)",
                           "profit",
                           weekValue,
                           session["user_id"],
             )

             # get total of weeklyProfits
             totalWeeklyProfits = 0

             # go through every row of profits
             for row in weeklyProfits:
                # in each row get the product's price
                totalWeeklyProfits += row["price"] * row["quantity"]

             # get expenses of current week
             weeklyExpenses = db.execute("SELECT * FROM history WHERE history = (?) AND week = (?) AND id = (?)",
                            "expense",
                            weekValue,
                            session["user_id"],
             )

             # get total of weeklyExpenses
             totalWeeklyExpenses = 0

             # go through every row of profits
             for row in weeklyExpenses:
                # in each row get the product's price
                totalWeeklyExpenses += row["price"] * row["quantity"]

             # get all weekly history
             history = db.execute("SELECT * FROM history WHERE week = (?) AND id = (?)",
                     weekValue,
                     session["user_id"]
             )

             # display index with week display
             return render_template("index.html", totalProfits=totalWeeklyProfits, totalExpenses=totalWeeklyExpenses, history=history)

         # if user chose month
         if display == "month":

             # get profits of current month
             monthlyProfits = db.execute("SELECT * FROM history WHERE history = (?) AND month = (?) AND id = (?)",
                           "profit",
                           monthValue,
                           session["user_id"],
             )

             # get total of monthlyProfits
             totalMonthlyProfits = 0

             # go through every row of profits
             for row in monthlyProfits:
                # in each row get the product's total price
                totalMonthlyProfits += row["price"] * row["quantity"]

             # get expenses of current month
             monthlyExpenses = db.execute("SELECT * FROM history WHERE history = (?) AND month = (?) AND id = (?)",
                            "expense",
                            monthValue,
                            session["user_id"],
             )

             # get total of monthlyExpenses
             totalMonthlyExpenses = 0

             # go through every row of expenses
             for row in monthlyExpenses:
                # in each row get the product's total price
                totalMonthlyExpenses += row["price"] * row["quantity"]

             # get all monthly history
             history = db.execute("SELECT * FROM history WHERE month = (?) AND id = (?)",
                     monthValue,
                     session["user_id"]
             )

             # display index with month display
             return render_template("index.html", totalProfits=totalMonthlyProfits, totalExpenses=totalMonthlyExpenses, history=history)

         # if user chose year
         if display == "year":

            # get profits of current year
            yearlyProfits = db.execute("SELECT * FROM history WHERE history = (?) AND year = (?) AND id = (?)",
                           "profit",
                           yearValue,
                           session["user_id"],
            )

            # get total of year profits
            totalYearlyProfits = 0

            # go through every row of profits
            for row in yearlyProfits:
                # in each row get the product's total price
                totalYearlyProfits += row["price"] * row["quantity"]

            # get expenses of current year
            yearlyExpenses = db.execute("SELECT * FROM history WHERE history = (?) AND year = (?) AND id = (?)",
                            "expense",
                            yearValue,
                            session["user_id"],
            )

            # get total of yearlyExpenses
            totalYearlyExpenses = 0

            # go through every row of expenses
            for row in yearlyExpenses:
                # in each row get the product's total price
                totalYearlyExpenses += row["price"] * row["quantity"]

            # get all monthly history
            history = db.execute("SELECT * FROM history WHERE year = (?) AND id = (?)",
                    yearValue,
                    session["user_id"]
            )

            # display index with month display
            return render_template("index.html", totalProfits=totalYearlyProfits, totalExpenses=totalYearlyExpenses, history=history)

@app.route("/profit", methods=["GET", "POST"])
@login_required
def profit():
    # if get
    if request.method == "GET":

        # get current date
        date = db.execute("SELECT CURRENT_DATE")

        # get the profits of the current date
        profits = db.execute("SELECT * FROM history WHERE history = (?) AND date = (?) AND id = (?)",
                "profit",
                date[0]["CURRENT_DATE"],
                session["user_id"]
        )

        # get total of profits
        totalProfits = 0
        # go through every row of profits
        for row in profits:
            # in each row get the product's price
            totalProfits += row["price"] * row["quantity"]

        # display profit.html
        return render_template("profit.html", profits=profits, totalProfits=totalProfits, date=date)

    # if post
    if request.method == "POST":

        # get current date
        date = db.execute("SELECT CURRENT_DATE")

        # get current week
        week = db.execute("SELECT strftime('%W','now') AS Week")

        weekValue = week[0]["Week"]

        # get current month
        month = db.execute("SELECT strftime('%m','now') AS Month")

        monthValue = month[0]["Month"]

        # get current year
        year = db.execute("SELECT strftime('%Y','now') AS Year")

        yearValue = year[0]["Year"]

        # store info in history table
        db.execute("INSERT INTO history (id, product, quantity, price, history, date, week, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"],
                   request.form.get("product"),
                   request.form.get("quantity"),
                   request.form.get("price"),
                   "profit",
                   date[0]["CURRENT_DATE"],
                   weekValue,
                   monthValue,
                   yearValue,
        )

        # return back to profit page
        return redirect("/profit")

@app.route("/expense", methods=["GET", "POST"])
def expense():
    # if get
    if request.method == "GET":

            # get current date
            date = db.execute("SELECT CURRENT_DATE")

            # get the expenses of the current date
            expenses = db.execute("SELECT * FROM history WHERE history = (?) AND date = (?) AND id = (?)",
                    "expense",
                    date[0]["CURRENT_DATE"],
                    session["user_id"]
            )

            # get total of expenses
            totalExpenses = 0

            # go through every row of profits
            for row in expenses:
                # in each row get the product's price
                totalExpenses += row["price"] * row["quantity"]

            # display expense.html
            return render_template("expense.html", date=date, expenses=expenses, totalExpenses=totalExpenses)

    # if post
    if request.method == "POST":
        # get date
        date = db.execute("SELECT CURRENT_DATE")

        # get week
        week = db.execute("SELECT strftime('%W','now') AS Week")

        weekValue = week[0]["Week"]

        # get month
        month = db.execute("SELECT strftime('%m','now') AS Month")

        monthValue = month[0]["Month"]

        # get current year
        year = db.execute("SELECT strftime('%Y','now') AS Year")

        yearValue = year[0]["Year"]

        # store info in history table
        db.execute("INSERT INTO history (id, product, quantity, price, history, date, week, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"],
                   request.form.get("product"),
                   request.form.get("quantity"),
                   request.form.get("price"),
                   "expense",
                   date[0]["CURRENT_DATE"],
                   weekValue,
                   monthValue,
                   yearValue,
        )

        # return back to expense.html
        return redirect("/expense")

@app.route("/history", methods=["GET"])
@login_required
def history():
    # if get
    if request.method == "GET":
        # pass history table
        history = db.execute("SELECT * FROM history WHERE id = (?)",
                session["user_id"]
        )

        # display history.html
        return render_template("history.html", history=history)

@app.route("/logout")
def logout():
    # clear id
    session.clear()

    #go back to index
    return redirect("/")













