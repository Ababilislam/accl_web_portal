from datetime import datetime

# def get_month_year_range(start_date, end_date):
#     # Parse the input date strings
#     start = datetime.strptime(start_date, '%Y-%m-%d')
#     end = datetime.strptime(end_date, '%Y-%m-%d')
    
#     # Initialize the list of month-year strings
#     month_year_range = []
    
#     # Iterate over the months between the start and end dates
#     current = start
#     while current <= end:
#         # Append the month-year string to the list
#         month_year_range.append(current.strftime('%b-%Y'))
#         # Move to the next month
#         if current.month == 12:
#             current = datetime(current.year + 1, 1, 1)
#         else:
#             current = datetime(current.year, current.month + 1, 1)
    
#     # Join the list into a single string
#     return ','.join(month_year_range)

# # Example usage
# start_date = '2024-08-01'
# end_date = '2024-09-30'
# print(get_month_year_range(start_date, end_date))





months_to_find = 'Aug-2024, Sep-2024'

months = {
    'month1' : 'Jul-2024',
    'month2' : 'Aug-2024',
    'month3' : 'Sep-2024',
    'month4' : 'Oct-2024',
    'month5' : 'Nov-2024',
    'month6' : 'Dec-2024',
    'month7' : 'Jan-2025',
    'month8' : 'Feb-2025',
    'month9' : 'Mar-2025',
    'month10' : 'Apr-2025',
    'month11' : 'May-2025',
    'month12' : 'Jun-2025',
    'month13' : 'Jul-2025',
    'month14' : 'Aug-2025',
    'month15' : 'Sep-2025',
    'month16' : 'Oct-2025',
    'month17' : 'Nov-2025',
    'month18' : 'Dec-2025'
    }

matching_keys = []
for key, value in months.items():
    if value in months_to_find:
        matching_keys.append(key)

print(matching_keys)



months = {
    'input1' : 'Jul-2024',
    'input2' : 'Aug-2024',
    'input3' : 'Sep-2024',
    'input4' : 'Oct-2024',
    'input5' : 'Nov-2024',
    'input6' : 'Dec-2024',
    'input7' : 'Jan-2025',
    'input8' : 'Feb-2025',
    'input9' : 'Mar-2025',
    'input10' : 'Apr-2025',
    'input11' : 'May-2025',
    'input12' : 'Jun-2025',
    'input13' : 'Jul-2025',
    'input14' : 'Aug-2025',
    'input15' : 'Sep-2025',
    'input16' : 'Oct-2025',
    'input17' : 'Nov-2025',
    'input18' : 'Dec-2025'
}