def rep():
    response.title = 'Representative'
    cid = session.cid
    
    add_btn = request.vars.add_btn

    rep_id = request.vars.rep_id_input
    rep_name = request.vars.rep_name_input
    rep_user_type = request.vars.rep_type_input
    rep_mobile = request.vars.rep_mobile_input
    rep_pass = request.vars.rep_password_input
    rep_status = request.vars.status

    page = request.vars.page_no

    if page == '' or page == 'None' or page == None:
        page = 1

    page_limit = 20
    page_no = int(page)
    start_index = (page_no - 1) * page_limit

    if add_btn:
        if rep_id == '':
            response.flash = 'Enter representative ID'
        elif rep_name == '':
            response.flash = 'Enter representative name'
        elif rep_user_type == '':
            response.flash = 'Enter representative type'
        elif rep_mobile == '':
            response.flash = 'Enter representative mobile number'
        elif rep_pass == '':
            response.flash = 'Enter representative password'
        else:
            check_rep_sql = f"SELECT * FROM sm_rep WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND password = '{rep_pass}' LIMIT 1;"
            check_rep = db.executesql(check_rep_sql, as_dict=True)

            if len(check_rep) == 0:
                insert_rep_sql = f"INSERT INTO sm_rep (cid, rep_id, name, mobile_no, password, status, user_type) VALUES ('{cid}','{rep_id.upper()}','{rep_name}','{rep_mobile}','{rep_pass}','{rep_status.upper()}','{rep_user_type}');"
                db.executesql(insert_rep_sql)

    get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' ORDER BY id ASC LIMIT {start_index}, {page_limit};"
    rep_records = db.executesql(get_rep_list_sql, as_dict = True)

    return dict(rep_records = rep_records, page = page)


def rep_edit():
    return locals()


def rep_area():
    response.title = 'Representative Area'
    cid = session.cid
    
    add_btn = request.vars.add_btn

    rep_id = request.vars.rep_id_input
    rep_name = request.vars.rep_name_input
    rep_user_type = request.vars.rep_type_input
    rep_mobile = request.vars.rep_mobile_input
    rep_pass = request.vars.rep_password_input
    rep_status = request.vars.status

    page = request.vars.page_no

    if page == '' or page == 'None' or page == None:
        page = 1

    page_limit = 20
    page_no = int(page)
    start_index = (page_no - 1) * page_limit

    if add_btn:
        if rep_id == '':
            response.flash = 'Enter representative ID'
        elif rep_name == '':
            response.flash = 'Enter representative name'
        elif rep_user_type == '':
            response.flash = 'Enter representative type'
        elif rep_mobile == '':
            response.flash = 'Enter representative mobile number'
        elif rep_pass == '':
            response.flash = 'Enter representative password'
        else:
            check_rep_sql = f"SELECT * FROM sm_rep WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND password = '{rep_pass}' LIMIT 1;"
            check_rep = db.executesql(check_rep_sql, as_dict=True)

            if len(check_rep) == 0:
                insert_rep_sql = f"INSERT INTO sm_rep (cid, rep_id, name, mobile_no, password, status, user_type) VALUES ('{cid}','{rep_id.upper()}','{rep_name}','{rep_mobile}','{rep_pass}','{rep_status.upper()}','{rep_user_type}');"
                db.executesql(insert_rep_sql)

    get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' ORDER BY id ASC LIMIT {start_index}, {page_limit};"
    rep_records = db.executesql(get_rep_list_sql, as_dict = True)
    
    return dict(rep_records = rep_records, page = page)


def sup_level():
    response.title = 'Supervisor Level'
    cid = session.cid
    
    add_btn = request.vars.add_btn

    sup_id = request.vars.sup_id_input
    sup_name = request.vars.sup_name_input
    sup_level_id = request.vars.sup_level_id_input
    sup_level_name = request.vars.sup_level_name_input

    page = request.vars.page_no

    if page == '' or page == 'None' or page == None:
        page = 1

    page_limit = 20
    page_no = int(page)
    start_index = (page_no - 1) * page_limit

    if add_btn:
        if sup_id == '':
            response.flash = 'Enter representative ID'
        elif sup_name == '':
            response.flash = 'Enter representative name'
        elif sup_level_id == '':
            response.flash = 'Enter level ID'
        elif sup_level_name == '':
            response.flash = 'Enter level name'
        else:
            check_sup_sql = f"SELECT user_type FROM sm_rep WHERE cid = '{cid}' AND rep_id = '{sup_id}' and name = '{sup_name}' LIMIT 1;"
            check_sup = db.executesql(check_sup_sql, as_dict=True)

            if len(check_sup) != 0:
                for s in range(len(check_sup)):
                    sup_data = check_sup[s]
                    user_type = str(sup_data['user_type'])
                
                if user_type == 'sup':
                    get_level_id_sql = f"SELECT level_id FROM sm_supervisor_level"

                insert_sup_sql = f"INSERT INTO sm_rep (cid, rep_id, name, mobile_no, password, status, user_type) VALUES ('{cid}','{sup_id.upper()}','{sup_name}','{sup_mobile}','{sup_pass}','{sup_status.upper()}','{sup_user_type}');"
                db.executesql(insert_sup_sql)

    get_sup_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' AND user_type = 'sup' ORDER BY id ASC LIMIT {start_index}, {page_limit};"
    sup_records = db.executesql(get_sup_list_sql, as_dict = True)
    
    return dict(sup_records = sup_records, page = page)