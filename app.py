from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
import hashlib, csv

app = Flask(__name__)
app.secret_key = "mysecretkey"

host = 'http://127.0.0.1:5000/'

current_user = None
current_role = None
in_bidseller = False
@app.route('/')
def index():
    return render_template('first.html')

#initialize and load database when button is pressed
@app.route('/loaddb', methods=['POST', 'GET'])
def loaddb():
    error = None

    connection = sql.connect('database1.db')
    connection.execute('DROP TABLE IF EXISTS users;')
    connection.commit()
    connection.execute('CREATE TABLE IF NOT EXISTS users(ID TEXT PRIMARY KEY, Password TEXT);')
    connection.commit()

    connection.execute('DROP TABLE IF EXISTS sellers;')
    connection.commit()
    connection.execute('CREATE TABLE IF NOT EXISTS sellers(ID TEXT PRIMARY KEY, routing_num TEXT, account_num TEXT, balance TEXT);')
    connection.commit()
    connection.execute('ALTER TABLE sellers ADD COLUMN name TEXT;')
    connection.commit()
    connection.execute('ALTER TABLE sellers ADD COLUMN address TEXT;')
    connection.commit()
    connection.execute('ALTER TABLE sellers ADD COLUMN phone TEXT;')
    connection.commit()

    connection.execute('DROP TABLE IF EXISTS bidders;')
    connection.commit()
    connection.execute('CREATE TABLE IF NOT EXISTS bidders(ID TEXT PRIMARY KEY, fname TEXT, lname TEXT, gender TEXT, age INTEGER, address TEXT, major TEXT);')
    connection.commit()

    connection.execute('DROP TABLE IF EXISTS helpdesk;')
    connection.commit()
    connection.execute('CREATE TABLE IF NOT EXISTS helpdesk(ID TEXT PRIMARY KEY, job TEXT);')
    connection.commit()

    connection.execute('DROP TABLE IF EXISTS listings;')
    connection.commit()
    connection.execute('CREATE TABLE IF NOT EXISTS listings(email TEXT, listingid TEXT, category TEXT, title TEXT, name TEXT, descr TEXT, amount integer, price text, max text, status text);')
    connection.commit()

    connection.execute('DROP TABLE IF EXISTS categories;')
    connection.commit()
    connection.execute('CREATE TABLE IF NOT EXISTS categories(parent TEXT, cat TEXT);')
    connection.commit()

    with open("./Sellers.csv", 'r', encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            first = row[0]
            second = row[1]
            third = row[2]
            fourth = row[3]

            connection.execute('INSERT INTO sellers (ID, routing_num, account_num, balance) VALUES (?,?,?,?);', (first, second, third, fourth))
            connection.commit()

    with open("./Users.csv", 'r', encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            userID = row[0]
            userPass = bytes(row[1], 'utf-8')
            m = hashlib.sha256()
            m.update(userPass)
            hashedPass = m.hexdigest()

            connection.execute('INSERT INTO users (ID, Password) VALUES (?,?);', (userID, hashedPass))
            connection.commit()

    with open("./Bidders.csv", 'r', encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            first = row[0]
            second = row[1]
            third = row[2]
            fourth = row[3]
            fifth = row[4]
            sixth = row[5]
            seventh = row[6]

            connection.execute('INSERT INTO bidders (ID, fname, lname, gender, age, address, major) VALUES (?,?,?,?,?,?,?);', (first, second, third, fourth, fifth, sixth, seventh))
            connection.commit()

    with open("./Helpdesk.csv", 'r', encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            first = row[0]
            second = row[1]
            connection.execute('INSERT INTO helpdesk (ID, job) VALUES (?,?);', (first, second))
            connection.commit()

    with open("./Auction_Listings.csv", 'r', encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            a = row[0]
            b = row[1]
            c = row[2]
            d = row[3]
            e = row[4]
            f = row[5]
            g = row[6]
            h = row[7]
            i = row[8]
            j = row[9]
            connection.execute('INSERT INTO listings (email,listingid,category,title,name,descr,amount,price,max,status) VALUES (?,?,?,?,?,?,?,?,?,?);', (a,b,c,d,e,f,g,h,i,j))
            connection.commit()

    with open("./Categories.csv", 'r', encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            first = row[0]
            second = row[1]
            connection.execute('INSERT INTO categories (parent, cat) VALUES (?,?);', (first, second))
            connection.commit()

    return render_template('loaddb.html', error=error)

@app.route('/newuser', methods=['POST','GET'])
def newuser():
    return render_template('newuser.html', error=None)

@app.route('/createnew', methods=['POST','GET'])
def createuser():
    if request.method=='POST':
        role = request.form['option']
        userID = request.form['ID']
        global current_user 
        current_user = userID
        Password = request.form['Password']

        userPass = bytes(Password, 'utf-8')
        m = hashlib.sha256()
        m.update(userPass)
        hashedPass = m.hexdigest()

        global current_role
        current_role = role

        connection = sql.connect('database1.db')
        connection.execute('INSERT INTO users (ID, Password) VALUES (?,?);', (userID,hashedPass))
        connection.commit()

        if role=="bidder":
            return render_template('createbidder.html', error=None)
        if role=="seller":
            return render_template('createseller.html',error=None)
        if role=="bidseller":
            return render_template('createbidseller.html', error=None)

    
@app.route('/createbidder', methods=['POST','GET'])
def createbidder():
    if request.method =='POST':
        global current_user
        global in_bidseller
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        age = request.form['age']
        address = request.form['address']
        major = request.form['major']

        connection = sql.connect('database1.db')
        connection.execute('INSERT INTO bidders (ID,fname,lname,gender,age,address,major) VALUES (?,?,?,?,?,?,?);', (current_user,fname,lname,gender,age,address,major))
        connection.commit()
        return render_template('bidders.html')

@app.route('/createseller',methods=['POST','GET'])
def createseller():
    if request.method == 'POST':
        global current_user
        rout = request.form['rout']
        account = request.form['account']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        
        connection = sql.connect('database1.db')
        connection.execute('INSERT INTO sellers (ID,routing_num,account_num,balance,name,address,phone) VALUES (?,?,?,?,?,?,?);', (current_user,rout,account,None,name,address,phone))
        connection.commit()
        return render_template('sellers.html')

@app.route('/createbidsell', methods = ['POST','GET'])
def createbidseller():
    global current_user
    global in_bidseller
    in_bidseller = True
    rout = request.form['rout']
    account = request.form['account']
    bus_name = request.form['bus_name']
    bus_address = request.form['bus_address']
    phone = request.form['phone']
    connection = sql.connect('database1.db')
    connection.execute(
        'INSERT INTO sellers (ID,routing_num,account_num,balance,name,address,phone) VALUES (?,?,?,?,?,?,?);',
        (current_user, rout, account, None, bus_name, bus_address, phone))
    connection.commit()

    fname = request.form['fname']
    lname = request.form['lname']
    gender = request.form['gender']
    age = request.form['age']
    address = request.form['address']
    major = request.form['major']
    connection = sql.connect('database1.db')
    connection.execute('INSERT INTO bidders (ID,fname,lname,gender,age,address,major) VALUES (?,?,?,?,?,?,?);',
                       (current_user, fname, lname, gender, age, address, major))
    connection.commit()
    
    return render_template('bidsellers.html')

@app.route('/trylogin', methods=['POST', 'GET'])
def trylogin():
    error = None

    if request.method == 'POST':
        userID = request.form['ID']
        Password = request.form['Password']
        userPass = bytes(Password, 'utf-8')
        m = hashlib.sha256()
        m.update(userPass)
        hashedPass = m.hexdigest()

        result = valid_login(userID, hashedPass)
        if ((userID, hashedPass) in result):
            global current_user
            current_user = userID
            return render_template('second.html', error=error)

    return render_template('three.html', error=error)


def valid_login(userID, hashedPass):
    connection = sql.connect('database1.db')
    cursor = connection.execute('SELECT ID, Password FROM users WHERE ID = ? AND Password = ?;', (userID, hashedPass))
    return cursor.fetchall()

@app.route('/pagebyrole', methods=['POST', 'GET'])
def getPageForRole():
    error = None
    global in_bidseller


    connection = sql.connect('database1.db')
    cursor = connection.execute('SELECT ID FROM sellers WHERE ID = ?;', (current_user,))
    results_sellers = cursor.fetchall()

    cursor = connection.execute('SELECT ID FROM bidders WHERE ID = ?;', (current_user,))
    results_bidders = cursor.fetchall()

    cursor = connection.execute('SELECT ID FROM helpdesk;')
    results_helpdesk = cursor.fetchall()

    if (current_user,) in results_sellers and (current_user,) in results_bidders:
        in_bidseller = True
        return render_template('bidsellers.html', error=error)

    if (current_user,) in results_sellers:
        in_bidseller = False
        return render_template('sellers.html',error=error)

    if (current_user,) in results_bidders:
        in_bidseller = False
        return render_template('bidders.html', error=error)

    if (current_user,) in results_helpdesk:
        in_bidseller = False
        return render_template('helpdesk.html',error=error)

    return render_template('bidders.html', error=error)

@app.route('/bidderInfo', methods=['POST','GET'])
def load_bidder_info():
    if request.method=='GET':
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT * FROM bidders WHERE ID = ?;', (current_user,))
        result = cursor.fetchall()
        return render_template('bidders.html', error=None, result=result)

@app.route('/sellerInfo', methods=['POST','GET'])
def load_seller_info():
    if request.method=='GET':
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT * FROM sellers WHERE ID = ?;', (current_user,))
        result = cursor.fetchall()
        return render_template('sellers.html', error=None, result=result)

@app.route('/bidsellerInfo', methods=['POST','GET'])
def load_bidseller_info():
    if request.method == 'GET':
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT * FROM sellers where ID = ?;', (current_user,))
        result = cursor.fetchall()

        cursor = connection.execute('SELECT * FROM bidders WHERE ID = ?;', (current_user,))
        result1 = cursor.fetchall()
        return render_template('bidsellers.html', error=None, result=result, result1=result1)

@app.route('/biddings', methods=['POST', 'GET'])
def biddings():
    if request.method == 'GET':
        parent_duplicates = []
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT parent FROM categories;')
        for parent in cursor.fetchall():
            parent_duplicates.append(parent)

        parents = []
        [parents.append(x) for x in parent_duplicates if x not in parents]

        return render_template('biddings.html', error=None, parents=parents)

    if request.method == 'POST':
        data = request.get_json()
        data = data.replace("(", "")
        data = data.replace(")", "")
        data = data.replace(",", "")
        data = data.replace("'", "")

        category_duplicates = []
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT cat FROM categories WHERE parent=?;', (data,))
        for sub in cursor.fetchall():
            category_duplicates.append(sub)

        subcat = []
        [subcat.append(x) for x in category_duplicates if x not in subcat]

        session['data'] = data
        session['subcat'] = subcat

        return redirect(url_for('goto_subcat'))


@app.route('/sub_category', methods=['POST', 'GET'])
def goto_subcat():
    data = session.get('data')
    subcat = session.get('subcat')

    if request.method == 'GET':
        return render_template('subcategory.html', data=data, subcat=subcat)

    if request.method == 'POST':
        data = request.get_json()
        data = data.replace("(", "")
        data = data.replace(")", "")
        data = data.replace(",", "")
        data = data.replace("'", "")
        session['data'] = data
        category_duplicates = []
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT cat FROM categories WHERE parent=?;', (data,))
        for sub in cursor.fetchall():
            category_duplicates.append(sub)

        subcat = []
        [subcat.append(x) for x in category_duplicates if x not in subcat]

        session['data'] = data
        session['subcat'] = subcat
        return render_template('show_listings.html',data=data,subcat=subcat)


@app.route('/show_listings', methods=['POST','GET'])
def show_listings():
    if request.method == 'POST':
        data = session.get('data')
        cat_listings = session.get('subcat')
        connection = sql.connect('database1.db')
        cursor = connection.execute('SELECT * FROM listings WHERE category = ?;', (data,))
        cat_listings = cursor.fetchall()
        return render_template('show_listings.html', error=None, cat_listings=cat_listings, data=data)


@app.route('/bidedit3', methods=['POST', 'GET'])
def edit3():
    global current_user
    new_info = request.form['gender']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE bidders SET gender = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('bidders.html', error=None)

@app.route('/bidedit4', methods=['POST', 'GET'])
def edit4():
    global current_user
    new_info = request.form['age']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE bidders SET age = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('bidders.html', error=None)

@app.route('/bidedit5', methods=['POST', 'GET'])
def edit5():
    global current_user
    new_info = request.form['address']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE bidders SET address = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('bidders.html', error=None)

@app.route('/bidedit6', methods=['POST', 'GET'])
def edit6():
    global current_user
    new_info = request.form['major']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE bidders SET major = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('bidders.html', error=None)

@app.route('/selledit1', methods=['POST','GET'])
def selledit1():
    global current_user
    new_info = request.form['rout']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE sellers SET routing_num = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('sellers.html', error=None)

@app.route('/selledit2', methods=['POST','GET'])
def selledit2():
    global current_user
    new_info = request.form['account']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE sellers SET account_num = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('sellers.html', error=None)

@app.route('/selledit3', methods=['POST','GET'])
def selledit3():
    global current_user
    new_info = request.form['bus_name']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE sellers SET name = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('sellers.html', error=None)

@app.route('/selledit4', methods=['POST','GET'])
def selledit4():
    global current_user
    new_info = request.form['bus_add']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE sellers SET address = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('sellers.html', error=None)

@app.route('/selledit5', methods=['POST','GET'])
def selledit5():
    global current_user
    new_info = request.form['phone']
    connection = sql.connect('database1.db')
    connection.execute('UPDATE sellers SET phone = ? WHERE ID = ?;', (new_info, current_user))
    connection.commit()
    if in_bidseller:
        return render_template('bidsellers.html', error=None)
    return render_template('sellers.html', error=None)

if __name__ == "__main__":
    app.run()
