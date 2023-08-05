import mysql.connector
import logging

def rfhistoric_setup(opts):

    # connect to database
    print("INFO: Connecting to dB")
    mydb = connect_to_mysql(opts.host, opts.username, opts.password)

    # create new user
    obj = mydb.cursor()
    print("INFO: Creating superuser with local access")
    try:
        obj.execute("CREATE USER IF NOT EXISTS 'superuser'@'localhost' IDENTIFIED BY 'passw0rd';")
        obj.execute("GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'localhost' WITH GRANT OPTION;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Creating superuser with remote access")
    try:
        obj.execute("CREATE USER 'superuser'@'%' IDENTIFIED BY 'passw0rd';")
        obj.execute("GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'%' WITH GRANT OPTION;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Reloading grant table")
    try:
        obj.execute("FLUSH PRIVILEGES;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Creating robothistoric2 dB")
    try:
        obj.execute("CREATE DATABASE IF NOT EXISTS robothistoric2;")
    except Exception as e:
        print(str(e))

    print("INFO: Creating required tables")
    rfdb = connect_to_mysql_db(opts.host, opts.username, opts.password, "robothistoric2")
    try:
        rfobj = rfdb.cursor()
        rfobj.execute("CREATE TABLE IF NOT EXISTS project ( pid INT NOT NULL auto_increment primary key, name TEXT, image TEXT, created DATETIME, updated DATETIME, total INT, percentage FLOAT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS execution ( eid INT NOT NULL auto_increment primary key, pid INT, description TEXT, time DATETIME, total INT, pass INT, fail INT, skip INT, etime TEXT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS test ( tid INT NOT NULL auto_increment primary key, eid INT, pid INT, name TEXT, status TEXT, time TEXT, error TEXT, comment TEXT, assigned TEXT, eta TEXT, review TEXT, type TEXT, tag TEXT, updated DATETIME);")
    except Exception as e:
        print(str(e))

    commit_and_close_db(mydb)

def connect_to_mysql(host, user, pwd):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd
        )
        return mydb
    except Exception as e:
        print(e)

def connect_to_mysql_db(host, user, pwd, db):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception as e:
        print(e)

def commit_and_close_db(db):
    db.commit()
    db.close()