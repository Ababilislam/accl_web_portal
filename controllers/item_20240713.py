import gluon.contenttype

def item_screen():
    response.title = 'Item'

    cid = session.cid
    user_id = session.u_id

    submit_btn = request.vars.submit_btn
    filter_btn = request.vars.filter_item_btn
    all_btn = request.vars.all

    condition = ''
    session.item_id_name = ''
    session.category_id = ''
    session.manufacturer = ''
    session.price = ''
    session.status = ''

    page = request.vars.page_no

    if page == '' or page == 'None' or page == None:
        page = 1

    page_limit = 20
    page_no = int(page)
    start_index = (page_no - 1) * page_limit

    if submit_btn:
        item_id = str(request.vars.item_id_input).upper()
        # name = str(request.vars.item_name_input).upper()
        # pack_size = str(request.vars.pack_size_input)
        pack_size = ''
        des = str(request.vars.desc_input)
        category_id = str(request.vars.cat_id_input).upper()
        category_id_sp = str(request.vars.category_id_sp).upper()
        unit_type = str(request.vars.unit_type_input).upper()
        manufacturer = str(request.vars.manufacturer_input).upper()
        # item_carton = int(request.vars.item_carton_input) if request.vars.item_carton_input else None
        item_carton = 0
        conv_factor = float(request.vars.conv_factor_input) if request.vars.conv_factor_input else None
        price = float(request.vars.price_input) if request.vars.price_input else None
        # dist_price = float(request.vars.dis_price_input) if request.vars.dis_price_input else None
        dist_price = 0.0
        # vat_amt = float(request.vars.vat_amt_input) if request.vars.vat_amt_input else None
        vat_amt = 0.0
        total_amt = 0.0
        status = str(request.vars.status_input).upper()
        field1 = str(request.vars.field1_input).upper()
        # field2 = int(request.vars.field2) if request.vars.field2 else None
        note = str(request.vars.note_input).upper()

        # if (item_id != '' and name != '' and pack_size != '' and des != '' and category_id != '' and unit_type != '' and manufacturer != '' and item_carton > 0 and price > 0.00 and dist_price > 0.00 and vat_amt > 0.00 and status != '' and total_amt > 0 and field1 != '' and note != ''):
        if (item_id != '' and des != '' and category_id != '' and category_id_sp != '' and unit_type != '' and manufacturer != '' and conv_factor > 0.00 and price > 0.00 and status != '' and field1 != '' and note != ''):
            item_check_sql = f"SELECT item_id, name FROM sm_item WHERE cid='ACCL' AND item_id='{str(item_id)}' AND name='{str(des)}';"
            item_check = db.executesql(item_check_sql)

            if len(item_check) != 0:
                response.flash = "This item already exists!"
                
            else:
                insert_item_sql = f"INSERT INTO sm_item (cid, item_id, name, pack_size, des, category_id, category_id_sp, unit_type, manufacturer, item_carton, conv_factor, price, dist_price, vat_amt, total_amt, status, field1, note, created_on, created_by) VALUES ('{cid}','{str(item_id)}','{str(des)}','{str(pack_size)}','{str(des)}','{str(category_id)}','{str(category_id_sp)}','{str(unit_type)}','{str(manufacturer)}','{str(item_carton)}','{str(conv_factor)}','{str(price)}','{str(dist_price)}','{str(vat_amt)}','{str(total_amt)}','{str(status)}','{str(field1)}','{str(note)}','{date_fixed}','{user_id}');"
                db.executesql(insert_item_sql)

                response.flash = "Success"

        else:
            response.flash = "All fields required!"

    if filter_btn:
        item_id = ''
        item_name = ''

        item_id_name = str(request.vars.item_id_name)
        item_id_name_list = item_id_name.strip().split('|')

        if len(item_id_name_list) > 0:
            item_id = item_id_name_list[0]
            if len(item_id_name_list) == 1:
                item_name = item_id_name_list[0].strip()
            else:
                item_name = item_id_name_list[1].strip()
        
        category_id = str(request.vars.category_id)
        manufacturer = str(request.vars.manufacturer)
        price = str(request.vars.price)
        status = str(request.vars.status)

        if session.item_id_name != '' or item_id_name != '':
            condition += f"AND item_id = '{str(item_id)}' OR name like '%{str(item_name)}%'"
            session.item_id_name = item_id_name

        if session.category_id != '' or category_id != '':
            condition += f"AND category_id = '{str(category_id)}'"
            session.category_id = category_id

        if session.manufacturer != '' or manufacturer != '':
            condition += f"AND manufacturer = '{str(manufacturer)}'"
            session.manufacturer = manufacturer

        if session.price != '' or price != '':
            condition += f"AND price = '{str(price)}'"
            session.price = price

        if session.status != '' or status != '':
            condition += f"AND status = '{str(status)}'"
            session.status = status
    
        session.condition = condition


    if all_btn:
        condition =''
        session.item_id_name=''
        session.category_id=''
        session.manufacturer=''
        session.price=''
        session.status=''
        session.condition = condition

    if session.condition == '' or session.condition == 'None' or session.condition == None:
        all_item_sql = f"SELECT * FROM sm_item WHERE cid='ACCL' LIMIT {start_index}, {page_limit};"
    else:
        all_item_sql = f"SELECT * FROM sm_item WHERE cid='ACCL' {session.condition} LIMIT {start_index}, {page_limit};"


    item_rec = db.executesql(all_item_sql, as_dict=True)

    session.condition = condition

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_item WHERE cid='ACCL' {session.condition} ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']
    
    return dict(total = total_rec, item_records = item_rec, page = page)
   

def item_download():
    cid = session.cid
    condition = session.condition

    item_record_sql = f"SELECT * FROM sm_item WHERE cid='{str(cid)}' {condition}"
    item_record = db.executesql(item_record_sql, as_dict=True)

    myString = 'ITEM LIST\n\n'
    myString += 'Item ID,Name,Pack Size,Description,Product Category,Product Class,Product Type,Brand,Item Carton,Price,Dist. Price,VAT Amount,Total Amount,Status,Tax,Origin\n'

    for i in range(len(item_record)):
        item = item_record[i]
        item_id = str(item["item_id"])
        name = str(item["name"])
        pack_size = str(item["pack_size"])
        des = str(item["des"])
        category_id = str(item["category_id"])
        category_id_sp = str(item["category_id_sp"])
        unit_type = str(item["unit_type"])
        manufacturer = str(item["manufacturer"])
        item_carton = str(item["item_carton"])
        price = str(item["price"])
        dist_price = str(item["dist_price"])
        vat_amt = str(item["vat_amt"])
        total_amt = str(item["total_amt"])
        status = str(item["status"])
        field1 = str(item["field1"])
        field2 = str(item["field2"])
        note = str(item["note"])
        # created_on = str(item["created_on"])
        # created_by = str(item["created_by"])
        # updated_on = str(item["updated_on"])
        # updated_by = str(item["updated_by"])

        myString += str(item_id)+','+str(name)+','+str(pack_size)+','+str(des)+','+str(category_id)+','+str(category_id_sp)+',' +str(unit_type)+','+str(manufacturer)+','+str(item_carton)+','+str(price)+','+str(dist_price)+','+str(vat_amt)+','+str(total_amt)+','+str(status)+','+str(field1)+',' +str(note)+'\n'   
    
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=Download_Item_List.csv'

    return str(myString)


def item_edit():
    user_id = session.u_id

    item_id = str(request.args(0)).strip()
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_item_record_sql = f"SELECT * FROM sm_item WHERE item_id = '{item_id}' GROUP BY item_id LIMIT 1;"
    selected_item_record = db.executesql(select_item_record_sql, as_dict = True)

    if len(selected_item_record) != 0 :
        for i in range(len(selected_item_record)):
            item = selected_item_record[i]
            item_id = str(item["item_id"])
            name = str(item["name"])
            pack_size = str(item["pack_size"])
            des = str(item["des"])
            category_id = str(item["category_id"])
            category_id_sp = str(item["category_id_sp"])
            unit_type = str(item["unit_type"])
            manufacturer = str(item["manufacturer"])
            item_carton = str(item["item_carton"])
            conv_factor = str(item["conv_factor"])
            price = str(item["price"])
            dist_price = str(item["dist_price"])
            vat_amt = str(item["vat_amt"])
            total_amt = str(item["total_amt"])
            status = str(item["status"])
            field1 = str(item["field1"])
            field2 = str(item["field2"])
            note = str(item["note"])
    
    if update_btn:
        item_id_up = str(request.vars.item_id_input)
        name_up = str(request.vars.item_name_input)
        pack_size_up = str(request.vars.pack_size_input)
        des_up = str(request.vars.desc_input)
        category_id_up = str(request.vars.cat_id_input)
        category_id_sp_up = str(request.vars.cat_id_sp_input)
        unit_type_up = str(request.vars.unit_type_input)
        manufacturer_up = str(request.vars.manufacturer_input)
        item_carton_up = int(request.vars.item_carton_input) if request.vars.item_carton_input else None
        conv_factor_up = float(request.vars.conv_factor_input) if request.vars.conv_factor_input else None
        price_up = float(request.vars.price_input) if request.vars.price_input else None
        dist_price_up = float(request.vars.dis_price_input) if request.vars.dis_price_input else None
        vat_amt_up = float(request.vars.vat_amt_input) if request.vars.vat_amt_input else None
        total_amt_up = float(request.vars.total_amt_input) if request.vars.total_amt_input else None
        status_up = str(request.vars.status_input)
        field1_up = str(request.vars.field1_input)
        field2_up = int(request.vars.field2_input) if request.vars.field2_input else None
        note_up = str(request.vars.note_input)

        update_sql = f"UPDATE sm_item SET item_id = '{str(item_id_up)}', name = '{str(name_up)}',  pack_size = '{str(pack_size_up)}', des = '{str(des_up)}', category_id = '{str(category_id_up)}', category_id_sp = '{str(category_id_sp_up)}', unit_type = '{str(unit_type_up)}', manufacturer = '{str(manufacturer_up)}', item_carton = '{str(item_carton_up)}', conv_factor = '{str(conv_factor_up)}', price = '{str(price_up)}', dist_price = '{str(dist_price_up)}', vat_amt = '{str(vat_amt_up)}', total_amt = '{str(total_amt_up)}', status = '{str(status_up)}', field1 = '{str(field1_up)}', field2 = '{str(field2_up)}', note = '{str(note_up)}', updated_on = '{date_fixed}', updated_by = '{user_id}' WHERE item_id = '{str(item_id)}' LIMIT 1;"
        db.executesql(update_sql)

        session.flash = 'Update Successfully!'

        redirect(URL('item','item_screen'))

    if delete_btn:
        delete_sql = f"DELETE FROM sm_item WHERE item_id='{item_id}' LIMIT 1;"
        db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('item','item_screen'))
            
    return dict(item_id=item_id,name=name,pack_size=pack_size,des=des,category_id=category_id,category_id_sp=category_id_sp,unit_type=unit_type,manufacturer=manufacturer,item_carton=item_carton,price=price,dist_price=dist_price,vat_amt=vat_amt,total_amt=total_amt,status=status,field1=field1,field2=field2, note=note, conv_factor=conv_factor)


def get_all_item_list():
    retStr = ''
    cid = session.cid
    # rows = db(db.sm_item.cid == cid).select(db.sm_item.item_id, db.sm_item.name, orderby=db.sm_item.name)
    
    sql_query = "SELECT si.item_id, si.name from sm_item as si where si.cid = '"+str(cid)+"' order by si.name"

    # print('get_all_item_list: sql_query: ', sql_query)
    rows = db.executesql(sql_query, as_dict = True)

    # print('rows: ',len(rows))

    for idx in range(len(rows)):
        # item_id = str(row.item_id)
        # name = str(row.name).replace('|', ' ').replace(',', ' ')
        item_id = rows[idx]['item_id']
        name = rows[idx]['name']
        # print(item_id, ' :: ', name)

        if retStr == '':
            retStr = item_id + '|' + name
        else:
            retStr += ',' + item_id + '|' + name

    return retStr

