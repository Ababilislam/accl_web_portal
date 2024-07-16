def notice():
    if session.cid == '' or session.cid == 'None' or session.cid == None:
        redirect(URL(c='default', f='index'))
        

    else:
        response.title = 'Notify Users'
        cid = session.cid
        user_id = session.user_id
        # session.flash_msg=""
        # session.flash_msg_w =""
        
        get_notice_sql = f"SELECT * FROM sm_notice WHERE cid='{cid}';"
        notice_rec = db.executesql(get_notice_sql, as_dict=True)

        return dict(data_records = notice_rec)


def submit_notice():
    cid = session.cid
    user_id = session.user_id
    session.flash_msg=""
    session.flash_msg_w =""
    data = str(request.vars.notice_data).replace('None','')
    # return data
    if data =="" or data =="None" or data ==None:
        session.flash_msg_w = 'No notice data received!'
    else:
        insert_notice_sql = f"INSERT INTO sm_notice (cid, notice_date, notice, created_on, created_by) VALUES ('{cid}','{str(date_fixed)}','{str(data)}','{date_fixed}','{user_id}');"
        db.executesql(insert_notice_sql)
        session.flash_msg = 'Notice saved successfully!'

    # if data!="" or data!="None" or data!=None:
    #     insert_notice_sql = f"INSERT INTO sm_notice (cid, notice_date, notice, created_on, created_by) VALUES ('{cid}','{str(date_fixed)}','{str(data)}','{date_fixed}','{user_id}');"
    #     db.executesql(insert_notice_sql)
    #     session.flash_msg = 'Notice saved successfully!'
    # elif data=="" or data==None:
    #     session.flash_msg_w = 'No notice data received!'

    redirect(URL(c='notice',f='notice'))


def delete_notice():
    cid = session.cid
    if cid == '' or cid == 'None' or cid == None:
        redirect(URL(c='default', f='index'))
    # ntc = request.args[0]
    # return ntc
    session.flash_msg=""
    notice_id = request.vars.id
    # return notice_id
    delete_notice_sql = f"DELETE FROM sm_notice WHERE cid='{cid}' and id='{notice_id}';"
    # return delete_notice_sql
    db.executesql(delete_notice_sql)
    session.flash_msg="Deleted successfully!"
    return redirect("notice")