from datetime import datetime, timedelta

#========================== FORCASTING HOME PAGE FOR REP =======================================#

def forcasting_for_mpo():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecasting'

        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        # DEFAULT DATE RANGE VALUE SET 
        op_date = '1990-01-01 00:00:00'.split(' ')[0]
        cl_date = '1990-01-01 00:00:00'.split(' ')[0]

        opening_date = datetime.strptime(op_date, "%Y-%m-%d").date()
        closing_date = datetime.strptime(cl_date, "%Y-%m-%d").date()

        # FORECAST DATE RANGE ----------------------------------------------------------------------
        current_date_window = datetime.strptime(current_month, "%Y-%m-%d")
        current_date_window = str(current_date_window).split(' ')[0]
        current_date_window = datetime.strptime(current_date_window, "%Y-%m-%d").date()

        get_forecast_window_sql = f"SELECT opening_date, closing_date FROM forecast_date_range WHERE cid = '{cid}' AND ym_date = (SELECT MAX(ym_date) FROM forecast_date_range WHERE cid = '{cid}');"
        get_forcast_window = db.executesql(get_forecast_window_sql, as_dict = True)

        if len(get_forcast_window) != 0:
            for i in range(len(get_forcast_window)):
                data = get_forcast_window[i]
                opening_date = str(data['opening_date']).strip()
                closing_date = str(data['closing_date']).strip()

                # Converting string to datetime object
                opening_date = datetime.strptime(opening_date, "%Y-%m-%d").date()
                closing_date = datetime.strptime(closing_date, "%Y-%m-%d").date()
        # ------------------------------------------------------------------------------------------
        
        if user_type == 'rep':
            all_forecast_sql = f"SELECT * FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY rep_id, first_date, item_code;"
            # all_forecast_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY rep_id, first_date, item_code;"
            all_forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

            length = 0
            if len(all_forecast_rec) != 0:
                check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                forecast_status = db.executesql(check_forcasting_status, as_dict=True)

                frcst_status = ''
                if len(forecast_status) != 0:
                    for f in range(len(forecast_status)):
                        forecast = forecast_status[f]
                        frcst_status = str(forecast['status']).upper().strip()

                if frcst_status == 'APPROVED':
                    session.approved_message = "Forecasting Approved"
                elif frcst_status == 'REJECTED':
                    session.rejected_message = "Forecasting Rejected. Please Resubmit."

                get_item_record_sql = "SELECT item_id, name, unit_type, price from sm_item where cid = '"+cid+"' group by item_id order by item_id;"
                get_item_record = db.executesql(get_item_record_sql, as_dict=True)
                
                return dict(length = length, status = frcst_status, current_date = current_date_window, opening_date = opening_date, closing_date = closing_date)

            else:
                forecast_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY rep_id, first_date, item_code;"
                forecast_rec = db.executesql(forecast_sql, as_dict=True)

                # length = 0
                if len(forecast_rec) == 0:
                    # check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    check_forcasting_status = f"SELECT status FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()

                    if frcst_status == 'APPROVED':
                        session.approved_message = "Forecasting Approved"
                    elif frcst_status == 'REJECTED':
                        session.rejected_message = "Forecasting Rejected. Please Resubmit."

                    get_item_record_sql = "SELECT item_id, name, unit_type, price from sm_item where cid = '"+cid+"' group by item_id order by item_id;"
                    get_item_record = db.executesql(get_item_record_sql, as_dict=True)
                    
                    return dict(length = length, status = frcst_status, current_date = current_date_window, opening_date = opening_date, closing_date = closing_date)

                else:
                    # check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    check_forcasting_status = f"SELECT status FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()

                    if frcst_status == 'APPROVED':
                        session.approved_message = "Forecasting Approved"
                    elif frcst_status == 'REJECTED':
                        session.rejected_message = "Forecasting Rejected. Please Resubmit."
                    
                    length += 1
                    return dict(length = length, status = frcst_status, current_date = current_date_window, opening_date = opening_date, closing_date = closing_date)


#========================== GENERATE FORCASTING CSV FILE =======================================#

def forcasting_csv_for_mpo():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid

        # area_id = ''
        area_name = ''

        rep_id = request.args(0)

        if rep_id == None:
            rep_id = session.user_id

        get_area_id_sql = f"SELECT * FROM sm_rep_area WHERE cid = '{cid}' AND rep_id = '{str(rep_id)}' GROUP BY rep_id LIMIT 1;"
        get_area_id = db.executesql(get_area_id_sql, as_dict=True)

        for a in range(len(get_area_id)):
            recordsStr = get_area_id[a]
            # area_id = str(recordsStr['area_id'])
            area_name = str(recordsStr['area_name'])

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        months.append(current_date.strftime("%b-%Y"))

        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        months = str(months).replace('[','').replace(']','').replace("'","")
        
        myString = f'Territory: {area_name} \n'
        myString += f'Planning Month: {planning_month} \n\n\n'
        myString += f'Item_Code,Description,UoM,{months}\n'  
    
        total=0
        attTime = ''
        totalCount = 0
        item_wise_total = 0
        month1_total = 0
        month2_total = 0
        month3_total = 0
        month4_total = 0
        month5_total = 0
        month6_total = 0
        month7_total = 0
        month8_total = 0
        month9_total = 0
        month10_total = 0
        month11_total = 0
        month12_total = 0
        month13_total = 0
        month14_total = 0
        month15_total = 0
        month16_total = 0
        month17_total = 0
        month18_total = 0
        count = 1
        forcasting_first_date = ''

        check_forecasting_sql = "SELECT * FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"'  AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"') GROUP BY rep_id, item_code, forcasting_first_date;"
        check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

        if len(check_forecasting) == 0 :
            temp_check_forecasting_sql = "SELECT * FROM forecast_mpo_temp WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"') GROUP BY rep_id, item_code, forcasting_first_date;"
            temp_check_forecasting = db.executesql(temp_check_forecasting_sql, as_dict=True) 

            if len(temp_check_forecasting) > 0 :
                for i in range(len(temp_check_forecasting)):
                    forecast_records_str = temp_check_forecasting[i]
                    
                    if i == 0:
                        i += 1
                        continue
                    
                    item_code = str(forecast_records_str['item_code'])
                    item_name = str(forecast_records_str['item_name'])
                    unit_type = str(forecast_records_str['UoM'])
                    forcasting_first_date = str(forecast_records_str['forcasting_first_date'])

                    # SHIFT 1 COLUMN LEFT FOR NEXT MONTH'S FORECASTING 
                    if planning_month != forcasting_first_date:
                        month1 = forecast_records_str['month2']
                        month2 = forecast_records_str['month3']
                        month3 = forecast_records_str['month4']
                        month4 = forecast_records_str['month5']
                        month5 = forecast_records_str['month6']
                        month6 = forecast_records_str['month7']
                        month7 = forecast_records_str['month8']
                        month8 = forecast_records_str['month9']
                        month9 = forecast_records_str['month10']
                        month10 = forecast_records_str['month11']
                        month11 = forecast_records_str['month12']
                        month12 = forecast_records_str['month13']
                        month13 = forecast_records_str['month14']
                        month14 = forecast_records_str['month15']
                        month15 = forecast_records_str['month16']
                        month16 = forecast_records_str['month17']
                        month17 = forecast_records_str['month18']
                        month18 = 0.0

                        month1_total += float(month1)
                        month2_total += float(month2)
                        month3_total += float(month3)
                        month4_total += float(month4)
                        month5_total += float(month5)
                        month6_total += float(month6)
                        month7_total += float(month7)
                        month8_total += float(month8)
                        month9_total += float(month9)
                        month10_total += float(month10)
                        month11_total += float(month11)
                        month12_total += float(month12)
                        month13_total += float(month13)
                        month14_total += float(month14)
                        month15_total += float(month15)
                        month16_total += float(month16)
                        month17_total += float(month17)
                        month18_total += float(month18)

                    else:
                        month1 = forecast_records_str['month1']
                        month2 = forecast_records_str['month2']
                        month3 = forecast_records_str['month3']
                        month4 = forecast_records_str['month4']
                        month5 = forecast_records_str['month5']
                        month6 = forecast_records_str['month6']
                        month7 = forecast_records_str['month7']
                        month8 = forecast_records_str['month8']
                        month9 = forecast_records_str['month9']
                        month10 = forecast_records_str['month10']
                        month11 = forecast_records_str['month11']
                        month12 = forecast_records_str['month12']
                        month13 = forecast_records_str['month13']
                        month14 = forecast_records_str['month14']
                        month15 = forecast_records_str['month15']
                        month16 = forecast_records_str['month16']
                        month17 = forecast_records_str['month17']
                        month18 = forecast_records_str['month18']

                        month1_total += float(month1)
                        month2_total += float(month2)
                        month3_total += float(month3)
                        month4_total += float(month4)
                        month5_total += float(month5)
                        month6_total += float(month6)
                        month7_total += float(month7)
                        month8_total += float(month8)
                        month9_total += float(month9)
                        month10_total += float(month10)
                        month11_total += float(month11)
                        month12_total += float(month12)
                        month13_total += float(month13)
                        month14_total += float(month14)
                        month15_total += float(month15)
                        month16_total += float(month16)
                        month17_total += float(month17)
                        month18_total += float(month18)

                    # item_wise_total = int(float(month1)) + int(float(month2))+int(float(month3)) + int(float(month4))+int(float(month5)) + int(float(month6))+int(float(month7)) + int(float(month8))+int(float(month9)) + int(float(month10))+int(float(month11)) + int(float(month12))+int(float(month13)) + int(float(month14))+int(float(month15)) + int(float(month16))+int(float(month17)) + int(float(month18))

                    i += 1

                    # myString += str(item_code) + ',' + str(item_name) + ',' + str(unit_type) + ',' + str(int(float(month1))) + ',' + str(int(float(month2))) + ',' + str(int(float(month3))) + ',' + str(int(float(month4))) + ',' + str(int(float(month5))) + ',' + str(int(float(month6))) + ',' + str(int(float(month7))) + ',' + str(int(float(month8))) + ',' + str(int(float(month9))) + ',' + str(int(float(month10))) + ',' + str(int(float(month11))) + ',' + str(int(float(month12))) + ',' + str(int(float(month13))) + ',' + str(int(float(month14))) + ',' + str(int(float(month15))) + ',' + str(int(float(month16))) + ',' + str(int(float(month17))) + ',' + str(int(float(month18)))+',\n'

                    myString += str(item_code) + ',' + str(item_name) + ',' + str(unit_type) + ',' + str(round(float(month1),2)) + ',' + str(round(float(month2),2)) + ',' + str(round(float(month3),2)) + ',' + str(round(float(month4),2)) + ',' + str(round(float(month5),2)) + ',' + str(round(float(month6),2)) + ',' + str(round(float(month7),2)) + ',' + str(round(float(month8),2)) + ',' + str(round(float(month9),2)) + ',' + str(round(float(month10),2)) + ',' + str(round(float(month11),2)) + ',' + str(round(float(month12),2)) + ',' + str(round(float(month13),2)) + ',' + str(round(float(month14),2)) + ',' + str(round(float(month15),2)) + ',' + str(round(float(month16),2)) + ',' + str(round(float(month17),2)) + ',' + str(round(float(month18),2))+',\n'

                    # myString += '' + ',' + '' + ',' + '' + ',' + str(month1) + ',' + str(month2) + ',' + str(month3) + ',' + str(month4) + ',' + str(month5) + ',' + str(month6) + ',' + str(month7) + ',' + str(month8) + ',' + str(month9) + ',' + str(month10) + ',' + str(month11) + ',' + str(month12) + ',' + str(month13) + ',' + str(month14) + ',' + str(month15) + ',' + str(month16) + ',' + str(month17) + ',' + str(month18)+',\n'

                    # myString += '' + ',' + '' + ',' + '' + ',' + str(month1_total) + ',' + str(month2_total) + ',' + str(month3_total) + ',' + str(month4_total) + ',' + str(month5_total) + ',' + str(month6_total) + ',' + str(month7_total) + ',' + str(month8_total) + ',' + str(month9_total) + ',' + str(month10_total) + ',' + str(month11_total) + ',' + str(month12_total) + ',' + str(month13_total) + ',' + str(month14_total) + ',' + str(month15_total) + ',' + str(month16_total) + ',' + str(month17_total) + ',' + str(month18_total)+',\n'

            else:
                get_item_record_sql = "SELECT item_id, name, unit_type, price from sm_item where cid = '"+cid+"' group by item_id order by item_id;"
                get_item_record = db.executesql(get_item_record_sql, as_dict=True)

                for i in range(len(get_item_record)):
                    recordsStr = get_item_record[i]
                    item_id = str(recordsStr['item_id'])
                    name = str(recordsStr['name'])
                    unit_type = str(recordsStr['unit_type'])
                    price = str(recordsStr['price'])
                    
                    myString += str(item_id) + ',' + str(name) + ',' + str(unit_type) + ',\n'

        else:
            for i in range(len(check_forecasting)):
                forecast_records_str = check_forecasting[i]
                
                if i == 0:
                    i += 1
                    continue
                
                item_code = str(forecast_records_str['item_code'])
                item_name = str(forecast_records_str['item_name'])
                unit_type = str(forecast_records_str['UoM'])
                forcasting_first_date = str(forecast_records_str['forcasting_first_date'])

                if planning_month != forcasting_first_date:
                    month1 = forecast_records_str['month2']
                    month2 = forecast_records_str['month3']
                    month3 = forecast_records_str['month4']
                    month4 = forecast_records_str['month5']
                    month5 = forecast_records_str['month6']
                    month6 = forecast_records_str['month7']
                    month7 = forecast_records_str['month8']
                    month8 = forecast_records_str['month9']
                    month9 = forecast_records_str['month10']
                    month10 = forecast_records_str['month11']
                    month11 = forecast_records_str['month12']
                    month12 = forecast_records_str['month13']
                    month13 = forecast_records_str['month14']
                    month14 = forecast_records_str['month15']
                    month15 = forecast_records_str['month16']
                    month16 = forecast_records_str['month17']
                    month17 = forecast_records_str['month18']
                    month18 = 0.0

                    month1_total += float(month1)
                    month2_total += float(month2)
                    month3_total += float(month3)
                    month4_total += float(month4)
                    month5_total += float(month5)
                    month6_total += float(month6)
                    month7_total += float(month7)
                    month8_total += float(month8)
                    month9_total += float(month9)
                    month10_total += float(month10)
                    month11_total += float(month11)
                    month12_total += float(month12)
                    month13_total += float(month13)
                    month14_total += float(month14)
                    month15_total += float(month15)
                    month16_total += float(month16)
                    month17_total += float(month17)
                    month18_total += float(month18)

                else:
                    month1 = forecast_records_str['month1']
                    month2 = forecast_records_str['month2']
                    month3 = forecast_records_str['month3']
                    month4 = forecast_records_str['month4']
                    month5 = forecast_records_str['month5']
                    month6 = forecast_records_str['month6']
                    month7 = forecast_records_str['month7']
                    month8 = forecast_records_str['month8']
                    month9 = forecast_records_str['month9']
                    month10 = forecast_records_str['month10']
                    month11 = forecast_records_str['month11']
                    month12 = forecast_records_str['month12']
                    month13 = forecast_records_str['month13']
                    month14 = forecast_records_str['month14']
                    month15 = forecast_records_str['month15']
                    month16 = forecast_records_str['month16']
                    month17 = forecast_records_str['month17']
                    month18 = forecast_records_str['month18']

                    month1_total += float(month1)
                    month2_total += float(month2)
                    month3_total += float(month3)
                    month4_total += float(month4)
                    month5_total += float(month5)
                    month6_total += float(month6)
                    month7_total += float(month7)
                    month8_total += float(month8)
                    month9_total += float(month9)
                    month10_total += float(month10)
                    month11_total += float(month11)
                    month12_total += float(month12)
                    month13_total += float(month13)
                    month14_total += float(month14)
                    month15_total += float(month15)
                    month16_total += float(month16)
                    month17_total += float(month17)
                    month18_total += float(month18)

                # item_wise_total = int(float(month1)) + int(float(month2))+int(float(month3)) + int(float(month4))+int(float(month5)) + int(float(month6))+int(float(month7)) + int(float(month8))+int(float(month9)) + int(float(month10))+int(float(month11)) + int(float(month12))+int(float(month13)) + int(float(month14))+int(float(month15)) + int(float(month16))+int(float(month17)) + int(float(month18))

                i += 1

                myString += str(item_code) + ',' + str(item_name) + ',' + str(unit_type) + ',' + str(round(float(month1),2)) + ',' + str(round(float(month2),2)) + ',' + str(round(float(month3),2)) + ',' + str(round(float(month4),2)) + ',' + str(round(float(month5),2)) + ',' + str(round(float(month6),2)) + ',' + str(round(float(month7),2)) + ',' + str(round(float(month8),2)) + ',' + str(round(float(month9),2)) + ',' + str(round(float(month10),2)) + ',' + str(round(float(month11),2)) + ',' + str(round(float(month12),2)) + ',' + str(round(float(month13),2)) + ',' + str(round(float(month14),2)) + ',' + str(round(float(month15),2)) + ',' + str(round(float(month16),2)) + ',' + str(round(float(month17),2)) + ',' + str(round(float(month18),2))+',\n'
        
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=mpo_forecasting_file.csv'
        return str(myString)
 

#========================== UPLOAD FORCASTING CSV FILE FOR MPO =======================================#

def forcasting_csv_upload_for_mpo():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        import csv
        import io

        # GET SUBMITTED DATE
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]
        current_date_yr = datetime.strptime(current_month, "%Y-%m-%d")
        first_month = current_date_yr.strftime("%b-%Y")
        # current_date = datetime.strptime(current_month, "%Y-%m-%d")

        months = []
        months.append(current_date_yr.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date_yr += timedelta(days=30)
            if str(current_date_yr) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date_yr.strftime("%b-%Y"))
    
        uuploaded_file = request.vars.csvFile.file
        text_file = io.TextIOWrapper(uuploaded_file, encoding='utf-8')
        csv_reader = csv.reader(text_file)

        cid = session.cid
        rep_id = session.user_id
        rep_name = ''
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''

        if session.user_type == 'rep':
            # check_forecasting_sql = "SELECT * FROM  forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND date(submitted_date) <= '"+str(current_month)+"' GROUP BY rep_id, item_code, forcasting_first_date;"
            # check_forecasting_sql = "SELECT * FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND forcasting_first_date = '"+str(submitted_first_date)+"' GROUP BY rep_id, item_code, forcasting_first_date;"
            check_forecasting_sql = "SELECT * FROM forecast_mpo_temp WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND forcasting_first_date = '"+str(submitted_first_date)+"' GROUP BY rep_id, item_code, forcasting_first_date;"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

        # elif session.user_type == 'sup':
        #     check_forecasting_sql = "SELECT * FROM  forecast_am WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' AND forcasting_first_date = '"+str(submitted_first_date)+"' GROUP BY sup_id, item_code, forcasting_first_date;"
        #     check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)
        
        if len(check_forecasting) == 0:
            # if session.user_type == 'sup':
            #     get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            #     get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
            #     for a in range(len(get_level_depth)):
            #         records = get_level_depth[a]
            #         sup_name = records['sup_name']
            #         level_id = records['level_id']
            #         level_depth = records['level_depth_no']

            #     get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            #     get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            #     for a in range(len(get_level_records)):
            #         records_level = get_level_records[a]
            #         level0  = records_level['level0']
            #         level0_name = records_level['level0_name']
            #         level1  = records_level['level1']
            #         level1_name = records_level['level1_name']
            #         level2  = records_level['level2']
            #         level2_name = records_level['level2_name']
            #         level3  = records_level['level3']
            #         level3_name = records_level['level3_name']

            if session.user_type == 'rep':
                get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' LIMIT 1;"
                get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
                for a in range(len(get_level_depth)):
                    records = get_level_depth[a]
                    rep_name = records['rep_name']
                    area_id = records['area_id']

                get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
                get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                for a in range(len(get_level_records)):
                    records_level = get_level_records[a]
                    level0  = records_level['level0']
                    level0_name = records_level['level0_name']
                    level1  = records_level['level1']
                    level1_name = records_level['level1_name']
                    level2  = records_level['level2']
                    level2_name = records_level['level2_name']
                    level3  = records_level['level3']
                    level3_name = records_level['level3_name']

            # myString = ''
            planning_month_str = ''

            i = 1
            for row in csv_reader:
                if i <= 4:
                    if i == 2:
                        planning_month_str = row[0]

                    i += 1
                    continue

                item_code = row[0]
                item_name = row[1]
                UoM = row[2]
                month1 = row[3]
                month2 = row[4]
                month3 = row[5]
                month4 = row[6]
                month5 = row[7]
                month6 = row[8]
                month7 = row[9]
                month8 = row[10]
                month9 = row[11]
                month10 = row[12]
                month11 = row[13]
                month12 = row[14]
                month13 = row[15]
                month14 = row[16]
                month15 = row[17]
                month16 = row[18]
                month17 = row[19]
                month18 = row[20]

                # key = str(planning_month.split(':')[0])
                planning_month = str(planning_month_str.split(':')[1]).strip()

                # TO GET CURRENT FORECASTING MONTH IN CASE PREVIOUS MONTH'S EXCEL FILE UPLOADED
                if planning_month != submitted_first_date:
                    forecasting_first_date = submitted_first_date

                else:
                    month1 = str(month1).strip()
                    if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                        forecasting_first_date="2024-01-01"
                    elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                        forecasting_first_date="2024-02-01"
                    elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                        forecasting_first_date="2024-03-01"
                    elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                        forecasting_first_date="2024-04-01"
                    elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                        forecasting_first_date="2024-05-01"
                    elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                        forecasting_first_date="2024-06-01"
                    elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                        forecasting_first_date="2024-07-01"
                    elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                        forecasting_first_date="2024-08-01"
                    elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                        forecasting_first_date="2024-09-01"
                    elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                        forecasting_first_date="2024-10-01"
                    elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                        forecasting_first_date="2024-11-01"
                    elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                        forecasting_first_date="2024-12-01"
                
                # SHIFT 1 COLUMN LEFT FOR NEXT MONTH'S FORECASTING 
                if planning_month != forecasting_first_date:
                    month1 = row[4]
                    month2 = row[5]
                    month3 = row[6]
                    month4 = row[7]
                    month5 = row[8]
                    month6 = row[9]
                    month7 = row[10]
                    month8 = row[11]
                    month9 = row[12]
                    month10 = row[13]
                    month11 = row[14]
                    month12 = row[15]
                    month13 = row[16]
                    month14 = row[17]
                    month15 = row[18]
                    month16 = row[19]
                    month17 = row[20]
                    month18 = '0'

                # return month1
                # DYNAMIC FIRST DATE GENERATION
                # month1 = str(month1).strip()
                # month1_date_obj = datetime.strptime(month1, '%b-%Y')
                # no_of_month = month1_date_obj.month

                # for m in range(1, 13):
                #     if m == no_of_month:
                #         if m <= 9:
                #             forecasting_first_date = f"{year}-0{m}-01"
                #         else:
                #             forecasting_first_date = f"{year}-{m}-01"

                status = "SUBMITTED"
                # price = 0

                if i == 5:
                    item_code = ''
                    item_name = ''
                    UoM = ''
                
                else:
                    get_item_price_sql = "SELECT item_id, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_code)+"' GROUP BY item_id LIMIT 1;"
                    get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                    for a in range(len(get_item_price)):
                        item_record = get_item_price[a]
                        price = item_record['price']

                    # month1_p = (float(month1) * float(price))
                    # month2_p = (float(month2) * float(price))
                    # month3_p = (float(month3) * float(price))
                    # month4_p = (float(month4) * float(price))
                    # month5_p = (float(month5) * float(price))
                    # month6_p = (float(month6) * float(price))
                    # month7_p = (float(month7) * float(price))
                    # month8_p = (float(month8) * float(price))
                    # month9_p = (float(month9) * float(price))
                    # month10_p = (float(month10) * float(price))
                    # month11_p = (float(month11) * float(price))
                    # month12_p = (float(month12) * float(price))
                    # month13_p = (float(month13) * float(price))
                    # month14_p = (float(month14) * float(price))
                    # month15_p = (float(month15) * float(price))
                    # month16_p = (float(month16) * float(price))
                    # month17_p = (float(month17) * float(price))
                    # month18_p = (float(month18) * float(price))

                if session.user_type == 'rep':
                    try:
                        parts = month1.split('-')
                        if len(parts) == 2:
                            # year_xx = int(parts[1]) 
                            
                            if month18 == '0':
                                month18 = str(months[17])
                            
                            # month name insert sql 
                            insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status,created_by) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"','"+str(rep_id)+"')"

                        else:
                            raise ValueError("Invalid month format")
                        
                    except ValueError:
                        try:
                            # numeric_value = int(float(month1))
                            month1 = round(float(month1), 2)
                            month2 = round(float(month2), 2)
                            month3 = round(float(month3), 2)
                            month4 = round(float(month4), 2)
                            month5 = round(float(month5), 2)
                            month6 = round(float(month6), 2)
                            month7 = round(float(month7), 2)
                            month8 = round(float(month8), 2)
                            month9 = round(float(month9), 2)
                            month10 = round(float(month10), 2)
                            month11 = round(float(month11), 2)
                            month12 = round(float(month12), 2)
                            month13 = round(float(month13), 2)
                            month14 = round(float(month14), 2)
                            month15 = round(float(month15), 2)
                            month16 = round(float(month16), 2)
                            month17 = round(float(month17), 2)
                            month18 = round(float(month18), 2)

                            insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status,created_by) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"','"+str(rep_id)+"')"

                        except ValueError:
                            return None
                        
                    db.executesql(insert_forcasting_header_sql)

                # elif session.user_type == 'sup':
                #     try:
                #         parts = month1.split('-')
                #         if len(parts) == 2:
                #             # year_xx = int(parts[1])

                #             return month17

                #             # month name insert sql 
                #             insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                #         else:
                #             raise ValueError("Invalid month format")

                #     except ValueError:
                #         try:
                #             # numeric_value = int(float(month1))
                #             insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"

                #         except ValueError:
                #             return None
                    
                #     db.executesql(insert_forcasting_header_sql)

                i += 1
                
            session.upload_flash = "File Uploaded Successfully"

        else:
            session.error_flash = "File Already Uploaded Once"


        # if session.user_type == 'rep':
        redirect(URL('forcasting','forcasting_for_mpo'))
        # else:
        #     redirect(URL('forcasting','forcasting_for_sup'))

        # return dict()


#========================== GENERATE MPO FORCASTING CSV FILE FOR SUP =======================================#

def forcasting_csv_download_for_mpo():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        user_id = session.user_id

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))

        months = str(months).replace('[','').replace(']','').replace("'","")

        myString = f'Territory: CP\n'
        myString += f'Planning Month: {planning_month} \n\n\n'
        myString += f'Item_Code,Description,UoM,{months}\n'

        total = 0
        attTime = ''
        totalCount = 0
        item_wise_total = 0
        month1_total = 0
        month2_total = 0
        month3_total = 0
        month4_total = 0
        month5_total = 0
        month6_total = 0
        month7_total = 0
        month8_total = 0
        month9_total = 0
        month10_total = 0
        month11_total = 0
        month12_total = 0
        month13_total = 0
        month14_total = 0
        month15_total = 0
        month16_total = 0
        month17_total = 0
        month18_total = 0

        mpo_rep_id = request.args[0]

        # check_forecasting_sql = "SELECT * FROM  forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(mpo_rep_id)+"' AND date(submitted_date) <= '"+str(current_month)+"' GROUP BY rep_id, item_code, forcasting_first_date;"
        # check_forecasting_sql = "SELECT * FROM  forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(mpo_rep_id)+"' AND date(forcasting_first_date) <= '"+str(current_month)+"' GROUP BY rep_id, item_code, forcasting_first_date;"
        # check_forecasting_sql = "SELECT * FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(mpo_rep_id)+"' AND date(forcasting_first_date) <= '"+str(current_month)+"' GROUP BY rep_id, item_code, forcasting_first_date ORDER BY first_date ASC;"
        check_forecasting_sql = "SELECT * FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id = '"+str(mpo_rep_id)+"' AND forcasting_first_date = '"+str(planning_month)+"' GROUP BY rep_id, item_code, forcasting_first_date ORDER BY item_code;"
        # return check_forecasting_sql
        check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

        # count = 1

        if len(check_forecasting) > 0:
            # for loop for calculating column price total
            for i in range(len(check_forecasting)):
                forecast_records_str = check_forecasting[i]

                if i == 0:
                    i += 1
                    continue

                item_code = str(forecast_records_str['item_code'])
                item_name = str(forecast_records_str['item_name'])
                unit_type = str(forecast_records_str['UoM'])
                month1 = forecast_records_str['month1']
                month2 = forecast_records_str['month2']
                month3 = forecast_records_str['month3']
                month4 = forecast_records_str['month4']
                month5 = forecast_records_str['month5']
                month6 = forecast_records_str['month6']
                month7 = forecast_records_str['month7']
                month8 = forecast_records_str['month8']
                month9 = forecast_records_str['month9']
                month10 = forecast_records_str['month10']
                month11 = forecast_records_str['month11']
                month12 = forecast_records_str['month12']
                month13 = forecast_records_str['month13']
                month14 = forecast_records_str['month14']
                month15 = forecast_records_str['month15']
                month16 = forecast_records_str['month16']
                month17 = forecast_records_str['month17']
                month18 = forecast_records_str['month18']

                try:
                    parts = month1.split('-')
                    if len(parts) == 2:
                        i += 1
                        continue
                    else:
                        raise ValueError("Invalid format")

                except ValueError:
                    try:
                        get_item_price_sql = "SELECT item_id, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_code)+"' GROUP BY item_id LIMIT 1;"
                        get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                        for a in range(len(get_item_price)):
                            item_record = get_item_price[a]
                            conv_factor = item_record['conv_factor']
                            price = item_record['price']

                            month1_total += round(float(month1) * (float(price)/float(conv_factor)), 2)
                            month2_total += round(float(month2) * (float(price)/float(conv_factor)), 2)
                            month3_total += round(float(month3) * (float(price)/float(conv_factor)), 2)
                            month4_total += round(float(month4) * (float(price)/float(conv_factor)), 2)
                            month5_total += round(float(month5) * (float(price)/float(conv_factor)), 2)
                            month6_total += round(float(month6) * (float(price)/float(conv_factor)), 2)
                            month7_total += round(float(month7) * (float(price)/float(conv_factor)), 2)
                            month8_total += round(float(month8) * (float(price)/float(conv_factor)), 2)
                            month9_total += round(float(month9) * (float(price)/float(conv_factor)), 2)
                            month10_total += round(float(month10) * (float(price)/float(conv_factor)), 2)
                            month11_total += round(float(month11) * (float(price)/float(conv_factor)), 2)
                            month12_total += round(float(month12) * (float(price)/float(conv_factor)), 2)
                            month13_total += round(float(month13) * (float(price)/float(conv_factor)), 2)
                            month14_total += round(float(month14) * (float(price)/float(conv_factor)), 2)
                            month15_total += round(float(month15) * (float(price)/float(conv_factor)), 2)
                            month16_total += round(float(month16) * (float(price)/float(conv_factor)), 2)
                            month17_total += round(float(month17) * (float(price)/float(conv_factor)), 2)
                            month18_total += round(float(month18) * (float(price)/float(conv_factor)), 2)

                        item_wise_total = float(month1) + float(month2)+float(month3) + float(month4)+float(month5) + float(month6)+float(month7) + float(month8)+float(month9) + float(month10)+float(month11) + float(month12)+float(month13) + float(month14)+float(month15) + float(month16)+float(month17) + float(month18)

                    except ValueError:
                        return None
                
                i += 1

            myString += '' + ',' + '' + ',' + '' + ',' + str(round(month1_total, 2))+ ',' + str(round(month2_total, 2))+ ',' + str(round(month3_total, 2))+ ',' + str(round(month4_total, 2))+ ',' + str(round(month5_total, 2))+ ',' + str(round(month6_total, 2))+ ',' + str(round(month7_total, 2))+ ',' + str(round(month8_total, 2))+ ',' + str(round(month9_total, 2))+ ',' + str(round(month10_total, 2)) + ',' + str(round(month11_total, 2)) + ',' + str(round(month12_total, 2)) + ',' + str(round(month13_total, 2)) + ',' + str(round(month14_total, 2)) + ',' + str(round(month15_total, 2)) + ',' + str(round(month16_total, 2)) + ',' + str(round(month17_total, 2)) + ',' + str(round(month18_total, 2))+',\n'


        if len(check_forecasting) > 0:
            item_wise_total = 0

            # for loop for item column data
            for i in range(len(check_forecasting)):
                forecast_records_str = check_forecasting[i]

                if i == 0:
                    i += 1
                    continue

                item_code = str(forecast_records_str['item_code'])
                item_name = str(forecast_records_str['item_name'])
                unit_type = str(forecast_records_str['UoM'])
                month1 = forecast_records_str['month1']
                month2 = forecast_records_str['month2']
                month3 = forecast_records_str['month3']
                month4 = forecast_records_str['month4']
                month5 = forecast_records_str['month5']
                month6 = forecast_records_str['month6']
                month7 = forecast_records_str['month7']
                month8 = forecast_records_str['month8']
                month9 = forecast_records_str['month9']
                month10 = forecast_records_str['month10']
                month11 = forecast_records_str['month11']
                month12 = forecast_records_str['month12']
                month13 = forecast_records_str['month13']
                month14 = forecast_records_str['month14']
                month15 = forecast_records_str['month15']
                month16 = forecast_records_str['month16']
                month17 = forecast_records_str['month17']
                month18 = forecast_records_str['month18']

                # return item_code

                # month1_total += float(month1)
                # month2_total += float(month2)
                # month3_total += float(month3)
                # month4_total += float(month4)
                # month5_total += float(month5)
                # month6_total += float(month6)
                # month7_total += float(month7)
                # month8_total += float(month8)
                # month9_total += float(month9)
                # month10_total += float(month10)
                # month11_total += float(month11)
                # month12_total += float(month12)
                # month13_total += float(month13)
                # month14_total += float(month14)
                # month15_total += float(month15)
                # month16_total += float(month16)
                # month17_total += float(month17)
                # month18_total += float(month18)

                try:
                    parts = month1.split('-')
                    if len(parts) == 2:
                        i += 1
                        continue
                    else:
                        raise ValueError("Invalid format")

                except ValueError:
                    try:
                        item_wise_total = float(month1) + float(month2) + float(month3) + float(month4) + float(month5) + float(month6) + float(month7) + float(month8) + float(month9) + float(month10) + float(month11) + float(month12) + float(month13) + float(month14) + float(month15) + float(month16) + float(month17) + float(month18)
                    
                    except ValueError:
                        return None
                    
                i += 1

                myString += str(item_code) + ',' + str(item_name) + ',' + str(unit_type) + ',' + str(int(float(month1))) + ',' + str(int(float(month2))) + ',' + str(int(float(month3))) + ',' + str(int(float(month4))) + ',' + str(int(float(month5))) + ',' + str(int(float(month6))) + ',' + str(int(float(month7))) + ',' + str(int(float(month8))) + ',' + str(int(float(month9))) + ',' + str(int(float(month10))) + ',' + str(int(float(month11))) + ',' + str(int(float(month12))) + ',' + str(int(float(month13))) + ',' + str(int(float(month14))) + ',' + str(int(float(month15))) + ',' + str(int(float(month16))) + ',' + str(int(float(month17))) + ',' + str(int(float(month18)))+',' + str(int(float(item_wise_total)))+',\n'
    
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=mpo_forcasting_file.csv'

        return str(myString)


#========================== FORCASTING SUBMIT FOR SUP =======================================#

def forcasting_submit_for_sup():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        # user_id = session.user_id
        # return 'forecast submit sup'

        mpo_id_list = request.vars.mpo_list
        first_date_of_month = session.first_date_of_month

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        area_name = ''
        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))

        months = str(months).replace('[','').replace(']','').replace("'","")
        myString = f'Area: {area_name} \n'
        myString += f'Planning Month: {planning_month} \n\n\n'
        myString += f'Item_Code,Description,UoM,{months}\n'
        # return myString

        month1_total = 0
        month2_total = 0
        month3_total = 0
        month4_total = 0
        month5_total = 0
        month6_total = 0
        month7_total = 0
        month8_total = 0
        month9_total = 0
        month10_total = 0
        month11_total = 0
        month12_total = 0
        month13_total = 0
        month14_total = 0
        month15_total = 0
        month16_total = 0
        month17_total = 0
        month18_total = 0
        count = 1

        check_forcasting_for_mpo_sql = "SELECT item_code, item_name, UoM, SUM(month1) AS month1, SUM(month2) AS month2, SUM(month3) AS month3, SUM(month4) AS month4, SUM(month5) AS month5, SUM(month6) AS month6, SUM(month7) AS month7, SUM(month8) AS month8, SUM(month9) AS month9, SUM(month10) AS month10, SUM(month11) AS month11, SUM(month12) AS month12, SUM(month13) AS month13, SUM(month14) AS month14, SUM(month15) AS month15, SUM(month16) AS month16, SUM(month17) AS month17, SUM(month18) AS month18 FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id IN ("+str(mpo_id_list)+") AND submitted_date in (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '"+cid+"' and rep_id in ("+str(mpo_id_list)+") GROUP by rep_id) AND status = 'APPROVED' GROUP BY item_code;"
        # return check_forcasting_for_mpo_sql
        check_forcasting_for_mpo = db.executesql(check_forcasting_for_mpo_sql, as_dict = True)
        
        # for column data
        if len(check_forcasting_for_mpo) > 0 :
            for i in range(len(check_forcasting_for_mpo)):
                forecast_records_str = check_forcasting_for_mpo[i]
                if i == 0:
                    i += 1
                    continue

                item_code = str(forecast_records_str['item_code'])
                item_name = str(forecast_records_str['item_name'])
                unit_type = str(forecast_records_str['UoM'])
                month1 = forecast_records_str['month1']
                month2 = forecast_records_str['month2']
                month3 = forecast_records_str['month3']
                month4 = forecast_records_str['month4']
                month5 = forecast_records_str['month5']
                month6 = forecast_records_str['month6']
                month7 = forecast_records_str['month7']
                month8 = forecast_records_str['month8']
                month9 = forecast_records_str['month9']
                month10 = forecast_records_str['month10']
                month11 = forecast_records_str['month11']
                month12 = forecast_records_str['month12']
                month13 = forecast_records_str['month13']
                month14 = forecast_records_str['month14']
                month15 = forecast_records_str['month15']
                month16 = forecast_records_str['month16']
                month17 = forecast_records_str['month17']
                month18 = forecast_records_str['month18']
                
                try:
                    month1_total += float(month1)
                    month2_total += float(month2)
                    month3_total += float(month3)
                    month4_total += float(month4)
                    month5_total += float(month5)
                    month6_total += float(month6)
                    month7_total += float(month7)
                    month8_total += float(month8)
                    month9_total += float(month9)
                    month10_total += float(month10)
                    month11_total += float(month11)
                    month12_total += float(month12)
                    month13_total += float(month13)
                    month14_total += float(month14)
                    month15_total += float(month15)
                    month16_total += float(month16)
                    month17_total += float(month17)
                    month18_total += float(month18)

                except:
                    pass

                i += 1

                myString += str(item_code) + ',' + str(item_name) + ',' + str(unit_type) + ',' + str(int(float(month1))) + ',' + str(int(float(month2))) + ',' + str(int(float(month3))) + ',' + str(int(float(month4))) + ',' + str(int(float(month5))) + ',' + str(int(float(month6))) + ',' + str(int(float(month7))) + ',' + str(int(float(month8))) + ',' + str(int(float(month9))) + ',' + str(int(float(month10))) + ',' + str(int(float(month11))) + ',' + str(int(float(month12))) + ',' + str(int(float(month13))) + ',' + str(int(float(month14))) + ',' + str(int(float(month15))) + ',' + str(int(float(month16))) + ',' + str(int(float(month17))) + ',' + str(int(float(month18)))+',\n'
                # return myString
        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename=final_forecasting_file.csv'
        return str(myString)


#========================== FORCASTING HOME PAGE FOR SUP =======================================#

def forcasting_for_sup():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecasting'

        cid = session.cid
        user_id = session.user_id
        # user_type = session.user_type

        current_date = str(date_fixed).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
        year = current_date.year
        month = current_date.month
        first_date_of_month = str(datetime(year, month, 1)).split(' ')[0]
        session.first_date_of_month = first_date_of_month

        # DEFAULT DATE RANGE VALUE SET 
        op_date = '1990-01-01 00:00:00'.split(' ')[0]
        cl_date = '1990-01-01 00:00:00'.split(' ')[0]

        opening_date = datetime.strptime(op_date, "%Y-%m-%d").date()
        closing_date = datetime.strptime(cl_date, "%Y-%m-%d").date()

        # FORECAST DATE RANGE ----------------------------------------------------------------------
        current_date_window = datetime.strptime(current_month, "%Y-%m-%d")
        current_date_window = str(current_date_window).split(' ')[0]
        current_date_window = datetime.strptime(current_date_window, "%Y-%m-%d").date()

        get_forecast_window_sql = f"SELECT opening_date, closing_date FROM forecast_date_range WHERE cid = '{cid}' AND ym_date = (SELECT MAX(ym_date) FROM forecast_date_range WHERE cid = '{cid}');"
        get_forcast_window = db.executesql(get_forecast_window_sql, as_dict = True)

        if len(get_forcast_window) != 0:
            for i in range(len(get_forcast_window)):
                data = get_forcast_window[i]
                opening_date = str(data['opening_date']).strip()
                closing_date = str(data['closing_date']).strip()

                # Converting string to datetime object
                opening_date = datetime.strptime(opening_date, "%Y-%m-%d").date()
                closing_date = datetime.strptime(closing_date, "%Y-%m-%d").date()
        # ------------------------------------------------------------------------------------------

        level_id= ''
        depth = 0
        territory_list = []
        level_list = []
        get_rep_list = ''
        check_supervisor_level_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' GROUP BY sup_id LIMIT 1 ;"
        check_supervisor_level = db.executesql(check_supervisor_level_sql, as_dict = True)

        if len(check_supervisor_level):
            for s in range(len(check_supervisor_level)):
                level_records = check_supervisor_level[s]
                level_id = level_records['level_id']
                depth = level_records['level_depth_no']

            session.level_id = level_id
            session.level_depth = depth

            if depth == 2:
                check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level2 = '"+str(level_id)+"' AND is_leaf = '1' GROUP BY level0, level1, level2, level3;"
                check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

                if len(check_territory_level):
                    for s in range(len(check_territory_level)):
                        level2_records = check_territory_level[s]
                        level_id = level2_records['level3']
                        level_name = level2_records['level3_name']
                        territory_list.append(level_id)

                territory_list = str(territory_list).replace('[','').replace(']','')            
                get_rep_list_sql = "SELECT * FROM sm_rep_area WHERE cid = '"+cid+"' AND area_id IN ("+str(territory_list)+") GROUP BY rep_id;"
                get_rep_list = db.executesql(get_rep_list_sql, as_dict = True)
            
                return dict(get_rep_list = get_rep_list, first_date_of_month = first_date_of_month, current_date = current_date_window, opening_date = opening_date, closing_date = closing_date)
            
            elif depth == 1:
                check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND parent_level_id = '"+str(level_id)+"' AND level1 = '"+str(level_id)+"' AND is_leaf = '0' GROUP BY level0, level1, level2, level3;"
                check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

                if len(check_territory_level):
                    for s in range(len(check_territory_level)):
                        level1_records = check_territory_level[s]
                        level_id = level1_records['level2']
                        level_name = level1_records['level2_name']
                        level_list.append(level_id)

                level_list = str(level_list).replace('[','').replace(']','')            
                get_sup_list_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND level_id IN ("+str(level_list)+") GROUP BY sup_id;"
                get_sup_list = db.executesql(get_sup_list_sql, as_dict = True)

                return dict(get_sup_list = get_sup_list, first_date_of_month = first_date_of_month, current_date = current_date_window, opening_date = opening_date, closing_date = closing_date)

            elif depth == 0:
                check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND parent_level_id = '"+str(level_id)+"' AND level0 = '"+str(level_id)+"' AND is_leaf = '0' GROUP BY level0, level1, level2, level3;"
                check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

                if len(check_territory_level):
                    for s in range(len(check_territory_level)):
                        level0_records = check_territory_level[s]
                        level_id = level0_records['level1']
                        level_name = level0_records['level1_name']
                        level_list.append(level_id)
            
                level_list = str(level_list).replace('[','').replace(']','')            
                get_sup_list_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND level_id IN ("+str(level_list)+") GROUP BY sup_id;"
                get_sup_list = db.executesql(get_sup_list_sql, as_dict = True)

                return dict(get_sup_list = get_sup_list, first_date_of_month = first_date_of_month, current_date = current_date_window, opening_date = opening_date, closing_date = closing_date)


#========================== FORCASTING APPROVE/REJECT FOR SUP =======================================#

def forcasting_mpo_approve_reject():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        sup_id = session.user_id
        sup_name = session.name
        first_date_of_month = session.first_date_of_month
        rep_id = request.args(0)
        approve_btn = request.vars.approve
        reject_btn = request.vars.reject

        if approve_btn == "Approve":
            # update_forcasting_status_sql = "UPDATE forecast_mpo SET status = 'APPROVED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"';"
            
            # approve data in temp table
            update_forcasting_status_sql = "UPDATE forecast_mpo_temp SET status = 'APPROVED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"';"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            
            # move approved data from temp table to main table
            all_forecast_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}') AND status = 'APPROVED' GROUP BY rep_id, first_date, item_code;"
            forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            if len(forecast_rec) != 0:
                for r in range(len(forecast_rec)):
                    records = forecast_rec[r]
                    rep_name = str(records['rep_name'])
                    submitted_first_date = str(records['first_date'])
                    submitted_date = str(records['submitted_date'])
                    forecasting_first_date = str(records['forcasting_first_date'])
                    division  = str(records['division'])
                    country = str(records['country'])
                    zone_id = str(records['zone_id'])
                    zone_name = str(records['zone_name'])
                    region_id = str(records['region_id'])
                    region_name = str(records['region_name'])
                    area_id = str(records['area_id'])
                    area_name = str(records['area_name'])
                    territory_id = str(records['territory_id'])
                    territory_name = str(records['territory_name'])
                    sale_unit_id = str(records['sale_unit_id'])
                    sale_unit_name = str(records['sale_unit_name'])
                    item_code = str(records['item_code'])
                    item_name = str(records['item_name'])
                    UoM  = str(records['UoM'])
                    month1 = str(records['month1'])
                    month2 = str(records['month2'])
                    month3 = str(records['month3'])
                    month4 = str(records['month4'])
                    month5 = str(records['month5'])
                    month6 = str(records['month6'])
                    month7 = str(records['month7'])
                    month8 = str(records['month8'])
                    month9 = str(records['month9'])
                    month10 = str(records['month10'])
                    month11 = str(records['month11'])
                    month12 = str(records['month12'])
                    month13 = str(records['month13'])
                    month14 = str(records['month14'])
                    month15 = str(records['month15'])
                    month16 = str(records['month16'])
                    month17 = str(records['month17'])
                    month18 = str(records['month18'])
                    status  = str(records['status'])
                    approve_by_id = str(records['approve_by_id'])
                    approve_by_name = str(records['approve_by_name'])
                    
                    # copy-paste data from one table to another
                    insert_forcasting_header_sql = "INSERT INTO forecast_mpo (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, division, country, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status, approve_by_id, approve_by_name) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(division)+"','"+str(country)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(region_id)+"','"+str(region_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(sale_unit_id)+"','"+str(sale_unit_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"','"+str(approve_by_id)+"','"+str(approve_by_name)+"')"
                    db.executesql(insert_forcasting_header_sql)

                delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                db.executesql(delete_forecasting_sql)

            response.flash = "APPROVED Successfully"



        elif reject_btn == "Reject":
            update_forcasting_status_sql = "UPDATE forecast_mpo_temp SET status = 'REJECTED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"' ;"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)

            response.flash = "REJECTED Successfully"

        redirect(URL('forcasting','forcasting_for_sup'))


#========================== MERGE MPO FORECASTING FOR SUP =======================================#

def process_forcasting():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        user_id = session.user_id

        user_name = ''
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''

        rep_count = request.vars.mpo_count
        mpo_id_list = request.vars.mpo_list
        first_date_of_month = session.first_date_of_month
        process_btn = request.vars.process_btn

        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        months = []

        if process_btn:
            check_status_sql = "SELECT COUNT(DISTINCT rep_id) AS approved_rep_count FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id IN ("+str(mpo_id_list)+") AND forcasting_first_date = '"+str(submitted_first_date)+"' AND status = 'APPROVED';"
            get_status = db.executesql(check_status_sql, as_dict=True)

            if len(get_status) > 0:
                approved_mpo = int(get_status[0]['approved_rep_count'])
            else:
                approved_mpo = 0

            if int(approved_mpo) < int(rep_count):
                session.process_flash = "All Forecast Not Approved Yet"
            
            else:
                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1_total = 0
                month2_total = 0
                month3_total = 0
                month4_total = 0
                month5_total = 0
                month6_total = 0
                month7_total = 0
                month8_total = 0
                month9_total = 0
                month10_total = 0
                month11_total = 0
                month12_total = 0
                month13_total = 0
                month14_total = 0
                month15_total = 0
                month16_total = 0
                month17_total = 0
                month18_total = 0
                count = 1

                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"

                status = 'PROCESSED'

                check_forecasting_sql = "SELECT * FROM forecast_am_temp WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' AND forcasting_first_date = '"+str(submitted_first_date)+"' AND status = 'PROCESSED' GROUP BY sup_id, item_code, forcasting_first_date;"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)
                
                if len(check_forecasting) == 0:
                    get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' LIMIT 1;"
                    get_level_depth = db.executesql(get_level_id_sql, as_dict = True)

                    for a in range(len(get_level_depth)):
                        records = get_level_depth[a]
                        sup_name = records['sup_name']
                        level_id = records['level_id']
                        level_depth = records['level_depth_no']

                    get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
                    get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                    for a in range(len(get_level_records)):
                        records_level = get_level_records[a]
                        level0  = records_level['level0']
                        level0_name = records_level['level0_name']
                        level1  = records_level['level1']
                        level1_name = records_level['level1_name']
                        level2  = records_level['level2']
                        level2_name = records_level['level2_name']
                        level3  = records_level['level3']
                        level3_name = records_level['level3_name']

                    # merging all mpo data
                    get_forcasting_for_mpo_sql = "SELECT item_code, item_name, UoM, SUM(month1) AS month1, SUM(month2) AS month2, SUM(month3) AS month3, SUM(month4) AS month4, SUM(month5) AS month5, SUM(month6) AS month6, SUM(month7) AS month7, SUM(month8) AS month8, SUM(month9) AS month9, SUM(month10) AS month10, SUM(month11) AS month11, SUM(month12) AS month12, SUM(month13) AS month13, SUM(month14) AS month14, SUM(month15) AS month15, SUM(month16) AS month16, SUM(month17) AS month17, SUM(month18) AS month18 FROM forecast_mpo WHERE cid = '"+cid+"' AND rep_id IN ("+str(mpo_id_list)+") AND submitted_date in (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '"+cid+"' and rep_id in ("+str(mpo_id_list)+") GROUP by rep_id) AND status = 'APPROVED' GROUP BY item_code;"
                    get_forcasting_for_mpo = db.executesql(get_forcasting_for_mpo_sql, as_dict = True)

                    # inserting into table
                    if len(get_forcasting_for_mpo) > 0 :
                        # insert processed data
                        for i in range(len(get_forcasting_for_mpo)):
                            forecast_records_str = get_forcasting_for_mpo[i]
                            
                            if i == 0:
                                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months
                                
                                # FOR TEMP TABLE - processed data 
                                # month name insert sql 
                                insert_forcasting_header_sql = "INSERT INTO forecast_am_temp(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                db.executesql(insert_forcasting_header_sql)

                                # FOR MAIN TABLE
                                # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                # db.executesql(insert_forcasting_header_sql)
                                continue

                            item_code = str(forecast_records_str['item_code'])
                            item_name = str(forecast_records_str['item_name'])
                            UoM = str(forecast_records_str['UoM'])
                            month1 = forecast_records_str['month1']
                            month2 = forecast_records_str['month2']
                            month3 = forecast_records_str['month3']
                            month4 = forecast_records_str['month4']
                            month5 = forecast_records_str['month5']
                            month6 = forecast_records_str['month6']
                            month7 = forecast_records_str['month7']
                            month8 = forecast_records_str['month8']
                            month9 = forecast_records_str['month9']
                            month10 = forecast_records_str['month10']
                            month11 = forecast_records_str['month11']
                            month12 = forecast_records_str['month12']
                            month13 = forecast_records_str['month13']
                            month14 = forecast_records_str['month14']
                            month15 = forecast_records_str['month15']
                            month16 = forecast_records_str['month16']
                            month17 = forecast_records_str['month17']
                            month18 = forecast_records_str['month18']
                            
                            try:
                                month1_total += float(month1)
                                month2_total += float(month2)
                                month3_total += float(month3)
                                month4_total += float(month4)
                                month5_total += float(month5)
                                month6_total += float(month6)
                                month7_total += float(month7)
                                month8_total += float(month8)
                                month9_total += float(month9)
                                month10_total += float(month10)
                                month11_total += float(month11)
                                month12_total += float(month12)
                                month13_total += float(month13)
                                month14_total += float(month14)
                                month15_total += float(month15)
                                month16_total += float(month16)
                                month17_total += float(month17)
                                month18_total += float(month18)

                            except:
                                pass

                            i += 1
                            
                            # FOR TEMP TABLE - processed data
                            # numerical value insert sql
                            insert_forcasting_header_sql = "INSERT INTO forecast_am_temp(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                            db.executesql(insert_forcasting_header_sql)

                            # FOR MAIN TABLE
                            # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                            # db.executesql(insert_forcasting_header_sql)
                        
                        # insert submitted data
                        for i in range(len(get_forcasting_for_mpo)):
                            forecast_records_str = get_forcasting_for_mpo[i]
                            
                            if i == 0:
                                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                                # FOR TEMP TABLE - submitted data
                                # month name insert sql 
                                insert_forcasting_header_sql = "INSERT INTO forecast_am_temp(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','SUBMITTED')"
                                db.executesql(insert_forcasting_header_sql)

                                # FOR MAIN TABLE
                                # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                # db.executesql(insert_forcasting_header_sql)
                                continue

                            item_code = str(forecast_records_str['item_code'])
                            item_name = str(forecast_records_str['item_name'])
                            UoM = str(forecast_records_str['UoM'])
                            month1 = round(float(forecast_records_str['month1']), 2)
                            month2 = round(float(forecast_records_str['month2']), 2)
                            month3 = round(float(forecast_records_str['month3']), 2)
                            month4 = round(float(forecast_records_str['month4']), 2)
                            month5 = round(float(forecast_records_str['month5']), 2)
                            month6 = round(float(forecast_records_str['month6']), 2)
                            month7 = round(float(forecast_records_str['month7']), 2)
                            month8 = round(float(forecast_records_str['month8']), 2)
                            month9 = round(float(forecast_records_str['month9']), 2)
                            month10 = round(float(forecast_records_str['month10']), 2)
                            month11 = round(float(forecast_records_str['month11']), 2)
                            month12 = round(float(forecast_records_str['month12']), 2)
                            month13 = round(float(forecast_records_str['month13']), 2)
                            month14 = round(float(forecast_records_str['month14']), 2)
                            month15 = round(float(forecast_records_str['month15']), 2)
                            month16 = round(float(forecast_records_str['month16']), 2)
                            month17 = round(float(forecast_records_str['month17']), 2)
                            month18 = round(float(forecast_records_str['month18']), 2)
                            
                            try:
                                month1_total += float(month1)
                                month2_total += float(month2)
                                month3_total += float(month3)
                                month4_total += float(month4)
                                month5_total += float(month5)
                                month6_total += float(month6)
                                month7_total += float(month7)
                                month8_total += float(month8)
                                month9_total += float(month9)
                                month10_total += float(month10)
                                month11_total += float(month11)
                                month12_total += float(month12)
                                month13_total += float(month13)
                                month14_total += float(month14)
                                month15_total += float(month15)
                                month16_total += float(month16)
                                month17_total += float(month17)
                                month18_total += float(month18)

                            except:
                                pass

                            i += 1

                            # FOR TEMP TABLE - submitted data
                            # numerical value insert sql
                            insert_forcasting_header_sql = "INSERT INTO forecast_am_temp(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','SUBMITTED')"
                            db.executesql(insert_forcasting_header_sql)

                            # FOR MAIN TABLE
                            # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                            # db.executesql(insert_forcasting_header_sql)
                        
                    session.process_flash = "Forecast Ready to View"

        else:
            session.process_flash = "Already Processed Once"
  
  
        redirect(URL('forcasting','forcasting_for_sup'))


#========================== FORCASTING VIEW - GENERAL ==========================#

def forcasting_view_mpo():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type

        # btns
        rep_view_btn = request.vars.rep_view
        post_btn = request.vars.post_btn

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        if user_type == 'sup':
            length = 0

            if rep_view_btn:
                rep_id = request.args[0]

                all_forecast_sql = f"SELECT * FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{rep_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{rep_id}') GROUP BY rep_id, first_date, item_code;"
                forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
                
                if len(forecast_rec) != 0:
                    check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{rep_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{rep_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()
                    
                    length += 1
                
                else:
                    all_forecast_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}') GROUP BY rep_id, first_date, item_code;"
                    forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
                    
                    if len(forecast_rec) != 0:
                        check_forcasting_status = f"SELECT status FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}') GROUP BY status;"
                        forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                        
                        frcst_status = ''
                        if len(forecast_status) != 0:
                            for f in range(len(forecast_status)):
                                forecast = forecast_status[f]
                                frcst_status = str(forecast['status']).upper().strip()
                        
                        length += 1

                return dict(months = months, forecast_records = forecast_rec, length = length, status = frcst_status, mpo_id = rep_id)


            # elif post_btn:
            #     mpo_id = request.args[0]

            #     #====================== GET SUBMITTED DATE =============================#
            #     submitted_date = str(date_fixed)
            #     submitted_date_str = str(date_fixed).split(' ')[0]
            #     submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
            #     year = submitted_first_date.year
            #     month = submitted_first_date.month
            #     submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
            #     current_month = str(date_fixed).split(' ')[0]

            #     get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(mpo_id)+"' LIMIT 1;"
            #     get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
            #     for a in range(len(get_level_depth)):
            #         records = get_level_depth[a]
            #         rep_name = records['rep_name']
            #         area_id = records['area_id']

            #     get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
            #     get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            #     for a in range(len(get_level_records)):
            #         records_level = get_level_records[a]
            #         level0 = records_level['level0']
            #         level0_name = records_level['level0_name']
            #         level1 = records_level['level1']
            #         level1_name = records_level['level1_name']
            #         level2 = records_level['level2']
            #         level2_name = records_level['level2_name']
            #         level3 = records_level['level3']
            #         level3_name = records_level['level3_name']
                
            #     curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            #     curr_month = curr_date.strftime('%b-%y')

                # month1 = str(curr_month).strip()
                # if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                #     forecasting_first_date="2024-01-01"
                # elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                #     forecasting_first_date="2024-02-01"
                # elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                #     forecasting_first_date="2024-03-01"
                # elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                #     forecasting_first_date="2024-04-01"
                # elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                #     forecasting_first_date="2024-05-01"
                # elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                #     forecasting_first_date="2024-06-01"
                # elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                #     forecasting_first_date="2024-07-01"
                # elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                #     forecasting_first_date="2024-08-01"
                # elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                #     forecasting_first_date="2024-09-01"
                # elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                #     forecasting_first_date="2024-10-01"
                # elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                #     forecasting_first_date="2024-11-01"
                # elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                #     forecasting_first_date="2024-12-01"
                
            #     status = "POSTED"

            #     item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                
            #     inputs_combined = [
            #         request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
            #         request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
            #         request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
            #         request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
            #         request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
            #         request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
            #         request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
            #         request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
            #         request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
            #         request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
            #         request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
            #         request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
            #         request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
            #         request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
            #         request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
            #         request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
            #         request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
            #         request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            #     ]   

            #     output_dict = {}  # Dictionary to store inputs grouped by item code
            #     for item_code in item_codes:
            #         output_dict[item_code] = []

            #     for i in range(len(item_codes)):
            #         for j in range(len(inputs_combined)):
            #             if inputs_combined[j][i] != '':
            #                 output_dict[item_codes[i]].append(inputs_combined[j][i])

            #     out_str = ''
            #     for item_code in output_dict:
            #         out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
            #     if out_str.endswith('|'):
            #         out_str = out_str[:-1]

            #     rows = out_str.split("|")

            #     data_array = []
            #     for row in rows:
            #         values = row.split(",")
            #         data_array.append(values)
                
            #     # price = 0.0

            #     current_month = str(date_fixed).split(' ')[0]
            #     first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            #     current_date = datetime.strptime(current_month, "%Y-%m-%d")
            #     year = first_date_str.year
            #     month = first_date_str.month
            #     planning_month = str(datetime(year, month, 1)).split(' ')[0]
            #     months = []

            #     # for i in range(18):
            #     #     months.append(current_date.strftime("%b-%Y"))
            #     #     current_date += timedelta(days=31)

            #     months.append(current_date.strftime("%b-%Y"))
            #     i = 1
            #     for i in range(17):
            #         current_date += timedelta(days=30)
            #         if str(current_date) == str(months[i-1]):
            #             i += 1
            #             continue
            #         else:
            #             months.append(current_date.strftime("%b-%Y"))

            #     month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months
                
            #     check_forecasting_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{mpo_id}' AND forcasting_first_date = '{forecasting_first_date}';"
            #     check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            #     # remove previous forecasting
            #     if len(check_forecasting) > 0:
            #         delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{mpo_id}' AND forcasting_first_date = '{forecasting_first_date}';"
            #         db.executesql(delete_forecasting_sql)
                
            #     # month name insert sql 
            #     insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(mpo_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            #     db.executesql(insert_forcasting_header_sql)
                
            #     for sublist in data_array:
            #         item_id, *months = sublist
            #         month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

            #         get_item_price_sql = "SELECT item_id, name, unit_type, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
            #         get_item_price = db.executesql(get_item_price_sql, as_dict = True)

            #         for a in range(len(get_item_price)):
            #             item_record = get_item_price[a]
            #             item_name = item_record['name']
            #             UoM = item_record['unit_type']
            #             # price = item_record['price']
                        
            #         # numerical value insert sql 
            #         insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(mpo_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(int(float(month1)))+"','"+str(int(float(month2)))+"','"+str(int(float(month3)))+"','"+str(int(float(month4)))+"','"+str(int(float(month5)))+"','"+str(int(float(month6)))+"','"+str(int(float(month7)))+"','"+str(int(float(month8)))+"','"+str(int(float(month9)))+"','"+str(int(float(month10)))+"','"+str(int(float(month11)))+"','"+str(int(float(month12)))+"','"+str(int(float(month13)))+"','"+str(int(float(month14)))+"','"+str(int(float(month15)))+"','"+str(int(float(month16)))+"','"+str(int(float(month17)))+"','"+str(int(float(month18)))+"','"+str(status)+"')"
            #         db.executesql(insert_forcasting_header_sql)


            redirect(URL('forcasting','forcasting_for_sup'))
                # redirect(URL('forcasting','forcasting_view_mpo'))


#========================== FORCASTING VIEW FOR REP =======================================#

def forcasting_rep_view():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        if user_type == 'rep':
            all_forecast_sql = f"SELECT * FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY rep_id, first_date, item_code;"
            # all_forecast_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY rep_id, first_date, item_code;"
            all_forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

            length = 0  
            if len(all_forecast_rec) != 0:
                check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                
                frcst_status = ''
                if len(forecast_status) != 0:
                    for f in range(len(forecast_status)):
                        forecast = forecast_status[f]
                        frcst_status = str(forecast['status']).upper().strip()

                length += 1
                return dict(months = months, forecast_records = all_forecast_rec, length = length, status = frcst_status, planning_month = planning_month)

            else:
                forecast_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY rep_id, first_date, item_code;"
                forecast_rec = db.executesql(forecast_sql, as_dict=True)
            
                # length = 0
                if len(forecast_rec) == 0:
                    # check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    check_forcasting_status = f"SELECT status FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()

                    get_item_record_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' GROUP BY item_id ORDER BY item_id;"
                    get_item_record = db.executesql(get_item_record_sql, as_dict=True)
                    
                    return dict(months = months, item_rec = get_item_record, length = length, status = frcst_status, planning_month = planning_month)

                else:
                    # check_forcasting_status = f"SELECT status FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    check_forcasting_status = f"SELECT status FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{user_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()

                    length += 1
                    return dict(months = months, forecast_records = forecast_rec, length = length, status = frcst_status, planning_month = planning_month)


#========================== VIEW ORIGINAL FILE FOR SUP =======================================#

def forcasting_view_only():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Compiled Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type
        depth = str(session.level_depth)

        if depth == '0':
            all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"

        elif depth == '1':
            all_forecast_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"
        
        elif depth == '2':
            all_forecast_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"

        forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

        return dict(forecast_records = forecast_rec)


#========================== EDITABLE VIEW FOP MPO =======================================#

def forcasting_mpo():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        # GET SUBMITTED DATE
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]

        cid = session.cid
        rep_id = session.user_id
        rep_name = ''
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''
        submit_btn_new = request.vars.submit_btn_new
        submit_btn_old = request.vars.submit_btn_old
        post_btn = request.vars.post_btn

        if session.user_type == 'rep':
            if submit_btn_new:
                get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' LIMIT 1;"
                get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
                for a in range(len(get_level_depth)):
                    records = get_level_depth[a]
                    rep_name = records['rep_name']
                    area_id = records['area_id']

                get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
                get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                for a in range(len(get_level_records)):
                    records_level = get_level_records[a]
                    level0  = records_level['level0']
                    level0_name = records_level['level0_name']
                    level1  = records_level['level1']
                    level1_name = records_level['level1_name']
                    level2  = records_level['level2']
                    level2_name = records_level['level2_name']
                    level3  = records_level['level3']
                    level3_name = records_level['level3_name']

                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')
                
                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"
                
                status = "SUBMITTED"

                item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]

                inputs_combined = [
                    request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                    request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                    request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                    request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                    request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                    request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                    request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                    request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                    request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                    request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                    request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                    request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                    request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                    request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                    request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                    request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                    request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                    request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
                ]   
                # return str(inputs_combined)

                inputs_combined_list = []

                # Replace empty strings with 0
                for columns in inputs_combined:
                    col = [value if value != '' else '0' for value in columns]
                    inputs_combined_list.append(col)
                
                output_dict = {}  # Dictionary to store inputs grouped by item code
                for item_code in item_codes:
                    output_dict[item_code] = []

                for i in range(len(item_codes)):
                    for j in range(len(inputs_combined_list)):
                        if inputs_combined_list[j][i] != '':
                            output_dict[item_codes[i]].append(inputs_combined_list[j][i])

                out_str = ''
                for item_code in output_dict:
                    out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'

                if out_str.endswith('|'):
                    out_str = out_str[:-1]
                
                rows = out_str.split("|")

                data_array = []
                for row in rows:
                    values = row.split(",")
                    data_array.append(values)

                months = []
                months = request.vars.month_list
                
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                # month name insert sql 
                insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)
                
                for sublist in data_array:
                    item_id, *months = sublist
                    month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                    # CONVERTING FLOAT INPUT TO 2 D.P. 
                    month1 = round(float(month1), 2)
                    month2 = round(float(month2), 2)
                    month3 = round(float(month3), 2)
                    month4 = round(float(month4), 2)
                    month5 = round(float(month5), 2)
                    month6 = round(float(month6), 2)
                    month7 = round(float(month7), 2)
                    month8 = round(float(month8), 2)
                    month9 = round(float(month9), 2)
                    month10 = round(float(month10), 2)
                    month11 = round(float(month11), 2)
                    month12 = round(float(month12), 2)
                    month13 = round(float(month13), 2)
                    month14 = round(float(month14), 2)
                    month15 = round(float(month15), 2)
                    month16 = round(float(month16), 2)
                    month17 = round(float(month17), 2)
                    month18 = round(float(month18), 2)

                    get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                    get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                    for a in range(len(get_item_price)):
                        item_record = get_item_price[a]
                        item_name = item_record['name']
                        UoM = item_record['unit_type']

                    # numerical value insert sql 
                    insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                    db.executesql(insert_forcasting_header_sql)

                session.update_flash = "Updated Successfully"
            
            elif submit_btn_old:
                get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' LIMIT 1;"
                get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
                for a in range(len(get_level_depth)):
                    records = get_level_depth[a]
                    rep_name = records['rep_name']
                    area_id = records['area_id']

                get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
                get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                for a in range(len(get_level_records)):
                    records_level = get_level_records[a]
                    level0 = records_level['level0']
                    level0_name = records_level['level0_name']
                    level1 = records_level['level1']
                    level1_name = records_level['level1_name']
                    level2 = records_level['level2']
                    level2_name = records_level['level2_name']
                    level3 = records_level['level3']
                    level3_name = records_level['level3_name']
                
                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01" 

                status = "SUBMITTED"

                item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                # return str(item_codes)
                
                inputs_combined = [
                    request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                    request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                    request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                    request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                    request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                    request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                    request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                    request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                    request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                    request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                    request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                    request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                    request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                    request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                    request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                    request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                    request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                    request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
                ]   
                # return str(inputs_combined)
                
                output_dict = {}  # Dictionary to store inputs grouped by item code
                for item_code in item_codes:
                    output_dict[item_code] = []

                for i in range(len(item_codes)):
                    for j in range(len(inputs_combined)):
                        if inputs_combined[j][i] != '':
                            output_dict[item_codes[i]].append(inputs_combined[j][i])
                
                out_str = ''
                for item_code in output_dict:
                    out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
                if out_str.endswith('|'):
                    out_str = out_str[:-1]
                
                rows = out_str.split("|")

                data_array = []
                for row in rows:
                    values = row.split(",")
                    data_array.append(values)

                current_month = str(date_fixed).split(' ')[0]
                first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
                current_date = datetime.strptime(current_month, "%Y-%m-%d")
                year = first_date_str.year
                month = first_date_str.month
                planning_month = str(datetime(year, month, 1)).split(' ')[0]
                months = []

                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                check_forecasting_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

                # remove previous forecasting
                if len(check_forecasting) > 0:
                    delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                    db.executesql(delete_forecasting_sql)
                
                # month name insert sql 
                insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

                for sublist in data_array:
                    item_id, *months = sublist
                    month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                    # CONVERTING FLOAT INPUT TO 2 D.P. 
                    month1 = round(float(month1), 2)
                    month2 = round(float(month2), 2)
                    month3 = round(float(month3), 2)
                    month4 = round(float(month4), 2)
                    month5 = round(float(month5), 2)
                    month6 = round(float(month6), 2)
                    month7 = round(float(month7), 2)
                    month8 = round(float(month8), 2)
                    month9 = round(float(month9), 2)
                    month10 = round(float(month10), 2)
                    month11 = round(float(month11), 2)
                    month12 = round(float(month12), 2)
                    month13 = round(float(month13), 2)
                    month14 = round(float(month14), 2)
                    month15 = round(float(month15), 2)
                    month16 = round(float(month16), 2)
                    month17 = round(float(month17), 2)
                    month18 = round(float(month18), 2)
                    
                    get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                    get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                    for a in range(len(get_item_price)):
                        item_record = get_item_price[a]
                        item_name = item_record['name']
                        UoM = item_record['unit_type']
                        # price = item_record['price']
                    
                    # numerical value insert sql
                    insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                    db.executesql(insert_forcasting_header_sql)

                session.update_flash = "Updated Successfully"

            elif post_btn:
                get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' LIMIT 1;"
                get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
                for a in range(len(get_level_depth)):
                    records = get_level_depth[a]
                    rep_name = records['rep_name']
                    area_id = records['area_id']

                get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
                get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                for a in range(len(get_level_records)):
                    records_level = get_level_records[a]
                    level0 = records_level['level0']
                    level0_name = records_level['level0_name']
                    level1 = records_level['level1']
                    level1_name = records_level['level1_name']
                    level2 = records_level['level2']
                    level2_name = records_level['level2_name']
                    level3 = records_level['level3']
                    level3_name = records_level['level3_name']
                
                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"
                
                status = "POSTED"

                item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                
                inputs_combined = [
                    request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                    request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                    request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                    request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                    request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                    request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                    request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                    request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                    request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                    request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                    request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                    request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                    request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                    request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                    request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                    request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                    request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                    request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
                ]   

                output_dict = {}  # Dictionary to store inputs grouped by item code
                for item_code in item_codes:
                    output_dict[item_code] = []

                for i in range(len(item_codes)):
                    for j in range(len(inputs_combined)):
                        if inputs_combined[j][i] != '':
                            output_dict[item_codes[i]].append(inputs_combined[j][i])

                out_str = ''
                for item_code in output_dict:
                    out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
                if out_str.endswith('|'):
                    out_str = out_str[:-1]

                rows = out_str.split("|")

                data_array = []
                for row in rows:
                    values = row.split(",")
                    data_array.append(values)

                current_month = str(date_fixed).split(' ')[0]
                first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
                current_date = datetime.strptime(current_month, "%Y-%m-%d")
                year = first_date_str.year
                month = first_date_str.month
                planning_month = str(datetime(year, month, 1)).split(' ')[0]
                months = []

                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                check_forecasting_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

                # remove previous forecasting
                if len(check_forecasting) > 0:
                    delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                    db.executesql(delete_forecasting_sql)
                
                # month name insert sql 
                insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

                for sublist in data_array:
                    item_id, *months = sublist
                    month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                    # CONVERTING FLOAT INPUT TO 2 D.P. 
                    month1 = round(float(month1), 2)
                    month2 = round(float(month2), 2)
                    month3 = round(float(month3), 2)
                    month4 = round(float(month4), 2)
                    month5 = round(float(month5), 2)
                    month6 = round(float(month6), 2)
                    month7 = round(float(month7), 2)
                    month8 = round(float(month8), 2)
                    month9 = round(float(month9), 2)
                    month10 = round(float(month10), 2)
                    month11 = round(float(month11), 2)
                    month12 = round(float(month12), 2)
                    month13 = round(float(month13), 2)
                    month14 = round(float(month14), 2)
                    month15 = round(float(month15), 2)
                    month16 = round(float(month16), 2)
                    month17 = round(float(month17), 2)
                    month18 = round(float(month18), 2)

                    get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                    get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                    for a in range(len(get_item_price)):
                        item_record = get_item_price[a]
                        item_name = item_record['name']
                        UoM = item_record['unit_type']
                        # price = item_record['price']

                    # numerical value insert sql  
                    insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                    db.executesql(insert_forcasting_header_sql)

                session.post_flash = "Posted Successfully"

            redirect(URL('forcasting','forcasting_rep_view'))


#========================== EDITABLE VIEW FOR SUP =======================================#

def forcasting_sup():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        mpo_id = request.args[0]

        if mpo_id == '' or mpo_id == 'None' or mpo_id == None:
            mpo_id = ''

        #====================== GET SUBMITTED DATE =============================#
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]

        cid = session.cid
        rep_id = session.user_id
        rep_name = ''
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''
        submit_btn_new = request.vars.submit_btn_new
        submit_btn_old = request.vars.submit_btn_old
        post_btn = request.vars.post_btn
        
        if submit_btn_old:
            get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                rep_name = records['rep_name']
                area_id = records['area_id']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0 = records_level['level0']
                level0_name = records_level['level0_name']
                level1 = records_level['level1']
                level1_name = records_level['level1_name']
                level2 = records_level['level2']
                level2_name = records_level['level2_name']
                level3 = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "POSTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   
            
            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]

            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            # check_forecasting_sql = f"SELECT * FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
            check_forecasting_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)
            # return len(check_forecasting)

            # remove previous forecasting
            if len(check_forecasting) > 0:
                return 'del'
                delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                db.executesql(delete_forecasting_sql)
            
            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']
                    
                # numerical value insert sql
                insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(int(float(month1)))+"','"+str(int(float(month2)))+"','"+str(int(float(month3)))+"','"+str(int(float(month4)))+"','"+str(int(float(month5)))+"','"+str(int(float(month6)))+"','"+str(int(float(month7)))+"','"+str(int(float(month8)))+"','"+str(int(float(month9)))+"','"+str(int(float(month10)))+"','"+str(int(float(month11)))+"','"+str(int(float(month12)))+"','"+str(int(float(month13)))+"','"+str(int(float(month14)))+"','"+str(int(float(month15)))+"','"+str(int(float(month16)))+"','"+str(int(float(month17)))+"','"+str(int(float(month18)))+"','"+str(status)+"')"
                # return insert_forcasting_header_sql
                db.executesql(insert_forcasting_header_sql)

        elif post_btn:
            # for indv rep edit btn
            if mpo_id != '' or mpo_id != 'None' or mpo_id != None:
                get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(mpo_id)+"' LIMIT 1;"
                get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
                for a in range(len(get_level_depth)):
                    records = get_level_depth[a]
                    rep_name = records['rep_name']
                    area_id = records['area_id']

                get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
                get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                for a in range(len(get_level_records)):
                    records_level = get_level_records[a]
                    level0 = records_level['level0']
                    level0_name = records_level['level0_name']
                    level1 = records_level['level1']
                    level1_name = records_level['level1_name']
                    level2 = records_level['level2']
                    level2_name = records_level['level2_name']
                    level3 = records_level['level3']
                    level3_name = records_level['level3_name']
                
                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"
                
                status = "POSTED"

                item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                
                inputs_combined = [
                    request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                    request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                    request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                    request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                    request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                    request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                    request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                    request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                    request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                    request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                    request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                    request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                    request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                    request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                    request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                    request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                    request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                    request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
                ]   

                output_dict = {}  # Dictionary to store inputs grouped by item code
                for item_code in item_codes:
                    output_dict[item_code] = []

                for i in range(len(item_codes)):
                    for j in range(len(inputs_combined)):
                        if inputs_combined[j][i] != '':
                            output_dict[item_codes[i]].append(inputs_combined[j][i])

                out_str = ''
                for item_code in output_dict:
                    out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
                if out_str.endswith('|'):
                    out_str = out_str[:-1]

                rows = out_str.split("|")

                data_array = []
                for row in rows:
                    values = row.split(",")
                    data_array.append(values)
                
                # price = 0.0

                current_month = str(date_fixed).split(' ')[0]
                first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
                current_date = datetime.strptime(current_month, "%Y-%m-%d")
                year = first_date_str.year
                month = first_date_str.month
                planning_month = str(datetime(year, month, 1)).split(' ')[0]
                months = []

                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                # check_forecasting_sql = f"SELECT * FROM forecast_mpo WHERE cid='{cid}' AND rep_id = '{mpo_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                check_forecasting_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{mpo_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

                # remove previous forecasting
                if len(check_forecasting) > 0:
                    # delete_forecasting_sql = f"DELETE FROM forecast_mpo WHERE cid = '{cid}' AND rep_id = '{mpo_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                    delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{mpo_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                    db.executesql(delete_forecasting_sql)
                
                # month name insert sql 
                insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp(cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(mpo_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

                for sublist in data_array:
                    item_id, *months = sublist
                    month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                    get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                    get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                    for a in range(len(get_item_price)):
                        item_record = get_item_price[a]
                        item_name = item_record['name']
                        UoM = item_record['unit_type']
                        # price = item_record['price']

                    # numerical value insert sql
                    insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(mpo_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(int(float(month1)))+"','"+str(int(float(month2)))+"','"+str(int(float(month3)))+"','"+str(int(float(month4)))+"','"+str(int(float(month5)))+"','"+str(int(float(month6)))+"','"+str(int(float(month7)))+"','"+str(int(float(month8)))+"','"+str(int(float(month9)))+"','"+str(int(float(month10)))+"','"+str(int(float(month11)))+"','"+str(int(float(month12)))+"','"+str(int(float(month13)))+"','"+str(int(float(month14)))+"','"+str(int(float(month15)))+"','"+str(int(float(month16)))+"','"+str(int(float(month17)))+"','"+str(int(float(month18)))+"','"+str(status)+"')"
                    db.executesql(insert_forcasting_header_sql)

            # for sup edit btn
            else:
                get_level_id_sql = "SELECT rep_name, area_id FROM sm_rep_area WHERE cid = '"+cid+"' AND rep_id = '"+str(rep_id)+"' LIMIT 1;"
                get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
                for a in range(len(get_level_depth)):
                    records = get_level_depth[a]
                    rep_name = records['rep_name']
                    area_id = records['area_id']

                get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(area_id)+"' AND depth = '3' AND is_leaf = '1' GROUP BY level3 LIMIT 1;"
                get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                for a in range(len(get_level_records)):
                    records_level = get_level_records[a]
                    level0 = records_level['level0']
                    level0_name = records_level['level0_name']
                    level1 = records_level['level1']
                    level1_name = records_level['level1_name']
                    level2 = records_level['level2']
                    level2_name = records_level['level2_name']
                    level3 = records_level['level3']
                    level3_name = records_level['level3_name']
                
                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"
                
                status = "POSTED"

                item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                
                inputs_combined = [
                    request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                    request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                    request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                    request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                    request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                    request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                    request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                    request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                    request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                    request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                    request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                    request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                    request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                    request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                    request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                    request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                    request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                    request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
                ]   

                output_dict = {}  # Dictionary to store inputs grouped by item code
                for item_code in item_codes:
                    output_dict[item_code] = []

                for i in range(len(item_codes)):
                    for j in range(len(inputs_combined)):
                        if inputs_combined[j][i] != '':
                            output_dict[item_codes[i]].append(inputs_combined[j][i])

                out_str = ''
                for item_code in output_dict:
                    out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
                if out_str.endswith('|'):
                    out_str = out_str[:-1]

                rows = out_str.split("|")

                data_array = []
                for row in rows:
                    values = row.split(",")
                    data_array.append(values)
                
                # price = 0.0

                current_month = str(date_fixed).split(' ')[0]
                first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
                current_date = datetime.strptime(current_month, "%Y-%m-%d")
                year = first_date_str.year
                month = first_date_str.month
                planning_month = str(datetime(year, month, 1)).split(' ')[0]
                months = []

                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                check_forecasting_sql = f"SELECT * FROM forecast_mpo_temp WHERE cid='{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

                # remove previous forecasting
                if len(check_forecasting) > 0:
                    delete_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
                    db.executesql(delete_forecasting_sql)
                
                # month name insert sql 
                insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

                for sublist in data_array:
                    item_id, *months = sublist
                    month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                    get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                    get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                    for a in range(len(get_item_price)):
                        item_record = get_item_price[a]
                        item_name = item_record['name']
                        UoM = item_record['unit_type']
                        # price = item_record['price']

                    # numerical value insert sql    
                    insert_forcasting_header_sql = "INSERT INTO forecast_mpo_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(int(float(month1)))+"','"+str(int(float(month2)))+"','"+str(int(float(month3)))+"','"+str(int(float(month4)))+"','"+str(int(float(month5)))+"','"+str(int(float(month6)))+"','"+str(int(float(month7)))+"','"+str(int(float(month8)))+"','"+str(int(float(month9)))+"','"+str(int(float(month10)))+"','"+str(int(float(month11)))+"','"+str(int(float(month12)))+"','"+str(int(float(month13)))+"','"+str(int(float(month14)))+"','"+str(int(float(month15)))+"','"+str(int(float(month16)))+"','"+str(int(float(month17)))+"','"+str(int(float(month18)))+"','"+str(status)+"')"
                    db.executesql(insert_forcasting_header_sql)
            
        else:
            session.flash = "Already submitted once"

        if session.user_type == 'rep':
            redirect(URL('forcasting','forcasting_for_mpo'))
        else:
            redirect(URL('forcasting','forcasting_for_sup'))

        return dict()


#========================== FORCASTING VIEW FOR SUP =======================================#

def forcasting_sup_view():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type
        depth = str(session.level_depth)

        # btns
        sup_view_btn = request.vars.sup_view_edit

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))

        # if depth == '0':
        #     get_processed_data_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"
        #     processed_data = db.executesql(get_processed_data_sql, as_dict=True)

        #     length = 0
        #     # all_forecast_sql = f"SELECT * FROM forecast_rm WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY sup_id, first_date, item_code;"
        #     all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY sup_id, first_date, item_code;"
        #     forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
        #     if len(forecast_rec) != 0:
        #         # check_forcasting_status = f"SELECT status FROM forecast_rm WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
        #         check_forcasting_status = f"SELECT status FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
        #         forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                
        #         frcst_status = ''
        #         if len(forecast_status) != 0:
        #             for f in range(len(forecast_status)):
        #                 forecast = forecast_status[f]
        #                 frcst_status = str(forecast['status']).upper().strip() 
                
        #         length += 1

        # elif depth == '1':
        #     get_processed_data_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"
        #     processed_data = db.executesql(get_processed_data_sql, as_dict=True)

        #     length = 0
        #     # all_forecast_sql = f"SELECT * FROM forecast_zm WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY sup_id, first_date, item_code;"
        #     all_forecast_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY sup_id, first_date, item_code;"
        #     forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
        #     if len(forecast_rec) != 0:
        #         # check_forcasting_status = f"SELECT status FROM forecast_zm WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
        #         check_forcasting_status = f"SELECT status FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
        #         forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                
        #         frcst_status = ''
        #         if len(forecast_status) != 0:
        #             for f in range(len(forecast_status)):
        #                 forecast = forecast_status[f]
        #                 frcst_status = str(forecast['status']).upper().strip() 
                
        #         length += 1

        if depth == '2':
            get_processed_data_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"
            processed_data = db.executesql(get_processed_data_sql, as_dict=True)
            
            # check in main table first
            all_forecast_sql = f"SELECT * FROM forecast_am WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY sup_id, first_date, item_code;"
            forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            length = 0
            if len(forecast_rec) != 0:
                # check_forcasting_status = f"SELECT status FROM forecast_am WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
                check_forcasting_status = f"SELECT status FROM forecast_am WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
                forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                
                frcst_status = ''
                if len(forecast_status) != 0:
                    for f in range(len(forecast_status)):
                        forecast = forecast_status[f]
                        frcst_status = str(forecast['status']).upper().strip() 
                
                length += 1
                return dict(months = months, forecast_records = forecast_rec, processed_records = processed_data, length = length, status = frcst_status, planning_month = planning_month)
            
            # check in temp table, if not found in main table
            else:
                forecast_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY sup_id, first_date, item_code;"
                forecast_rec = db.executesql(forecast_sql, as_dict=True)
                
                # length = 0
                if len(forecast_rec) == 0:
                    check_forcasting_status = f"SELECT status FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()

                    get_item_record_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' GROUP BY item_id ORDER BY item_id;"
                    get_item_record = db.executesql(get_item_record_sql, as_dict=True)
                    
                    return dict(months = months, item_rec = get_item_record, processed_records = processed_data, length = length, status = frcst_status, planning_month = planning_month)

                else:
                    check_forcasting_status = f"SELECT status FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
                    # return check_forcasting_status
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    # return response.json(forecast_status)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()

                    length += 1
                    return dict(months = months, forecast_records = forecast_rec, processed_records = processed_data, length = length, status = frcst_status, planning_month = planning_month)
 

#========================== VIEW EDIT FOR SUP =======================================#

def forcasting_sup_edit():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        # GET SUBMITTED DATE
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]

        cid = session.cid
        rep_id = session.user_id
        rep_name = session.name
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''
        submit_btn_new = request.vars.submit_btn_new
        submit_btn_old = request.vars.submit_btn_old
        post_btn = request.vars.post_btn

        if submit_btn_new:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']

            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')
            
            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "SUBMITTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   

            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'

            if out_str.endswith('|'):
                out_str = out_str[:-1]
            
            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)

            months = []
            months = request.vars.month_list
            
            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)
            
            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                # return get_item_price_sql
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)
                # return response.json(get_item_price)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']

                # numerical value insert sql    
                insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                # return insert_forcasting_header_sql
                db.executesql(insert_forcasting_header_sql)
        
        elif submit_btn_old:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "SUBMITTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   

            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []
            
            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]
            
            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            # check_forecasting_sql = f"SELECT * FROM forecast_am WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}';"
            check_forecasting_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            # REMOVE PREVIOUS FORECASTING
            if len(check_forecasting) > 0:
                delete_forecasting_sql = f"DELETE FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
                db.executesql(delete_forecasting_sql)

            # month name insert sql     
            insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']

                # numerical value insert sql    
                insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

            session.update_flash = "Updated Succesfully"
        
        elif post_btn:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "POSTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   

            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]

            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            check_forecasting_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            # remove previous forecasting
            if len(check_forecasting) > 0:
                delete_forecasting_sql = f"DELETE FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
                db.executesql(delete_forecasting_sql)
            
            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']

                # numerical value insert sql    
                insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

            session.post_flash = "Posted Successfully"
                
        else:
            session.update_flash = "Already submitted once"

        # redirect(URL('forcasting','forcasting_for_sup'))
        redirect(URL('forcasting','forcasting_sup_view'))


#========================== INDIVIDUAL FORCASTING VIEW FOR AM ==========================#

def forcasting_view_am():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type

        # btns
        am_view_btn = request.vars.am_view
        post_btn = request.vars.post_btn

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        if user_type == 'sup':
            length = 0

            if am_view_btn:
                am_id = request.args[0]

                all_forecast_sql = f"SELECT * FROM forecast_am WHERE cid='{cid}' AND sup_id = '{am_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am WHERE cid = '{cid}' AND sup_id = '{am_id}') GROUP BY sup_id, first_date, item_code;"
                forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

                if len(forecast_rec) != 0:
                    check_forcasting_status = f"SELECT status FROM forecast_am WHERE cid='{cid}' AND sup_id = '{am_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am WHERE cid = '{cid}' AND sup_id = '{am_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()
                    
                    length += 1
                    
                else:
                    all_forecast_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{am_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{am_id}') GROUP BY sup_id, first_date, item_code;"
                    forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

                    if len(forecast_rec) != 0:
                        check_forcasting_status = f"SELECT status FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{am_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{am_id}') GROUP BY status;"
                        forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                        
                        frcst_status = ''
                        if len(forecast_status) != 0:
                            for f in range(len(forecast_status)):
                                forecast = forecast_status[f]
                                frcst_status = str(forecast['status']).upper().strip()
                        
                        length += 1
            
                return dict(months = months, forecast_records = forecast_rec, length = length, status = frcst_status, am_id = am_id)


            # elif post_btn:
            #     am_id = request.args[0]

            #     # GET SUBMITTED DATE
            #     submitted_date = str(date_fixed)
            #     submitted_date_str = str(date_fixed).split(' ')[0]
            #     submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
            #     year = submitted_first_date.year
            #     month = submitted_first_date.month
            #     submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
            #     current_month = str(date_fixed).split(' ')[0]

            #     get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(am_id)+"' LIMIT 1;"
            #     get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
            #     for a in range(len(get_level_depth)):
            #         records = get_level_depth[a]
            #         am_name = records['sup_name']
            #         level_id = records['level_id']
            #         level_depth = records['level_depth_no']

            #     get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            #     get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            #     for a in range(len(get_level_records)):
            #         records_level = get_level_records[a]
            #         level0 = records_level['level0']
            #         level0_name = records_level['level0_name']
            #         level1 = records_level['level1']
            #         level1_name = records_level['level1_name']
            #         level2 = records_level['level2']
            #         level2_name = records_level['level2_name']
            #         level3 = records_level['level3']
            #         level3_name = records_level['level3_name']
                
            #     curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            #     curr_month = curr_date.strftime('%b-%y')

            #     month1 = str(curr_month).strip()
                # if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                #     forecasting_first_date="2024-01-01"
                # elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                #     forecasting_first_date="2024-02-01"
                # elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                #     forecasting_first_date="2024-03-01"
                # elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                #     forecasting_first_date="2024-04-01"
                # elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                #     forecasting_first_date="2024-05-01"
                # elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                #     forecasting_first_date="2024-06-01"
                # elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                #     forecasting_first_date="2024-07-01"
                # elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                #     forecasting_first_date="2024-08-01"
                # elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                #     forecasting_first_date="2024-09-01"
                # elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                #     forecasting_first_date="2024-10-01"
                # elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                #     forecasting_first_date="2024-11-01"
                # elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                #     forecasting_first_date="2024-12-01"
                
            #     status = "POSTED"

            #     item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                
            #     inputs_combined = [
            #         request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
            #         request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
            #         request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
            #         request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
            #         request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
            #         request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
            #         request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
            #         request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
            #         request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
            #         request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
            #         request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
            #         request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
            #         request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
            #         request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
            #         request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
            #         request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
            #         request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
            #         request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            #     ]   
                
            #     output_dict = {}  # Dictionary to store inputs grouped by item code
            #     for item_code in item_codes:
            #         output_dict[item_code] = []

            #     for i in range(len(item_codes)):
            #         for j in range(len(inputs_combined)):
            #             if inputs_combined[j][i] != '':
            #                 output_dict[item_codes[i]].append(inputs_combined[j][i])

            #     out_str = ''
            #     for item_code in output_dict:
            #         out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
            #     if out_str.endswith('|'):
            #         out_str = out_str[:-1]

            #     rows = out_str.split("|")

            #     data_array = []
            #     for row in rows:
            #         values = row.split(",")
            #         data_array.append(values)
                
            #     # price = 0.0

            #     current_month = str(date_fixed).split(' ')[0]
            #     first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            #     current_date = datetime.strptime(current_month, "%Y-%m-%d")
            #     year = first_date_str.year
            #     month = first_date_str.month
            #     planning_month = str(datetime(year, month, 1)).split(' ')[0]
            #     months = []

            #     # for i in range(18):
            #     #     months.append(current_date.strftime("%b-%Y"))
            #     #     current_date += timedelta(days=31)

            #     months.append(current_date.strftime("%b-%Y"))
            #     i = 1
            #     for i in range(17):
            #         current_date += timedelta(days=30)
            #         if str(current_date) == str(months[i-1]):
            #             i += 1
            #             continue
            #         else:
            #             months.append(current_date.strftime("%b-%Y"))

            #     month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months
                
            #     check_forecasting_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{am_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'POSTED';"
            #     check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            #     # remove previous forecasting
            #     if len(check_forecasting) > 0:
            #         # return 'del'
            #         delete_forecasting_sql = f"DELETE FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{am_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'POSTED';"
            #         db.executesql(delete_forecasting_sql)

            #     # month name insert sql 
            #     insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(am_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            #     db.executesql(insert_forcasting_header_sql)
                
            #     for sublist in data_array:
            #         item_id, *months = sublist
            #         month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

            #         get_item_price_sql = "SELECT item_id, name, unit_type, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
            #         get_item_price = db.executesql(get_item_price_sql, as_dict = True)

            #         for a in range(len(get_item_price)):
            #             item_record = get_item_price[a]
            #             item_name = item_record['name']
            #             UoM = item_record['unit_type']
            #             # price = item_record['price']

            #         # numerical value insert sql    
            #         insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(am_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(int(float(month1)))+"','"+str(int(float(month2)))+"','"+str(int(float(month3)))+"','"+str(int(float(month4)))+"','"+str(int(float(month5)))+"','"+str(int(float(month6)))+"','"+str(int(float(month7)))+"','"+str(int(float(month8)))+"','"+str(int(float(month9)))+"','"+str(int(float(month10)))+"','"+str(int(float(month11)))+"','"+str(int(float(month12)))+"','"+str(int(float(month13)))+"','"+str(int(float(month14)))+"','"+str(int(float(month15)))+"','"+str(int(float(month16)))+"','"+str(int(float(month17)))+"','"+str(int(float(month18)))+"','"+str(status)+"')"
            #         db.executesql(insert_forcasting_header_sql)

            # redirect(URL('forcasting','forcasting_for_sup'))


#========================== FORCASTING APPROVED REJECT FOR AM =======================================#

def forcasting_am_approve_reject():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        sup_id = session.user_id
        sup_name = session.name
        first_date_of_month = session.first_date_of_month
        am_id = request.args(0)
        approve_btn = request.vars.approve
        reject_btn = request.vars.reject

        if approve_btn == "Approve":     
            # approve data in temp table
            update_forcasting_status_sql = "UPDATE forecast_am_temp SET status = 'APPROVED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND sup_id = '"+str(am_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"';"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            
            # move approved data from temp table to main table
            all_forecast_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{am_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{am_id}') AND status = 'APPROVED' GROUP BY sup_id, first_date, item_code;"
            forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            if len(forecast_rec) != 0:
                for r in range(len(forecast_rec)):
                    records = forecast_rec[r]
                    am_name = str(records['sup_name'])
                    submitted_first_date = str(records['first_date'])
                    submitted_date = str(records['submitted_date'])
                    forecasting_first_date = str(records['forcasting_first_date'])
                    division  = str(records['division'])
                    country = str(records['country'])
                    zone_id = str(records['zone_id'])
                    zone_name = str(records['zone_name'])
                    region_id = str(records['region_id'])
                    region_name = str(records['region_name'])
                    area_id = str(records['area_id'])
                    area_name = str(records['area_name'])
                    territory_id = str(records['territory_id'])
                    territory_name = str(records['territory_name'])
                    sale_unit_id = str(records['sale_unit_id'])
                    sale_unit_name = str(records['sale_unit_name'])
                    item_code = str(records['item_code'])
                    item_name = str(records['item_name'])
                    UoM  = str(records['UoM'])
                    month1 = str(records['month1'])
                    month2 = str(records['month2'])
                    month3 = str(records['month3'])
                    month4 = str(records['month4'])
                    month5 = str(records['month5'])
                    month6 = str(records['month6'])
                    month7 = str(records['month7'])
                    month8 = str(records['month8'])
                    month9 = str(records['month9'])
                    month10 = str(records['month10'])
                    month11 = str(records['month11'])
                    month12 = str(records['month12'])
                    month13 = str(records['month13'])
                    month14 = str(records['month14'])
                    month15 = str(records['month15'])
                    month16 = str(records['month16'])
                    month17 = str(records['month17'])
                    month18 = str(records['month18'])
                    status  = str(records['status'])
                    approve_by_id = str(records['approve_by_id'])
                    approve_by_name = str(records['approve_by_name'])
                    
                    # copy-paste data from one table to another
                    insert_forcasting_header_sql = "INSERT INTO forecast_am (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, division, country, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status, approve_by_id, approve_by_name) VALUES('"+str(cid)+"','"+str(am_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(division)+"','"+str(country)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(region_id)+"','"+str(region_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(sale_unit_id)+"','"+str(sale_unit_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"','"+str(approve_by_id)+"','"+str(approve_by_name)+"')"
                    db.executesql(insert_forcasting_header_sql)
                
                delete_forecasting_sql = f"DELETE FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{am_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'APPROVED';"
                db.executesql(delete_forecasting_sql)

            response.flash = "APPROVED Successfully"



        elif reject_btn == "Reject":
            update_forcasting_status_sql = "UPDATE forecast_am_temp SET status = 'REJECTED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND sup_id = '"+str(am_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"' ;"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            
            response.flash = "REJECTED Successfully"

        redirect(URL('forcasting','forcasting_for_sup'))


#========================== MERGE AM FORECASTING FOR ZM SUP =======================================#

def process_am_forcasting():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        user_id = session.user_id

        user_name = ''
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''

        am_count = request.vars.am_count
        am_id_list = request.vars.am_list
        first_date_of_month = session.first_date_of_month
        process_btn = request.vars.zm_process_btn
        
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        months = []

        if process_btn:
            check_status_sql = "SELECT COUNT(DISTINCT sup_id) AS approved_am_count FROM forecast_am WHERE cid = '"+cid+"' AND sup_id IN ("+str(am_id_list)+") AND forcasting_first_date = '"+str(submitted_first_date)+"' AND status = 'APPROVED';"
            get_status = db.executesql(check_status_sql, as_dict=True)

            if len(get_status) > 0:
                approved_am = int(get_status[0]['approved_am_count'])
            else:
                approved_am = 0

            if int(approved_am) < int(am_count):
                session.process_flash = "All Forecast Not Approved Yet"
            
            else:
                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1_total = 0
                month2_total = 0
                month3_total = 0
                month4_total = 0
                month5_total = 0
                month6_total = 0
                month7_total = 0
                month8_total = 0
                month9_total = 0
                month10_total = 0
                month11_total = 0
                month12_total = 0
                month13_total = 0
                month14_total = 0
                month15_total = 0
                month16_total = 0
                month17_total = 0
                month18_total = 0
                count = 1

                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"

                status = 'PROCESSED'

                check_forecasting_sql = "SELECT * FROM  forecast_zm_temp WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' AND forcasting_first_date = '"+str(submitted_first_date)+"' AND status = 'PROCESSED' GROUP BY sup_id, item_code, forcasting_first_date;"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)
                
                if len(check_forecasting) == 0:
                    get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' LIMIT 1;"
                    get_level_depth = db.executesql(get_level_id_sql, as_dict = True)

                    for a in range(len(get_level_depth)):
                        records = get_level_depth[a]
                        sup_name = records['sup_name']
                        level_id = records['level_id']
                        level_depth = records['level_depth_no']
                    
                    get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
                    get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                    for a in range(len(get_level_records)):
                        records_level = get_level_records[a]
                        level0  = records_level['level0']
                        level0_name = records_level['level0_name']
                        level1  = records_level['level1']
                        level1_name = records_level['level1_name']
                        level2  = records_level['level2']
                        level2_name = records_level['level2_name']
                        level3  = records_level['level3']
                        level3_name = records_level['level3_name']

                    # merging all AM data
                    get_forcasting_for_am_sql = "SELECT item_code, item_name, UoM, SUM(month1) AS month1, SUM(month2) AS month2, SUM(month3) AS month3, SUM(month4) AS month4, SUM(month5) AS month5, SUM(month6) AS month6, SUM(month7) AS month7, SUM(month8) AS month8, SUM(month9) AS month9, SUM(month10) AS month10, SUM(month11) AS month11, SUM(month12) AS month12, SUM(month13) AS month13, SUM(month14) AS month14, SUM(month15) AS month15, SUM(month16) AS month16, SUM(month17) AS month17, SUM(month18) AS month18 FROM forecast_am WHERE cid = '"+cid+"' AND sup_id IN ("+str(am_id_list)+") AND submitted_date in (SELECT MAX(submitted_date) FROM forecast_am WHERE cid = '"+cid+"' and sup_id in ("+str(am_id_list)+") GROUP by sup_id) AND status = 'APPROVED' GROUP BY item_code;"
                    get_forcasting_for_am = db.executesql(get_forcasting_for_am_sql, as_dict = True)

                    # inserting into table
                    if len(get_forcasting_for_am) > 0 :
                        # insert processed data
                        for i in range(len(get_forcasting_for_am)):
                            forecast_records_str = get_forcasting_for_am[i]
                            
                            if i == 0:
                                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months
                                
                                # FOR TEMP TABLE - processed data
                                # month name insert sql 
                                insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                db.executesql(insert_forcasting_header_sql)

                                # FOR MAIN TABLE
                                # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                # db.executesql(insert_forcasting_header_sql)
                                continue

                            item_code = str(forecast_records_str['item_code'])
                            item_name = str(forecast_records_str['item_name'])
                            UoM = str(forecast_records_str['UoM'])
                            month1 = forecast_records_str['month1']
                            month2 = forecast_records_str['month2']
                            month3 = forecast_records_str['month3']
                            month4 = forecast_records_str['month4']
                            month5 = forecast_records_str['month5']
                            month6 = forecast_records_str['month6']
                            month7 = forecast_records_str['month7']
                            month8 = forecast_records_str['month8']
                            month9 = forecast_records_str['month9']
                            month10 = forecast_records_str['month10']
                            month11 = forecast_records_str['month11']
                            month12 = forecast_records_str['month12']
                            month13 = forecast_records_str['month13']
                            month14 = forecast_records_str['month14']
                            month15 = forecast_records_str['month15']
                            month16 = forecast_records_str['month16']
                            month17 = forecast_records_str['month17']
                            month18 = forecast_records_str['month18']
                            
                            try:
                                month1_total += float(month1)
                                month2_total += float(month2)
                                month3_total += float(month3)
                                month4_total += float(month4)
                                month5_total += float(month5)
                                month6_total += float(month6)
                                month7_total += float(month7)
                                month8_total += float(month8)
                                month9_total += float(month9)
                                month10_total += float(month10)
                                month11_total += float(month11)
                                month12_total += float(month12)
                                month13_total += float(month13)
                                month14_total += float(month14)
                                month15_total += float(month15)
                                month16_total += float(month16)
                                month17_total += float(month17)
                                month18_total += float(month18)

                            except:
                                pass

                            i += 1
                            
                            # FOR TEMP TABLE - processed data
                            # numerical value insert sql
                            insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                            db.executesql(insert_forcasting_header_sql)

                            # FOR MAIN TABLE
                            # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                            # db.executesql(insert_forcasting_header_sql)
                        
                        # insert submitted data
                        for i in range(len(get_forcasting_for_am)):
                            forecast_records_str = get_forcasting_for_am[i]
                            
                            if i == 0:
                                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                                # FOR TEMP TABLE - submitted data
                                # month name insert sql 
                                insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','SUBMITTED')"
                                db.executesql(insert_forcasting_header_sql)

                                # FOR MAIN TABLE
                                # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                # db.executesql(insert_forcasting_header_sql)
                                continue

                            item_code = str(forecast_records_str['item_code'])
                            item_name = str(forecast_records_str['item_name'])
                            UoM = str(forecast_records_str['UoM'])
                            month1 = round(float(forecast_records_str['month1']), 2)
                            month2 = round(float(forecast_records_str['month2']), 2)
                            month3 = round(float(forecast_records_str['month3']), 2)
                            month4 = round(float(forecast_records_str['month4']), 2)
                            month5 = round(float(forecast_records_str['month5']), 2)
                            month6 = round(float(forecast_records_str['month6']), 2)
                            month7 = round(float(forecast_records_str['month7']), 2)
                            month8 = round(float(forecast_records_str['month8']), 2)
                            month9 = round(float(forecast_records_str['month9']), 2)
                            month10 = round(float(forecast_records_str['month10']), 2)
                            month11 = round(float(forecast_records_str['month11']), 2)
                            month12 = round(float(forecast_records_str['month12']), 2)
                            month13 = round(float(forecast_records_str['month13']), 2)
                            month14 = round(float(forecast_records_str['month14']), 2)
                            month15 = round(float(forecast_records_str['month15']), 2)
                            month16 = round(float(forecast_records_str['month16']), 2)
                            month17 = round(float(forecast_records_str['month17']), 2)
                            month18 = round(float(forecast_records_str['month18']), 2)
                            
                            try:
                                month1_total += float(month1)
                                month2_total += float(month2)
                                month3_total += float(month3)
                                month4_total += float(month4)
                                month5_total += float(month5)
                                month6_total += float(month6)
                                month7_total += float(month7)
                                month8_total += float(month8)
                                month9_total += float(month9)
                                month10_total += float(month10)
                                month11_total += float(month11)
                                month12_total += float(month12)
                                month13_total += float(month13)
                                month14_total += float(month14)
                                month15_total += float(month15)
                                month16_total += float(month16)
                                month17_total += float(month17)
                                month18_total += float(month18)

                            except:
                                pass

                            i += 1

                            # FOR TEMP TABLE - submitted data
                            # numerical value insert sql
                            insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','SUBMITTED')"
                            db.executesql(insert_forcasting_header_sql)

                            # FOR MAIN TABLE
                            # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                            # db.executesql(insert_forcasting_header_sql)
                        
                    session.process_flash = "Forecasting Ready To View"

        else:
            session.process_flash = "Already Processed Once"
            
            
        redirect(URL('forcasting','forcasting_for_sup'))  


#========================== FORCASTING VIEW FOR ZM SUP =======================================#

def forcasting_zm_view():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type
        depth = str(session.level_depth)

        # btns
        sup_view_btn = request.vars.zm_view_edit

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))

        if depth == '1':
            get_processed_data_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"
            processed_data = db.executesql(get_processed_data_sql, as_dict=True)

            length = 0
            # all_forecast_sql = f"SELECT * FROM forecast_zm WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY sup_id, first_date, item_code;"
            all_forecast_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY sup_id, first_date, item_code;"
            forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            if len(forecast_rec) != 0:
                check_forcasting_status = f"SELECT status FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
                forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                
                frcst_status = ''
                if len(forecast_status) != 0:
                    for f in range(len(forecast_status)):
                        forecast = forecast_status[f]
                        frcst_status = str(forecast['status']).upper().strip() 
                
                length += 1
        
        return dict(months = months, forecast_records = forecast_rec, processed_records = processed_data, length = length, status = frcst_status, planning_month = planning_month)


#========================== VIEW EDIT FOR SUP =======================================#

def forcasting_sup_edit_zm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        # GET SUBMITTED DATE
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]

        cid = session.cid
        rep_id = session.user_id
        rep_name = session.name
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''

        submit_btn_new = request.vars.submit_btn_new
        submit_btn_old = request.vars.submit_btn_old
        post_btn = request.vars.post_btn

        if submit_btn_new:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']

            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')
            
            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "SUBMITTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   

            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'

            if out_str.endswith('|'):
                out_str = out_str[:-1]
            
            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)

            months = []
            months = request.vars.month_list
            
            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)
            
            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    
                # numerical value insert sql
                insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)
        
        elif submit_btn_old:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "SUBMITTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   
            
            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]
            
            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            check_forecasting_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            # remove previous forecasting
            if len(check_forecasting) > 0:
                delete_forecasting_sql = f"DELETE FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
                db.executesql(delete_forecasting_sql)
            
            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES ('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']

                # numerical value insert sql   
                insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

            session.update_flash = "Updated Succesfully"
        
        elif post_btn:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "POSTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   
            
            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]

            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            check_forecasting_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            # remove previous forecasting
            if len(check_forecasting) > 0:
                delete_forecasting_sql = f"DELETE FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
                db.executesql(delete_forecasting_sql)
            
            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']

                # numerical value insert sql
                insert_forcasting_header_sql = "INSERT INTO forecast_zm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

            session.post_flash = "Posted Succesfully"
                
        else:
            session.flash = "Already submitted once"

        # redirect(URL('forcasting','forcasting_for_sup'))
        redirect(URL('forcasting','forcasting_zm_view'))


#========================== INDIVIDUAL FORCASTING VIEW FOR AM ==========================#

def forcasting_view_zm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type
        
        # btns
        zm_view_btn = request.vars.zm_view
        post_btn = request.vars.post_btn

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        if user_type == 'sup':
            length = 0

            if zm_view_btn:
                zm_id = request.args[0]

                all_forecast_sql = f"SELECT * FROM forecast_zm WHERE cid='{cid}' AND sup_id = '{zm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm WHERE cid = '{cid}' AND sup_id = '{zm_id}') GROUP BY sup_id, first_date, item_code;"
                forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

                if len(forecast_rec) != 0:
                    check_forcasting_status = f"SELECT status FROM forecast_zm WHERE cid='{cid}' AND sup_id = '{zm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm WHERE cid = '{cid}' AND sup_id = '{zm_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()
                    
                    length += 1
                
                else:
                    all_forecast_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{zm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{zm_id}') GROUP BY sup_id, first_date, item_code;"
                    forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
                    
                    if len(forecast_rec) != 0:
                        check_forcasting_status = f"SELECT status FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{zm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{zm_id}') GROUP BY status;"
                        forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                        
                        frcst_status = ''
                        if len(forecast_status) != 0:
                            for f in range(len(forecast_status)):
                                forecast = forecast_status[f]
                                frcst_status = str(forecast['status']).upper().strip()
                        
                        length += 1
                        return dict(months = months, forecast_records = forecast_rec, length = length, status = frcst_status, zm_id = zm_id)


            # elif post_btn:
            #     am_id = request.args[0]

            #     # GET SUBMITTED DATE
            #     submitted_date = str(date_fixed)
            #     submitted_date_str = str(date_fixed).split(' ')[0]
            #     submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
            #     year = submitted_first_date.year
            #     month = submitted_first_date.month
            #     submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
            #     current_month = str(date_fixed).split(' ')[0]

            #     get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(am_id)+"' LIMIT 1;"
            #     get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
            
            #     for a in range(len(get_level_depth)):
            #         records = get_level_depth[a]
            #         am_name = records['sup_name']
            #         level_id = records['level_id']
            #         level_depth = records['level_depth_no']

            #     get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            #     get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            #     for a in range(len(get_level_records)):
            #         records_level = get_level_records[a]
            #         level0 = records_level['level0']
            #         level0_name = records_level['level0_name']
            #         level1 = records_level['level1']
            #         level1_name = records_level['level1_name']
            #         level2 = records_level['level2']
            #         level2_name = records_level['level2_name']
            #         level3 = records_level['level3']
            #         level3_name = records_level['level3_name']
                
            #     curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            #     curr_month = curr_date.strftime('%b-%y')

            #     month1 = str(curr_month).strip()
                # if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                #     forecasting_first_date="2024-01-01"
                # elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                #     forecasting_first_date="2024-02-01"
                # elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                #     forecasting_first_date="2024-03-01"
                # elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                #     forecasting_first_date="2024-04-01"
                # elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                #     forecasting_first_date="2024-05-01"
                # elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                #     forecasting_first_date="2024-06-01"
                # elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                #     forecasting_first_date="2024-07-01"
                # elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                #     forecasting_first_date="2024-08-01"
                # elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                #     forecasting_first_date="2024-09-01"
                # elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                #     forecasting_first_date="2024-10-01"
                # elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                #     forecasting_first_date="2024-11-01"
                # elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                #     forecasting_first_date="2024-12-01"
                
            #     status = "POSTED"

            #     item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
                
            #     inputs_combined = [
            #         request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
            #         request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
            #         request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
            #         request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
            #         request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
            #         request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
            #         request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
            #         request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
            #         request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
            #         request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
            #         request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
            #         request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
            #         request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
            #         request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
            #         request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
            #         request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
            #         request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
            #         request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            #     ]   
                
            #     output_dict = {}  # Dictionary to store inputs grouped by item code
            #     for item_code in item_codes:
            #         output_dict[item_code] = []

            #     for i in range(len(item_codes)):
            #         for j in range(len(inputs_combined)):
            #             if inputs_combined[j][i] != '':
            #                 output_dict[item_codes[i]].append(inputs_combined[j][i])

            #     out_str = ''
            #     for item_code in output_dict:
            #         out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
                
            #     if out_str.endswith('|'):
            #         out_str = out_str[:-1]

            #     rows = out_str.split("|")

            #     data_array = []
            #     for row in rows:
            #         values = row.split(",")
            #         data_array.append(values)
                
            #     # price = 0.0

            #     current_month = str(date_fixed).split(' ')[0]
            #     first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            #     current_date = datetime.strptime(current_month, "%Y-%m-%d")
            #     year = first_date_str.year
            #     month = first_date_str.month
            #     planning_month = str(datetime(year, month, 1)).split(' ')[0]
            #     months = []

            #     # for i in range(18):
            #     #     months.append(current_date.strftime("%b-%Y"))
            #     #     current_date += timedelta(days=31)

            #     months.append(current_date.strftime("%b-%Y"))
            #     i = 1
            #     for i in range(17):
            #         current_date += timedelta(days=30)
            #         if str(current_date) == str(months[i-1]):
            #             i += 1
            #             continue
            #         else:
            #             months.append(current_date.strftime("%b-%Y"))

            #     month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months
                
            #     check_forecasting_sql = f"SELECT * FROM forecast_am_temp WHERE cid='{cid}' AND sup_id = '{am_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'POSTED';"
            #     check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            #     # remove previous forecasting
            #     if len(check_forecasting) > 0:
            #         delete_forecasting_sql = f"DELETE FROM forecast_am_temp WHERE cid = '{cid}' AND sup_id = '{am_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'POSTED';"
            #         db.executesql(delete_forecasting_sql)
                
            #     # month name insert sql 
            #     insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(am_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            #     db.executesql(insert_forcasting_header_sql)
                
            #     for sublist in data_array:
            #         item_id, *months = sublist
            #         month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

            #         get_item_price_sql = "SELECT item_id, name, unit_type, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
            #         get_item_price = db.executesql(get_item_price_sql, as_dict = True)

            #         for a in range(len(get_item_price)):
            #             item_record = get_item_price[a]
            #             item_name = item_record['name']
            #             UoM = item_record['unit_type']
            #             # price = item_record['price']
                        
            #         # numerical value insert sql
            #         insert_forcasting_header_sql = "INSERT INTO forecast_am_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(am_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(int(float(month1)))+"','"+str(int(float(month2)))+"','"+str(int(float(month3)))+"','"+str(int(float(month4)))+"','"+str(int(float(month5)))+"','"+str(int(float(month6)))+"','"+str(int(float(month7)))+"','"+str(int(float(month8)))+"','"+str(int(float(month9)))+"','"+str(int(float(month10)))+"','"+str(int(float(month11)))+"','"+str(int(float(month12)))+"','"+str(int(float(month13)))+"','"+str(int(float(month14)))+"','"+str(int(float(month15)))+"','"+str(int(float(month16)))+"','"+str(int(float(month17)))+"','"+str(int(float(month18)))+"','"+str(status)+"')"
            #         db.executesql(insert_forcasting_header_sql)

            redirect(URL('forcasting','forcasting_for_sup'))


#========================== FORCASTING APPROVED REJECT FOR AM =======================================#

def forcasting_zm_approve_reject():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        sup_id = session.user_id
        sup_name = session.name
        first_date_of_month = session.first_date_of_month
        zm_id = request.args(0)
        approve_btn = request.vars.approve
        reject_btn = request.vars.reject

        if approve_btn == "Approve":     
            # approve data in temp table
            update_forcasting_status_sql = "UPDATE forecast_zm_temp SET status = 'APPROVED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND sup_id = '"+str(zm_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"';"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            
            # move approved data from temp table to main table
            all_forecast_sql = f"SELECT * FROM forecast_zm_temp WHERE cid='{cid}' AND sup_id = '{zm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{zm_id}') AND status = 'APPROVED' GROUP BY sup_id, first_date, item_code;"
            forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            if len(forecast_rec) != 0:
                for r in range(len(forecast_rec)):
                    records = forecast_rec[r]
                    am_name = str(records['sup_name'])
                    submitted_first_date = str(records['first_date'])
                    submitted_date = str(records['submitted_date'])
                    forecasting_first_date = str(records['forcasting_first_date'])
                    division  = str(records['division'])
                    country = str(records['country'])
                    zone_id = str(records['zone_id'])
                    zone_name = str(records['zone_name'])
                    region_id = str(records['region_id'])
                    region_name = str(records['region_name'])
                    area_id = str(records['area_id'])
                    area_name = str(records['area_name'])
                    territory_id = str(records['territory_id'])
                    territory_name = str(records['territory_name'])
                    sale_unit_id = str(records['sale_unit_id'])
                    sale_unit_name = str(records['sale_unit_name'])
                    item_code = str(records['item_code'])
                    item_name = str(records['item_name'])
                    UoM  = str(records['UoM'])
                    month1 = str(records['month1'])
                    month2 = str(records['month2'])
                    month3 = str(records['month3'])
                    month4 = str(records['month4'])
                    month5 = str(records['month5'])
                    month6 = str(records['month6'])
                    month7 = str(records['month7'])
                    month8 = str(records['month8'])
                    month9 = str(records['month9'])
                    month10 = str(records['month10'])
                    month11 = str(records['month11'])
                    month12 = str(records['month12'])
                    month13 = str(records['month13'])
                    month14 = str(records['month14'])
                    month15 = str(records['month15'])
                    month16 = str(records['month16'])
                    month17 = str(records['month17'])
                    month18 = str(records['month18'])
                    status  = str(records['status'])
                    approve_by_id = str(records['approve_by_id'])
                    approve_by_name = str(records['approve_by_name'])
                    
                    # copy-paste data from one table to another
                    insert_forcasting_header_sql = "INSERT INTO forecast_zm (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, division, country, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status, approve_by_id, approve_by_name) VALUES('"+str(cid)+"','"+str(zm_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(division)+"','"+str(country)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(region_id)+"','"+str(region_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(sale_unit_id)+"','"+str(sale_unit_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"','"+str(approve_by_id)+"','"+str(approve_by_name)+"')"
                    db.executesql(insert_forcasting_header_sql)
                
                delete_forecasting_sql = f"DELETE FROM forecast_zm_temp WHERE cid = '{cid}' AND sup_id = '{zm_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'APPROVED';"
                db.executesql(delete_forecasting_sql)

            response.flash = "APPROVED Successfully"



        elif reject_btn == "Reject":
            update_forcasting_status_sql = "UPDATE forecast_am SET status = 'REJECTED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND am_id = '"+str(am_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"' ;"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            response.flash = "REJECTED Successfully"

        redirect(URL('forcasting','forcasting_for_sup'))


#========================== MERGE AM FORECASTING FOR ZM SUP =======================================#

def process_zm_forcasting():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        user_id = session.user_id

        user_name = ''
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''

        zm_count = request.vars.zm_count
        zm_id_list = request.vars.zm_list
        first_date_of_month = session.first_date_of_month
        process_btn = request.vars.rm_process_btn
        
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        months = []

        if process_btn:
            check_status_sql = "SELECT COUNT(DISTINCT sup_id) AS approved_zm_count FROM forecast_zm WHERE cid = '"+cid+"' AND sup_id IN ("+str(zm_id_list)+") AND forcasting_first_date = '"+str(submitted_first_date)+"' AND status = 'APPROVED';"
            get_status = db.executesql(check_status_sql, as_dict=True)

            if len(get_status) > 0:
                approved_zm = int(get_status[0]['approved_zm_count'])
            else:
                approved_zm = 0

            if int(approved_zm) < int(zm_count):
                session.process_flash = "All Forecast Not Approved Yet"
            
            else:
                # for i in range(18):
                #     months.append(current_date.strftime("%b-%Y"))
                #     current_date += timedelta(days=31)

                months.append(current_date.strftime("%b-%Y"))
                i = 1
                for i in range(17):
                    current_date += timedelta(days=30)
                    if str(current_date) == str(months[i-1]):
                        i += 1
                        continue
                    else:
                        months.append(current_date.strftime("%b-%Y"))

                month1_total = 0
                month2_total = 0
                month3_total = 0
                month4_total = 0
                month5_total = 0
                month6_total = 0
                month7_total = 0
                month8_total = 0
                month9_total = 0
                month10_total = 0
                month11_total = 0
                month12_total = 0
                month13_total = 0
                month14_total = 0
                month15_total = 0
                month16_total = 0
                month17_total = 0
                month18_total = 0
                count = 1

                curr_date = datetime.strptime(current_month, '%Y-%m-%d')
                curr_month = curr_date.strftime('%b-%y')

                month1 = str(curr_month).strip()
                if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                    forecasting_first_date="2024-01-01"
                elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                    forecasting_first_date="2024-02-01"
                elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                    forecasting_first_date="2024-03-01"
                elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                    forecasting_first_date="2024-04-01"
                elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                    forecasting_first_date="2024-05-01"
                elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                    forecasting_first_date="2024-06-01"
                elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                    forecasting_first_date="2024-07-01"
                elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                    forecasting_first_date="2024-08-01"
                elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                    forecasting_first_date="2024-09-01"
                elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                    forecasting_first_date="2024-10-01"
                elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                    forecasting_first_date="2024-11-01"
                elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                    forecasting_first_date="2024-12-01"

                status = 'PROCESSED'

                check_forecasting_sql = "SELECT * FROM  forecast_rm_temp WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' AND forcasting_first_date = '"+str(submitted_first_date)+"' AND status = 'PROCESSED' GROUP BY sup_id, item_code, forcasting_first_date;"
                check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)
                
                if len(check_forecasting) == 0:
                    get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' LIMIT 1;"
                    get_level_depth = db.executesql(get_level_id_sql, as_dict = True)

                    for a in range(len(get_level_depth)):
                        records = get_level_depth[a]
                        sup_name = records['sup_name']
                        level_id = records['level_id']
                        level_depth = records['level_depth_no']
                    
                    get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
                    get_level_records = db.executesql(get_level_records_sql, as_dict = True)

                    for a in range(len(get_level_records)):
                        records_level = get_level_records[a]
                        level0  = records_level['level0']
                        level0_name = records_level['level0_name']
                        level1  = records_level['level1']
                        level1_name = records_level['level1_name']
                        level2  = records_level['level2']
                        level2_name = records_level['level2_name']
                        level3  = records_level['level3']
                        level3_name = records_level['level3_name']

                    # merging all ZM data
                    get_forcasting_for_zm_sql = "SELECT item_code, item_name, UoM, SUM(month1) AS month1, SUM(month2) AS month2, SUM(month3) AS month3, SUM(month4) AS month4, SUM(month5) AS month5, SUM(month6) AS month6, SUM(month7) AS month7, SUM(month8) AS month8, SUM(month9) AS month9, SUM(month10) AS month10, SUM(month11) AS month11, SUM(month12) AS month12, SUM(month13) AS month13, SUM(month14) AS month14, SUM(month15) AS month15, SUM(month16) AS month16, SUM(month17) AS month17, SUM(month18) AS month18 FROM forecast_zm WHERE cid = '"+cid+"' AND sup_id IN ("+str(zm_id_list)+") AND submitted_date in (SELECT MAX(submitted_date) FROM forecast_zm WHERE cid = '"+cid+"' and sup_id in ("+str(zm_id_list)+") GROUP by sup_id) AND status = 'APPROVED' GROUP BY item_code;"
                    get_forcasting_for_zm = db.executesql(get_forcasting_for_zm_sql, as_dict = True)

                    # inserting into table
                    if len(get_forcasting_for_zm) > 0 :
                        # insert processed data
                        for i in range(len(get_forcasting_for_zm)):
                            forecast_records_str = get_forcasting_for_zm[i]
                            
                            if i == 0:
                                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months
                                
                                # FOR TEMP TABLE - processed data
                                # month name insert sql 
                                insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                db.executesql(insert_forcasting_header_sql)

                                # FOR MAIN TABLE
                                # insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                # return insert_forcasting_header_sql
                                # db.executesql(insert_forcasting_header_sql)
                                continue
                            
                            item_code = str(forecast_records_str['item_code'])
                            item_name = str(forecast_records_str['item_name'])
                            UoM = str(forecast_records_str['UoM'])
                            month1 = forecast_records_str['month1']
                            month2 = forecast_records_str['month2']
                            month3 = forecast_records_str['month3']
                            month4 = forecast_records_str['month4']
                            month5 = forecast_records_str['month5']
                            month6 = forecast_records_str['month6']
                            month7 = forecast_records_str['month7']
                            month8 = forecast_records_str['month8']
                            month9 = forecast_records_str['month9']
                            month10 = forecast_records_str['month10']
                            month11 = forecast_records_str['month11']
                            month12 = forecast_records_str['month12']
                            month13 = forecast_records_str['month13']
                            month14 = forecast_records_str['month14']
                            month15 = forecast_records_str['month15']
                            month16 = forecast_records_str['month16']
                            month17 = forecast_records_str['month17']
                            month18 = forecast_records_str['month18']
                            
                            try:
                                month1_total += float(month1)
                                month2_total += float(month2)
                                month3_total += float(month3)
                                month4_total += float(month4)
                                month5_total += float(month5)
                                month6_total += float(month6)
                                month7_total += float(month7)
                                month8_total += float(month8)
                                month9_total += float(month9)
                                month10_total += float(month10)
                                month11_total += float(month11)
                                month12_total += float(month12)
                                month13_total += float(month13)
                                month14_total += float(month14)
                                month15_total += float(month15)
                                month16_total += float(month16)
                                month17_total += float(month17)
                                month18_total += float(month18)

                            except:
                                pass

                            i += 1
                            
                            # FOR TEMP TABLE - processed data
                            # numerical value insert sql
                            insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                            db.executesql(insert_forcasting_header_sql)

                            # FOR MAIN TABLE
                            # insert_forcasting_header_sql = "INSERT INTO forecast_rm (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                            # db.executesql(insert_forcasting_header_sql)
                        
                        # insert submitted data
                        for i in range(len(get_forcasting_for_zm)):
                            forecast_records_str = get_forcasting_for_zm[i]
                            
                            if i == 0:
                                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

                                # FOR TEMP TABLE - submitted data
                                # month name insert sql 
                                insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','SUBMITTED')"
                                db.executesql(insert_forcasting_header_sql)

                                # FOR MAIN TABLE
                                # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                                # db.executesql(insert_forcasting_header_sql)
                                continue

                            item_code = str(forecast_records_str['item_code'])
                            item_name = str(forecast_records_str['item_name'])
                            UoM = str(forecast_records_str['UoM'])
                            month1 = round(float(forecast_records_str['month1']), 2)
                            month2 = round(float(forecast_records_str['month2']), 2)
                            month3 = round(float(forecast_records_str['month3']), 2)
                            month4 = round(float(forecast_records_str['month4']), 2)
                            month5 = round(float(forecast_records_str['month5']), 2)
                            month6 = round(float(forecast_records_str['month6']), 2)
                            month7 = round(float(forecast_records_str['month7']), 2)
                            month8 = round(float(forecast_records_str['month8']), 2)
                            month9 = round(float(forecast_records_str['month9']), 2)
                            month10 = round(float(forecast_records_str['month10']), 2)
                            month11 = round(float(forecast_records_str['month11']), 2)
                            month12 = round(float(forecast_records_str['month12']), 2)
                            month13 = round(float(forecast_records_str['month13']), 2)
                            month14 = round(float(forecast_records_str['month14']), 2)
                            month15 = round(float(forecast_records_str['month15']), 2)
                            month16 = round(float(forecast_records_str['month16']), 2)
                            month17 = round(float(forecast_records_str['month17']), 2)
                            month18 = round(float(forecast_records_str['month18']), 2)
                            
                            try:
                                month1_total += float(month1)
                                month2_total += float(month2)
                                month3_total += float(month3)
                                month4_total += float(month4)
                                month5_total += float(month5)
                                month6_total += float(month6)
                                month7_total += float(month7)
                                month8_total += float(month8)
                                month9_total += float(month9)
                                month10_total += float(month10)
                                month11_total += float(month11)
                                month12_total += float(month12)
                                month13_total += float(month13)
                                month14_total += float(month14)
                                month15_total += float(month15)
                                month16_total += float(month16)
                                month17_total += float(month17)
                                month18_total += float(month18)

                            except:
                                pass

                            i += 1

                            # FOR TEMP TABLE - submitted data
                            # numerical value insert sql
                            insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','SUBMITTED')"
                            db.executesql(insert_forcasting_header_sql)

                            # FOR MAIN TABLE
                            # insert_forcasting_header_sql = "INSERT INTO forecast_am(cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(user_id)+"','"+str(sup_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
                            # db.executesql(insert_forcasting_header_sql)
                        
                    session.process_flash = "Forecasting Ready To View"

        else:
            session.process_flash = "Already Processed Once"
    

        redirect(URL('forcasting','forcasting_for_sup'))  


#========================== FORCASTING VIEW FOR ZM SUP =======================================#

def forcasting_rm_view():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type
        depth = str(session.level_depth)

        # btns
        sup_view_btn = request.vars.rm_view_edit

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))
        
        # length = 0
        # all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY sup_id, first_date, item_code;"
        # forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
        
        # if len(forecast_rec) != 0:
        #     check_forcasting_status = f"SELECT status FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
        #     forecast_status = db.executesql(check_forcasting_status, as_dict=True)
            
        #     frcst_status = ''
        #     if len(forecast_status) != 0:
        #         for f in range(len(forecast_status)):
        #             forecast = forecast_status[f]
        #             frcst_status = str(forecast['status']).upper().strip() 
            
        #     length += 1
        
        if depth == '0':
            get_processed_data_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND status = 'PROCESSED') AND status = 'PROCESSED' GROUP BY sup_id, first_date, item_code;"
            processed_data = db.executesql(get_processed_data_sql, as_dict=True)

            length = 0
            all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') AND (status = 'SUBMITTED' OR status = 'POSTED' OR status = 'REJECTED') GROUP BY sup_id, first_date, item_code;"
            forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            if len(forecast_rec) != 0:
                check_forcasting_status = f"SELECT status FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{user_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}') GROUP BY status;"
                forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                
                frcst_status = ''
                if len(forecast_status) != 0:
                    for f in range(len(forecast_status)):
                        forecast = forecast_status[f]
                        frcst_status = str(forecast['status']).upper().strip() 
                
                length += 1
            
            return dict(months = months, forecast_records = forecast_rec, processed_records = processed_data, length = length, status = frcst_status, planning_month = planning_month)


#========================== VIEW EDIT FOR SUP =======================================#

def forcasting_sup_edit_rm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        # GET SUBMITTED DATE
        submitted_date = str(date_fixed)
        submitted_date_str = str(date_fixed).split(' ')[0]
        submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
        year = submitted_first_date.year
        month = submitted_first_date.month
        submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
        current_month = str(date_fixed).split(' ')[0]

        cid = session.cid
        rep_id = session.user_id
        rep_name = session.name
        area_id= ''
        level0 =''
        level0_name=''
        level1 =''
        level1_name=''
        level2 =''
        level2_name=''
        level3 =''
        level3_name=''
        forecasting_first_date = ''

        submit_btn_new = request.vars.submit_btn_new
        submit_btn_old = request.vars.submit_btn_old
        post_btn = request.vars.post_btn

        if submit_btn_new:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']

            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')
            
            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "SUBMITTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   

            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'

            if out_str.endswith('|'):
                out_str = out_str[:-1]
            
            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)

            months = []
            months = request.vars.month_list
            
            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)
            
            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    
                # numerical value insert sql
                insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, rep_id, rep_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)
        
        elif submit_btn_old:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "SUBMITTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   
            
            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]
            
            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            check_forecasting_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND (status = 'SUBMITTED' OR status = 'REJECTED');"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            # remove previous forecasting
            if len(check_forecasting) > 0:
                delete_forecasting_sql = f"DELETE FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND (status = 'SUBMITTED' OR status = 'REJECTED');"
                db.executesql(delete_forecasting_sql)
            
            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES ('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']

                # numerical value insert sql    
                insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)
        
            session.update_flash = "Updated Succesfully"
        
        elif post_btn:
            get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rep_id)+"' LIMIT 1;"
            get_level_depth = db.executesql(get_level_id_sql, as_dict = True)
        
            for a in range(len(get_level_depth)):
                records = get_level_depth[a]
                sup_name = records['sup_name']
                level_id = records['level_id']
                level_depth = records['level_depth_no']

            get_level_records_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level_id = '"+str(level_id)+"' AND depth = '"+str(level_depth)+"' AND is_leaf = '0' GROUP BY level3 LIMIT 1;"
            get_level_records = db.executesql(get_level_records_sql, as_dict = True)

            for a in range(len(get_level_records)):
                records_level = get_level_records[a]
                level0  = records_level['level0']
                level0_name = records_level['level0_name']
                level1  = records_level['level1']
                level1_name = records_level['level1_name']
                level2  = records_level['level2']
                level2_name = records_level['level2_name']
                level3  = records_level['level3']
                level3_name = records_level['level3_name']
            
            curr_date = datetime.strptime(current_month, '%Y-%m-%d')
            curr_month = curr_date.strftime('%b-%y')

            month1 = str(curr_month).strip()
            if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
                forecasting_first_date="2024-01-01"
            elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
                forecasting_first_date="2024-02-01"
            elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
                forecasting_first_date="2024-03-01"
            elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
                forecasting_first_date="2024-04-01"
            elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
                forecasting_first_date="2024-05-01"
            elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
                forecasting_first_date="2024-06-01"
            elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
                forecasting_first_date="2024-07-01"
            elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
                forecasting_first_date="2024-08-01"
            elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
                forecasting_first_date="2024-09-01"
            elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
                forecasting_first_date="2024-10-01"
            elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
                forecasting_first_date="2024-11-01"
            elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
                forecasting_first_date="2024-12-01"
            
            status = "POSTED"

            item_codes = request.vars.item_code if isinstance(request.vars.item_code, (list, tuple)) else [request.vars.item_code]
            
            inputs_combined = [
                request.vars.input1 if isinstance(request.vars.input1, (list, tuple)) else [request.vars.input1],
                request.vars.input2 if isinstance(request.vars.input2, (list, tuple)) else [request.vars.input2],
                request.vars.input3 if isinstance(request.vars.input3, (list, tuple)) else [request.vars.input3],
                request.vars.input4 if isinstance(request.vars.input4, (list, tuple)) else [request.vars.input4],
                request.vars.input5 if isinstance(request.vars.input5, (list, tuple)) else [request.vars.input5],
                request.vars.input6 if isinstance(request.vars.input6, (list, tuple)) else [request.vars.input6],
                request.vars.input7 if isinstance(request.vars.input7, (list, tuple)) else [request.vars.input7],
                request.vars.input8 if isinstance(request.vars.input8, (list, tuple)) else [request.vars.input8],
                request.vars.input9 if isinstance(request.vars.input9, (list, tuple)) else [request.vars.input9],
                request.vars.input10 if isinstance(request.vars.input10, (list, tuple)) else [request.vars.input10],
                request.vars.input11 if isinstance(request.vars.input11, (list, tuple)) else [request.vars.input11],
                request.vars.input12 if isinstance(request.vars.input12, (list, tuple)) else [request.vars.input12],
                request.vars.input13 if isinstance(request.vars.input13, (list, tuple)) else [request.vars.input13],
                request.vars.input14 if isinstance(request.vars.input14, (list, tuple)) else [request.vars.input14],
                request.vars.input15 if isinstance(request.vars.input15, (list, tuple)) else [request.vars.input15],
                request.vars.input16 if isinstance(request.vars.input16, (list, tuple)) else [request.vars.input16],
                request.vars.input17 if isinstance(request.vars.input17, (list, tuple)) else [request.vars.input17],
                request.vars.input18 if isinstance(request.vars.input18, (list, tuple)) else [request.vars.input18]
            ]   
            
            output_dict = {}  # Dictionary to store inputs grouped by item code
            for item_code in item_codes:
                output_dict[item_code] = []

            for i in range(len(item_codes)):
                for j in range(len(inputs_combined)):
                    if inputs_combined[j][i] != '':
                        output_dict[item_codes[i]].append(inputs_combined[j][i])

            out_str = ''
            for item_code in output_dict:
                out_str += str(item_code) + ', ' + ', '.join(output_dict[item_code]) + '|'
            
            if out_str.endswith('|'):
                out_str = out_str[:-1]

            rows = out_str.split("|")

            data_array = []
            for row in rows:
                values = row.split(",")
                data_array.append(values)
            
            # price = 0.0

            current_month = str(date_fixed).split(' ')[0]
            first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
            current_date = datetime.strptime(current_month, "%Y-%m-%d")
            year = first_date_str.year
            month = first_date_str.month
            planning_month = str(datetime(year, month, 1)).split(' ')[0]
            months = []

            # for i in range(18):
            #     months.append(current_date.strftime("%b-%Y"))
            #     current_date += timedelta(days=31)

            months.append(current_date.strftime("%b-%Y"))
            i = 1
            for i in range(17):
                current_date += timedelta(days=30)
                if str(current_date) == str(months[i-1]):
                    i += 1
                    continue
                else:
                    months.append(current_date.strftime("%b-%Y"))

            month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = months

            check_forecasting_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
            check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            # remove previous forecasting
            if len(check_forecasting) > 0:
                delete_forecasting_sql = f"DELETE FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rep_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'SUBMITTED';"
                db.executesql(delete_forecasting_sql)
            
            # month name insert sql 
            insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12,month13,month14,month15,month16,month17,month18,status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
            db.executesql(insert_forcasting_header_sql)

            for sublist in data_array:
                item_id, *months = sublist
                month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 = map(str.strip, months)

                get_item_price_sql = "SELECT item_id, name, unit_type, conv_factor, price FROM sm_item WHERE cid = '"+cid+"' AND item_id = '"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
                get_item_price = db.executesql(get_item_price_sql, as_dict = True)

                for a in range(len(get_item_price)):
                    item_record = get_item_price[a]
                    item_name = item_record['name']
                    UoM = item_record['unit_type']
                    # price = item_record['price']

                # numerical value insert sql    
                insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
                db.executesql(insert_forcasting_header_sql)

            session.post_flash = "Posted Succesfully"
                
        else:
            session.update_flash = "Already submitted once"

        # redirect(URL('forcasting','forcasting_for_sup'))
        redirect(URL('forcasting','forcasting_rm_view'))



#========================== GENERATE FORCASTING CSV FILE FOR RM =======================================#

def forcasting_csv_download_rm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        user_id = session.user_id

        first_date_of_month = session.first_date_of_month

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        months = []

        div_id = ''
        div_name = ''
        get_div_sql = f"SELECT level_id, level_name FROM sm_supervisor_level WHERE cid = '{cid}' AND sup_id = '{user_id}';"
        get_div_data = db.executesql(get_div_sql, as_dict=True)

        for i in range(len(get_div_data)):
            data = get_div_data[i]
            div_id = data['level_id']
            div_name = data['level_name']

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        months.append(current_date.strftime("%b-%Y"))
        i = 1
        for i in range(17):
            current_date += timedelta(days=30)
            if str(current_date) == str(months[i-1]):
                i += 1
                continue
            else:
                months.append(current_date.strftime("%b-%Y"))

        months = str(months).replace('[','').replace(']','').replace("'","")
        myString = f'Division: {div_name} \n'
        myString += f'Planning Month: {planning_month} \n\n\n'
        myString += f'Item_Code,Description,UoM,{months}\n'
        # return myString

        month1_total = 0
        month2_total = 0
        month3_total = 0
        month4_total = 0
        month5_total = 0
        month6_total = 0
        month7_total = 0
        month8_total = 0
        month9_total = 0
        month10_total = 0
        month11_total = 0
        month12_total = 0
        month13_total = 0
        month14_total = 0
        month15_total = 0
        month16_total = 0
        month17_total = 0
        month18_total = 0
        count = 1

        check_forcasting_for_rm_sql = f"SELECT item_code, item_name, UoM, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{user_id}' AND submitted_date in (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' and sup_id = '{user_id}' GROUP by sup_id) AND (status = 'SUBMITTED' OR status = 'POSTED') GROUP BY item_code;"
        check_forcasting_for_rm = db.executesql(check_forcasting_for_rm_sql, as_dict = True)
        
        # for column data
        if len(check_forcasting_for_rm) > 0 :
            for i in range(len(check_forcasting_for_rm)):
                forecast_records_str = check_forcasting_for_rm[i]
                
                if i == 0:
                    i += 1
                    continue

                item_code = str(forecast_records_str['item_code'])
                item_name = str(forecast_records_str['item_name'])
                unit_type = str(forecast_records_str['UoM'])
                month1 = forecast_records_str['month1']
                month2 = forecast_records_str['month2']
                month3 = forecast_records_str['month3']
                month4 = forecast_records_str['month4']
                month5 = forecast_records_str['month5']
                month6 = forecast_records_str['month6']
                month7 = forecast_records_str['month7']
                month8 = forecast_records_str['month8']
                month9 = forecast_records_str['month9']
                month10 = forecast_records_str['month10']
                month11 = forecast_records_str['month11']
                month12 = forecast_records_str['month12']
                month13 = forecast_records_str['month13']
                month14 = forecast_records_str['month14']
                month15 = forecast_records_str['month15']
                month16 = forecast_records_str['month16']
                month17 = forecast_records_str['month17']
                month18 = forecast_records_str['month18']
                
                try:
                    month1_total += float(month1)
                    month2_total += float(month2)
                    month3_total += float(month3)
                    month4_total += float(month4)
                    month5_total += float(month5)
                    month6_total += float(month6)
                    month7_total += float(month7)
                    month8_total += float(month8)
                    month9_total += float(month9)
                    month10_total += float(month10)
                    month11_total += float(month11)
                    month12_total += float(month12)
                    month13_total += float(month13)
                    month14_total += float(month14)
                    month15_total += float(month15)
                    month16_total += float(month16)
                    month17_total += float(month17)
                    month18_total += float(month18)

                except:
                    pass

                i += 1

                myString += str(item_code) + ',' + str(item_name) + ',' + str(unit_type) + ',' + str(float(month1)) + ',' + str(float(month2)) + ',' + str(float(month3)) + ',' + str(float(month4)) + ',' + str(float(month5)) + ',' + str(float(month6)) + ',' + str(float(month7)) + ',' + str(float(month8)) + ',' + str(float(month9)) + ',' + str(float(month10)) + ',' + str(float(month11)) + ',' + str(float(month12)) + ',' + str(float(month13)) + ',' + str(float(month14)) + ',' + str(float(month15)) + ',' + str(float(month16)) + ',' + str(float(month17)) + ',' + str(float(month18))+',\n'
                # return myString

        import gluon.contenttype
        response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
        response.headers['Content-disposition'] = 'attachment; filename='+f'{div_id}'+'_final_forecasting_file.csv'
        return str(myString)