from datetime import datetime, timedelta

# ----------------- FORECASTING DATE RANGE -----------------

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

        current_year_month = datetime.now().strftime("%Y-%m")
        session.current_year_month = current_year_month

        # setting default date to current date
        date_from = str(date_fixed).split(' ')[0]
        date_to = str(date_fixed).split(' ')[0]

        session.from_dt = date_from
        session.to_date = date_to

        submit_btn = request.vars.save_btn

        if submit_btn:
            planning_month = str(request.vars.planning_month).strip()
            date_from = str(request.vars.from_date).strip()
            date_to = str(request.vars.to_date).strip()

            # GETTING FIRST DATE FOR PLANNING MONTH
            p_month_date_obj = datetime.strptime(planning_month, '%b-%Y')
            p_month_first_date = p_month_date_obj.strftime('%Y-%m-%d')

            from_dt = datetime.strptime(date_from, "%Y-%m-%d").date()
            to_dt = datetime.strptime(date_to, "%Y-%m-%d").date()

            if from_dt <= to_dt:
                session.from_dt = date_from
                session.to_date = date_to

                check_date_range_sql = f"SELECT * FROM forecast_date_range WHERE cid = '{cid}' AND ym_date = (SELECT MAX(ym_date) FROM forecast_date_range WHERE cid = '{cid}');"
                check_date_range = db.executesql(check_date_range_sql, as_dict = True)

                ym_date = ''
                if len(check_date_range) < 1:
                    try:
                        Id = str(check_date_range[0]['id'])
                        ym_date = str(check_date_range[0]['ym_date'])

                    except:
                        Id = ''
                        ym_date = ''
                    
                    if ym_date == str(first_date):
                        update_date_range_sql = f"UPDATE forecast_date_range SET planning_month_first_date = '{str(p_month_first_date)}', planning_month = '{str(planning_month)}', opening_date = '{str(date_from)}', opening_datetime = '{str(date_from)+' 00:00:00'}', closing_date = '{str(date_to)}', closing_datetime = '{str(date_to)+' 00:00:00'}', updated_on = '{str(date_fixed)}', updated_by = '{user_id}' WHERE id = '{Id}' AND cid = '{cid}' AND ym_date = '{first_date}';"
                        db.executesql(update_date_range_sql)

                    else:
                        insert_date_range_sql = f"INSERT INTO forecast_date_range (cid, user_id, user_name, planning_month_first_date, planning_month, opening_date, opening_datetime, closing_date, closing_datetime, ym_date, created_on, created_by) VALUES ('{cid}','{user_id}','{user_name}','{str(p_month_first_date)}','{planning_month}','{str(date_from)}','{str(date_from)+' 00:00:00'}','{str(date_to)}','{str(date_to)+' 00:00:00'}','{str(first_date)}','{str(date_fixed)}','{user_id}');"
                        db.executesql(insert_date_range_sql)

                    session.save_flash = 'Saved Successfully'
            
            else:
                session.error_flash = 'Invalid Date Range'
                redirect(URL(c='forcasting_admin', f='set_forecasting_window'))
        
        get_date_range_sql = f"SELECT * FROM forecast_date_range WHERE cid = '{cid}' AND ym_date = (SELECT MAX(ym_date) FROM forecast_date_range WHERE cid = '{cid}');"
        get_date_range = db.executesql(get_date_range_sql, as_dict = True)
        
        return dict(date_records = get_date_range, current_year_month = current_year_month)



def edit_date_range():
    cid = session.cid
    user_id = session.user_id
    # user_name = session.name

    current_month = str(date_fixed).split(' ')[0]
    first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
    year = first_date_str.year
    month = first_date_str.month
    first_date = str(datetime(year, month, 1)).split(' ')[0]
    current_date_obj = datetime.strptime(first_date, '%Y-%m-%d')

    planning_month = str(request.vars.pl_month).strip()
    # return planning_month

    date_from = str(request.vars.op_date).strip()
    date_to = str(request.vars.cl_date).strip()

    from_dt = datetime.strptime(date_from, "%Y-%m-%d").date()
    to_dt = datetime.strptime(date_to, "%Y-%m-%d").date()

    # p_month_date_obj = datetime.strptime(planning_month, '%b-%Y')
    p_month_date_obj = datetime.strptime(planning_month, '%Y-%m')
    # return p_month_date_obj
    p_month_first_date = p_month_date_obj.strftime('%Y-%m-%d')
    # return p_month_first_date

    if (from_dt <= to_dt) and (p_month_date_obj >= current_date_obj):
        update_date_range_sql = f"UPDATE forecast_date_range SET planning_month_first_date = '{str(p_month_first_date)}', planning_month = '{str(planning_month)}', opening_date = '{str(date_from)}', opening_datetime = '{str(date_from)+' 00:00:00'}', closing_date = '{str(date_to)}', closing_datetime = '{str(date_to)+' 00:00:00'}', updated_on = '{str(date_fixed)}', updated_by = '{user_id}' WHERE cid = '{cid}' AND ym_date = '{first_date}';"
        db.executesql(update_date_range_sql)

        session.update_flash = 'Updated Successfully'

    else:
        session.error_flash = 'Invalid Date Range'
    
    redirect(URL(c='forcasting_admin', f='set_forecasting_window'))



# ----------------- APPROVE RM FORECASTING -----------------

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

                all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}') GROUP BY sup_id, first_date, item_code;"
                forecast_rec = db.executesql(all_forecast_sql, as_dict=True)

                if len(forecast_rec) != 0:
                    check_forcasting_status = f"SELECT status FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}') GROUP BY status;"
                    forecast_status = db.executesql(check_forcasting_status, as_dict=True)
                    
                    frcst_status = ''
                    if len(forecast_status) != 0:
                        for f in range(len(forecast_status)):
                            forecast = forecast_status[f]
                            frcst_status = str(forecast['status']).upper().strip()
                    
                    length += 1
                
                    return dict(months = months, forecast_records = forecast_rec, length = length, status = frcst_status, rm_id = rm_id)

            # elif rm_view_btn == 'Edit':
            #     rm_id = request.args[0]

            #     # GET SUBMITTED DATE
            #     submitted_date = str(date_fixed)
            #     submitted_date_str = str(date_fixed).split(' ')[0]
            #     submitted_first_date = datetime.strptime(submitted_date_str, "%Y-%m-%d")
            #     year = submitted_first_date.year
            #     month = submitted_first_date.month
            #     submitted_first_date = str(datetime(year, month, 1)).split(' ')[0]
            #     current_month = str(date_fixed).split(' ')[0]

            #     get_level_id_sql = "SELECT sup_name, level_id, level_depth_no FROM sm_supervisor_level WHERE cid = '"+cid+"' AND sup_id = '"+str(rm_id)+"' LIMIT 1;"
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
            #     if month1 == 'Jan-24' or month1 == 'Jan-2024' or month1 == '24-Jan' or month1 == '2024-Jan':
            #         forecasting_first_date="2024-01-01"
            #     elif month1 == 'Feb-24' or month1 == 'Feb-2024' or month1 == '24-Feb' or month1 == '2024-Feb':
            #         forecasting_first_date="2024-02-01"
            #     elif month1 == 'Mar-24' or month1 == 'Mar-2024' or month1 == '24-Mar' or month1 == '2024-Mar':
            #         forecasting_first_date="2024-03-01"
            #     elif month1 == 'Apr-24' or month1 == 'Apr-2024' or month1 == '24-Apr' or month1 == '2024-Apr':
            #         forecasting_first_date="2024-04-01"
            #     elif month1 == 'May-24' or month1 == 'May-2024' or month1 == '24-May' or month1 == '2024-May':
            #         forecasting_first_date="2024-05-01"
            #     elif month1 == 'Jun-24' or month1 == 'Jun-2024' or month1 == '24-Jun' or month1 == '2024-Jun':
            #         forecasting_first_date="2024-06-01"
            #     elif month1 == 'Jul-24' or month1 == 'Jul-2024' or month1 == '24-Jul' or month1 == '2024-Jul':
            #         forecasting_first_date="2024-07-01"
            #     elif month1 == 'Aug-24' or month1 == 'Aug-2024' or month1 == '24-Aug' or month1 == '2024-Aug':
            #         forecasting_first_date="2024-08-01"
            #     elif month1 == 'Sep-24' or month1 == 'Sep-2024' or month1 == '24-Sep' or month1 == '2024-Sep':
            #         forecasting_first_date="2024-09-01"
            #     elif month1 == 'Oct-24' or month1 == 'Oct-2024' or month1 == '24-Oct' or month1 == '2024-Oct':
            #         forecasting_first_date="2024-10-01"
            #     elif month1 == 'Nov-24' or month1 == 'Nov-2024' or month1 == '24-Nov' or month1 == '2024-Nov':
            #         forecasting_first_date="2024-11-01"
            #     elif month1 == 'Dec-24' or month1 == 'Dec-2024' or month1 == '24-Dec' or month1 == '2024-Dec':
            #         forecasting_first_date="2024-12-01"
                
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
                
            #     check_forecasting_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rm_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'POSTED';"
            #     check_forecasting = db.executesql(check_forecasting_sql, as_dict=True)

            #     # remove previous forecasting
            #     if len(check_forecasting) > 0:
            #         delete_forecasting_sql = f"DELETE FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'POSTED';"
            #         db.executesql(delete_forecasting_sql)
                
            #     # month name insert sql 
            #     insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES ('"+str(cid)+"','"+str(rm_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','','','','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"')"
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
            #         insert_forcasting_header_sql = "INSERT INTO forecast_rm_temp (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status) VALUES('"+str(cid)+"','"+str(rm_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(level1)+"','"+str(level1_name)+"','"+str(level0)+"','"+str(level0_name)+"','"+str(level2)+"','"+str(level2_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(level3)+"','"+str(level3_name)+"','"+str(item_id)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(float(month1))+"','"+str(float(month2))+"','"+str(float(month3))+"','"+str(float(month4))+"','"+str(float(month5))+"','"+str(float(month6))+"','"+str(float(month7))+"','"+str(float(month8))+"','"+str(float(month9))+"','"+str(float(month10))+"','"+str(float(month11))+"','"+str(float(month12))+"','"+str(float(month13))+"','"+str(float(month14))+"','"+str(float(month15))+"','"+str(float(month16))+"','"+str(float(month17))+"','"+str(float(month18))+"','"+str(status)+"')"
            #         db.executesql(insert_forcasting_header_sql)
            
            # redirect(URL('forcasting_admin','forcasting_for_admin'))



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
            # approve data in temp table
            update_forcasting_status_sql = "UPDATE forecast_rm_temp SET status = 'APPROVED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND sup_id = '"+str(rm_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"';"
            # return update_forcasting_status_sql
            update_forcasting_status = db.executesql(update_forcasting_status_sql)
            
            # move approved data from temp table to main table
            all_forecast_sql = f"SELECT * FROM forecast_rm_temp WHERE cid='{cid}' AND sup_id = '{rm_id}' AND submitted_date = (SELECT MAX(submitted_date) FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}') AND status = 'APPROVED' GROUP BY sup_id, first_date, item_code;"
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
                    insert_forcasting_header_sql = "INSERT INTO forecast_rm (cid, sup_id, sup_name, first_date, submitted_date, forcasting_first_date, division, country, zone_id, zone_name, region_id, region_name, area_id, area_name, territory_id, territory_name, sale_unit_id, sale_unit_name, item_code, item_name, Uom, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18, status, approve_by_id, approve_by_name) VALUES('"+str(cid)+"','"+str(rm_id)+"','"+str(am_name)+"','"+str(submitted_first_date)+"','"+str(submitted_date)+"','"+str(forecasting_first_date)+"','"+str(division)+"','"+str(country)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(region_id)+"','"+str(region_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(sale_unit_id)+"','"+str(sale_unit_name)+"','"+str(item_code)+"','"+str(item_name)+"','"+str(UoM)+"','"+str(month1)+"','"+str(month2)+"','"+str(month3)+"','"+str(month4)+"','"+str(month5)+"','"+str(month6)+"','"+str(month7)+"','"+str(month8)+"','"+str(month9)+"','"+str(month10)+"','"+str(month11)+"','"+str(month12)+"','"+str(month13)+"','"+str(month14)+"','"+str(month15)+"','"+str(month16)+"','"+str(month17)+"','"+str(month18)+"','"+str(status)+"','"+str(approve_by_id)+"','"+str(approve_by_name)+"')"
                    db.executesql(insert_forcasting_header_sql)
                
                delete_forecasting_sql = f"DELETE FROM forecast_rm_temp WHERE cid = '{cid}' AND sup_id = '{rm_id}' AND forcasting_first_date = '{forecasting_first_date}' AND status = 'APPROVED';"
                db.executesql(delete_forecasting_sql)

            response.flash = "APPROVED Successfully"



        elif reject_btn == "Reject":
            update_forcasting_status_sql = "UPDATE forecast_rm_temp SET status = 'REJECTED', approve_by_id = '"+str(sup_id)+"', approve_by_name = '"+str(sup_name)+"' WHERE cid = '"+cid+"' AND sup_id = '"+str(rm_id)+"' AND status = 'POSTED' AND first_date = '"+str(first_date_of_month)+"' ;"
            update_forcasting_status = db.executesql(update_forcasting_status_sql)

            response.flash = "REJECTED Successfully"

        redirect(URL('forcasting_admin','forcasting_for_admin'))



def forcasting_csv_download_rm():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        # user_id = session.user_id
        # user_id = 'ACCA000314'
        user_id = session.rm_id

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



def forcasting_csv_download_rm_prev():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        cid = session.cid
        user_id = session.rm_id

        # first_date_of_month = session.first_date_of_month
        selected_month = str(request.vars.select_month).strip()
        sl_month_date_obj = datetime.strptime(selected_month, '%Y-%m')
        sl_month_first_date = sl_month_date_obj.strftime('%Y-%m-%d')
        sl_month_STR = str(sl_month_date_obj.strftime('%b-%y')).replace('-','_')
        # return sl_month_STR

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        current_date = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        planning_month = str(datetime(year, month, 1)).split(' ')[0]
        # months = []

        # div_id = ''
        div_name = ''
        get_div_sql = f"SELECT level_id, level_name FROM sm_supervisor_level WHERE cid = '{cid}' AND sup_id = '{user_id}';"
        get_div_data = db.executesql(get_div_sql, as_dict=True)

        for i in range(len(get_div_data)):
            data = get_div_data[i]
            # div_id = data['level_id']
            div_name = data['level_name']

        # for i in range(18):
        #     months.append(current_date.strftime("%b-%Y"))
        #     current_date += timedelta(days=31)

        # months.append(current_date.strftime("%b-%Y"))
        # i = 1
        # for i in range(17):
        #     current_date += timedelta(days=30)
        #     if str(current_date) == str(months[i-1]):
        #         i += 1
        #         continue
        #     else:
        #         months.append(current_date.strftime("%b-%Y"))

        # months = str(months).replace('[','').replace(']','').replace("'","")
        myString = f'Division: {div_name} \n'
        myString += f'Planning Month: {sl_month_first_date} \n\n\n'
        # myString += f'Item_Code,Description,UoM,{months}\n'
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

        check_forcasting_for_rm_sql = f"SELECT item_code, item_name, UoM, month1, month2, month3, month4, month5, month6, month7, month8, month9, month10, month11, month12, month13, month14, month15, month16, month17, month18 FROM forecast_rm WHERE cid = '{cid}' AND sup_id = '{user_id}' AND forcasting_first_date = '{str(sl_month_first_date)}' AND status = 'APPROVED' GROUP BY item_code;"
        # return check_forcasting_for_rm_sql
        check_forcasting_for_rm = db.executesql(check_forcasting_for_rm_sql, as_dict = True)
        # return len(check_forcasting_for_rm)
        
        # for column data
        if len(check_forcasting_for_rm) > 0 :
            for i in range(len(check_forcasting_for_rm)):
                forecast_records_str = check_forcasting_for_rm[i]
                
                if i == 0:
                    # return response.json(check_forcasting_for_rm[i])
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
                    # return month1

                    myString += f'Item_Code,Description,UoM,{month1},{month2},{month3},{month4},{month5},{month6},{month7},{month8},{month9},{month10},{month11},{month12},{month13},{month14},{month15},{month16},{month17},{month18}\n'
                    
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
            response.headers['Content-disposition'] = 'attachment; filename='+f'{sl_month_STR}'+'_forecasting_file.csv'
            return str(myString)
    
        else:
            session.download_error_flash = 'No Forecast Available for This Month'
            redirect(URL(c='forcasting_admin', f='forcasting_for_admin'))




# ----------------- BLOCK ITEM ENTRY -----------------

def item_entry_block():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Block Item'

        cid = session.cid
        user_id = session.user_id
        user_name = session.name
        # return user_name

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
            try:
                item_id = str(request.vars.item_id_name).split('|')[0].strip()
                item_name = str(request.vars.item_id_name).split('|')[1].strip()
            except:
                item_id = ''
                item_name = ''
            
            date_from = str(request.vars.from_date).strip()
            date_to = str(request.vars.to_date).strip()
            # status = str(request.vars.status).strip()

            # from_dt = datetime.strptime(date_from, "%Y-%m-%d").date()
            # to_dt = datetime.strptime(date_to, "%Y-%m-%d").date()
            from_dt = datetime.strptime(date_from, "%b-%Y").date()
            to_dt = datetime.strptime(date_to, "%b-%Y").date()

            # start_dt = datetime.strptime(date_from, "%Y-%m-%d")
            # end_dt = datetime.strptime(date_to, "%Y-%m-%d")
            start_dt = datetime.strptime(date_from, "%b-%Y")
            end_dt = datetime.strptime(date_to, "%b-%Y")

            month_year_range = []
            month_year_str = ''
            
            current = start_dt
            while current <= end_dt:
                month_year_range.append(current.strftime('%b-%Y'))
                
                if current.month == 12:
                    current = datetime(current.year + 1, 1, 1)
                else:
                    current = datetime(current.year, current.month + 1, 1)
                pass
            
            month_year_str = ', '.join(month_year_range)

            if from_dt <= to_dt:
                check_item_date_sql = f"SELECT * FROM block_item WHERE cid = '{cid}' AND item_id = '{item_id}';"
                check_item_date = db.executesql(check_item_date_sql, as_dict = True)

                if len(check_item_date) == 0:
                    insert_item_date_sql = f"INSERT INTO block_item (cid, item_id, item_name, start_date, start_datetime, end_date, end_datetime, blocked_months, status, ym_date, created_on, created_by) VALUES ('{cid}','{item_id}','{item_name}','{str(from_dt)}','{str(from_dt)+' 00:00:00'}','{str(to_dt)}','{str(to_dt)+' 00:00:00'}','{month_year_str}','ACTIVE','{str(first_date)}','{str(date_fixed)}','{user_id}');"
                    db.executesql(insert_item_date_sql)

                    session.save_flash = 'Saved Successfully'
                
                else:
                    session.error_flash = 'Item Already Blocked'
            
            else:
                session.error_flash = 'Invalid Date Range'
                redirect(URL(c='forcasting_admin', f='set_forecasting_window'))
        
        get_item_date_sql = f"SELECT * FROM block_item WHERE cid = '{cid}' ORDER BY item_id;"
        get_item_date = db.executesql(get_item_date_sql, as_dict = True)
        
        return dict(data_records = get_item_date)



def delete_data():
    cid = session.cid

    try:
        item_id = str(request.args[0]).replace('None','')
        start_date = str(request.args[1]).replace('None','')
        end_date = str(request.args[2]).replace('None','')

    except:
        item_id = ''
        start_date = ''
        end_date = ''

    if item_id != '' and start_date != '' and end_date != '':
        delete_sql = f"DELETE FROM block_item WHERE cid = '{cid}' AND item_id = '{item_id}' AND start_date = '{start_date}' AND end_date = '{end_date}';"
        db.executesql(delete_sql)

    session.update_flash = 'Deleted Successfully'

    redirect(URL(c='forcasting_admin', f='item_entry_block'))



def get_item_list():
    cid = session.cid
    retStr = ''

    itemRows_sql = f"SELECT item_id, name FROM sm_item WHERE cid = '{cid}' GROUP BY item_id ORDER BY id;"
    itemRows = db.executesql(itemRows_sql, as_dict=True)

    for i in range(len(itemRows)):
        records_ov_dict = itemRows[i] 
        item_id = str(records_ov_dict['item_id'])
        item_name = str(records_ov_dict['name'])
            
        if retStr == '':
            retStr = item_id+' | '+item_name
        else:
            retStr += ',' + item_id+' | '+item_name
    
    return retStr