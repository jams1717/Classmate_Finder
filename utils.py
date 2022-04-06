def find_school_year(n = 5, offset = 0):
    from datetime import date
    year = date.today().year
    month = date.today().month
    if month <= 6:
        year_start = year-1
    if month > 6:
        year_start = year
    ans = []
    year_start = year_start + offset
    for x in range(n):
        ans.append(f'{year_start - x}-{year_start - x + 1}')
    return ans

def validate_data(firstname, lastname, p_courses = [], p_rooms = [], err_msg = ''):
    skip = False
    if firstname in ['', None]:
        skip = True
        err_msg = err_msg + f'<br> Please input first name.'
    if lastname in ['', None]:
        skip = True
        err_msg = err_msg + f'<br> Please input last name.'
    for per in p_courses:
        try:
            if p_rooms[per] in ['', None]:
                skip = True
                err_msg = err_msg + f'<br> Room not correctly filled out for period {per}.'
        except KeyError:
            skip = True
            err_msg = err_msg + f'<br> Room not correctly filled out for period {per}.'

    return skip, err_msg