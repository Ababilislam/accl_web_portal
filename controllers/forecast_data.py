from datetime import datetime, timedelta

def reset_data():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))

    else:
        response.title = 'Reset Data'

        cid = session.cid
        session.delete_flash = ''

        current_month = str(date_fixed).split(' ')[0]
        first_date_str = datetime.strptime(current_month, "%Y-%m-%d")
        year = first_date_str.year
        month = first_date_str.month
        first_date = str(datetime(year, month, 1)).split(' ')[0]

        # session.current_month_date = first_date

        reset_btn = str(request.vars.reset_btn)

        if reset_btn == 'Reset':   
            delete_mpo_forecasting_sql = f"DELETE FROM forecast_mpo WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_mpo_forecasting_sql)

            delete_mpo_temp_forecasting_sql = f"DELETE FROM forecast_mpo_temp WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_mpo_temp_forecasting_sql)

            delete_am_forecasting_sql = f"DELETE FROM forecast_am WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_am_forecasting_sql)

            delete_am_temp_forecasting_sql = f"DELETE FROM forecast_am_temp WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_am_temp_forecasting_sql)

            delete_zm_forecasting_sql = f"DELETE FROM forecast_zm WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_zm_forecasting_sql)

            delete_zm_temp_forecasting_sql = f"DELETE FROM forecast_zm_temp WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_zm_temp_forecasting_sql)

            delete_rm_forecasting_sql = f"DELETE FROM forecast_rm WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_rm_forecasting_sql)

            delete_rm_temp_forecasting_sql = f"DELETE FROM forecast_rm_temp WHERE cid = '{cid}' AND first_date = '{first_date}';"
            db.executesql(delete_rm_temp_forecasting_sql)

            response.delete_flash = 'Deleted Successfully'

        return dict()