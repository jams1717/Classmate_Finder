import sqlite3 as sl
con = sl.connect('class.db')

with con:
    try:
        con.execute('SELECT COUNT(*) FROM USER')
    except:
        con.execute("""
            CREATE TABLE USER (
                user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                firstname TEXT,
                lastname TEXT
            );
        """)

with con:
    try:
        con.execute('SELECT COUNT(*) FROM TIMETABLE')
    except:
        con.execute("""
            CREATE TABLE TIMETABLE (
                user_id INTEGER NOT NULL,
                period TEXT,
                course_id INTEGER NOT NULL,
                room_num TEXT,
                school_year TEXT
            );
        """)


def insert_user(firstname, lastname, con = con):
    with con:
        user_ids = list(con.execute(f"SELECT DISTINCT user_id FROM USER WHERE firstname = '{firstname}' AND lastname = '{lastname}'"))
        if len(user_ids) == 0:
            con.execute(f"INSERT INTO USER (firstname, lastname) values('{firstname}', '{lastname}');")
            user_ids = list(con.execute(f"SELECT DISTINCT user_id FROM USER WHERE firstname = '{firstname}' AND lastname = '{lastname}'"))
    return user_ids[0][0]


def insert_timetable(user_id, period, course_id, room_num, school_year, con = con):
    with con:
        rows = con.execute(f'''SELECT * FROM TIMETABLE WHERE user_id = '{user_id}'
                                                                AND
                                                                    period <= '{period}'
                                                                AND 
                                                                    school_year = '{school_year}' ''').fetchall()
        row = [x for x in rows if x[1] == period]
        prev_course = [x for x in rows if x[2] == course_id and x[1] != period]
        if len(prev_course) != 0:
            err_msg = f'<br> Course {course_id} already being taken in other period {prev_course[0][1]}'
            return err_msg
        if len(row) == 0:
            print('This course slot has not been filled; creating it now.')
            con.execute(f'''INSERT INTO TIMETABLE (user_id, period, course_id, room_num, school_year)
                        values('{user_id}', '{period}', '{course_id}', '{room_num}', '{school_year}') ''')
        else:
            print(f'''This course slot has been filled before with course {row[0][2]} in room {row[0][3]}; 
            updating it now to course {course_id} in room {room_num}''')
            con.execute(f'''UPDATE TIMETABLE
                        SET 
                            course_id = '{course_id}',
                            room_num = '{room_num}' 
                        WHERE 
                            user_id = '{user_id}' AND 
                            period = '{period}' AND
                            school_year = '{school_year}' ''')
        return ''


def return_common(user_id, school_year, specific_users = None, period = ''):
    if specific_users == None:
        specific_users = []
    with con:
         courses = con.execute(f'''SELECT * FROM TIMETABLE WHERE user_id = '{user_id}' AND 
                                                                school_year = '{school_year}' ''').fetchall()
         main_dict = {}
         for course in courses:
            commons = con.execute(f'''SELECT 
                                        tbl.user_id,
                                        firstname,
                                        lastname
                                    FROM TIMETABLE AS tbl
                                    
                                    LEFT JOIN USER AS usr
                                        ON tbl.user_id = usr.user_id
                                    
                                    WHERE   
                                        period = '{course[1]}'AND
                                        course_id = '{course[2]}' AND
                                        room_num = '{course[3]}' AND
                                        school_year = '{course[4]}' AND
                                        tbl.user_id <> '{user_id}' ''').fetchall()

            main_dict[course[1]] = {'Year': course[4],
                                    'Room': course[3],
                                    'Course': course[2],
                                    'Common Students': commons}
    return main_dict

'''insert_user('Julia', 'Muresan')
insert_user('Adrian', 'Muresan')
insert_user('John', 'Doe')
insert_user('Jane', 'Smith')

insert_timetable(1, 'A', 101, 'room_2', '2021')
insert_timetable(1, 'B', 103, 'room_7', '2021')
insert_timetable(1, 'C', 104, 'room_32', '2021')
insert_timetable(1, 'D', 105, 'room_4', '2021')
insert_timetable(1, 'E', 106, 'room_5', '2021')
insert_timetable(1, 'F', 107, 'room_10', '2021')
insert_timetable(1, 'G', 108, 'room_21', '2021')
insert_timetable(1, 'H', 103, 'room_7', '2021')

insert_timetable(4, 'A', 101, 'room_2', '2021')
insert_timetable(4, 'B', 108, 'room_2', '2021')
insert_timetable(4, 'C', 105, 'room_34', '2021')
insert_timetable(4, 'D', 107, 'room_6', '2021')
insert_timetable(4, 'E', 106, 'room_89', '2021')
insert_timetable(4, 'F', 109, 'room_5', '2021')
insert_timetable(4, 'G', 104, 'room_11', '2021')
insert_timetable(4, 'H', 103, 'room_7', '2021')


insert_timetable(2, 'A', 101, 'room_2', '2021')
insert_timetable(3, 'A', 102, 'room_3', '2021')




test = return_common(1, '2021')
for period in test:
    print(period, test[period])'''

