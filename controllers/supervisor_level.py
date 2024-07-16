
def sup_level():
    today=str(date_fixed).split(' ')[0]
    response.title = 'Supervisor Level'
    cid = session.cid
    session.search_sup=''
    session.search_lvl=""
    add_btn = request.vars.add_btn
    delete_btn=request.vars.delete_btn
    rep_id = request.vars.rep_id_input
    rep_name = request.vars.rep_name_input
    sup_filter_condition =""
    page = request.vars.page_no
    # search_sup = ''
    # search_lvl =''
    
    
    
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
    

    btn_filter_item=request.vars.btn_filter_item
    btn_all=request.vars.all

    if btn_filter_item:
        search_sup = request.vars.search_sup
        search_lvl = request.vars.search_value
        # return search_value

        session.search_sup=search_sup
        session.search_lvl=search_lvl
        
        if search_sup:
            id=str(search_sup).split('|')[0].strip().upper()
            name=str(search_sup).split('|')[1].strip().upper()
            # return f" ({id}) ({name}) "
            sup_filter_condition= f" and sup_id='{id}' and sup_name='{name}' "
        else:
            response.filter_error="Invalid Sup"

        if search_lvl:
            id=str(search_lvl).split('|')[0].strip().upper()
            name=str(search_lvl).split('|')[1].strip().upper()
            level_depth_no=str(search_lvl).split('|')[2].strip().upper()
            sup_filter_condition+= f" and level_id='{id}'"
        else:
            response.filter_error="Invalid Sup Level"  
        session.sup_filter_condition = sup_filter_condition

    if btn_all:
        session.sup_filter_condition=""   
        session.search_sup=""
        session.search_lvl="" 
            
      
    if add_btn:
        sup_input = str(request.vars.sup_input).strip()
        level_input = request.vars.level_input
        if sup_input == '':
            response.flash = 'Select Sup'
        elif level_input == '':
            response.flash = 'Select Level'
        else:
            try:
                sup_id = str(sup_input).strip().upper().split('|')[0]
                sup_name = str(sup_input).strip().upper().split('|')[1]
            except ValueError:
                response.flash_error = 'Invalid SUP Format'
            else:
                try:
                    level_id = str(level_input).strip().upper().split('|')[0]
                    level_name= str(level_input).strip().upper().split('|')[1]
                    depth = str(level_input).strip().upper().split('|')[2]
                except ValueError:
                    response.flash = 'Invalid Sup level Format'
                else:
                    check_sup_sql = f"SELECT * FROM sm_supervisor_level WHERE cid = '{cid}' AND sup_id = '{sup_id}' AND level_id = '{level_id}' order by sup_id LIMIT 1;"
                    # return check_sup_sql
                    check_sup = db.executesql(check_sup_sql, as_dict=True)
                    if len(check_sup) == 0:
                        insert_sup_lvl_sql = f"INSERT INTO sm_supervisor_level(cid, sup_id, sup_name, level_id, level_name, level_depth_no,  created_on, created_by) VALUES ('{cid}', '{sup_id}', '{sup_name}', '{level_id}', '{level_name}', '{depth}', '{today}','{session.user_id}');"
                        # return insert_rep_sql                         #to see that query is alright.
                        db.executesql(insert_sup_lvl_sql)
                        response.flash = 'Insert successfully!'
                    else:
                        response.flash = 'Record already Exist!'
                    
    
    if delete_btn:
        delete_record_id=request.vars.delete_record_id
        delete_level_sql = f"DELETE FROM sm_supervisor_level WHERE id = '{delete_record_id}';"
        db.executesql(delete_level_sql)
        session.flash='Delete Successfully!'
        redirect(URL('sup_level'))
    
    # if session.sup_filter_condition =="" or session.sup_filter_condition is None: 
    #     sup_filter_condition=""
    # else:
    #     sup_filter_condition=session.sup_filter_condition
    
    get_rep_list_sql = f"SELECT id,sup_id, sup_name, level_id, level_name, level_depth_no FROM sm_supervisor_level WHERE cid = '{cid}' {sup_filter_condition} ORDER BY id DESC LIMIT %d, %d;" %limitby
    
    # return get_rep_list_sql

    rep_records = db.executesql(get_rep_list_sql, as_dict = True)
    total_rec_sql = f"SELECT * FROM sm_supervisor_level WHERE cid = '{cid}' {sup_filter_condition} ORDER BY id DESC;"

    total_record = db.executesql(total_rec_sql, as_dict = True)

    # for download
    session.filter_record_sql=get_rep_list_sql
    
    return dict(rep_records = rep_records, page = page,total=len(total_record),items_per_page=items_per_page)




def sup_id_info():
    cid = session.cid
    if cid =="" or cid==None:
        redirect(URL('default', 'index'))

    retStr=''
    # Fetch MSO ID|Name values from the database
    sql_query = f"select rep_id,name from sm_rep where cid = '{cid}' and user_type = 'sup' order by rep_id"
    rows = db.executesql(sql_query, as_dict = True)
    for idx in range(len(rows)):
        rep_id = str(rows[idx]['rep_id'])
        name = str(rows[idx]['name']).replace('|', ' ').replace(',', ' ')
        

        if retStr == '':
            retStr = rep_id + '|' + name 
        else:
            retStr += ',' + rep_id + '|' + name 
    return retStr


def sup_lvl_info():
    cid = session.cid
    if cid =="" or cid==None:
        redirect(URL('default', 'index'))

    retStr=''
    sql_query = f"SELECT level_id, level_name, depth FROM `sm_level` WHERE cid='{cid}' order by level_id;"
    
    rows = db.executesql(sql_query, as_dict = True)

    for idx in range(len(rows)):
        level_id = str(rows[idx]['level_id'])
        level_name = str(rows[idx]['level_name']).replace('|', ' ').replace(',', ' ')
        depth = str(rows[idx]['depth'])

        if retStr == '':
            retStr = level_id + '|' + level_name + '|' + depth
        else:
            retStr += ',' + level_id + '|' + level_name + '|' + depth
    return retStr


def sup_input_list():
    c_id = session.cid
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    retStr = ''

    replistRows_sql = "select rep_id ,name from sm_rep where cid = '"+c_id+"' and user_type = 'sup' group by rep_id;"
    replistRows = db.executesql(replistRows_sql, as_dict=True)

    for i in range(len(replistRows)):
        rep_list_dict=replistRows[i]   
        rep_id=str(rep_list_dict["rep_id"])
        name=str(rep_list_dict["name"])
        if retStr == '':
            retStr = rep_id+' | '+name
        else:
            retStr += ',' + rep_id+' | '+name
    
    return retStr


def sup_lvl_input_list():
    c_id = session.cid
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    retStr = ''

    replistRows_sql = f"SELECT `level_id`, `level_name`, `depth` FROM `sm_level` WHERE cid='{c_id}' group by level_id;"
    replistRows = db.executesql(replistRows_sql, as_dict=True)

    for i in range(len(replistRows)):
        rep_list_dict=replistRows[i]   
        level_id=str(rep_list_dict["level_id"])
        level_name=str(rep_list_dict["level_name"])
        depth=str(rep_list_dict["depth"])
        if retStr == '':
            retStr = level_id+' | '+level_name+' | '+depth
        else:
            retStr += ',' + level_id+' | '+level_name+' | '+depth
    
    return retStr


def download_sup_lvl():
    cid = session.cid
    if (cid=='' or cid==None):
        redirect (URL('default','index'))
    sup_filter_condition = ''
    sup_filter_condition = session.sup_filter_condition
    if sup_filter_condition==None or sup_filter_condition=='':
        sup_filter_condition=''

    get_sup_lvl_list_sql = f"SELECT sup_id, sup_name, level_id, level_name, level_depth_no FROM sm_supervisor_level WHERE cid = '{cid}' {sup_filter_condition} ORDER BY id DESC;"
    # return get_sup_list_sql
    
    data = db.executesql(get_sup_lvl_list_sql, as_dict = True)
    
    myString = 'ACCL Supervisor Level List\n\n'
    myString += 'Sup ID, Sup Name, level Id, level Name, Depth \n'
    
    for item in range(len(data)):
        row = data[item]   
        sup_id=str(row["sup_id"])
        name=str(row["sup_name"])
        level_id=str(row["level_id"])
        level_name=str(row["level_name"])
        level_depth_no=str(row["level_depth_no"])
        

        myString += str(sup_id) + ',' + str(name) + ',' + str(level_id) + ',' + str(level_name) + ',' + str(level_depth_no) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=ACCL_Supervisor_Level_List.csv'
    return str(myString)



def sup_lvl_batch_upload():
    response.title = 'Supervisor level -Batch Upload'
    today=str(date_fixed).split(' ')[0]
    cid=session.cid
    btn_upload=request.vars.upload_btn
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
            
    if btn_upload=='Upload':
        excel_data=str(request.vars.excel_data)
       
        
        row_list=excel_data.split( '\n')
        # print(row_list)
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
                sup_id = str(coloum_list[0]).strip().upper()
                lvl_id = str(coloum_list[1]).strip().upper()
                
                # return f"sup:{sup_id} lvl_id:{lvl_id} "
                if (sup_id==None or sup_id=='') or (lvl_id == None  or lvl_id== '') :
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    select_sup =f" SELECT rep_id, name FROM sm_rep WHERE cid = '{cid}' AND rep_id='{sup_id}' and user_type ='sup' ORDER BY rep_id LIMIT 1;"
                    # return select_sup
                    select_sup_data = db.executesql(select_sup, as_dict=True)
                    if len(select_sup_data) > 0:
                        # return "sup existe"
                        sup_ids = select_sup_data[0]['rep_id']
                        name = select_sup_data[0]['name']
                    else:
                        error_data=row_data+'(sup does not exists!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    
                    select_lvl_sql =f" SELECT level_id, level_name, depth FROM sm_level WHERE cid = '{cid}' AND level_id = '{lvl_id}' GROUP BY level_id LIMIT 1;"
                    # return select_lvl_sql
                    select_lvl = db.executesql(select_lvl_sql, as_dict=True)
                    if len(select_lvl)>0:
                        level_id = select_lvl[0]['level_id']
                        level_name = select_lvl[0]['level_name']
                        depth = select_lvl[0]['depth']
                        # return f"level_id {level_id} level_name,{level_name} , depth:{depth}"
                    else:
                        error_data=row_data+'(this this supervisor level does not exist)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    # existCheckRows= f"select * FROM sm_supervisor_level WHERE cid='{cid}' and sup_id='{sup_id}'"
                    existCheckRows= " select * FROM sm_supervisor_level WHERE cid='"+str(cid)+"' and sup_id = '"+str(sup_id)+"' and level_id= '"+str(lvl_id)+"' LIMIT 0,1"
                    # return existCheckRows    
                    existCheck = db.executesql(existCheckRows)
                    # return len(existCheck)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Supervisor please check!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        
                        try:
                            insert_sql =f"INSERT INTO sm_supervisor_level(cid, sup_id, sup_name, level_id, level_name, level_depth_no,  created_on, created_by) VALUES ('{cid}', '{sup_ids}', '{name}', '{level_id}', '{level_name}', '{depth}', '{today}','{session.user_id}');"

                            db.executesql(insert_sql)
                            count_inserted+=1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
  



def get_supervisor_list():
    cid = session.cid
    if (cid=='' or cid==None):
        return redirect(URL('sup_level'))
    sup_info_Str = ''
    get_sup_id_name =  f"SELECT sup_id, sup_name, level_id, level_name, level_depth_no FROM sm_supervisor_level WHERE cid = '{cid}' ORDER BY id DESC;"
    suplistRows = db.executesql(get_sup_id_name, as_dict=True)

    for i in range(len(suplistRows)):
        rep_list_dict=suplistRows[i]   
        rep_id=str(rep_list_dict["sup_id"])
        name=str(rep_list_dict["sup_name"])
        if sup_info_Str == '':
            sup_info_Str = rep_id+' | '+name
        else:
            sup_info_Str += ',' + rep_id+' | '+name
    
    return sup_info_Str


def get_supervisor_lvl_list():
    cid = session.cid
    if (cid=='' or cid==None):
        return redirect(URL('sup_level'))
    sup_lvlinfo_Str = ''
    get_sup_id_name =  f"SELECT sup_id, sup_name, level_id, level_name, level_depth_no FROM sm_supervisor_level WHERE cid = '{cid}' ORDER BY id DESC;"
    suplistRows = db.executesql(get_sup_id_name, as_dict=True)

    for i in range(len(suplistRows)):
        rep_list_dict=suplistRows[i]   
        level_id=str(rep_list_dict["level_id"])
        name=str(rep_list_dict["level_name"])
        depth=str(rep_list_dict["level_depth_no"])
        if sup_lvlinfo_Str == '':
            sup_lvlinfo_Str = level_id+' | '+name+" | "+depth
        else:
            sup_lvlinfo_Str += ',' + level_id+' | '+name+" | "+depth
    
    return sup_lvlinfo_Str