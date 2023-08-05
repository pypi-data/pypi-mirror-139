from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config
from .args import parse_options

app = Flask (__name__,
            static_url_path='', 
            static_folder='templates',
            template_folder='templates')

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

@app.route('/updatedb')
def updatedb_url():
    return render_template('updatedb.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "robothistoric2")
        cursor.execute("SELECT * FROM project WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('home.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "robothistoric2")
        cursor.execute("SELECT * FROM project;")
        data = cursor.fetchall()
        return render_template('home.html', data=data)

@app.route('/<db>/deldbconf', methods=['GET'])
def delete_db_conf(db):
    return render_template('deldbconf.html', db_name = db)

@app.route('/<db>/delete', methods=['GET'])
def delete_db(db):
    cursor = mysql.connection.cursor()
    # cursor.execute("DROP DATABASE %s;" % db)
    # use_db(cursor, "robothistoric")
    cursor.execute("DELETE FROM robothistoric2.project WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/newdb', methods=['GET', 'POST'])
def add_db():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_image = request.form['dbimage']
        cursor = mysql.connection.cursor()

        try:
            # update created database info in robothistoric.project table
            cursor.execute("INSERT INTO robothistoric2.project ( pid, name, image, created, updated, total, percentage) VALUES (0, '%s', '%s', NOW(), NOW(), 0, 0);" % (db_name, db_image))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('home'))
    else:
        return render_template('newdb.html')

@app.route('/<db>/dashboardAll', methods=['GET'])
def dashboardAll(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from robothistoric2.execution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from robothistoric2.test WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from robothistoric2.execution WHERE pid=%s;" % db)
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT ROUND((pass/total)*100, 2) from robothistoric2.execution WHERE pid=%s;" % db)
        exe_perc_data = cursor.fetchall()

        results = []
        results.append(get_count_by_perc(exe_perc_data, 100, 90))
        results.append(get_count_by_perc(exe_perc_data, 89, 80))
        results.append(get_count_by_perc(exe_perc_data, 79, 70))
        results.append(get_count_by_perc(exe_perc_data, 69, 60))
        results.append(get_count_by_perc(exe_perc_data, 59, 0))

        return render_template('dashboardAll.html', exe_id_avg_data=exe_id_avg_data,
         results=results, results_data=results_data, db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/dashboardRecent', methods=['GET'])
def dashboardRecent(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, 'robothis')

    cursor.execute("SELECT COUNT(eid) from robothistoric2.execution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from robothistoric2.test WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 2;" % db)
        exe_info = cursor.fetchall()

        if len(exe_info) == 2:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])

        # handle db columns not exist issue
        try:
            cursor.execute("SELECT pass, fail, total, etime, skip from robothistoric2.execution WHERE eid=%s" % exe_info[0][0])
            last_exe_data = cursor.fetchall()

            cursor.execute("SELECT pass, fail, total, etime, skip from robothistoric2.execution WHERE eid=%s" % exe_info[1][0])
            prev_exe_data = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND status = 'FAIL' AND comment IS NULL" % exe_info[0][0])
            req_anal_data = cursor.fetchall()

            cursor.execute("SELECT ROUND(AVG(time),2) from robothistoric2.test WHERE eid=%s;" % exe_info[0][0])
            test_avg_dur_data = cursor.fetchall()
        
            cursor.execute("SELECT COUNT(*) From (SELECT name, eid from robothistoric2.test WHERE status='FAIL' AND pid=%s AND eid >= %s GROUP BY name HAVING COUNT(name) = 1) AS T WHERE eid=%s" % (db, exe_info[1][0],exe_info[0][0]))
            new_failed_tests_count = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND pid=%s AND type LIKE '%%Application%%';" % (exe_info[0][0], db))
            app_failure_anl_count = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND pid=%s AND type LIKE '%%Automation%%';" % (exe_info[0][0], db))
            auto_failure_anl_count = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND pid=%s AND type LIKE '%%Other%%';" % (exe_info[0][0], db))
            other_failure_anl_count = cursor.fetchall()

            # required analysis percentage
            if last_exe_data[0][1] > 0 and last_exe_data[0][1] != req_anal_data[0][0]:
                req_anal_perc_data = round( ((last_exe_data[0][1] - req_anal_data[0][0]) / last_exe_data[0][1])*100  ,2)
            else:
                req_anal_perc_data = 0
            
            new_tests_count = exe_info[0][1] - exe_info[1][1]
            passed_test_dif = last_exe_data[0][0] - prev_exe_data[0][0]
            failed_test_dif = prev_exe_data[0][1] - last_exe_data[0][1]
            skipped_test_dif = prev_exe_data[0][4] - last_exe_data[0][4]

            return render_template('dashboardRecent.html', last_exe_data=last_exe_data, exe_info=exe_info,
            prev_exe_data=prev_exe_data, new_failed_tests_count=new_failed_tests_count,
            req_anal_data=req_anal_data, app_failure_anl_count=app_failure_anl_count,
            req_anal_perc_data=req_anal_perc_data, auto_failure_anl_count=auto_failure_anl_count,
            new_tests_count=new_tests_count,other_failure_anl_count=other_failure_anl_count,
            passed_test_dif=passed_test_dif,
            failed_test_dif=failed_test_dif,
            skipped_test_dif=skipped_test_dif,
            test_avg_dur_data=test_avg_dur_data,
            db_name=db)
        except Exception as e:
            print(e)
            return redirect(url_for('updatedb_url'))

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/dashboard/<eid>', methods=['GET'])
def eid_dashboard(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from robothistoric2.execution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from robothistoric2.test WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from robothistoric2.execution WHERE pid=%s AND eid <=%s order by eid desc LIMIT 2;" % (db, eid))
        exe_info = cursor.fetchall()

        if len(exe_info) == 2:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])

        cursor.execute("SELECT pass, fail, total, etime, skip from robothistoric2.execution WHERE eid=%s;" % exe_info[0][0])
        last_exe_data = cursor.fetchall()

        cursor.execute("SELECT pass, fail, total, etime, skip from robothistoric2.execution WHERE eid=%s;" % exe_info[1][0])
        prev_exe_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND status = 'FAIL' AND comment IS NULL;" % exe_info[0][0])
        req_anal_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(time),2) from robothistoric2.test WHERE eid=%s;" % exe_info[0][0])
        test_avg_dur_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) From (SELECT name, eid From robothistoric2.test WHERE status='FAIL' AND pid=%s AND eid >= %s GROUP BY name HAVING COUNT(name) = 1) AS T WHERE eid=%s" % (db, exe_info[1][0],exe_info[0][0]))
        new_failed_tests_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND pid=%s AND type LIKE '%%Application%%';" % (exe_info[0][0], db))
        app_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND pid=%s AND type LIKE '%%Automation%%';" % (exe_info[0][0], db))
        auto_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from robothistoric2.test WHERE eid=%s AND pid=%s AND type LIKE '%%Other%%';" % (exe_info[0][0], db))
        other_failure_anl_count = cursor.fetchall()

        # required analysis percentage
        if last_exe_data[0][1] > 0 and last_exe_data[0][1] != req_anal_data[0][0]:
            req_anal_perc_data = round( ((last_exe_data[0][1] - req_anal_data[0][0]) / last_exe_data[0][1])*100  ,2)
        else:
            req_anal_perc_data = 0
        
        new_tests_count = exe_info[0][1] - exe_info[1][1]
        passed_test_dif = last_exe_data[0][0] - prev_exe_data[0][0]
        failed_test_dif = prev_exe_data[0][1] - last_exe_data[0][1]
        skipped_test_dif = prev_exe_data[0][4] - last_exe_data[0][4]

        return render_template('dashboardByEid.html', last_exe_data=last_exe_data, exe_info=exe_info,
         prev_exe_data=prev_exe_data, new_failed_tests_count=new_failed_tests_count,
         req_anal_data=req_anal_data, app_failure_anl_count=app_failure_anl_count,
         req_anal_perc_data=req_anal_perc_data, auto_failure_anl_count=auto_failure_anl_count,
         new_tests_count=new_tests_count, other_failure_anl_count=other_failure_anl_count,
         passed_test_dif=passed_test_dif,
         failed_test_dif=failed_test_dif,
         skipped_test_dif=skipped_test_dif,
         test_avg_dur_data=test_avg_dur_data,
         db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/dashboardRecentFive', methods=['GET'])
def dashboardRecentFive(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from robothistoric2.execution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from robothistoric2.test WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 5;" % db)
        exe_info = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from robothistoric2.execution WHERE eid >= %s;" % exe_info[-1][0])
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT eid, pass, fail, etime, skip from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 5;" % db)
        exe_id_filter_data = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        return render_template('dashboardRecentFive.html', exe_id_avg_data=exe_id_avg_data,
         exe_id_filter_data=exe_id_filter_data, results_data=results_data,
         new_tests=new_tests,db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/dashboardRecentTen', methods=['GET'])
def dashboardRecentTen(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from robothistoric2.execution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from robothistoric2.test WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 10;" % db)
        exe_info = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from robothistoric2.execution WHERE pid=%s AND eid >= %s;" % (db, exe_info[-1][0]))
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT eid, pass, fail, etime, skip from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 10;" % db)
        exe_id_filter_data = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        return render_template('dashboardRecentTen.html', exe_id_avg_data=exe_id_avg_data,
         exe_id_filter_data=exe_id_filter_data, results_data=results_data,
         new_tests=new_tests, db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/dashboardRecentThirty', methods=['GET'])
def dashboardRecentThirty(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from robothistoric2.execution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from robothistoric2.test WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 30;" % db)
        exe_info = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from robothistoric2.execution WHERE pid=%s AND eid >= %s;" % (db, exe_info[-1][0]))
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT eid, pass, fail, etime, skip from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 30;" % db)
        exe_id_filter_data = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        return render_template('dashboardRecentThirty.html', exe_id_avg_data=exe_id_avg_data,
         exe_id_filter_data=exe_id_filter_data, results_data=results_data,
         new_tests=new_tests, db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/ehistoric', methods=['GET'])
def ehistoric(db):
    cursor = mysql.connection.cursor()
    # # use_db(cursor, db)
    cursor.execute("SELECT * from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 500;" % db)
    data = cursor.fetchall()
    return render_template('ehistoric.html', data=data, db_name=db)

@app.route('/<db>/deleconf/<eid>', methods=['GET'])
def delete_eid_conf(db, eid):
    return render_template('deleconf.html', db_name = db, eid = eid)

@app.route('/<db>/edelete/<eid>', methods=['GET'])
def delete_eid(db, eid):
    cursor = mysql.connection.cursor()
    # # use_db(cursor, db)
    # remove execution from tables: execution, suite, test
    cursor.execute("DELETE FROM robothistoric2.execution WHERE eid='%s';" % eid)
    cursor.execute("DELETE FROM robothistoric2.test WHERE eid='%s';" % eid)
    # get latest execution info
    cursor.execute("SELECT pass, total from robothistoric2.execution WHERE pid=%s ORDER BY eid DESC LIMIT 1;" % db)
    data = cursor.fetchall()

    try:
        if data[0][0] > 0:
            recent_pass_perf = float("{0:.2f}".format((data[0][0]/data[0][1]*100)))
        else:
            recent_pass_perf = 0
    except:
        recent_pass_perf = 0

    # update robothistoric project
    cursor.execute("UPDATE robothistoric2.project SET total=%s, updated=now(), percentage=%s WHERE pid='%s';" % (int(data[0][1]), recent_pass_perf, db))
    # commit changes
    mysql.connection.commit()
    return redirect(url_for('ehistoric', db = db))

@app.route('/<db>/tmetrics', methods=['GET', 'POST'])
def tmetrics(db):
    cursor = mysql.connection.cursor()
    # # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update robothistoric2.test SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT eid from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 1;" % db)
    data = cursor.fetchone()
    print(data)
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from robothistoric2.test WHERE eid={eid} and pid={pid};".format(eid=data[0], pid=db))
    data = cursor.fetchall()
    return render_template('tmetrics.html', data=data, db_name=db)

@app.route('/<db>/tmetrics/<eid>', methods=['GET', 'POST'])
def eid_tmetrics(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update robothistoric2.test SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from robothistoric2.test WHERE eid=%s; and pid=%s" % (eid, db))
    data = cursor.fetchall()
    return render_template('eidtmetrics.html', data=data, db_name=db)

@app.route('/<db>/failures/<eid>', methods=['GET', 'POST'])
def eid_failures(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update robothistoric2.test SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from robothistoric2.test WHERE pid=%s and eid=%s and status='FAIL';" % (db, eid))
    data = cursor.fetchall()
    return render_template('failures.html', data=data, db_name=db)

@app.route('/<db>/failures', methods=['GET', 'POST'])
def recent_failures(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update robothistoric2.test SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT eid from robothistoric2.execution order by eid desc LIMIT 1;")
    data = cursor.fetchone()
    cursor.execute("SELECT * from robothistoric2.test WHERE eid=%s and status='FAIL';" % data)
    data = cursor.fetchall()
    return render_template('failures.html', data=data, db_name=db)

@app.route('/<db>/ttags/<eid>', methods=['GET', 'POST'])
def eid_ttags(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT eid, name, status, tag from robothistoric2.test WHERE eid=%s and pid=%s" % (eid, db))
    data = cursor.fetchall()
    return render_template('ttags.html', data=data, db_name=db)

@app.route('/<db>/search', methods=['GET', 'POST'])
def search(db):
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        try:
            if search:
                cursor.execute("SELECT * from robothistoric2.test WHERE (pid={pid}) and (name LIKE '%{name}%' OR status LIKE '%{name}%' OR eid LIKE '%{name}%') ORDER BY eid DESC LIMIT 500;".format(name=search, pid=db))
                data = cursor.fetchall()
                return render_template('search.html', data=data, db_name=db, error_message="")
            else:
                return render_template('search.html', db_name=db, error_message="Search text should not be empty")
        except Exception as e:
            print(str(e))
            return render_template('search.html', db_name=db, error_message="Could not perform search. Avoid single quote in search or use escaping character")
    else:
        return render_template('search.html', db_name=db, error_message="")

@app.route('/<db>/flaky', methods=['GET'])
def flaky(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT eid from ( SELECT eid from robothistoric2.execution ORDER BY eid DESC LIMIT 5 ) as tmp ORDER BY eid ASC LIMIT 1;")
    last_five = cursor.fetchall()
    cursor.execute("SELECT eid from robothistoric2.execution WHERE pid=%s ORDER BY eid DESC LIMIT 5;" % db)
    last_five_ids = cursor.fetchall()
    sql_query = "SELECT name, eid, status from robothistoric2.test WHERE pid=%s and eid >= %s ORDER BY eid DESC;" % (db, str(last_five[0][0]))
    cursor.execute(sql_query)
    data = cursor.fetchall()
    # print("==== Before Sorted Data ===")
    # print(data)
    sorted_data = sort_tests(data)
    # print("==== After Sorted Data ===")
    # print(sorted_data)
    return render_template('flaky.html', data=sorted_data, db_name=db, builds=last_five_ids)

@app.route('/<db>/compare', methods=['GET', 'POST'])
def compare(db):
    if request.method == "POST":
        eid_one = request.form['eid_one']
        eid_two = request.form['eid_two']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        # fetch first eid tets results
        cursor.execute("SELECT name, eid, status, time, error from robothistoric2.test WHERE eid=%s and pid=%s;" % (eid_one, db) )
        first_data = cursor.fetchall()
        # fetch second eid test results
        cursor.execute("SELECT name, eid, status, time, error from robothistoric2.test WHERE eid=%s and pid=%s;" % (eid_two, db) )
        second_data = cursor.fetchall()
        if first_data and second_data:
            # combine both tuples
            data = first_data + second_data
            sorted_data = sort_tests(data)
            return render_template('compare.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data, eid_one = eid_one, eid_two = eid_two, error_message="")
        else:
            return render_template('compare.html', db_name=db, error_message="EID not found, try with existing EID")    
    else:
        return render_template('compare.html', db_name=db, error_message="")

@app.route('/<db>/query', methods=['GET', 'POST'])
def query(db):
    # if request.method == "POST":
    #     query = request.form['query']
    #     cursor = mysql.connection.cursor()
    #     # use_db(cursor, db)
    #     try:
    #         cursor.execute("{name}".format(name=query))
    #         data = cursor.fetchall()
    #         return render_template('query.html', data=data, db_name=db, error_message="")
    #     except Exception as e:
    #         print(str(e))
    #         return render_template('query.html', db_name=db, error_message=str(e))
    # else:
    #     return render_template('query.html', db_name=db, error_message="")
    return redirect(url_for('home'))

@app.route('/<db>/comment', methods=['GET', 'POST'])
def comment(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT eid from robothistoric2.execution WHERE pid=%s order by eid desc LIMIT 1;" % db)
    recent_eid = cursor.fetchone()

    if request.method == "POST":
        error = request.form['error']
        eid = request.form['eid']
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']

        try:
            cursor.execute('Update robothistoric2.test SET comment=\'{}\', assigned=\'{}\', eta=\'{}\', review=\'{}\', type=\'{}\', updated=now() WHERE pid={} AND eid={} AND error LIKE \'%{}%\''.format(db, str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(eid), str(error)))
            mysql.connection.commit()
            return render_template('comment.html', error_message="", recent_eid=recent_eid)
        except Exception as e:
            print(str(e))
            return render_template('comment.html', error_message=str(e), recent_eid=recent_eid)
    
    else:
        return render_template('comment.html', error_message="", recent_eid=recent_eid)

def use_db(cursor, db_name):
    cursor.execute("USE %s;" % db_name)

def sort_tests(data_list):
    out = {}
    for elem in data_list:
        try:
            out[elem[0]].extend(elem[1:])
        except KeyError:
            out[elem[0]] = list(elem)
    return [tuple(values) for values in out.values()]

def get_count_by_perc(data_list, max, min):
    count = 0
    for item in data_list:
        if item[0] <= max and item[0] >= min:
            count += 1
    return count

def main():
    args = parse_options()
    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password
    app.config['auth_plugin'] = 'mysql_native_password'
    app.run(host=args.apphost)