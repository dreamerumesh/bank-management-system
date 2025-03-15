import sqlite3
from datetime import datetime

conn = sqlite3.connect("fixedDatabase.db")
cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON;")

# Create users table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phno TEXT NOT NULL,
        email TEXT unique NOT NULL,
        pwd TEXT NOT NULL
    )
""")

conn.commit()
cur.execute("SELECT COUNT(*) FROM users WHERE name = ?", ("admin",))
exists = cur.fetchone()[0]

if exists == 0:  # Insert only if no admin is there
    cur.execute("""
        INSERT INTO users (name, phno, email, pwd)
        VALUES (?, ?, ?, ?)
    """, ("admin", "1234567890", "admin@example.com", "admin@123"))  
    conn.commit()
   
else:
     print()

#create accounts table
cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
       acc_num INTEGER PRIMARY KEY AUTOINCREMENT,
       ifsc INTEGER not null,
       acc_holder_name text not null,
       balance integer,
       id INTEGER,
       FOREIGN KEY (id) REFERENCES users(user_id) on delete cascade
    );
""")

conn.commit()

#history table
cur.execute("""
    create table if not exists history (
            acc_num int,
            loan_type text,
            timestamp text
            );
"""
)


#cur.execute("INSERT INTO history (acc_num, loan_type, timestamp) VALUES (?, ?, datetime('now'))", (1, 'Deposit'))
conn.commit()

# loans table
cur.execute("""
    create table if not exists loans (
            acc_num integer,
            loan_type text,
            amount integer,
            open_date text ,
            duration integer,
            status text default 'pending',
            FOREIGN KEY (acc_num) REFERENCES accounts(acc_num) on delete cascade
            );
"""
)

#loans interest table
cur.execute("""
    create table if not exists loans_interest (
            loan_type text,
            roi integer
            
            );
"""
)
conn.commit()

cur.execute("insert into loans_interest (loan_type, roi) values ('personal', 10)")
cur.execute("insert into loans_interest (loan_type, roi) values ('home', 8)")
cur.execute("insert into loans_interest (loan_type, roi) values ('gold', 12)")
cur.execute("insert into loans_interest (loan_type, roi) values ('education', 9)")
cur.execute("insert into loans_interest (loan_type, roi) values ('agriculture', 7)")
conn.commit()

#fixed deposit table
cur.execute("""
    create table if not exists fixed_deposit (
            acc_num integer,
            amount integer,
            deposit_date text,
            duration integer,
            roi real default 6,
            currentamt integer,
            FOREIGN KEY (acc_num) REFERENCES accounts(acc_num) on delete cascade
            );
"""
)
# some changes above in deposit data

# transactions table
cur.execute("""
    create table if not exists transactions (
            acc_num integer,
            amount integer,
            loan_type text,
            timstamp text
            );
"""
)

while True:
    print("Welcome to Bank")
    print("Login or Register")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    ch = int(input("Enter option: "))
    print()
    if ch == 1:
        email = input("Enter email: ")
        pwd = input("Enter password: ")
        if email=="admin@example.com":
            while True:
                print()
                print("-----------------------------------------------------------")
                print("1. See all transactions")
                print("2. Accounts creation or deletion")
                print("3. Loan approvals")
                print("4. Total transactions")
                print("5. Total history")
                print("6. See all history")
                print("7.Exit")
                op = int(input("Enter option: "))
                if op == 1:
                    cur.execute("select * from transactions")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                elif op == 2:
                    print("1. Created accounts")
                    print("2. Deleted accounts")
                    ch = int(input("Enter option: "))
                    if ch == 1:
                        cur.execute("select * from history where loan_type = 'Account opened'")
                        rows = cur.fetchall()
                        for row in rows:
                            print(row)
                    elif ch == 2:
                        cur.execute("select * from history where loan_type = 'Account deleted'")
                        rows = cur.fetchall()
                        for row in rows:
                            print(row)
                elif op == 3:
                    cur.execute("select * from loans where status = 'pending'")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                    while True:
                        acc_num = int(input("Enter account number to approve or -1 to stop: "))
                        if acc_num == -1:
                            break
                        cur.execute(f"update loans set status = 'approved' where acc_num = {acc_num}")
                        conn.commit()
                        print("Loan approved successfully")
                elif op == 4:
                    cur.execute("select * from transactions")
                    rows = cur.fetchall()
                    print("Total transactions:", len(rows))
                elif op == 5:
                    cur.execute("select * from history")
                    rows = cur.fetchall()
                    print("Total history:", len(rows))
                elif op == 6:
                    cur.execute("select * from history")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                else:
                    break
        elif (email!="admin"):    
            
            valid = cur.execute("SELECT user_id FROM users WHERE email = ? AND pwd = ?", (email, pwd))
            user = valid.fetchone()
            #print(user)
            if user:  
                id = user[0]
                x = cur.execute(f"select acc_num from accounts where id = {id}")

                if x:
                    #acc_num = x.fetchone()[0]
                    #print(acc_num)
                    print("Login successful")
                    print("Welcome")
                    while True:
                        print()
                        print("-----------------------------------------------------------")              
                        # print("1. Open account")
                        # print("2. Check balance")
                        # print("3. Deposit")
                        # print("4. Withdraw")
                        # print("5. Transfer")
                        # print("6. Apply for loan")
                        # print("7. Apply for fixed deposit")
                        # print("8. View history(direct)")
                        # print("9. View history(filters)")
                        # print("10. Account Delete")
                        # print("11. Exit")
                        x = cur.execute(f"select acc_num from accounts where id = {id}")
                        if not x.fetchone():
                            print()
                            print("You should create Account first")
                            print("1. Open account")
                            print("11. Exit")

                        else:
                            x = cur.execute(f"select acc_num from accounts where id = {id}")
                            acc_num = x.fetchone()[0]
                            print("2. Check balance")
                            print("3. Deposit")
                            print("4. Withdraw")
                            print("5. Transfer")
                            print("6. Apply for loan")
                            print("7. Apply for fixed deposit")
                            print("8. View history(direct)")
                            print("9. View history(filters)")
                            print("10. Account Delete")
                            print("11. Exit")

                        #acc_num = x.fetchone()[0]
                        #print(acc_num)
                        ch = int(input("Enter option: "))
                        if ch == 1:
                            dup =  cur.execute(f"select acc_num from accounts where id = {id}")
                            if dup.fetchone(): 
                                print("Already you have an account")
                                continue
                            name = input("Enter account holder name: ")
                            balance = int(input("Enter initial balance(>200): "))
                            ifsc = 1001
                            cur.execute("insert into accounts (ifsc, acc_holder_name, balance, id) values (?, ?, ?, ?)", (ifsc, name, balance, id))
                            conn.commit()
                            print("Account opened successfully")
                            us = cur.execute(f"select acc_num from accounts where id = {id}");
                            acc_num = us.fetchone()[0]
                            cur.execute("INSERT INTO history (acc_num,loan_type, timestamp) VALUES (?, ?, datetime('now'))", (acc_num,'Account opened'))
                            
                            conn.commit()
                        
                        elif ch == 2:
                            print("1. savings amount")
                            print("2. fixed amount")
                            print("3. loan amount")
                            ch = int(input("Enter option: "))
                            if ch == 1:
                                cur.execute(f"select balance from accounts where id = {id}")
                                result = cur.fetchone()
                                if result:  # Check if data exists
                                    print("Saving's Balance:", result[0])
                                    cur.execute("INSERT INTO history (acc_num, loan_type, timestamp) VALUES (?, ?, datetime('now'))", (1, 'Deposit'))
                                    conn.commit()
                                else:
                                    print("No balance deposit account found for this acc_num.")

                            elif ch == 2:
                                

                                cur.execute("SELECT currentamt FROM fixed_deposit WHERE acc_num = ?", (acc_num,))
                                result = cur.fetchone()

                                if result:  # Check if data exists
                                    print("Fixed deposit Balance:", result[0])
                                    cur.execute("INSERT INTO history (acc_num, loan_type, timestamp ) VALUES (?, ?,datetime('now'))", (acc_num, "Balance checked"))
                                    conn.commit()
                                else:
                                    print("No fixed deposit account found for this acc_num.")
                            elif ch == 3:
                                cur.execute(f"select amount from loans where acc_num = {acc_num}")
                                result = cur.fetchone()
                                if result:
                                    print("Loan Balance:", result[0])
                                    cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "Balance checked" ))
                                    conn.commit()
                                else:
                                    print("No loan account found for this acc_num.")
                                
                            
                        elif ch == 3:
                            print("1.Saving's Deposit")
                            print("2. Loan repayment")
                            print("3. Go back")
                            ch = int(input("Enter option: "))
                            if ch == 1:
                                amount = int(input("Enter amount to deposit: "))
                                cur.execute("update accounts set balance = balance + ? where id = ?", (amount,id))
                                conn.commit()
                                print("Amount deposited successfully")
                                cur.execute("insert into transactions (acc_num, amount,loan_type, timstamp) values (?, ?,?, datetime('now'))", (acc_num,amount,"Deposit"))
                                conn.commit()
                            elif ch == 2:
                                
                                cur.execute(f"select amount from loans where acc_num = {acc_num}")
                                result = cur.fetchone()
                                if result:
                                    loan_amount = result[0]
                                    amount = int(input("Enter amount to repay: "))
                                    if loan_amount >= amount:
                                        cur.execute("update loans set amount = amount - ? where acc_num = ?", (amount,acc_num))
                                        conn.commit()
                                        print("Loan repaid successfully")
                                        cur.execute("insert into transactions (acc_num, amount, loan_type, timstamp) values (?, ?, ?, datetime('now'))", (acc_num, amount, "Loan repayment"))
                                        conn.commit()
                                    else:
                                        print("Amount is greater than loan amount")
                                else:
                                    print("No loan account found")
                            else:
                                continue
                            
                        elif ch == 4:
                            amount = int(input("Enter amount to withdraw: "))
                            cur.execute(f"select balance from accounts where id = {id}")
                            result = cur.fetchone()
                            if result:
                                balance = result[0]
                                if balance >= amount:
                                    cur.execute("update accounts set balance = balance - ? where id = ?", (amount,id))
                                    conn.commit()
                                    print("Amount withdrawn successfully")
                                    
                                    cur.execute("insert into transactions (acc_num, amount, loan_type, timstamp) values (?, ?, ?, datetime('now'))", (acc_num, amount, "Withdraw"))
                                    conn.commit()

                                else:
                                    print("Insufficient balance")
                            else:
                                print("You don't have bank account! please open first")
                        elif ch == 5:
                            acc_num = int(input("Enter account number to transfer: "))
                            amount = int(input("Enter amount to transfer: "))
                            cur.execute(f"select balance from accounts where id = {id}")
                            result  = cur.fetchone()
                            if result:
                                balance = result[0]
                                if balance >= amount:
                                    cur.execute("update accounts set balance = balance - ? where id = ?", (amount,id))
                                    cur.execute("update accounts set balance = balance + ? where acc_num = ?", (amount, acc_num))
                                    conn.commit()
                                    print("Amount transferred successfully")
                                    cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "Amount Transfered"))
                                    conn.commit()
                                    cur.execute("insert into transactions (acc_num, amount, loan_type, timstamp) values (?, ?, ?, datetime('now'))", (acc_num, amount, "Transfer"))
                                else:
                                    print("Insufficient balance")
                            else:
                                print("You don't have a account please open first")
                        elif ch == 6:
                            print()
                            print("1. Personal loan")
                            print("2. Home loan")
                            print("3. Gold loan")
                            print("4. Education loan")
                            print("5. Agriculture loan")
                            print("6. Go back")
                            ch = int(input("Enter option: "))
                            if ch == 1:
                                cur.execute("select roi from loans_interest where loan_type = 'personal'")
                                roi = cur.fetchone()[0] 
                                loan_type = "personal"
                            elif ch == 2:
                                cur.execute("select roi from loans_interest where loan_type = 'home'")
                                roi = cur.fetchone()[0]
                                loan_type = "home"
                            elif ch == 3:
                                cur.execute("select roi from loans_interest where loan_type = 'gold'")
                                roi = cur.fetchone()[0]
                                loan_type = "gold"
                            elif ch == 4:
                                cur.execute("select roi from loans_interest where loan_type = 'education'")
                                roi = cur.fetchone()[0]
                                loan_type = "education"
                            elif ch == 5:
                                cur.execute("select roi from loans_interest where loan_type = 'agriculture'")
                                roi = cur.fetchone()[0]
                                loan_type = "agriculture"
                            else: continue
                            amount = int(input("Enter amount to apply for loan: "))
                            dur = int(input("Enter duration in years: "))
                            interest = (amount * roi * dur) / 100
                            amount += interest
                            cur.execute(f"select balance from accounts where id = {id}")
                            result = cur.fetchone()
                            if result:
                                balance = result[0]
                                if balance >= amount:
                                    cur.execute("SELECT acc_num FROM accounts WHERE id = ?", (id,))
                                    acc_row = cur.fetchone()
                                    if acc_row:
                                        acc_num = acc_row[0]
                                        cur.execute("insert into loans (acc_num, loan_type, amount,open_date,duration) values (?, ?, ?,datetime('now'),?)", (acc_num, loan_type, amount,dur,))
                                        conn.commit()
                                        print("Loan applied successfully")
                                        cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?,datetime('now') )", (acc_num, 'Applied loan',))
                                        conn.commit()
                                else:
                                    print("You are not allowed")
                            else:
                                print("You don't saving's account! please first open it")
                        elif ch == 7:
                            amount = int(input("Enter amount to apply for fixed deposit: "))
                            duration = int(input("Enter duration in years: "))
                            cur.execute("select balance from accounts where id = ?", (id,))
                            result = cur.fetchone()
                            if result:
                                balance = result[0]
                                if balance >= amount:
                                    cur.execute("SELECT acc_num FROM accounts WHERE id = ?", (id,))
                                    acc_row = cur.fetchone()
                                    if acc_row:
                                        acc_num = acc_row[0]
                                        cur.execute("INSERT INTO fixed_deposit (acc_num, amount, deposit_date, duration, currentamt) VALUES (?, ?, datetime('now'), ?, ?)", 
            (acc_num, amount, duration, amount))

                                        conn.commit()
                                        print("Fixed deposit applied successfully")
                                        cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "Fixed deposit",))
                                        conn.commit()
                                        cur.execute("insert into transactions (acc_num, amount, loan_type, timstamp) values (?, ?, ?, datetime('now'))", (acc_num, amount, "Fixed deposit"))
                                    else:
                                        print("Account number not found")
                                else:
                                    print("Insufficient balance")
                            else:
                                print("First open saving's account")
                        elif ch == 8:
                            cur.execute(f"select * from history where acc_num = {acc_num}")
                            rows = cur.fetchall()
                            print("History:")
                            cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "History check"))
                            conn.commit()
                            for row in rows:
                                print(row)
                        elif ch == 9:
                            print("1. Mini statement")
                            print("2. Transaction type")
                            print("3. Date range")
                            print("4. Exit")
                            ch = int(input("Enter option: "))
                            if ch == 1:
                                cur.execute(f"select * from transactions where acc_num = {acc_num} order by timstamp desc limit 5")
                                rows = cur.fetchall()
                                print("Transactions:")
                                cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "Mini statement"))
                                conn.commit()
                                for row in rows:
                                    print(row)
                            elif ch == 2:
                                print("1. Deposit")
                                print("2. Withdraw")
                                print("3. Transfer")
                                print("4.Fixed deposit")
                                ch = int(input("Enter transaction type: "))
                                if ch == 1:
                                    loan_type = "Deposit"
                                elif ch == 2:
                                    loan_type = "Withdraw"
                                elif ch == 3:
                                    loan_type = "Transfer"
                                elif ch == 4:
                                    loan_type = "Fixed deposit"
                                cur.execute(f"select * from transactions where acc_num = {acc_num} and loan_type = '{loan_type}' order by timstamp desc limit 5")
                                rows = cur.fetchall()
                                print("Transactions:")
                                cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "History check"))
                                conn.commit()
                                for row in rows:
                                    print(row)
                            elif ch == 3:
                                start = input("Enter start date: ")
                                end = input("Enter end date: ")
                                cur.execute(f"select * from transactions where acc_num = {acc_num} and timstamp between '{start}' and '{end}' order by timstamp desc limit 5")
                                rows = cur.fetchall()
                                print("Transactions:")
                                cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "Mini statement"))
                                conn.commit()
                                for row in rows:
                                    print(row)
                            else:
                                break
                            
                            
                        elif ch == 10:
                            cur.execute("delete from accounts where id = ?", (id,))
                            conn.commit()
                            print("Account deleted successfully")
                            cur.execute("Insert into history (acc_num, loan_type, timestamp) values (?, ?, datetime('now'))", (acc_num, "Account deleted"))
                            conn.commit()
                        else:
                           break
                else: print("No account found")
            else:
                print()
                print("Invalid email or password")
                print()
    elif ch == 2:
        print()
        name = input("Enter name: ")
        phno = input("Enter phone number: ")
        email = input("Enter email: ")
        while True:
            pwd = input("Enter password: ")
            if(len(pwd) < 8): print("Password must be of minimum length 8")
            else: break
        
        cur.execute("insert into users (name, phno, email, pwd) values (?, ?, ?, ?)", (name, phno, email, pwd))
        conn.commit()
        print("Registration successful")
    else:
        break
conn.close()