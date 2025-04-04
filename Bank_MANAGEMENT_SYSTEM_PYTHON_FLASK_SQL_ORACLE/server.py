    

from flask import Flask, render_template, request, redirect, url_for
import cx_Oracle

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = cx_Oracle.connect("system/1123@localhost")
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():  # it means on createaccount post or get request, this craeteaccount() will get run..
     conn = get_db_connection()
     curr = conn.cursor()
     curr.execute("SELECT COUNT(*) FROM Account")  
     count = curr.fetchone()[0]  # Get total accounts
     account_no = "SBI" + str(count + 1)  # Generate next account number

     if request.method == 'POST':
       
        
        name = request.form['name']  # getting the value from "form" in html,,and also note that method =POST and action is /submit ie, with subit clicking this will get executed..
        balance = int(request.form['balance'])
        pin = request.form['pin']
        acc_type = request.form['acc_type']
        
        # Fetch the current number of accounts
      
        # Insert the new account into the database
        curr.execute("Insert into Account (account_no, name, balance, pin, type) values(:1, :2, :3, :4, :5)",
                     (account_no, name, balance, pin, acc_type))
        conn.commit()
        
        curr.close()
        conn.close()
      
        return redirect(url_for('home'))  ## Redirect to the home page after processing
   
     return render_template('create_account.html',account_no=account_no)  ##if some fault is there then the webpage will be still in he createaccount page ..


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        conn = get_db_connection()
        curr = conn.cursor()

        acno = request.form['acno']
        pin = request.form['pin']
        money = int(request.form['money'])

        # Validate account number and pin
        curr.execute("Select * from Account where account_no=:1 and pin=:2", (acno, pin))
        if curr.fetchone():
            curr.execute("Update Account set balance=balance+:1 where account_no=:2", (money, acno))
            conn.commit()
            message = "Money deposited successfully."
        else:
            message = "Invalid account number or pin."

        curr.close()
        conn.close()

        return render_template('deposit.html', message=message)# will be rendered when post request..
    
    return render_template('deposit.html')# will be rendered when get request..

@app.route('/withdraw', methods=['GET', 'POST'])  #  both get and post because we want to render the html elements first..
def withdraw():
    if request.method == 'POST':
        conn = get_db_connection()
        curr = conn.cursor()

        acno = request.form['acno']
        pin = request.form['pin']
        money = int(request.form['money'])

        # Validate account number and pin
        curr.execute("Select * from Account where account_no=:1 and pin=:2", (acno, pin))
        x = curr.fetchone()
        if x:
            bal_original = x[2]
            if bal_original >= money:
                curr.execute("Update Account set balance=balance-:1 where account_no=:2", (money, acno))
                conn.commit()
                message = "Money withdrawn successfully."
            else:
                message = "Insufficient funds."
        else:
            message = "Invalid account number or pin."

        curr.close()
        conn.close()

        return render_template('withdraw.html', message=message)

    return render_template('withdraw.html')

@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        conn = get_db_connection()
        curr = conn.cursor()

        acno = request.form['acno']
        pin = request.form['pin']

        # Validate account number and pin
        curr.execute("Select * from Account where account_no=:1 and pin=:2", (acno, pin))
        x = curr.fetchone()
        if x:
            account_details = {
                'account_no': x[0],
                'name': x[1],
                'balance': x[2],
                'type': x[4]
            }
        else:
            account_details = None

        curr.close()
        conn.close()

        return render_template('display.html', account_details=account_details)

    return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)
