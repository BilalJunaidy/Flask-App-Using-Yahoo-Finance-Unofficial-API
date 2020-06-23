from flask import Flask, request, redirect, render_template, url_for, flash
from helpers import lookup, lookup_year_end

app = Flask(__name__)

app.config["SECRET_KEY"] = 'this is a secret key'
app.config["TEMPLATE_AUTO_UPLOAD"] = True

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        symbol = request.form.get('symbol')
        data = lookup(symbol)
        if data is None:
            flash(f'You entered {request.form.get("symbol")}. Based on data extraction, no such ticker exists. Please double check the symbol and submit the form again. Thank you')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('SelectStatements', symbol=symbol))
##    if request.method == "GET":
    else:
        return render_template("User_Selection.html")

@app.route('/SelectStatements/<symbol>', methods = ["GET", "POST"])
def SelectStatements(symbol):
    if request.method == "POST":
        data_list = request.form.getlist('year(s)_selected')
        print(data_list)
        print("hold")
        data = request.form
        print(data)
        print(type(data))
        print("hold")
        data0 = request.form.get('option0')
        print(data0)
        

        print("hold")
        data1 = request.form.get('option1')
        print(data1)

        print("hold")
        data2 = request.form.get('option2')
        print(data2)

        print("hold")
        data3 = request.form.get('option3')
        print(data3)
        
##        data = request.form.get("yearends")
##        print(type(data))
##        print(data)
####        dict_data = data.values()
####        for v in dict_data:
####            print(v)
####        print("")
####        print(dict_data)
##        print(len(data))
        
        return render_template("todelete.html")
    else:
        year_end_list = lookup_year_end(symbol)
        return render_template("Select_Statements.html", list = year_end_list, size = len(year_end_list), symbol=f"{symbol}")
    
        
        
        

        
