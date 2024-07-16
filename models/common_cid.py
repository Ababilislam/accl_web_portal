import datetime

db = DAL('mysql://root:@localhost/accl')
mreporting_http_pass = 'abC321'
date_fixed = datetime.datetime.now() + datetime.timedelta(hours=6)
