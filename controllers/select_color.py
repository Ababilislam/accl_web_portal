def select_color():
    submit=request.vars.Update
    if submit:
        bg_color = str(request.vars.Background_Color)
        Layout_Color = str(request.vars.Layout_Color)
        Button_Color = str(request.vars.Button_Color)
        Button_text_Color = str(request.vars.Button_text_Color)
        Heading_Text_Color = str(request.vars.Heading_Text_Color)
        Text_Color = str(request.vars.Text_Color)
        # if bg_color !=""and bg_color.startswith('#')and Layout_Color !="" and Layout_Color.startswith('#') and Button_Color !="" and Button_Color.startswith('#') and Button_text_Color !="" and Button_text_Color.startswith('#') and  Heading_Text_Color !="" and Heading_Text_Color.startswith('#') and Text_Color !="" and Text_Color.startswith('#'):
        update_sql="update colors Set bg_color='"+str(bg_color)+"',	layout_color='"+str(Layout_Color)+"',button_color='"+str(Button_Color)+"',button_text_color='"+str(Button_text_Color)+"',heading_text='"+str(Heading_Text_Color)+"',text_color='"+str(Text_Color)+"' WHERE cid='ACCL' limit 1;"
        db.executesql(update_sql)
        session.flash='Update Success'
        redirect(URL('default','index'))
        # else:
        #     session.flash='Somethig Worng'
            
        
    
    return dict()