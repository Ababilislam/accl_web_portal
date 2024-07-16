
import urllib.parse, random, string

def index():
    select_color = "SELECT * From colors WHERE cid = 'ACCL' group by cid limit 1 ;"
    item_record = db.executesql(select_color, as_dict = True)

    if len(item_record)>0:
        for i in range(len(item_record)):
            items = item_record[i]
            session.cid =str(items["cid"])
            session.bg_color=str(items["bg_color"])
            session.layout_color=str(items["layout_color"])
            session.button_color=str(items["button_color"])
            session.button_text_color=str(items["button_text_color"])
            session.heading_text=str(items["heading_text"])
            session.text_color  =str(items["text_color"])
    return dict()

   
def login():
    c_id=str(request.vars.c_id).strip().upper()
    u_id = str(request.vars.u_id).strip().upper()
    u_pass = str(request.vars.u_pass).strip()
    
    redirect(URL(c='default', f='check_user', vars=dict(c_id=c_id, uid=u_id, u_pass=u_pass)))


def check_user():
    
    c_id=str(request.vars.c_id).strip().upper()
    u_id = str(request.vars.uid).strip().upper()
    u_pass = str(request.vars.u_pass).strip()

    
    if (u_id=='' or u_pass==''):
        session.flash = 'User ID and Password required !'
        redirect(URL('index'))
        
    else:         
        session.cid = c_id
        session.user_id = u_id
        mac_address='-'
        hdd_address='-'
        ip_address='-'
        access_module='RetailerMapping'
        http_pass=''
        mreporting_http_pass = 'abC321'
        http_pass = mreporting_http_pass

        user_type = ''
        name = ''
        # check_user_type_sql = "SELECT * FROM sm_rep where cid = '"+c_id+"' and rep_id = '"+str(u_id)+"' group by rep_id limit 1 ;"
        check_user_type_sql = "SELECT * FROM sm_rep where cid = '"+c_id+"' and rep_id = '"+str(u_id)+"' and password = '"+str(u_pass)+"' group by rep_id limit 1 ;"
        check_user_type = db.executesql(check_user_type_sql, as_dict = True)
        if len(check_user_type):
            for u in range(len(check_user_type)):
                user_records = check_user_type[u]
                user_type = user_records['user_type']
                name = user_records['name']

        else:
            session.error_flash = 'Invalid User !'
            redirect(URL('index'))

        session.user_type = user_type
        session.name = name
        # return session.user_type
        # return access_module
        userText = str(c_id).strip() + '<url>' + str(u_id).strip() + '<url>' + str(u_pass).strip() + '<url>' + str(mac_address) + '<url>' + str(hdd_address).strip() + '<url>' + str(ip_address).strip() + '<url>' + str(http_pass).strip() + '<url>' + str(access_module).strip()
        # userText = str(c_id).strip() + '<url>' + str(u_id).strip() + '<url>' + str(u_pass).strip()
        
        # return userText
        request_text = urllib.parse.quote(userText)
        # return request_text
        
        url = 'http://ww11.yeapps.com/cpanelmrep/login_permission/check_login?login_data=' + request_text
        redirect(URL('home'));
    #     try:
    #         result = fetch(url)
    #         # return result
            
    #         # return url
    #         #STARTsuccess<fd>SKF<fd>ADMIN<fd>Admin<fd>6<fd>1<fd>1<fd>rm_client_cat_manage,rm_client_manage,rm_depot_manage,rm_depot_payment_manage,rm_depot_setting_manage,rm_depot_type_manage,rm_depot_user_manage,rm_device_manage,rm_doctor_manage,rm_ff_target_manage,rm_item_cat_unit_manage,rm_item_manage,rm_reparea_manage,rm_report_process_manage,rm_rep_manage,rm_requisition_view,rm_stock_damage_view,rm_stock_issue_view,rm_stock_receive_view,rm_sup_manage,rm_tpcp_rules_manage,rm_utility_manage,rm_visit_manage,rm_workingarea_manage,rm_client_payment_view,rm_invoice_view,rm_campaign_manage,rm_delivery_man_manage,rm_analysis_view,rm_doctor_visit_manage,rm_credit_policy_manage,rm_stock_trans_dispute_view,rm_depot_belt_manage,rm_depot_market_manage,rm_doctor_visit_view,rm_item_batch_manage,rm_stock_transfer_view<fd>Transcom Distribution Company Ltd.<compfdsep>1234<compfdsep>tdclmohakhali@transcombd.com<compfdsep>Sadar Road, Mohakhali, Dhaka. Ph: 9896479,9862763, 8855371-80 Ext:258 Fax:8860325<compfdsep>Dhaka<compfdsep>Bangladesh<compfdsep>1200<compfdsep><fd>NOEND
    #         #STARTsuccess<fd>SKF<fd>SAVAR<fd>Depot<fd>6<fd>1<fd>1<fd>rm_client_manage,rm_client_payment_manage,rm_depot_payment_manage,rm_doctor_view,rm_doctor_visit_view,rm_item_view,rm_reparea_view,rm_rep_view,rm_requisition_manage,rm_stock_damage_manage,rm_stock_issue_manage,rm_tpcp_rules_view,rm_visit_list_view,rm_stock_receive_view,rm_invoice_manage,rm_print_manager_view,rm_stock_receive_manage,rm_stock_trans_dispute_manage,rm_delivery_man_view,rm_analysis_view,rm_sup_view,rm_depot_market_manage,rm_depot_belt_manage,rm_item_batch_manage,rm_stock_transfer_manage,rm_campaign_view,rm_credit_policy_view,rm_workingarea_view,rm_ff_target_view<fd>Transcom Distribution Company Ltd.<compfdsep>1234<compfdsep>tdclmohakhali@transcombd.com<compfdsep>Sadar Road, Mohakhali, Dhaka. Ph: 9896479,9862763, 8855371-80 Ext:258 Fax:8860325<compfdsep>Dhaka<compfdsep>Bangladesh<compfdsep>1200<compfdsep><fd>NOEND
    #     except:
    #         session.flash = 'Connection Time out. Please try again after few minutes.'
    #         redirect(URL('index'))
            
    #     if (str(result).find('START') == (-1) or str(result).find('END') == (-1)):
    #         session.flash = 'Communication error'
    #         redirect(URL('index'))
    #     else:
    #         myDecReslutStr = str(result)[7:-3]
    #         separator = '<fd>'
    #         urlList = myDecReslutStr.split(separator, myDecReslutStr.count(separator))
    #         if len(urlList) == 2:  # Failed
    #             myDecReslutStr = urlList[0]
                
    # if myDecReslutStr != 'failed':
    #     separator = '<fd>'
    #     sepCount = myDecReslutStr.count(separator)        
    #     urlList = myDecReslutStr.split(separator, sepCount)
        
    #     if len(urlList) >= 10:
    #         myRes = urlList[0];
    #         # return myRess
    #         if myRes == 'success':
    #             redirect(URL('home'));

    #     else:
    #         return "Password is Wrong"

  
 
def home():
    response.title = 'ACCL'
    return dict()


def logout():
    session.clear()

    redirect(URL(c='default',f='index'))



# def loginHome():
    
#     # cid = str(request.vars.cid).strip().upper()
#     username = str(request.vars.username).strip()
#     password = str(request.vars.password).strip()
#     # mac_hdd = str(request.vars.uploadkey)
#     return username, password 
#     session.cid = cid
#       userText = str(cid).strip() + '<url>' + str(uid).strip() + '<url>' + str(password).strip() + '<url>' + str(mac_address) + '<url>' + str(hdd_address).strip() + '<url>' + str(ip_address).strip() + '<url>' + str(http_pass).strip() + '<url>' + str(access_module).strip()
#       request_text = urllib.parse.quote(userText)
#       url = 'http://ww11.yeapps.com/cpanelmrep/login_permission/check_login?login_data=' + request_text
#       try:
#             result = fetch(url)
#             # return url 
#       except:
#             session.flash = 'Connection Time out. Please try again after few minutes.'
#             redirect(URL('index'))
#       if (str(result).find('START') == (-1) or str(result).find('END') == (-1)):
#             session.flash = 'Communication error'
#             redirect(URL('index'))
      # else:
      #  return dict()
    
    