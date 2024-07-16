def item_batch_upload():
    response.title = 'Item Batch Upload'

    btn_upload = request.vars.upload_btn

    cid = session.cid
    user_id = session.u_id

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
            
            if len(column_list) != 14:
                error_data = row_data + '(14 columns needed in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:
                item_id = str(column_list[0]).strip().upper()
                name = str(column_list[1]).strip().upper()
                pack_size = str(column_list[2]).strip().upper()
                item_desc = str(column_list[3]).strip().upper()
                category_id = str(column_list[4]).strip().upper()
                category_id_sp = str(column_list[5]).strip().upper()
                unit_type= str(column_list[6]).strip().upper()
                manufacturer = str(column_list[7]).strip().upper()
                item_carton = str(column_list[8]).strip().upper()
                price = str(column_list[9]).strip().upper()
                dist_price = str(column_list[10]).strip().upper()
                vat_amt = str(column_list[11]).strip().upper()
                total_amt = str(column_list[12]).strip().upper()
                status = str(column_list[13]).strip().upper()
                                               
                if (item_id == '' or item_id == 'NONE') or (name == '' or name == 'None'):
                    error_data = row_data + '(Item ID/Name required)\n'
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
                            item_data_insert_sql = f"INSERT INTO sm_item (cid, item_id, name, pack_size, des, category_id, category_id_sp, unit_type, manufacturer, item_carton, price, dist_price, vat_amt, total_amt, status, created_on, created_by) VALUES ('{cid}','{item_id}','{name}','{pack_size}','{item_desc}','{category_id}','{category_id_sp}','{unit_type}','{manufacturer}','{item_carton}','{price}','{dist_price}','{vat_amt}','{total_amt}','{status}','{date_fixed}','{user_id}');"
                            db.executesql(item_data_insert_sql)

                            count_inserted += 1

                        except Exception as e:
                            error_str = 'Please do not insert special characters.'
                        
        if error_str == '':
            error_str = 'Uploaded!'
    
    return dict(count_inserted = count_inserted, count_error = count_error, error_str = error_str, total_row = total_row)
