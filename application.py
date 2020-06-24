from flask import Flask, request, redirect, render_template, url_for, flash, send_file, abort
from helpers import lookup, lookup_year_end, IncomeStatement, BalanceSheet
import csv

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
    else:
        return render_template("User_Selection.html")


IS_record_row = []
BS_record_row = []


@app.route('/SelectStatements/<symbol>', methods = ["GET", "POST"])
def SelectStatements(symbol):
    year_end_list = lookup_year_end(symbol)
    print("year_end_list: ")
    print(year_end_list)
    
    if request.method == "POST":
        #Managing users who have submitted an empty form
        IS_list = request.form.getlist('IS_year(s)_selected')
        BS_list = request.form.getlist('BS_year(s)_selected')
        if len(IS_list) == 0 and len(BS_list) == 0:
            flash_message = """You need to select at least one year end date to download to use this FS tool!"""
            flash(flash_message)
            return render_template("Select_Statements.html", list = year_end_list, size = len(year_end_list), symbol=f"{symbol}")
        
        #Generating IS_years_selected list so that it can be used in the generation of the user's requested years
        IS_years_selected = []
        for i in range(len(year_end_list)):
            if year_end_list[i] in IS_list:
                IS_years_selected.append(i)
        print("IS_years_selected: ")
        print(IS_years_selected)
        
        if len(IS_list) != 0:
            global IS_record_row
            IS_record_row = IncomeStatement(symbol,IS_years_selected)

        print("IS_record_row: ")
        print(IS_record_row)

        #Generating BS_years_selected list so that it can be used in the generation of the user's requested years        
        BS_years_selected = []
        for i in range(len(year_end_list)):
            if year_end_list[i] in BS_list:
                BS_years_selected.append(i)
        print("BS_years_selected: ")
        print(BS_years_selected)

        if len(BS_list) != 0:
            global BS_record_row
            BS_record_row = BalanceSheet(symbol,BS_years_selected)

        
        print("BS_record_row: ")
        print(BS_record_row)

        return redirect('/download_results')       
            
    else:
        return render_template("Select_Statements.html", list = year_end_list, size = len(year_end_list), symbol=f"{symbol}")
    

@app.route('/download_results', methods = ["GET", "POST"])
def download_results():
    
    if request.method == "POST":
        if request.form.get('Income Statement'):
            with open("Income_Statement.csv", "w", newline="") as csv_file_1:
                IS_writer = csv.writer(csv_file_1)
                IS_writer.writerow([f'Please find the Income Statement for your selected fiscal year ends'])
                for row in IS_record_row:
                    IS_writer.writerow(row)
            try:
                return send_file("Income_Statement.csv",  as_attachment=True)
            except FileNotFoundError:
                abort(404)
                
        if request.form.get('Balance Sheet'):
            with open("Balance_Sheet.csv", "w", newline="") as csv_file_2:
                BS_writer = csv.writer(csv_file_2)
                BS_writer.writerow([f'Please find the Balance Sheet for your selected fiscal year ends'])
                for row in BS_record_row:
                    BS_writer.writerow(row)
            try:
                return send_file("Balance_Sheet.csv",  as_attachment=True)
            except FileNotFoundError:
                abort(404)
                
        return redirect(url_for('download_results', symbol=symbol, IS_record_row=IS_record_row, BS_record_row=BS_record_row))
    else:
        return render_template("download_results.html")
        

        
