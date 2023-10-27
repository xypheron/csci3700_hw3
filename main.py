from flask import Flask, render_template
from psycopg2 import Error
import util

app = Flask(__name__)

username='raywu1990'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/api/update_basket_a

@app.route('/api/update_basket_a')
# define a function in Python
def update():
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    
    record = util.run_and_commit_sql(cursor, connection, "INSERT INTO basket_a (a, fruit_a) VALUES (5,'Cherry');")
    
    if record != 1:
        log = record
    else:
        log = "Success!"
    
    util.disconnect_from_db(connection,cursor)
    
    return render_template('index.html', log_html = log)

@app.route('/api/unique')
def index():
    
    # this is the index page
    # connect to database
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    record = util.run_and_fetch_sql(cursor, "Select fruit_a,fruit_b FROM basket_a FULL JOIN basket_b on fruit_a = fruit_b where a is NULL OR b is NULL;")
    if isinstance(record, (Exception, Error)):
        return render_template('index.html', log_html = record)
    else:
        # will return all column names of the select result table
        # ['customer_id','store_id','first_name','last_name','email','address_id','activebool','create_date','last_update','active']
        col_names = [desc[0] for desc in cursor.description]
        # only uses the first five rows
        log = record[:5]
        # log=[[1,2],[3,4]]
    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('index2.html', sql_table = log, table_title=col_names)
    
if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)

