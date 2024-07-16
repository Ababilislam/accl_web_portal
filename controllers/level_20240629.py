from urllib.parse import unquote

def level():
    response.title = 'Area Structure'

    cid = session.cid
    user_id = session.user_id

    add_btn = request.vars.add_btn
    update_btn = request.vars.edit_btn

    division_id = request.vars.div_id_input
    division_name = request.vars.div_name_input

    if add_btn:
        if division_id == '':
            response.flash = 'Enter division ID'
        elif division_name == '':
            response.flash = 'Enter division name'
        else:
            check_level_sql = f"SELECT level0, level0_name FROM sm_level WHERE cid = '{cid}' AND level0 = '{division_id}' AND level0_name = '{division_name}' GROUP BY level0;"
            check_level = db.executesql(check_level_sql, as_dict=True)

            if len(check_level) == 0:
                insert_division_sql = f"INSERT INTO sm_level (cid, level_id, level_name, parent_level_id, parent_level_name, is_leaf, depth, level0, level0_name, created_on, created_by) VALUES ('{cid}','{division_id}','{division_name}','0','','0','{0}','{division_id}','{division_name}','{date_fixed}','{user_id}');"
                db.executesql(insert_division_sql)

    if update_btn:
        div_id = request.args(0, default=None)
        div_name = request.vars.div_name

        update_level_sql = f"UPDATE sm_level SET level0_name = '{div_name}', updated_on = '{date_fixed}', updated_by = '{user_id}' WHERE cid = '{cid}' AND level0 = '{div_id}';"
        db.executesql(update_level_sql)
    
    get_level_list_sql = f"SELECT level0, level0_name FROM sm_level WHERE cid = '{cid}' GROUP BY level0;"
    level_records = db.executesql(get_level_list_sql, as_dict = True)
    
    return dict(level_records = level_records)


def zone():
    response.title = 'Area Structure'

    cid = session.cid
    user_id = session.user_id

    # getting vars from url 
    div_id = request.args(0, default=None)
    div_name = request.args(1, default=None)

    if div_name is not None:
        div_name = unquote(div_name.replace('_', ' '))

    # sending to btn 
    response.div_id = div_id 
    response.div_name = div_name

    # search_btn = request.vars.search_btn
    add_btn = request.vars.add_btn
    # ret_btn = request.vars.return_btn
    # next_btn = request.vars.next_btn
    update_btn = request.vars.edit_btn

    zone_id = request.vars.zone_id_input
    zone_name = request.vars.zone_name_input

    if add_btn:
        if zone_id == '':
            response.flash = 'Please enter the zone ID'
        elif zone_name == '':
            response.flash = 'Please enter the zone name'
        else:
            check_level_sql = f"SELECT level1, level1_name FROM sm_level WHERE cid = '{cid}' AND level1 = '{zone_id}' AND level1_name = '{zone_name}' AND level0 = '{response.div_id}' AND level0_name = '{response.div_name}' GROUP BY level1;"
            check_level = db.executesql(check_level_sql, as_dict=True)

            if len(check_level) > 0:
                response.flash = 'Zone already existing'
            else:
                insert_zone_sql = f"INSERT INTO sm_level (cid, level_id, level_name, parent_level_id, parent_level_name, is_leaf, depth, level0, level0_name, level1, level1_name, created_on, created_by) VALUES ('{cid}','{zone_id}','{zone_name}','{response.div_id}','{response.div_name}','0','{1}','{response.div_id}','{response.div_name}','{zone_id}','{zone_name}','{date_fixed}','{user_id}');"
                db.executesql(insert_zone_sql)

    if update_btn:
        z_id = request.args(0, default=None)
        z_name = request.vars.zone_name

        update_level_sql = f"UPDATE sm_level SET level1_name = '{z_name}', updated_on = '{date_fixed}', updated_by = '{user_id}' WHERE cid = '{cid}' AND level1 = '{z_id}';"
        db.executesql(update_level_sql)
    
    get_level_list_sql = f"SELECT level1, level1_name FROM `sm_level` WHERE cid = '{cid}' AND level0 = '{div_id}' AND level0_name = '{div_name}' GROUP BY level1;"
    level_records = db.executesql(get_level_list_sql, as_dict = True)
    
    return dict(level_records = level_records)


def area():
    response.title = 'Area Structure'

    cid = session.cid
    user_id = session.user_id

    # getting vars from url 
    div_id = request.args(0, default=None)
    div_name = request.args(1, default=None)
    zone_id = request.args(2, default=None)
    zone_name = request.args(3, default=None)

    if div_name is not None:
        div_name = unquote(div_name.replace('_', ' '))

    if zone_name is not None:
        zone_name = unquote(zone_name.replace('_', ' '))

    # sending to btn 
    response.div_id = div_id
    response.div_name = div_name
    response.zone_id = zone_id
    response.zone_name = zone_name

    search_btn = request.vars.search_btn
    add_btn = request.vars.add_btn
    next_btn = request.vars.next_btn
    update_btn = request.vars.edit_btn

    area_id = request.vars.area_id_input
    area_name = request.vars.area_name_input

    if add_btn:
        if area_id == '':
            response.flash = 'Enter zone ID'
        elif area_name == '':
            response.flash = 'Enter zone name'
        else:
            check_level_sql = f"SELECT level2, level2_name FROM sm_level WHERE cid = '{cid}' AND level2 = '{area_id}' AND level2_name = '{area_name}' AND level1 = '{response.zone_id}' AND level1_name = '{response.zone_name}' AND level0 = '{response.div_id}' AND level0_name = '{response.div_name}' GROUP BY level2;"
            check_level = db.executesql(check_level_sql, as_dict=True)

            if len(check_level) > 0:
                response.flash = 'Area already existing'
            else:
                insert_area_sql = f"INSERT INTO sm_level (cid, level_id, level_name, parent_level_id, parent_level_name, is_leaf, depth, level0, level0_name, level1, level1_name, level2, level2_name, created_on, created_by) VALUES ('{cid}','{area_id}','{area_name}','{response.zone_id}','{response.zone_name}','0','{2}','{response.div_id}','{response.div_name}','{response.zone_id}','{response.zone_name}','{area_id}','{area_name}','{date_fixed}','{user_id}');"
                db.executesql(insert_area_sql)

    if update_btn:
        area_id = request.args(0, default=None)
        area_name = request.vars.area_name

        update_level_sql = f"UPDATE sm_level SET level2_name = '{area_name}' WHERE cid = '{cid}' AND level2 = '{area_id}';"
        db.executesql(update_level_sql)

    get_level_list_sql = f"SELECT level2, level2_name FROM sm_level WHERE cid = '{cid}' AND level0 = '{response.div_id}' AND level0_name = '{response.div_name}' AND level1 = '{response.zone_id}' AND level1_name = '{response.zone_name}' GROUP BY level2;"
    level_records = db.executesql(get_level_list_sql, as_dict = True)
    
    return dict(level_records = level_records)

    
def territory():
    response.title = 'Area Structure'
    
    cid = session.cid
    user_id = session.user_id

    # getting vars from url 
    div_id = request.args(0, default=None)
    div_name = request.args(1, default=None)
    zone_id = request.args(2, default=None)
    zone_name = request.args(3, default=None)
    area_id = request.args(4, default=None)
    area_name = request.args(5, default=None)

    if div_name is not None:
        div_name = unquote(div_name.replace('_', ' '))

    if zone_name is not None:
        zone_name = unquote(zone_name.replace('_', ' '))

    if area_name is not None:
        area_name = unquote(area_name.replace('_', ' '))

    # sending to btn 
    response.div_id = div_id
    response.div_name = div_name
    response.zone_id = zone_id
    response.zone_name = zone_name
    response.area_id = area_id
    response.area_name = area_name

    # search_btn = request.vars.search_btn
    add_btn = request.vars.add_btn
    # next_btn = request.vars.next_btn
    # update_btn = request.vars.edit_btn

    territory_id = request.vars.territory_id_input
    territory_name = request.vars.territory_name_input

    if add_btn:
        if territory_id == '':
            response.flash = 'Enter territory ID'
        elif territory_name == '':
            response.flash = 'Enter territory name'
        else:
            check_level_sql = f"SELECT level3, level3_name FROM sm_level WHERE cid = '{cid}' AND level3 = '{territory_id}' AND level3_name = '{territory_name}' AND level2 = '{area_id}' AND level2_name = '{area_name}' AND level1 = '{response.zone_id}' AND level1_name = '{response.zone_name}' AND level0 = '{response.div_id}' AND level0_name = '{response.div_name}' GROUP BY level2;"
            check_level = db.executesql(check_level_sql, as_dict=True)

            if len(check_level) > 0:
                response.flash = 'Territory already exists'
            else:
                insert_territory_sql = f"INSERT INTO sm_level (cid, level_id, level_name, parent_level_id, parent_level_name, is_leaf, depth, level0, level0_name, level1, level1_name, level2, level2_name, level3, level3_name, created_on, created_by) VALUES ('{cid}','{territory_id}','{territory_name}','{response.area_id}','{response.area_name}','1','{3}','{response.div_id}','{response.div_name}','{response.zone_id}','{response.zone_name}','{response.area_id}','{response.area_name}','{territory_id}','{territory_name}','{date_fixed}','{user_id}');"
                db.executesql(insert_territory_sql)

    get_level_list_sql = f"SELECT level3, level3_name FROM `sm_level` WHERE cid = '{cid}' AND level2 = '{area_id}' AND level2_name = '{area_name}' GROUP BY level3;"
    level_records = db.executesql(get_level_list_sql, as_dict = True)
    
    return dict(level_records = level_records)
