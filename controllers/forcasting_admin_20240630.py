from datetime import datetime, timedelta

def set_forecasting_window():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Set Forecast Window'

        cid = session.cid
        user_id = session.user_id
        user_name = session.name

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        first_date = str(datetime(year, month, 1)).split(' ')[0]

        # setting default date to current date
        date_from = str(date_fixed).split(' ')[0]
        date_to = str(date_fixed).split(' ')[0]

        session.from_dt = date_from
        session.to_date = date_to

        submit_btn = request.vars.save_btn

        if submit_btn:
            date_from = str(request.vars.from_dt).strip()
            date_to = str(request.vars.to_date).strip()

            from_dt = datetime.strptime(date_from, "%Y-%m-%d").date()
            to_dt = datetime.strptime(date_to, "%Y-%m-%d").date()

            if from_dt <= to_dt:
                session.from_dt = date_from
                session.to_date = date_to

                check_date_range_sql = f"SELECT * FROM forecast_date_range WHERE cid = '{cid}' AND ym_date = (SELECT MAX(ym_date) FROM forecast_date_range WHERE cid = '{cid}');"
                check_date_range = db.executesql(check_date_range_sql, as_dict = True)

                ym_date = ''
                if len(check_date_range) != 0:
                    id = str(check_date_range[0]['id'])
                    ym_date = str(check_date_range[0]['ym_date'])
                    
                    if ym_date == str(first_date):
                        update_date_range_sql = f"UPDATE forecast_date_range SET opening_date = '{str(date_from)}', opening_datetime = '{str(date_from)+' 00:00:00'}', closing_date = '{str(date_to)}', closing_datetime = '{str(date_to)+' 00:00:00'}', updated_on = '{str(date_fixed)}', updated_by = '{user_id}' WHERE id = '{id}' AND cid = '{cid}' AND ym_date = '{first_date}';"
                        db.executesql(update_date_range_sql)
 
                    else:
                        insert_date_range_sql = f"INSERT INTO forecast_date_range (cid, user_id, user_name, opening_date, opening_datetime, closing_date, closing_datetime, ym_date, created_on, created_by) VALUES ('{cid}','{user_id}','{user_name}','{str(date_from)}','{str(date_from)+' 00:00:00'}','{str(date_to)}','{str(date_to)+' 00:00:00'}','{str(first_date)}','{str(date_fixed)}','{user_id}');"
                        db.executesql(insert_date_range_sql)

                    session.flash = 'Saved Successfully'
            
            else:
                redirect(URL(c='forcasting_admin', f='set_forecasting_window'))
        
        get_date_range_sql = f"SELECT * FROM forecast_date_range WHERE cid = '{cid}' AND ym_date = (SELECT MAX(ym_date) FROM forecast_date_range WHERE cid = '{cid}');"
        get_date_range = db.executesql(get_date_range_sql, as_dict = True)
        
        return dict(date_records = get_date_range)


def forcasting_for_admin():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecasting'

        cid = session.cid
        user_id = session.user_id

        current_date = str(date_fixed).split(' ')[0]
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
        year = current_date.year
        month = current_date.month
        first_date_of_month = str(datetime(year, month, 1)).split(' ')[0]
        session.first_date_of_month = first_date_of_month

        level_id= ''
        # depth = 0
        # territory_list = []
        level_list = []
        # get_sup_list = ''

        check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND is_leaf = '0' AND depth = '0' GROUP BY level0;"
        check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

        if len(check_territory_level):
            for s in range(len(check_territory_level)):
                level0_records = check_territory_level[s]
                level_id = level0_records['level_id']
                level_name = level0_records['level_name']
                level_list.append(level_id)
    
        level_list = str(level_list).replace('[','').replace(']','')            
        get_sup_list_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND level_id IN ("+str(level_list)+") GROUP BY sup_id;"
        get_sup_list = db.executesql(get_sup_list_sql, as_dict = True)

        return dict(get_sup_list = get_sup_list, first_date_of_month = first_date_of_month)
    

#========================== INDIVIDUAL FORCASTING VIEW FOR AM ==========================#

def forcasting_view_rm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Forecast Data'
        
        cid = session.cid
        user_id = session.user_id
        user_type = session.user_type
        
        # btns
        rm_view_btn = request.vars.rm_view

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
        
        if user_type == 'admin':
            length = 0

            if rm_view_btn:
                rm_id = request.args[0]

                all_forecast_sql = f"SELECT * FROM forecast_rm WHERE cid='{cid}' AND sup_id = '{rm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm WHERE cid = '{cid}' AND sup_id = '{rm_id}') GROUP BY sup_id, first_date, item_code;"
                forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

                if len(forecast_rec) != 0:
                    check_forcasting_status = f"SELECT status FROM forecast_rm WHERE cid='{cid}' AND sup_id = '{rm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm WHERE cid = '{cid}' AND sup_id = '{rm_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()
                    
                    length += 1
                
                    return dict(months = months, forecast_records = forecast_rec, length = length, status = frcst_status, rm_id = rm_id)

            redirect(URL('forcasting_admin','forcasting_for_admin'))



#========================== FORCASTING APPROVED REJECT FOR AM =======================================#

def forcasting_rm_approve_reject():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        sup_id = session.user_id
        sup_name = session.name
        first_date_of_month = session.first_date_of_month

        rm_id = request.args(0)

        approve_btn = request.vars.approve
        reject_btn = request.vars.reject

        if approve_btn == "Approve":     
            # approve data in main table
            update_forcasting_status_sql = "UPDATE forecast_rm SET status = 'APPROVED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND sup_id = '"+str(rm_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"';"
            # return update_forcasting_status_sql
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            
            # move approved data from temp table to main table
            # all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}') AND status = 'APPROVED' GROUP BY sup_id, first_date, item_code;"
            # forecast_rec = db.executesql(all_forecast_sql, as_dict=True)
            
            # if len(forecast_rec) != 0:
            #     for r in range(len(forecast_rec)):
            #         records = forecast_rec[r]
            #         am_name = str(records['sup_name'])
            #         submitted_first_date = str(records['first_date'])
            #         submitted_date = str(records['submitted_date'])
            #         forecasting_first_date = str(records['forcasting_first_date'])
            #         division  = str(records['division'])
            #         country = str(records['country'])
            #         zone_id = str(records['zone_id'])
            #         zone_name = str(records['zone_name'])
            #         region_id = str(records['region_id'])
            #         region_name = str(records['region_name'])
            #         area_id = str(records['area_id'])
            #         area_name = str(records['area_name'])
            #         territory_id = str(records['territory_id'])
            #         territory_name = str(records['territory_name'])
            #         sale_unit_id = str(records['sale_unit_id'])
            #         sale_unit_name = str(records['sale_unit_name'])
            #         item_code = str(records['item_code'])
            #         item_name = str(records['item_name'])
            #         UoM  = str(records['UoM'])
            #         month1 = str(records['month1'])
            #         month2 = str(records['month2'])
            #         month3 = str(records['month3'])
            #         month4 = str(records['month4'])
            #         month5 = str(records['month5'])
            #         month6 = str(records['month6'])
            #         month7 = str(records['month7'])
            #         month8 = str(records['month8'])
            #         month9 = str(records['month9'])
            #         month10 = str(records['month10'])
            #         month11 = str(records['month11'])
            #         month12 = str(records['month12'])
            #         month13 = str(records['month13'])
            #         month14 = str(records['month14'])
            #         month15 = str(records['month15'])
            #         month16 = str(records['month16'])
            #         month17 = str(records['month17'])
            #         month18 = str(records['month18'])
            #         status  = str(records['status'])
            #         approve_by_id = str(records['approve_by_id'])
            #         approve_by_name = str(records['approve_by_name'])
                    
            #         # copy-paste data from one table to another
            #         insert_forcasting_header_sql = "INSERT INTO forecast_rm (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, division, country, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status, approve_by_id, approve_by_name) VALUES('"+str(cid)+"','"+str(rm_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(division)+"','"+str(country)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(region_id)+"','"+str(region_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(sale_unit_id)+"','"+str(sale_unit_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"','"+str(approve_by_id)+"','"+str(approve_by_name)+"')"
            #         db.executesql(insert_forcasting_header_sql)
                
            #     delete_forecasting_sql = f"DELETE FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'APPROVED';"
            #     db.executesql(delete_forecasting_sql)

            response.flash = "APPROVED Successfully"

        elif reject_btn == "Reject":
            update_forcasting_status_sql = "UPDATE forecast_rm SET status = 'REJECTED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND am_id = '"+str(am_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"' ;"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            response.flash = "REJECTED Successfully"

        redirect(URL('forcasting_admin','forcasting_for_admin'))





#========================== GENERATE FORCASTING CSV FILE FOR RM =======================================#

def forcasting_csv_download_rm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        # user_id = session.user_id
        user_id = 'ACCA000314'

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

        check_forcasting_for_rm_sql = f"SELECT item_code, item_name, UoM, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 FROM forecast_rm WHERE cid = '{cid}' AND sup_id = '{user_id}' AND submitted_date in (SELECT MAX(submitted_date) FROM forecast_rm WHERE cid = '{cid}' and sup_id = '{user_id}' GROUP by sup_id) AND status = 'APPROVED' GROUP BY item_code;"
        # return check_forcasting_for_rm_sql
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
        response.headers['Content-disposition'] = 'attachment; filename=final_forecasting_file.csv'
        return str(myString)



#========================== FORCASTING HOME PAGE FOR SUP =======================================#

# def forcasting_for_sup():
#     if session.cid == '' or session.cid == 'None' or session.cid == None:
#         redirect(URL(c='default', f='index'))

#     else:
#         response.title = 'Forecasting'

#         cid = session.cid
#         user_id = session.user_id
#         # user_type = session.user_type

#         current_date = str(date_fixed).split(' ')[0]
#         current_date = datetime.strptime(current_date, "%Y-%m-%d")
#         year = current_date.year
#         month = current_date.month
#         first_date_of_month = str(datetime(year, month, 1)).split(' ')[0]
#         session.first_date_of_month = first_date_of_month

#         level_id= ''
#         depth = 0
#         territory_list = []
#         level_list = []
#         get_rep_list = ''

#         check_supervisor_level_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(user_id)+"' GROUP BY sup_id LIMIT 1 ;"
#         check_supervisor_level = db.executesql(check_supervisor_level_sql, as_dict = True)

#         if len(check_supervisor_level):
#             for s in range(len(check_supervisor_level)):
#                 level_records = check_supervisor_level[s]
#                 level_id = level_records['level_id']
#                 depth = level_records['level_depth_no']

#             session.level_id = level_id
#             session.level_depth = depth

#             if depth == 2:
#                 check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND level2 = '"+str(level_id)+"' AND is_leaf = '1' GROUP BY level0, level1, level2, level3;"
#                 check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

#                 if len(check_territory_level):
#                     for s in range(len(check_territory_level)):
#                         level2_records = check_territory_level[s]
#                         level_id = level2_records['level3']
#                         level_name = level2_records['level3_name']
#                         territory_list.append(level_id)

#                 territory_list = str(territory_list).replace('[','').replace(']','')            
#                 get_rep_list_sql = "SELECT * FROM sm_rep_area WHERE cid = '"+cid+"' AND area_id IN ("+str(territory_list)+") GROUP BY rep_id;"
#                 get_rep_list = db.executesql(get_rep_list_sql, as_dict = True)
            
#                 return dict(get_rep_list = get_rep_list, first_date_of_month = first_date_of_month)
            
#             elif depth == 1:
#                 check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND parent_level_id = '"+str(level_id)+"' AND level1 = '"+str(level_id)+"' AND is_leaf = '0' GROUP BY level0, level1, level2, level3;"
#                 check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

#                 if len(check_territory_level):
#                     for s in range(len(check_territory_level)):
#                         level1_records = check_territory_level[s]
#                         level_id = level1_records['level2']
#                         level_name = level1_records['level2_name']
#                         level_list.append(level_id)

#                 level_list = str(level_list).replace('[','').replace(']','')            
#                 get_sup_list_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND level_id IN ("+str(level_list)+") GROUP BY sup_id;"
#                 get_sup_list = db.executesql(get_sup_list_sql, as_dict = True)

#                 return dict(get_sup_list = get_sup_list, first_date_of_month = first_date_of_month)

#             elif depth == 0:
#                 check_territory_level_sql = "SELECT * FROM sm_level WHERE cid = '"+cid+"' AND parent_level_id = '"+str(level_id)+"' AND level0 = '"+str(level_id)+"' AND is_leaf = '0' GROUP BY level0, level1, level2, level3;"
#                 check_territory_level = db.executesql(check_territory_level_sql, as_dict = True)

#                 if len(check_territory_level):
#                     for s in range(len(check_territory_level)):
#                         level0_records = check_territory_level[s]
#                         level_id = level0_records['level1']
#                         level_name = level0_records['level1_name']
#                         level_list.append(level_id)
            
#                 level_list = str(level_list).replace('[','').replace(']','')            
#                 get_sup_list_sql = "SELECT * FROM sm_supervisor_level WHERE cid = '"+cid+"' AND level_id IN ("+str(level_list)+") GROUP BY sup_id;"
#                 get_sup_list = db.executesql(get_sup_list_sql, as_dict = True)

#                 return dict(get_sup_list = get_sup_list, first_date_of_month = first_date_of_month)

