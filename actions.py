import main, pandas as pd

def find_classmates(id, school_year, con):
    print(id)
    #return pd.DataFrame(columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    q = f'''
    select 
        tt.period,
        tt.period || ': ' || tt.course_id as class,
        usr.firstname || ' ' || usr.lastname as name
    from
        timetable as tt
    inner join(
        select distinct
            period,
            course_id,
            room_num,
            school_year
        from timetable
            where user_id = {id}    
                and school_year = '{school_year}'   
    ) as courses
        on courses.period = tt.period
            and courses.room_num = tt.room_num
            and courses.course_id = tt.course_id
            and courses.school_year = tt.school_year
    left join user as usr
        on usr.user_id = tt.user_id
    where tt.user_id != {id}
        order by class, name
    '''


    temp = pd.read_sql(q, con)
    periods = list(temp['class'].unique())
    ans_dict = {c: [ x for x in temp[temp['class'] == c]['name'].values ] for c in periods}
    return ans_dict

def write_to_file(firstname, lastname, year, p_courses, p_rooms, con):
    '''
    This function's purpose is to insert the inputted user and course from the website into the database.
    :param firstname: The user's given name.
    :param lastname: The user's surname.
    :param year: The school year the course is being taken.
    :param p_courses: A dictionary containing the school periods as keys and the course codes as values.
    :param p_rooms: A dictionary containing the school periods as keys and the room numbers as values.
    :param con: The connection to the database.
    :return: An error message if something goes wrong.
    '''
    err_msg = ''
    id = main.insert_user(firstname, lastname, con)
    for per in p_courses:
        err_msg = err_msg + main.insert_timetable(id, per, p_courses[per], p_rooms[per], year, con)
    return err_msg