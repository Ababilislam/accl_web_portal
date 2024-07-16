def supervisor_create(): 
    response.title = 'Supervisor'
    cid = session.cid
    user_id = session.u_id
    if cid =="" or cid==None:
        redirect(URL('default', 'index'))
    
    submit_btn = request.vars.submit_btn
    filter_btn = request.vars.btn_filter
    all_btn = request.vars.btn_rep_all

    sup_condition = ''
   
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
        sup_id = str(request.vars.sup_id).upper()
        sup_name = str(request.vars.sup_name).upper()
        sup_name =check_special_char(sup_name)
        # return f"name:{rep_name}"
        sup_mobile = str(request.vars.sup_mobile).upper()
        sup_pass = str(request.vars.sup_password)
        # sup_pass = random.randint(0000,9999)
        # rep_pass = str(request.vars.rep_password)
        sup_status = str(request.vars.status).strip().upper()
        sup_user_type = str(request.vars.sup_type).strip()
        # user_type = "sup"
        
        if (sup_id !="" and sup_name !=""and sup_user_type !="" and sup_mobile !=""and sup_pass !="" and sup_status !=""):
            sup_check_sql =f"SELECT * FROM sm_rep WHERE cid = '{cid}' AND rep_id = '{sup_id}' LIMIT 1;"
            check_sup = db.executesql(sup_check_sql,as_dict=True)

            if len(check_sup)>0:
                response.flash = "User already exists!"
                response.flash_type = "warning"
            else:
                insert_sup_sql = f"INSERT INTO sm_rep (cid, rep_id, name, mobile_no, password, status, user_type) VALUES ('{cid}','{sup_id}','{sup_name}','{sup_mobile}','{sup_pass}','{sup_status}','{sup_user_type}');"
                # return insert_rep_sql
                db.executesql(insert_sup_sql)
                response.flash = 'Representative added successfully'
                response.flash_type = "success"
                redirect(URL('supervisor','supervisor_create'))              
        else:
            response.flash = "All fields required!"

    if filter_btn:
        sup_id = ''
        sup_name = ''
        sup_mobile = ''
        select_optn = str(request.vars.search_type)
        search_value = str(request.vars.search_value)
        # print(select_optn)
        try:
            sup_id = search_value.split('|')[0]
            sup_name = search_value.split('|')[1]
            sup_mobile = search_value.split('|')[2]
            # return rep_id, rep_name, rep_mobile
        except:
            sup_id = ''
            sup_name = ''
            sup_mobile = ''
        
        if select_optn == 'RepID':
            if session.search_value !="" or search_value != "":
                sup_condition = f" and (rep_id = '{sup_id}' and name like '{sup_name}' and mobile_no = '{sup_mobile}') "
                session.search_type=select_optn
                session.search_value = search_value
        if select_optn =='Status':
            sup_condition = f" and status = '{search_value}' "
            session.search_type=select_optn
            session.search_value = search_value
        session.sup_condition = sup_condition
    if all_btn:
        sup_condition =''
        session.search_type=''
        session.search_value=''
        session.sup_condition = sup_condition
        # return "helo"
    if session.sup_condition=='' or session.sup_condition==None:
        sup_condition=""
    else:
        sup_condition=session.sup_condition
    # get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' {condition} ORDER BY id DESC LIMIT {start_index},{page_limit};"
    get_rep_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password,note FROM sm_rep WHERE cid = '{cid}' {sup_condition} and user_type = 'sup' ORDER BY id DESC LIMIT %d, %d;" % limitby 
    sup_records = db.executesql(get_rep_list_sql, as_dict = True)
    # return get_rep_list_sql
    total_rep_sql = f"SELECT * FROM sm_rep WHERE cid = '{cid}' {sup_condition} and user_type = 'sup' ORDER BY id DESC;"
    total_rec = db.executesql(total_rep_sql, as_dict = True)
    total = len(total_rec)
    # print(total)

    return dict(rep_records = sup_records, total=total, page = page, items_per_page = items_per_page)
   



def supervisor_edit():
    response.title = 'Representative Edit'

    cid = session.cid
    user_id = session.u_id
    if cid =="" or cid==None:
        redirect(URL('default', 'index'))
    
    sup_id = str(request.args(0)).strip().replace('_',' ')
    
    # return rep_id                         #
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_sup_record_sql = f"SELECT * FROM sm_rep WHERE rep_id = '{sup_id}' GROUP BY rep_id LIMIT 1;"
    sup_record = db.executesql(select_sup_record_sql, as_dict = True)

    if len(sup_record) != 0 :
        for i in range(len(sup_record)):
            item = sup_record[i]
            sup_id = str(item["rep_id"])
            sup_name = str(item["name"])
            sup_mobile = str(item["mobile_no"])
            sup_pass = str(item["password"])
            sup_status = str(item["status"])
            sup_user_type = str(item["user_type"])
        # print(rep_user_type)
        # print("rep_id:"+ rep_id, "rep_name:"+rep_name, "rep_mobile:"+rep_mobile, "rep_pass:"+rep_pass, "rep_status:"+rep_status , "rep_user_type:"+rep_user_type)
    if update_btn:
        # return "hello"
        sup_id = str(request.vars.sup_id)
        # return rep_id
        sup_name_up = str(request.vars.sup_name).upper()
        sup_mobile_up = str(request.vars.sup_mobile).upper()
        sup_pass_up = str(request.vars.sup_password)
        sup_status_up = str(request.vars.status).strip().upper()
        sup_user_type_up = str(request.vars.sup_type).upper()
        # print("rep_name:"+rep_name_up, "rep_mobile_up:"+rep_mobile_up, "rep_pass_up:"+rep_pass_up, "rep_status_up:"+rep_status_up,"rep_user_type_up:"+rep_user_type_up )
        
        update_sup_sql = f"UPDATE sm_rep SET name = '{sup_name_up}', mobile_no = '{sup_mobile_up}', password = '{sup_pass_up}', status = '{sup_status_up}', user_type = '{sup_user_type_up}' WHERE cid='{cid}' and rep_id='{(str(sup_id))}' limit 1;"
        # return update_rep_sql
        db.executesql(update_sup_sql)
        session.flash = 'Successfully Updated'
        return redirect(URL("supervisor_create"))

    if delete_btn:
        sup_id = str(request.vars.sup_id)
        delete_sql = f"DELETE FROM sm_rep WHERE cid='{cid}' and rep_id='{sup_id}' LIMIT 1;"
        # return delete_sql                 #to see the return sql
        db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('supervisor','supervisor_create'))
    return dict(sup_id=sup_id, sup_name=sup_name,sup_mobile=sup_mobile, sup_pass=sup_pass,rep_status=sup_status,sup_type=sup_user_type)



def supervisor_batch_upload():
    response.title = 'Supervisor -Batch Upload'
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
            
            if len(coloum_list)!=6:
                error_data=row_data+'(6 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                sup_id = str(coloum_list[0]).strip().upper()
                sup_name = str(coloum_list[1]).strip().upper()
                mobile = str(coloum_list[2]).strip().upper()
                type = str(coloum_list[3]).strip().upper()
                pswrd = str(coloum_list[4]).strip().upper()
                status = str(coloum_list[5]).strip().upper()
                # pswrd = random.randint(0000,9999)
                # return f"sup:{sup_id} sup_name:{sup_name} mobile:{mobile} type:{type} status:{status} pswrd:{pswrd}"
                if (sup_id==None or sup_id=='') or (sup_name == None  or sup_name== '') or (mobile == None  or mobile== '') or (type == None  or type== '') or (status == None  or status== '') or (pswrd == None or pswrd ==''):
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue                    
                
                else:
                    existCheckRows= " select * FROM sm_rep WHERE cid='"+str(cid)+"' and rep_id = '"+str(sup_id)+"' and user_type LIKE 'SUP' LIMIT 0,1"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate Supervisor please check!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        try:
                            insert_sql =f"INSERT INTO sm_rep (cid, rep_id, name, mobile_no, password, status, user_type) VALUES ('{cid}','{sup_id}','{sup_name}','{mobile}','{pswrd}','{status}','{type}');"
                            # return insert_sql
                            db.executesql(insert_sql)
                            count_inserted+=1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                                
        if error_str=='':
            error_str='No error'

    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)
  



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




#====================================== sup auto complete ---------- 


def get_sup_list():
    retStr = ''
    cid = session.cid

    search_type = request.vars.search_type.strip()
    
    sql_query = f"select sr.rep_id, sr.name, sr.mobile_no from sm_rep as sr where sr.cid = '{cid}' and user_type = 'sup' order by sr.rep_id"
    
    rows = db.executesql(sql_query, as_dict = True)

    for idx in range(len(rows)):
        sup_id = str(rows[idx]['rep_id'])
        name = str(rows[idx]['name']).replace('|', ' ').replace(',', ' ')
        mobile_no = str(rows[idx]['mobile_no'])

        if retStr == '':
            retStr = sup_id + '|' + name + '|' + mobile_no
        else:
            retStr += ',' + sup_id + '|' + name + '|' + mobile_no

    return retStr


def download_supervisor():
    cid = session.cid
    if (cid=='' or cid==None):
        redirect (URL('default','index'))
    sup_condition = ''
    sup_condition = session.sup_condition
    if sup_condition==None or sup_condition=='None':
        sup_condition=''

    get_sup_list_sql = f"SELECT rep_id, name, mobile_no, status, user_type, password FROM sm_rep WHERE cid = '{cid}' {sup_condition} and user_type = 'sup' ORDER BY rep_id DESC;"
    
    data = db.executesql(get_sup_list_sql, as_dict = True)
    
    myString = 'ACCL Supervisor List\n\n'
    myString += 'Sup ID, Name, Type, Password, Status, Mobile \n'
    
    for item in range(len(data)):
        row = data[item]   
        sup_id=str(row["rep_id"])
        name=str(row["name"])
        user_type=str(row["user_type"])
        password=str(row["password"])
        status=str(row["status"])
        mobile=str(row["mobile_no"])

        myString += str(sup_id) + ',' + str(name) + ',' + str(user_type) + ',' + str(password) + ',' + str(status) + ',' + str(mobile) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=ACCL_Supervisor_List.csv'
    return str(myString)
#===================================



