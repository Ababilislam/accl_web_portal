def rep():
    response.title = 'Representative'
    cid = session.cid
    user_id = session.u_id
    if cid =="" or cid==None:
        redirect(URL('default', 'index'))
    
    

    submit_btn = request.vars.submit_btn
    filter_btn = request.vars.btn_filter
    all_btn = request.vars.btn_rep_all

    rep_condition = ''
    # pagination 
    # page = request.vars.page_no
    
    # if page == '' or page == 'None' or page == None:
    #     page = 1

    # page_limit = 20
    # page_no = int(page)
    # start_index = (page_no - 1) * page_limit
    #  end pagination
    # --------paging
    reqPage = len(request.args)

    session.items_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    if(page==0):
        limitby = (page * items_per_page, (page + 1) * items_per_page)
    else:
        limitby = ((page* items_per_page), items_per_page)
    # --------end paging

    if submit_btn:
        rep_id = str(request.vars.rep_id).upper()
        rep_name = str(request.vars.rep_name).upper()

        rep_mobile = str(request.vars.rep_mobile).upper()
        rep_pass = str(request.vars.rep_password)
        rep_status = str(request.vars.status).strip().upper()
        rep_user_type = str(request.vars.rep_type).upper()
        
        if (rep_id !="" and rep_name !=""and rep_user_type !="" and rep_mobile !=""and rep_pass !="" and rep_status !=""):
            rep_check_sql =f"SELECT * FROM sm_rep WHERE cid = '{cid}' AND rep_id = '{rep_id}' AND password = '{rep_pass}' LIMIT 1;"
            check_rep = db.executesql(rep_check_sql,as_dict=True)

            if len(check_rep)>0:
                response.flash = "User already exists!"
                response.flash_type = "warning"
            else:
                insert_rep_sql = f"INSERT INTO sm_rep (cid, rep_id, name, mobile_no, password, status, user_type) VALUES ('{cid}','{rep_id}','{rep_name}','{rep_mobile}','{rep_pass}','{rep_status}','{rep_user_type}');"
                db.executesql(insert_rep_sql)
                response.flash = 'Representative added successfully'
                response.flash_type = "success"
                redirect(URL('representative','rep'))              
        else:
            response.flash = "All fields required!"

    if filter_btn:
        rep_id = ''
        rep_name = ''
        rep_mobile = ''
        select_optn = str(request.vars.search_type)
        search_value = str(request.vars.search_value)
        # print(select_optn)
        try:
            rep_id = search_value.split('|')[0]
            rep_name = search_value.split('|')[1]
            rep_mobile = search_value.split('|')[2]
            # return rep_id, rep_name, rep_mobile
        except:
            rep_id = ''
            rep_name = ''
            rep_mobile = ''
        
        if select_optn == 'RepID':
            if session.search_value !="" or search_value != "":
                rep_condition = f" and (rep_id = '{rep_id}' and name like '{rep_name}' and mobile_no = '{rep_mobile}') "
                session.search_type=select_optn
                session.search_value = search_value
        if select_optn =='Status':
            rep_condition = f" and status = '{search_value}' "
            session.search_type=select_optn
            session.search_value = search_value
        session.rep_condition = rep_condition
    if all_btn:
        rep_condition =''
        session.search_type=''
        session.search_value=''
        session.rep_condition = rep_condition
        # return "helo"
    if session.rep_condition=='' or session.rep_condition==None:
        rep_condition=""
    else:
        rep_condition=session.rep_condition
    # get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' {condition} ORDER BY id DESC LIMIT {start_index},{page_limit};"
    get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' {rep_condition} ORDER BY id DESC LIMIT %d, %d;" % limitby 
    rep_records = db.executesql(get_rep_list_sql, as_dict = True)
    # return get_rep_list_sql
    total_rep_sql = f"SELECT * FROM sm_rep WHERE cid = '{cid}' {rep_condition} ORDER BY id DESC;"
    total_rec = db.executesql(total_rep_sql, as_dict = True)
    total = len(total_rec)
    # print(total)

    return dict(rep_records = rep_records, total=total, page = page, items_per_page = items_per_page)
   



def rep_edit():
    response.title = 'Representative Edit'

    cid = session.cid
    user_id = session.u_id
    if cid =="" or cid==None:
        redirect(URL('default', 'index'))
    
    rep_id = str(request.args(0)).strip()
    
    # return rep_id                         #
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_rep_record_sql = f"SELECT * FROM sm_rep WHERE rep_id = '{rep_id}' GROUP BY rep_id LIMIT 1;"
    rep_record = db.executesql(select_rep_record_sql, as_dict = True)

    if len(rep_record) != 0 :
        for i in range(len(rep_record)):
            item = rep_record[i]
            rep_id = str(item["rep_id"])
            rep_name = str(item["name"])
            rep_mobile = str(item["mobile_no"])
            rep_pass = str(item["password"])
            rep_status = str(item["status"])
            rep_user_type = str(item["user_type"])
        # print("rep_id:"+ rep_id, "rep_name:"+rep_name, "rep_mobile:"+rep_mobile, "rep_pass:"+rep_pass, "rep_status:"+rep_status , "rep_user_type:"+rep_user_type)
    if update_btn:
        # return "hello"
        rep_id = str(request.vars.rep_id)
        # return rep_id
        rep_name_up = str(request.vars.rep_name).upper()
        rep_mobile_up = str(request.vars.rep_mobile).upper()
        rep_pass_up = str(request.vars.rep_password)
        rep_status_up = str(request.vars.status).strip().upper()
        rep_user_type_up = str(request.vars.rep_type).upper()
        # print("rep_name:"+rep_name_up, "rep_mobile_up:"+rep_mobile_up, "rep_pass_up:"+rep_pass_up, "rep_status_up:"+rep_status_up,"rep_user_type_up:"+rep_user_type_up )
        
        update_rep_sql = f"UPDATE sm_rep SET name = '{rep_name_up}', mobile_no = '{rep_mobile_up}', password = '{rep_pass_up}', status = '{rep_status_up}', user_type = '{rep_user_type_up}' WHERE cid='{cid}' and rep_id='{(str(rep_id))}' limit 1;"
        # return update_rep_sql
        db.executesql(update_rep_sql)
        session.flash = 'Successfully Updated'
        return redirect(URL("rep"))

    if delete_btn:
        rep_id = rep_id = str(request.vars.rep_id)
        delete_sql = f"DELETE FROM sm_rep WHERE cid='{cid}' and rep_id='{rep_id}' LIMIT 1;"
        # return delete_sql                 #to see the return sql
        db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('representative','rep'))
    return dict(rep_id=rep_id, rep_name=rep_name,rep_mobile=rep_mobile, rep_pass=rep_pass,rep_status=rep_status,rep_type=rep_user_type)


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
    
    
    
    # --------paging
    
    # if page == '' or page == 'None' or page == None:
    #     page = 1

    # page_limit = 20
    # page_no = int(page)
    # start_index = (page_no - 1) * page_limit
    
    reqPage = len(request.args)

    session.items_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    if(page==0):
        limitby = (page * items_per_page, (page + 1) * items_per_page)
    else:
        limitby = ((page* items_per_page), items_per_page)
    # --------end paging
    
    btn_filter_item=request.vars.btn_filter_item
    btn_all=request.vars.all
    if btn_filter_item:
        search_type = request.vars.search_type
        search_value = request.vars.search_value
        session.search_value_reparea=search_value
        
        if search_type == 'mso':
            try:
                session.option_selected=search_type
                id,name=str(search_value).strip().upper().split('|')
                filter_condition= f" and rep_id='{id}' and rep_name='{name}' "
            except:
                session.filter_error="Invalid MSO"

        elif search_type == 'territory':
            try:
                session.option_selected=search_type
                id,name=str(search_value).strip().upper().split('|')
                filter_condition= f" and area_id='{id}' and area_name='{name}' "
            except:
                session.filter_error="Invalid Territory"
        else:
            session.filter_error="Select a type"  

        session.filter_condition = filter_condition
    if btn_all:
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
    
    if session.filter_condition =="" or session.filter_condition is None: 
        filter_condition=""
    else:
        filter_condition=session.filter_condition

    get_rep_list_sql = f"SELECT id,rep_id, rep_name, area_id,area_name FROM sm_rep_area WHERE cid = '{cid}' {filter_condition} ORDER BY id DESC LIMIT %d, %d;" %limitby
    rep_records = db.executesql(get_rep_list_sql, as_dict = True)
    total_rec_sql = f"SELECT * FROM sm_rep_area WHERE cid = '{cid}' {filter_condition} ORDER BY id DESC;"

    total_record = db.executesql(total_rec_sql, as_dict = True)
    
    # for download
    session.filter_record_sql=get_rep_list_sql
    
    return dict(rep_records = rep_records, page = page,total=len(total_record),items_per_page=items_per_page)

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
    response.title = 'MSO-Territory Batch Upload'
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


def get_rep_list():
    retStr = ''
    cid = session.cid

    search_type = request.vars.search_type.strip()
    
    
    sql_query = f"select sr.rep_id, sr.name, sr.mobile_no from sm_rep as sr where sr.cid = '{cid}' order by sr.rep_id"
    
    rows = db.executesql(sql_query, as_dict = True)

    
    for idx in range(len(rows)):
        rep_id = str(rows[idx]['rep_id'])
        name = str(rows[idx]['name']).replace('|', ' ').replace(',', ' ')
        mobile_no = str(rows[idx]['mobile_no'])

        if retStr == '':
            retStr = rep_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + rep_id + '|' + name + '|' + mobile_no


    

    return retStr


    # return locals()


def rep_batch_upload():
    
    return dict()


def download_representative():
    cid = session.cid
    if (cid=='' or cid==None):
        redirect (URL('default','index'))
    rep_condition = ''
    rep_condition = session.rep_condition
    if rep_condition==None or rep_condition=='None':
        rep_condition=''

    get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' {rep_condition} ORDER BY rep_id DESC;"
    
    data = db.executesql(get_rep_list_sql, as_dict = True)
    
    myString = 'ACCL Representative List\n\n'
    myString += 'Rep ID, Name, Type, Password, Status, Mobile \n'
    
    for item in range(len(data)):
        row = data[item]   
        rep_id=str(row["rep_id"])
        name=str(row["name"])
        user_type=str(row["user_type"])
        password=str(row["password"])
        status=str(row["status"])
        mobile=str(row["mobile_no"])

        myString += str(rep_id) + ',' + str(name) + ',' + str(user_type) + ',' + str(password) + ',' + str(status) + ',' + str(mobile) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=ACCL_Representative_List.csv'
    return str(myString)



def get_rep_id_name_list():
    rep_id_name_Str = ''
    cid = session.cid
    if (cid == '' or cid == None):
        redirect(URL('default','index'))
    
    sql_query = f"select sr.rep_id, sr.name from sm_rep as sr where sr.cid = '{cid}' order by sr.rep_id"
    rows = db.executesql(sql_query, as_dict = True)

    for idx in range(len(rows)):
        rep_id = str(rows[idx]['rep_id'])
        name = str(rows[idx]['name']).replace('|', ' ').replace(',', ' ')


        if rep_id_name_Str == '':
            rep_id_name_Str = rep_id + '|' + name 
        else:
            rep_id_name_Str += ',' + rep_id + '|' + name


    

    return rep_id_name_Str