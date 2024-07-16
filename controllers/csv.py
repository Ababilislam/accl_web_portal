def item_batch_upload():
    response.title = 'Item Batch Upload'

    btn_upload = request.vars.upload_btn

    cid = session.cid
    user_id = session.user_id
    date = date_fixed


    count_inserted = 0
    count_error = 0
    total_row = 0
    error_str = ''
            
    if btn_upload:        
        excel_data = str(request.vars.excel_data)
        
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
                column_list = row_data.split('\t')
            
            if len(column_list) != 11:
                # return len(column_list)
                error_data = row_data + '(11 columns needed in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:
                item_id = str(column_list[0]).strip().upper()
                name = str(column_list[1]).strip().upper()
                item_desc = str(column_list[1]).strip().upper()
                product_catagory = str(column_list[2]).strip().upper()
                product_class = str(column_list[3]).strip().upper()
                product_type= str(column_list[4]).strip().upper()
                brand = str(column_list[5]).strip().upper()
                conv_factor = str(column_list[6]).strip().upper()
                price = str(column_list[7]).strip().upper()
                status = str(column_list[8]).strip().upper()
                tax = str(column_list[9]).strip().upper()
                origin = str(column_list[10]).strip().upper()
                
                                               
                if ((item_id == '' or item_id == 'NONE') or (name == '' or name == 'None') or (product_catagory =='' or product_catagory==None) or (product_class=='' or product_class==None) or (product_type=='' or product_type==None) or (brand=='' or brand==None)or (conv_factor=='' or conv_factor==None) or (price=='' or price==None) or (status=='' or status==None) or (tax =='' or tax==None) or (origin=='' or origin==None)):
                    error_data = row_data + '(All field required)\n'
                    error_str = error_str + error_data
                    count_error += 1
                    continue

                else:
                    item_check_sql = f"SELECT * FROM sm_item WHERE item_id = '{str(item_id)}' LIMIT 1"
                    item_check = db.executesql(item_check_sql, as_dict = True)

                    if len(item_check) != 0:
                        error_data = row_data + '(Item already exists)\n'
                        error_str = error_str + error_data
                        count_error += 1
                        continue

                    else:
                        try:
                            item_data_insert_sql = f"INSERT INTO sm_item (cid, item_id, name, des, category_id, category_id_sp, unit_type, manufacturer, conv_factor, price, status, field1, note,created_on, created_by) VALUES ('{cid}','{item_id}','{name}','{item_desc}','{product_catagory}','{product_class}','{product_type}','{brand}','{conv_factor}','{price}','{status}','{tax}','{origin}','{date}','{user_id}');"
                            # return item_data_insert_sql
                            db.executesql(item_data_insert_sql)

                            count_inserted += 1

                        except Exception as e:
                            error_str = 'Please do not insert special characters.'
                        
        if error_str == '':
            error_str = 'Uploaded!'
    
    return dict(count_inserted = count_inserted, count_error = count_error, error_str = error_str, total_row = total_row)
