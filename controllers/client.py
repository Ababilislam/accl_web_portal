 

def client():

    submit_btn = request.vars.submit
    filter_btn = request.vars.btn_filter_item
    all_btn=request.vars.all
    go_to_button = request.vars.go_to_btn
    condition=''
    _id = request.args(0)




    if len(request.args):
        page_Number = int(request.args[0])
        # return page
    else:
        page_Number = 0

    item_per_page = 20

    if page_Number is not None and item_per_page is not None:

        # limit_by = ((page_Number + 1) * item_per_page , item_per_page )
        limit_by = (page_Number * item_per_page, (page_Number + 1) * item_per_page + 1)

    # page_Number = request.args(0)
    # return page_Number
    page_Num = request.vars.page_num
    go_to_button = request.vars.go_to_btn
    # item_per_page = 10
    # limit_by = 0,15
    if go_to_button:
        # session.p_condition = p_condition
        try:
            page_Number = int(page_Num)
        except ValueError:
            return "Invalid page number"
        if page_Number is not None and item_per_page is not None:
            # limit_by = ((page_Number + 1) * item_per_page , item_per_page )
            limit_by = (page_Number * item_per_page, (page_Number + 1) * item_per_page + 1)

    session.page_Number = page_Number

  

    if submit_btn:
        item_id = str(request.vars.item_id)
        name = str(request.vars.name)
        pack_size = str(request.vars.pack_size)
        des = str(request.vars.des)
        category_id = str(request.vars.category_id)
        category_id_sp = str(request.vars.category_id_sp)
        unit_type = str(request.vars.unit_type)
        manufacturer = str(request.vars.manufacturer)
        item_carton = int(request.vars.item_carton) if request.vars.item_carton else None
        price = float(request.vars.price) if request.vars.price else None
        dist_price = float(request.vars.dist_price) if request.vars.dist_price else None
        vat_amt = float(request.vars.vat_amt) if request.vars.vat_amt else None
        total_amt = float(request.vars.total_amt) if request.vars.total_amt else None
        status = str(request.vars.status)
        field1 = str(request.vars.field1)
        field2 = int(request.vars.field2) if request.vars.field2 else None
        note = str(request.vars.note)
        created_by = "Test"
        updated_by = "Test"

        if (
            item_id != ""
            and name != ""
            and pack_size != ""
            and des != ""
            and category_id != ""
            and category_id_sp != ""
            and unit_type != ""
            and manufacturer != ""
            and item_carton > 0
            and price > 0.00
            and dist_price > 0.00
            and vat_amt > 0.00
            and status != ""
            and total_amt > 0
            and field1 != ""
            and field2 > 0
        ):
            check_inserted_sql = (
                "select item_id,name from sm_client where cid='ACCL' and item_id='"
                + str(item_id)
                + "' and name='"
                + str(name)
                + "';"
            )
            checkItemsRows = db.executesql(check_inserted_sql)
            if len(checkItemsRows) > 0:
                response.flash = "This Item Already Exists !"
            else:
                insert_sql = (
                    "INSERT INTO sm_client (cid,item_id,name,pack_size,des,category_id,category_id_sp,"
                    "unit_type,manufacturer,item_carton,price,dist_price,vat_amt,total_amt,status,field1,"
                    "field2,note) VALUES('ACCL','"
                    + str(item_id)
                    + "','"
                    + str(name)
                    + "','"
                    + str(pack_size)
                    + "','"
                    + str(des)
                    + "','"
                    + str(category_id)
                    + "','"
                    + str(category_id_sp)
                    + "','"
                    + str(unit_type)
                    + "','"
                    + str(manufacturer)
                    + "','"
                    +str(item_carton)
                    +"','"
                    +str(price)+"','"+str(dist_price)+"','"+str(vat_amt)+"','"+str(total_amt)+"','"+str(status)+"','"+str(field1)+"','"+str(field2)+"','"+str(note)+"');"
                )
                insertdb = db.executesql(insert_sql)
                # return insert_sql
                response.flash = "Success"
    if filter_btn:
      
        item_id_name = str(request.vars.item_id_name)
        category_id = str(request.vars.category_id)
        manufacturer = str(request.vars.manufacturer)
        price = str(request.vars.price)
        status = str(request.vars.status)
        if session.item_id_name!='' or item_id_name !='':
            condition+="and item_id= '"+str(item_id_name)+"'"
            session.item_id_name = item_id_name

        if session.category_id !='' or category_id!='':
            condition+="and category_id= '"+str(category_id)+"'"
            session.category_id = category_id

        if session.manufacturer !='' or manufacturer!='':
            condition+="and manufacturer = '"+str(manufacturer)+"'"
            session.manufacturer = manufacturer

        if session.price !='' or price !='':
            condition+="and price = '"+str(price)+"'"
            session.price = price

        if session.status !='' or status !='':
            
            condition+="and status = '"+str(status)+"'"
            session.status = status
    if all_btn:
        condition =''
        session.item_id_name=''
        session.category_id=''
        session.manufacturer=''
        session.price=''
        session.status=''
        
    if session.condition=='' and session.condition!=None and session.condition!='None':

        allClient="SELECT * FROM sm_client WHERE cid='ACCL' limit %d, %d;" % limit_by
    else:

        allClient="SELECT * FROM sm_client WHERE cid='ACCL' "+condition+" limit %d, %d;" % limit_by



    clientRow = db.executesql(allClient, as_dict=True)
    # return allClient
    totalrecordSql="SELECT count(id) as total from sm_client  WHERE cid='ACCL' "+condition+" order by id;";
    total_record = db.executesql(totalrecordSql,as_dict = True)
   
   	# return totalrecordSql

    session.condition = condition
    for i in range(len(clientRow)):
        clients=clientRow[i]
        _id=str(clients["id"])
        cid=str(clients["cid"])
        client_id=str(clients["client_id"])
        client_old_id=str(clients["client_old_id"])
        name=str(clients["name"])
        status=str(clients["status"])
        address=str(clients["address"])
        depot_name=str(clients["depot_name"])
        store_name=str(clients["store_name"])
        depot_belt_name=str(clients["depot_belt_name"])
        category_name=str(clients["category_name"])
        market_name=str(clients["market_name"])
        thana=str(clients["thana"])
        district=str(clients["district"])
        note=str(clients["note"])
        # return name,status
		
		
		
		
		
		
		
		
		
		
    # return client_id,client_old_id,name
    return dict(allClient=clientRow,total = "50",page_Number=page_Number, item_per_page = item_per_page)
    # return dict(total = "50",page_Number=page_Number, item_per_page = item_per_page)
		
	
	
	
    
    
   

def item_downdoad():
    cid='ACCL'
    clientRows_sql = "select * from poi WHERE cid='"+str(cid)+"' "+ session.condition+"  "
    records = db.executesql(clientRows_sql, as_dict=True)
    myString = 'POI List\n\n'
    myString += ' item_id, name, pack_size, des, category_id, category_id_sp,unit_type, manufacturer, item_carton, price, dist_price,vat_amt,total_amt,status,field1,field2,note, created_on,created_by,updated_on,updated_by \n'
    for i in range(len(records)):

        index=i
        items=allClient[i]
        #id=str(items["id"])
        #cid=str(items["cid"])
        item_id=str(items["item_id"])
        name=str(items["name"])
        pack_size=str(items["pack_size"])
        des=str(items["des"])
        category_id=str(items["category_id"])
        category_id_sp=str(items["category_id_sp"])
        unit_type=str(items["unit_type"])
        manufacturer=str(items["manufacturer"])
        item_carton=str(items["item_carton"])
        price=str(items["price"])
        dist_price=str(items["dist_price"])
        vat_amt=str(items["vat_amt"])
        total_amt=str(items["total_amt"])
        status=str(items["status"])
        field1=str(items["field1"])
        field2=str(items["field2"])
        note=str(items["note"])
        created_on=str(items["created_on"])
        created_by=str(items["created_by"])
        updated_on=str(items["updated_on"])
        updated_by=str(items["updated_by"])
        myString +=str(item_id)+','+str(name)+','+str(pack_size)+','+str(des)+','+str(category_id)+','+str(category_id_sp)+',' +str(unit_type)+','+str(manufacturer)+','+str(item_carton)+','+str(price)+','+str(dist_price)+','+str(vat_amt)+','+str(total_amt)+','+str(status)+','+str(field1)+','+str(field2)+',' +str(note)+',' +str(created_on)+','+str(created_by)+',' +str(updated_on)+',' +str(updated_by)+','    
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Download_Item_List.csv'
    return str(myString)

def item_edit():
    # _id = request.args(0)
    item_id = str(request.args(0)).strip()
    # return item_id
    update_btn=request.vars.update_btn
    delete_btn=request.vars.delete

    
    select_item_record_sql = "SELECT * From sm_client WHERE item_id = '"+item_id+"' group by item_id limit 1 ;"
    # return select_item_record_sql
    select_item_record = db.executesql(select_item_record_sql, as_dict = True)
    if len(select_item_record) > 0 :
        for i in range(len(select_item_record)):
            items = select_item_record[i]
            item_id=str(items["item_id"])
            name=str(items["name"])
            pack_size=str(items["pack_size"])
            des=str(items["des"])
            category_id=str(items["category_id"])
            category_id_sp=str(items["category_id_sp"])
            unit_type=str(items["unit_type"])
            manufacturer=str(items["manufacturer"])
            item_carton=str(items["item_carton"])
            price=str(items["price"])
            dist_price=str(items["dist_price"])
            vat_amt=str(items["vat_amt"])
            total_amt=str(items["total_amt"])
            status=str(items["status"])
            field1=str(items["field1"])
            field2=str(items["field2"])
            note=str(items["note"])
    
    if update_btn == 'Update':
        # return 'click'
        item_ID = str(request.vars.item_ID)
        name = str(request.vars.item_name)
        # return name
        pack_size = str(request.vars.pack_size)
        des = str(request.vars.des)
        category_id = str(request.vars.category_id)
        category_id_sp = str(request.vars.category_id_sp)
        unit_type = str(request.vars.unit_type)
        manufacturer = str(request.vars.manufacturer)
        item_carton = int(request.vars.item_carton) if request.vars.item_carton else None
        price = float(request.vars.price) if request.vars.price else None
        dist_price = float(request.vars.dist_price) if request.vars.dist_price else None
        vat_amt = float(request.vars.vat_amt) if request.vars.vat_amt else None
        total_amt = float(request.vars.total_amt) if request.vars.total_amt else None
        status = str(request.vars.status)
        field1 = str(request.vars.field1)
        field2 = int(request.vars.field2) if request.vars.field2 else None
        note = str(request.vars.note)
        created_by = "Test"
        updated_by = "Test"
        # return 'click'
        update_sql="update sm_client Set item_id='"+str(item_ID)+"',name='"+str(name)+"',pack_size='"+str(pack_size)+"',des='"+str(des)+"',category_id='"+str(category_id)+"',category_id_sp='"+str(category_id_sp)+"',unit_type='"+str(unit_type)+"',manufacturer='"+str(manufacturer)+"',item_carton='"+str(item_carton)+"',price='"+str(price)+"',dist_price='"+str(dist_price)+"',vat_amt='"+str(vat_amt)+"',total_amt='"+str(total_amt)+"',status='"+str(status)+"',field1='"+str(field1)+"',field2='"+str(field2)+"',note='"+str(note)+"' WHERE item_id='"+str(item_id)+"' limit 1;"
        # return locals()
        # return update_sql
        db.executesql(update_sql)
        session.flash='Update Success'
        redirect(URL('item','item_screen'))
    if delete_btn:
        delete_sql="Delete from sm_client WHERE item_id='"+item_id+"'limit 1"
        delete=db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect (URL('item','item_screen'))


            
    return dict(_id=id,item_id=item_id,name=name,pack_size=pack_size,des=des,category_id=category_id,category_id_sp=category_id_sp,unit_type=unit_type,manufacturer=manufacturer,item_carton=item_carton,price=price,dist_price=dist_price,vat_amt=vat_amt,total_amt=total_amt,status=status,field1=field1,field2=field2, note=note)