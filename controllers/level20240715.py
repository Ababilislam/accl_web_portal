from datetime import datetime

def level():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    depth = request.vars.depth
    if depth ==None or depth =='None':
        depth = 0
    depth = int(depth)
    response.title='Area Structure'
    c_id= session.cid
    
    session.insert_error=''
    session.update_delete_error=''
    session.search_error=''
    
    
    
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    submit_btn=request.vars.submit
    update_btn=request.vars.update_btn
    delete_btn=request.vars.delete_btn
    
    division_id= request.vars.division_id
    division_name= request.vars.division_name
    
    zone_id= request.vars.zone_id
    zone_name= request.vars.zone_name
    
    area_id= request.vars.area_id
    area_name= request.vars.area_name

    territory_id=request.vars.territory_id
    territory_name=request.vars.territory_name
    
    btn_search =request.vars.btn_search

    if btn_search:
        level_search=str(request.vars.level_search).strip().upper()
        session.level_search=level_search
        if level_search == "" or level_search == None:
           session.search_error='Please select level !'
        else:
            try:
                level_id,_=level_search.split('|')
            
                search_level_sql = f"select * from sm_level where level_id ='{level_id}' limit 1;"
                
                try:
                    search_level = db.executesql(search_level_sql,as_dict=True)
                    if len(search_level) > 0:
                        search_level=search_level[0]

                    item_id = search_level["id"]
                        
                    parent_id= search_level["parent_level_id"]
                    parent_name= search_level["parent_level_name"]
                    
                    depth = search_level["depth"]
                    
                    if depth == 0:
                        
                        division_id= search_level["level_id"]
                        division_name= search_level["level_name"]
                        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='0'  GROUP BY level0;"
                        level_records = db.executesql(get_level_list_sql, as_dict = True)
                        return dict(level_records = level_records,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,depth = depth,item_id=item_id)
                        
                    if depth == 1:
                        division_id= search_level["parent_level_id"]
                        division_name= search_level["parent_level_name"]
                        
                        zone_id= search_level["level_id"]
                        zone_name= search_level["level_name"]
                        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='"+str(parent_id)+"'  GROUP BY level1,level0;"
                        # return get_level_list_sql
                        level_records = db.executesql(get_level_list_sql, as_dict = True)
                        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,zone_id=zone_id,zone_name=zone_name,item_id=item_id)

                    if depth == 2:
                        division_id= search_level["level0"]
                        division_name= search_level["level0_name"]
                        
                        zone_id= search_level["parent_level_id"]
                        zone_name= search_level["parent_level_name"]
                        
                        area_id= search_level["level_id"]
                        area_name= search_level["level_name"]
                        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level2,level1,level0;"
                        # return get_level_list_sql
                        level_records = db.executesql(get_level_list_sql, as_dict = True)
                        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,zone_id=zone_id,zone_name=zone_name,area_id=area_id,area_name=area_name,item_id=item_id)
                    if depth == 3:
                        division_id= search_level["level0"]
                        division_name= search_level["level0_name"]
                        
                        zone_id= search_level["level1"]
                        zone_name= search_level["level1_name"]
                        
                        area_id= search_level["parent_level_id"]
                        area_name= search_level["parent_level_name"]
                        
                        territory_id=search_level["level_id"]
                        territory_name= search_level["level_name"]
                        
                        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level3,level2,level1,level0;"
                        # return get_level_list_sql
                        level_records = db.executesql(get_level_list_sql, as_dict = True)
                        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,zone_id=zone_id,zone_name=zone_name,area_id=area_id,
                                    area_name=area_name,territory_id=territory_id,territory_name=territory_name, item_id=item_id)
    
                except:
                    session.search_error=f'Invalid level ID: {level_id} !'
            except:
                session.search_error=f'Invalid level ID/Name !'    
    
    if depth == 0:
        parent_id= 0
        parent_name= ''
        
        if submit_btn:
            if division_id == '' or division_id == 'None' or division_id==None:
                session.insert_error='Please enter the Division ID!'
            elif division_name == '' or division_name == 'None' or division_name==None:
                session.insert_error='Please enter the Division Name!'
            elif check_level_id(division_id) == True:
                session.insert_error='Level id already exists!'
            else:
                insert_national_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(division_id)+"','"+str(division_name)+"','0','','0','0','"+str(division_id)+"','"+str(division_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_national=db.executesql(insert_national_sql)
                session.insert_error='Successfully saved!'

        if update_btn:
            update_name=request.vars.division_name
            update_record( nthLevel_id="level0",nth_level_name="level0_name",update_level_id=division_id,update_level_data=update_name)
        if delete_btn:
            item_id = request.vars.item_id
            delete_record(depth=depth,level_id=division_id,item_id=item_id)

        # get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='0'  GROUP BY level0;"
        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and depth=0 GROUP BY level0;"
        # return get_level_list_sql
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,zone_id='',zone_name='',area_id='',area_name='',territory_id='',territory_name='')
    elif depth == 1:
        parent_id= request.vars.division_id
        parent_name= request.vars.division_name

        if submit_btn:
            
            if zone_id == '' or zone_id == 'None' or zone_id==None:
               session.insert_error='Please enter the Zone ID!'
            elif zone_name == '' or zone_name == 'None' or zone_name==None:
               session.insert_error='Please enter the Zone Name!'
            elif check_level_id(zone_id) == True:
                session.insert_error='Level id already exists!'
            else:
                insert_nat_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,level1,level1_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(parent_id)+"','"+str(parent_name)+"','0','1','"+str(parent_id)+"','"+str(parent_name)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_nat=db.executesql(insert_nat_sql)
                session.insert_error='Successfully saved!'
                   

        if update_btn:
            update_name=request.vars.zone_name
            update_record( nthLevel_id="level1",nth_level_name="level1_name",update_level_id=zone_id,update_level_data=update_name)
        if delete_btn:
            delete_id= request.vars.zone_id
            item_id = request.vars.item_id
            delete_record(depth=depth,level_id=delete_id,item_id=item_id)  

        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='"+str(parent_id)+"'  GROUP BY level1,level0;"
        # return get_level_list_sql
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name)
    elif depth == 2:
        parent_id= request.vars.zone_id
        parent_name= request.vars.zone_name

        if submit_btn:
            
            if area_id == '' or area_id == 'None' or area_id==None:
                session.insert_error='Please enter the Area ID!'
            elif area_name == '' or area_name == 'None' or area_name==None:
                session.insert_error='Please enter the Area Name!'
            elif check_level_id(area_id) == True:
               session.insert_error='Level id already exists!'
            else:
                insert_nat_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,level1,level1_name,level2,level2_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(parent_id)+"','"+str(parent_name)+"','0','2','"+str(division_id)+"','"+str(division_name)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_nat=db.executesql(insert_nat_sql)
                session.insert_error='Successfully saved!'

        if update_btn:
            update_name=request.vars.area_name
            update_record( nthLevel_id="level2",nth_level_name="level2_name",update_level_id=area_id,update_level_data=update_name)
        if delete_btn:
            delete_id=request.vars.area_id
            item_id = request.vars.item_id
            delete_record(depth=depth,level_id=delete_id,item_id=item_id)

        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level2,level1,level0;"
        # return get_level_list_sql
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,zone_id=zone_id,zone_name=zone_name,area_id=area_id,area_name=area_name,territory_id='',territory_name='')
    
    elif depth == 3:
        parent_id= request.vars.area_id
        parent_name= request.vars.area_name
        
        if submit_btn:
            
            if territory_id == '' or territory_id == 'None' or territory_id==None:
               session.insert_error='Please enter the Territory ID!'
            elif territory_name == '' or territory_name == 'None' or territory_name==None:
                session.insert_error='Please enter the Territory Name!'
            elif check_level_id(territory_id) == True:
                session.insert_error='Level id already exists!'
            else:
                insert_nat_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,level1,level1_name,level2,level2_name,level3,level3_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(parent_id)+"','"+str(parent_name)+"','1','3','"+str(division_id)+"','"+str(division_name)+"','"+str(zone_id)+"','"+str(zone_name)+"','"+str(area_id)+"','"+str(area_name)+"','"+str(territory_id)+"','"+str(territory_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_nat=db.executesql(insert_nat_sql)
                session.insert_error='Successfully saved!'

        if update_btn:
            update_data=request.vars.territory_name
            update_record( nthLevel_id="level3",nth_level_name="level3_name",update_level_id=territory_id,update_level_data=update_data)
        if delete_btn:
            item_id = request.vars.item_id
            delete_record(depth=depth,level_id=territory_id,item_id=item_id)

        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level3, level2,level1,level0;"
        # return get_level_list_sql
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,division_id=division_id,division_name=division_name,zone_id=zone_id,zone_name=zone_name,area_id=area_id,area_name=area_name,territory_id=territory_id,territory_name=territory_name)
        
    
def update_record( nthLevel_id,nth_level_name,update_level_id, update_level_data):
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    item_id = request.vars.item_id
    update_level_sql = f"""
        UPDATE sm_level SET
            parent_level_name = CASE WHEN parent_level_id = "{update_level_id}" THEN "{update_level_data}" ELSE parent_level_name END,
            level_name = CASE WHEN level_id = "{update_level_id}" THEN "{update_level_data}" ELSE level_name END,
            {nth_level_name} = CASE WHEN {nthLevel_id} = "{update_level_id}" THEN "{update_level_data}" ELSE {nth_level_name} END
        WHERE
            parent_level_id = "{update_level_id}"
            OR level_id = "{update_level_id}"
            OR {nthLevel_id} = "{update_level_id}";
    """
    db.executesql(update_level_sql)
    session.update_delete_error = 'Update Successfully!'

def delete_record(depth,level_id,item_id):
    child_level = check_child_level(depth=depth,parent_id=level_id)
    if child_level:
       session.update_delete_error='Delete child level first !'
    else:
        delete_level_sql = "DELETE FROM sm_level WHERE id = '"+str(item_id)+"' ;"
        db.executesql(delete_level_sql)
        session.update_delete_error='Delete Successfully!'
        
def check_level_id(level_id):
    c_id=session.cid
    level_id_sql="SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and level_id='"+str(level_id)+"' ;"
    # return level_id_sql
    level_id_records=db.executesql(level_id_sql, as_dict=True)
    if len(level_id_records)>0:
        return True
    else:
        return False
    
def check_child_level(depth,parent_id):
    depth = depth + 1
    c_id=session.cid
    level_id_sql="SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and depth = '"+str(depth)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level2,level1,level0;"
    level_id_records=db.executesql(level_id_sql, as_dict=True)
    if len(level_id_records)>0:
        return True
    else:
        return False


def get_level_list():
    resStr = ''
    cid = session.cid
    rows = db(db.sm_level.cid == cid).select(db.sm_level.level_id, db.sm_level.level_name, orderby=db.sm_level.level_name)
    # return db._lastsql
    for row in rows:
        level_id = str(row.level_id)
        name = str(row.level_name).replace('|', ' ').replace(',', ' ')
        # return level_id
        if resStr == '':
            resStr = level_id + '|' + name
        else:
            resStr += ',' + level_id + '|' + name
            
    return resStr

def download_level():
    c_id=session.cid
    records=''
    myString='Area Structure\n\n'
    myString+= 'Division,Zone,Area,Territory\n'

    download_sql = "select * from sm_level where cid = '"+c_id+"' group by level0,level1,level2,level3 order by level0,level1,level2,level3;"
    download_records = db.executesql(download_sql, as_dict=True)

        
    for i in range(len(download_records)):
        levelData=download_records[i]
        level_id=levelData['level_id']
        level_name=levelData['level_name']
        parent_level_id=levelData['parent_level_id']
        
        if (parent_level_id=='0'):    
            myString+=str(level_name)+'-'+str(level_id)+'\n'
        elif (parent_level_id==levelData['level0']):    
            myString+=','+str(level_name)+'-'+str(level_id)+'\n'

        elif (parent_level_id==levelData['level1']):    
            myString+=',,'+str(level_name)+'-'+str(level_id)+'\n'
    
        elif (parent_level_id==levelData['level2']):    
            myString+=',,,'+str(level_name)+'-'+str(level_id)+'\n'                       
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_level.csv'   
    return str(myString)



def download_level_classic():
    c_id=session.cid
    records=''
    maxDepth = 0
    myString='Area Structure\n\n'
    myString+='Division Name,Division ID,Zone Name,Zone ID,Area Name,Area ID,Territory Name, Territory ID\n'
    
    

    download_sql = "select * from sm_level where cid = '"+c_id+"' and depth='3' group by level0,level1,level2,level3 order by level0,level1,level2,level3;"
    download_records = db.executesql(download_sql, as_dict=True)
    
    for i in range(len(download_records)):
        row=download_records[i]
        level_id_0=row['level0']
        level_name_0=row['level0_name']
        level_id_1=row['level1']
        level_name_1=row['level1_name']
        level_id_2=row['level2']
        level_name_2=row['level2_name']
        level_id_3=row['level3']
        level_name_3=row['level3_name']
        
        
        myString+=str(level_name_0)+','+str(level_id_0)+','+str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+'\n'
                                
                                                
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_working_area_classic.csv'   
    return str(myString)