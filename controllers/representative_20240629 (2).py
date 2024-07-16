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
    today=str(date_fixed).split(' ')[0]
    response.title = 'Representative Area'
    cid = session.cid
    
    add_btn = request.vars.add_btn

    rep_id = request.vars.rep_id_input
    rep_name = request.vars.rep_name_input
   
    page = request.vars.page_no
    
    
    session.insert_error=''
    session.update_delete_error=''
    session.filter_error=''
    
    
    
    
    if page == '' or page == 'None' or page == None:
        page = 1

    page_limit = 20
    page_no = int(page)
    start_index = (page_no - 1) * page_limit
    
    
    btn_filter_item=request.vars.btn_filter_item
    all=request.vars.all
    if btn_filter_item:
        search_type = request.vars.search_type
        search_value = request.vars.search_value
        session.search_value_reparea=search_value
        
        if search_type == 'mso':
            try:
                session.option_selected=search_type
                id,name=str(search_value).strip().upper().split('|')
                session.filter_condition= f" and rep_id='{id}' and rep_name='{name}' "
            except:
                session.filter_error="Invalid MSO"

        elif search_type == 'territory':
            try:
                session.option_selected=search_type
                id,name=str(search_value).strip().upper().split('|')
                session.filter_condition= f" and area_id='{id}' and area_name='{name}' "
            except:
                session.filter_error="Invalid Territory"
        else:
            session.filter_error="Select a type"      
    if all:
        session.filter_condition=''   
        session.option_selected=''
        session.search_value_reparea=''  
            
      
    if add_btn:
        rep_input = request.vars.rep_input
        area_input = request.vars.area_input
        if rep_input == '':
            session.insert_error = 'Select MSO'
        elif area_input == '':
            session.insert_error = 'Select Territory'
        else:
            try:
                rep_id, rep_name = str(rep_input).strip().upper().split('|')
            except ValueError:
                session.insert_error = 'Invalid MSO Format'
            else:
                try:
                    area_id, area_name = str(area_input).strip().upper().split('|')
                except ValueError:
                    session.insert_error = 'Invalid Territory Format'
                else:
                    check_rep_sql = f"SELECT * FROM sm_rep_area WHERE cid = '{cid}' AND rep_id = '{rep_id}' OR area_id = '{area_id}' LIMIT 1;"
                    check_rep = db.executesql(check_rep_sql, as_dict=True)
                    if len(check_rep) == 0:
                        insert_rep_sql = f"INSERT INTO sm_rep_area (cid, rep_id, rep_name, area_id, area_name, created_on, created_by) VALUES ('{cid}', '{rep_id}', '{rep_name}', '{area_id}', '{area_name}', '{today}', '{session.user_id}');"
                        db.executesql(insert_rep_sql)
                        session.insert_error = 'Insert successfully!'
                    else:
                        session.insert_error = 'Record already Exist!'
    
    
    delete_btn=request.vars.delete_btn
    if delete_btn:
        delete_record_id=request.vars.delete_record_id
        delete_level_sql = f"DELETE FROM sm_rep_area WHERE id = '{delete_record_id}';"
        db.executesql(delete_level_sql)
        session.update_delete_error='Delete Successfully!'
        
    if session.filter_condition is None: 
        get_rep_list_sql = f"SELECT id,rep_id, rep_name, area_id,area_name FROM sm_rep_area WHERE cid = '{cid}' ORDER BY id DESC LIMIT {start_index}, {page_limit};"
    else:
        get_rep_list_sql = f"SELECT id,rep_id, rep_name, area_id,area_name FROM sm_rep_area WHERE cid = '{cid}' {session.filter_condition} ORDER BY id DESC LIMIT {start_index}, {page_limit};"

    rep_records = db.executesql(get_rep_list_sql, as_dict = True)
    
    # for download
    session.filter_record_sql=get_rep_list_sql
    
    return dict(rep_records = rep_records, page = page,total=len(rep_records))

def rep_input_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    replistRows_sql = "select rep_id ,name from sm_rep where cid = '"+c_id+"' group by rep_id;"
    replistRows = db.executesql(replistRows_sql, as_dict=True)

    for i in range(len(replistRows)):
        rep_list_dict=replistRows[i]   
        rep_id=str(rep_list_dict["rep_id"])
        name=str(rep_list_dict["name"])
        if retStr == '':
            retStr = rep_id+'|'+name
        else:
            retStr += ',' + rep_id+'|'+name
    
    return retStr

def area_input_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    arealistRows_sql = "select level3 ,level3_name from sm_level where cid = '"+c_id+"' group by level3_name;"
    arealistRows = db.executesql(arealistRows_sql, as_dict=True)

    for i in range(len(arealistRows)):
        area_list_dict=arealistRows[i]   
        terri_id=str(area_list_dict["level3"])
        terri_name=str(area_list_dict["level3_name"])
        if retStr == '':
            retStr =terri_id+'|'+terri_name
        else:
            retStr += ',' +terri_id+'|'+terri_name
    
    return retStr

def filter_autocomplete():
    search_type = request.vars.search_type
    values = []
    

    if search_type == 'mso':
        # Fetch MSO ID|Name values from the database
        rows = db(db.sm_rep_area).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name)
        values = [row.rep_id + '|' + row.rep_name for row in rows]

    elif search_type == 'territory':
        # Fetch Territory ID|Name values from the database
        rows = db(db.sm_rep_area).select(db.sm_rep_area.area_id, db.sm_rep_area.area_name)
        values = [row.area_id + '|' + row.area_name for row in rows]
    
    return ','.join(values)


def download_rep_area():
    c_id=session.cid

    
    myString= 'Rep ID,Rep Name,Teritory ID,Territory Name\n'

    download_records = db.executesql(session.filter_record_sql, as_dict=True)

        
    for i in range(len(download_records)):
        levelData=download_records[i]
        rep_id=levelData['rep_id']
        rep_name=levelData['rep_name']
        area_id=levelData['area_id']
        area_name=levelData['area_name']
         
        myString+=str(rep_id)+','+str(rep_name)+','+str(area_id)+','+str(area_name)+'\n'                       
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_level.csv'   
    return str(myString)



#====================================== REP AREA BATCH UPLOAD ---------- 
def area_batch_upload():
    response.title = 'Rep/MSO -Territory/Route -Batch Upload'
    cid=session.cid
    btn_upload=request.vars.btn_upload
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
            
    if btn_upload=='Upload':
        excel_data=str(request.vars.excel_data)
       
        
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        ff_list_excel=[]
                

        # ----------------------
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==2:
                    ffExcel=str(coloum_list[0]).strip().upper()
                    
                    if ffExcel!='':
                        if ffExcel not in ff_list_excel:ff_list_excel
                        ff_list_excel.append(ffExcel)       

        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]
                coloum_list=row_data.split( '\t')            
            
            if len(coloum_list)!=2:
                error_data=row_data+'(2 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                rep_id = str(coloum_list[0]).strip().upper()
                territory_id = str(coloum_list[1]).strip().upper()
              
                if rep_id=='NONE'or territory_id == 'NONE' or rep_id=='' or territory_id== '':
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    existCheckRows= " select * FROM sm_rep_area WHERE cid='"+str(cid)+"' and rep_id = '"+str(rep_id)+"' OR area_id = '"+str(territory_id)+"' LIMIT 0,1"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate MSO check)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        try:
                            rep_name_sql=f"select name from sm_rep where rep_id='{rep_id}' limit 1"
                            rep_name_exc=db.executesql(rep_name_sql,as_dict=True)
                            if len(rep_name_exc)==0:
                                error_data=row_data+'(Rep id is not present in sm_rep table)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue 
                            rep_name=rep_name_exc[0]['name']
                            
                            territory_name_sql=f"select level_name from sm_level where level_id='{territory_id}' limit 1"
                            territory_name=db.executesql(territory_name_sql,as_dict=True)
                            if len(territory_name)==0:
                                error_data=row_data+'(Territory id is not present in sm_level table)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue 
                            
                            territory_name=territory_name[0]['level_name']
                            
                            insert_sql = "INSERT INTO sm_rep_area (cid, rep_id, rep_name, area_id, area_name) VALUES ('"+str(cid)+"','"+str(rep_id)+"','"+str(rep_name)+"', '"+str(territory_id)+"','"+str(territory_name)+"');"
                            update_ff_list = db.executesql(insert_sql)
                            count_inserted+=1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
 
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