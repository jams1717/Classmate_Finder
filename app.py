from flask import Flask, render_template as rt, request, session
from actions import find_classmates as fc, write_to_file
from utils import find_school_year, validate_data
import sqlite3 as sl, pandas as pd, numpy as np, main

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def load():
    years = find_school_year(n=4)
    con = sl.connect('class.db')
    skip = False
    err_msg = ''
    p_grades = {'A': 9, 'B': 9, 'C': 9, 'D': 9, 'E': 9, 'F': 9, 'G': 9, 'H': 9}
    p_courses = {}
    p_rooms = {}
    firstname = ''
    lastname = ''
    timetable_df = pd.DataFrame(columns = ['Period', 'Grade', 'Course', 'Room', 'Year'])
    submit_click = False
    fc_click = False
    if request.method == 'GET':
        session['data_loaded'] = None
        session['classmates'] = {}
    if request.method == 'POST':
        #read from info from website and save as variables
        print('post found')
        firstname = request.form.get('user_firstname')
        lastname = request.form.get('user_lastname')
        year = request.form.get('school_year')
        years.insert(0, year)
        for per in p_grades:
            p_grades[per] = request.form.get(f'period_{per}_grade')
            temp_course = request.form.get(f'period_{per}_course')
            if temp_course != None:
                p_courses[per] = temp_course
            temp_room = request.form.get(f'period_{per}_room')
            if temp_room not in ['', None]:
                p_rooms[per] = temp_room

        if request.form.get('Submit') == 'Submit':
            #check that filled out data is correct, then insert to timetable
            #only cares about periods that have a course selected ex. only having period one filled out won't error
            print('Button clicked')
            skip, err_msg = validate_data(firstname, lastname, p_courses, p_rooms, err_msg)
            if not skip:
                temp = err_msg
                err_msg = err_msg + write_to_file(firstname, lastname, year, p_courses, p_rooms, con)
                if temp == err_msg:
                    submit_click = True

        if request.form.get('Get Previous Data') == 'Get Previous Data':
            skip, err_msg = validate_data(firstname, lastname, err_msg = err_msg)
            with con:
                print('Getting previous data')
                id = main.insert_user(firstname, lastname, con)
                session['data_loaded'] = id
                timetable_df = pd.read_sql_query(f'''
                                                SELECT 
                                                    user_id, 
                                                    timetable.course_id, 
                                                    courses.grade, 
                                                    timetable.room_num, 
                                                    timetable.period 
                                                FROM TIMETABLE 
                                                
                                                JOIN COURSES 
                                                    ON TIMETABLE.course_id = courses.course_code 
                                                    
                                                    WHERE user_id = '{id}' 
                                                    
                                                    ORDER BY period''', con)

                p_grades.update({row[4]:str(row[2]) for row in timetable_df.values})
                p_courses = {row[4]:str(row[1]) for row in timetable_df.values}
                p_rooms = {row[4]:str(row[3]) for row in timetable_df.values}

        if request.form.get('Clear Previous Data') == 'Clear Previous Data':
            skip, err_msg = validate_data(firstname, lastname, err_msg = err_msg)
            with con:
                id = main.insert_user(firstname, lastname, con)
                if session['data_loaded'] == id:
                    con.execute(f'DELETE FROM TIMETABLE WHERE user_id = {id}')
                    p_grades = {'A': 9, 'B': 9, 'C': 9, 'D': 9, 'E': 9, 'F': 9, 'G': 9, 'H': 9}
                    p_courses = {}
                    p_rooms = {}
                else:
                    err_msg = err_msg + 'Please load and check your previous data before deleting.'

        if request.form.get('Find my Classmates') == 'Find my Classmates':
            print('Classmates button clicked')
            skip, err_msg = validate_data(firstname, lastname, err_msg = err_msg)
            with con:
                id = main.insert_user(firstname, lastname, con)
                session['classmates'] = fc(id, year, con)
                fc_click = True


    with con:
        course_df = pd.read_sql_query(f"SELECT * FROM COURSES", con)
        course_df['grade'] = course_df['grade'].astype('str')
        course_grades = course_df['grade'].unique()
        course_grades = np.insert(course_grades, 0, 'Spare')
        course_grades = np.insert(course_grades, 0, '-')
        course_codes = {per:course_df[course_df['grade'] == p_grades[per]]['course_code'].values for per in p_grades}
        for per in p_courses:
            if p_courses[per] in course_codes[per]:
                #print(f'Here for period {per} and course {p_courses[per]}')
                course_codes[per] = np.insert(course_codes[per], 0, p_courses[per])

    return rt('main.html',
              years = years,
              grades = course_grades,
              courses = course_codes,
              p_grades = p_grades,
              err_msg = err_msg,
              user_firstname = firstname,
              user_lastname = lastname,
              p_rooms = p_rooms,
              current_timetable = timetable_df.to_html(),
              submit_click = submit_click,
              fc_click = fc_click,
              classmates = session['classmates'])

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(host="localhost", port=8883, debug=False)





