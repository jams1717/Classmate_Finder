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

print(find_school_year(5, 5))
