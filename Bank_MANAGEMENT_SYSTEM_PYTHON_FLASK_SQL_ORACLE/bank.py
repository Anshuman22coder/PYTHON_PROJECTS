####python codess####

import cx_Oracle
curr = None
conn = None

try:
    conn = cx_Oracle.connect("system/1123@localhost")
    curr = conn.cursor()
    print("Db connection successfully...")
    curr.execute("Select * from Account")
    l = 0
    x = curr.fetchall()
    l = len(x)

    def create_acc():
        account_no = "SBI" + str(l + 1)
        name = input("Enter your name: ")
        balance = int(input("Enter balance: "))
        pin = input("Enter your 4-digit password: ")
        acc_type = input("Enter type of a/c (Savings or Current): ")
        curr.execute("Insert into Account values(:1, :2, :3, :4, :5)",
                     (account_no, name, balance, pin, acc_type))
        print(f"A/C created successfully for {name}, A/C No -> {account_no} with {acc_type} type")
        conn.commit()

    def deposit():
        acno = input("Enter your account no: ")
        pin = input("Enter your pin: ")
        curr.execute("Select * from Account where account_no=:1 and pin=:2", (acno, pin))
        if curr.fetchone():  # Validating account no and pin
            money = int(input("Enter the amount to deposit: "))
            curr.execute("Update Account set balance=balance+:1 where account_no=:2", (money, acno))
            print("Money deposited successfully.")
        else:
            print("Invalid account number or pin.")
        conn.commit()

    def withdraw():
        acno = input("Enter your account no: ")
        pin = input("Enter your pin: ")
        curr.execute("Select * from Account where account_no=:1 and pin=:2", (acno, pin))
        x = curr.fetchone()
        if x:
            bal_original = x[2]
            money = int(input("Enter the amount to withdraw: "))
            if bal_original > money:
                curr.execute("Update Account set balance=balance-:1 where account_no=:2", (money, acno))
                print("Money withdrawn successfully.")
            else:
                print("Insufficient funds.")
        else:
            print("Invalid account number or pin.")
        conn.commit()

    def display():
        acno = input("Enter your account no: ")
        pin = input("Enter your pin: ")
        curr.execute("Select * from Account where account_no=:1 and pin=:2", (acno, pin))
        x = curr.fetchone()
        if x:
            print(f"A/c no-- {x[0]}")
            print(f"Name---- {x[1]}")
            print(f"Balance- {x[2]}")
            print(f"A/C type {x[4]}")
        else:
            print("Invalid account number or pin.")

    # Main menu
    while True:
      print("\n" + "=" * 30)
      print(f"{'Bank Management System':^30}")  # for The text "Bank Management System" is centered within a field of 30 characters.
                                                #Spaces are added on both sides to center the text.
      print("=" * 30)                           #:> use for right and :< for left alignment.. 
      print("1. Create Account")
      print("2. Deposit")
      print("3. Withdraw")
      print("4. Display Account")
      print("5. Exit")
      print("=" * 30)

      choice = input("Enter your choice: ")
      if choice == "1":
          create_acc()
      elif choice == "2":
          deposit()
      elif choice == "3":
          withdraw()
      elif choice == "4":
          display()
      elif choice == "5":
          break
      else:
          print("Invalid choice.")

except cx_Oracle.DatabaseError as e:
    print(f"Database Error: {e}")
except Exception as e:
    print(f"Some exception occurred: {e}")
finally:
    if curr:
        curr.close()
    if conn:
        conn.close()
    print("Connection closed successfully.")
