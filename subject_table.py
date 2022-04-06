import sqlite3 as sl, pandas as pd, numpy as np

con = sl.connect('class.db')

with con:
    try:
        con.execute('SELECT COUNT(*) FROM COURSES')
    except:
        con.execute("""
                    CREATE TABLE COURSES (
                        course_code TEXT,
                        course_name TEXT,
                        grade TEXT,
                        desc TEXT,
                        prereq TEXT,
                        note TEXT,
                        recommendation TEXT,
                        eff_dt DATE,
                        exp_dt DATE,
                        sys_active_flag TEXT,
                        sys_load_dt DATE
                    );
                """)

courses = pd.read_excel('C:\Julia\JApps\ClassFinder\subjects.xlsx', sheet_name = 'Sheet2', header = 0)

for col in courses.select_dtypes(exclude=np.number):
    courses[col].str.strip()

for index, row in courses.iterrows():
    with con:
        cur = con.execute(f"""SELECT * FROM COURSES WHERE course_code = '{row['Course Code']}' AND 
                                                                        sys_active_flag = 'Y' """).fetchall()
        if len(cur) > 0:
            cur = cur[0]
            same = True
            i = 0
            for col in courses:
                if row[col] != cur[i]:
                    same = False
                    print(f"For course code {row['Course Code']}, {col} has changed from {cur[i]} to {row[col]}")
                i = i + 1
        else:
            same = False
        if not same:
            con.execute(f"""UPDATE COURSES
                            SET
                                sys_active_flag = 'N',
                                exp_dt = DATE('now', 'localtime', '-1 day')
                            WHERE
                                course_code = '{row['Course Code']}' AND 
                                sys_active_flag = 'Y' """)
            con.execute(f"""INSERT INTO COURSES(
                                course_code, 
                                course_name, 
                                grade, 
                                desc, 
                                prereq, 
                                note, 
                                recommendation,
                                eff_dt,
                                exp_dt,
                                sys_active_flag,
                                sys_load_dt)
                            values(
                                '{(row['Course Code'])}',
                                '{row['Course Name']}',
                                '{row['Grade']}',
                                '{row['Description']}',
                                '{row['Prerequisite']}',
                                '{row['Note']}',
                                '{(row['Recommendation'])}',
                                DATE('now', 'localtime'),
                                '2999-12-31',
                                'Y',
                                DATE('now', 'localtime')
                                )                         
                            """)