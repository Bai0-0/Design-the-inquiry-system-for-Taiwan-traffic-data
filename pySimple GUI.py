
# %%
import PySimpleGUI as sg

##------------Layout Design--------------

header = ("VehicleType",'DerectionTime_O','Gantry_O','DerectionTime_D','Gantry_D','TripLength',"TripEnd")
vehicle_list = ('5','31','32','41','42')
layout_userPage =[[sg.Text("Please enter your ID and Password:")],
                [sg.Text("User ID  :"), sg.InputText(key = "userID")],
                [sg.Text("Password :"), sg.InputText(key = "pwd", password_char='*')],
                [sg.Button("Login"), sg.Button('Exit')]]



frame_search =sg.Frame(title ='Search',layout =[[sg.Text('Select one column to search:'),sg.Combo(values=header,key='search_col',enable_events = True)],

            [sg.Text('Keyword :')],
            [sg.Listbox(size=(20,12),values = vehicle_list,select_mode = 'multiple',visible = False,key = "Listbox_Vehicle")],
            [sg.Listbox(size=(20,12), values = ('Y','N'),select_mode = 'multiple',visible = False,key = 'Listbox_TripEnd')],
            [sg.Text("From 2019-08-30 08:",key = 'From',visible=False), sg.InputText(key = 'search_key1a',visible = False),sg.Text(':',key='colon1',visible=False),sg.InputText(key = 'search_key1b',visible = False)], 
            [sg.Text('To 2019-08-30 08:',key='To',visible=False), sg.InputText(key = 'search_key2a',visible = False),sg.Text(':',key='colon2',visible=False),sg.InputText(key = 'search_key2b',visible = False)],
            [sg.InputText(key = 'search_key3',visible = False)],

            [sg.Button("Add to search list", key = "Add"),sg.Button('SEARCH',key = "Search")],
            [sg.Text(k='search_output_list')]])

layout_homePage = [[frame_search]]

win_userPage = sg.Window('Login Page',layout_userPage)
win_homePage = sg.Window('HomePage', layout_homePage,finalize=True)
#win_homePage.hide()
win_homePage_active = False

def inviewAll_key():
    win_homePage['Listbox_Vehicle'].update(visible=False)
    win_homePage['Listbox_TripEnd'].update(visible=False)
    win_homePage['From'].update(visible=False)
    win_homePage['To'].update(visible=False)
    win_homePage['search_key1a'].update(visible=False)
    win_homePage['search_key1b'].update(visible=False)
    win_homePage['search_key2a'].update(visible=False)
    win_homePage['search_key2b'].update(visible=False)
    win_homePage['colon1'].update(visible=False)
    win_homePage['colon2'].update(visible=False)
    win_homePage['search_key3'].update(visible=False)

    
    #  %%

while True:
    ev1, vals1 = win_userPage.read()

    
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit' or ev1 == None:
        break

    '''-------------step 1: login page manipulation-----------'''
    if not win_homePage_active and ev1 == 'Login':  

        # ---------------call user class , read userID and pwd-----------------
        #(vals1["userID"], vals1["pwd"])

        win_homePage_active = True
        win_homePage.un_hide()
        win_userPage.hide()

    '''---------step2: Homepage manipulation----------'''
    if win_homePage_active:
        
        ev2, vals2 = win_homePage.read()
        #-------------to do-----------------
          #...search , sort design

        if ev2 == "search_col": # unhide corresponding key input space

            print(ev2, vals2['search_col'],win_homePage_active)
            
            inviewAll_key()

            if vals2['search_col'] == "VehicleType" :
                win_homePage['Listbox_Vehicle'].update(visible = True)

            elif vals2['search_col'] == 'TripEnd':         
                win_homePage['Listbox_TripEnd'].update(visible = True)
            
            elif vals2['search_col'] == 'Gantry_O':

                win_homePage['search_key3'].update(visible=True)


            elif vals2['search_col'] == "DerectionTime_O" or "DerectionTime_D":
                
                win_homePage['From'].update(visible=True)
                win_homePage['search_key1a'].update(visible=True)
                win_homePage['colon1'].update(visible=True)
                win_homePage['search_key1b'].update(visible=True)
                win_homePage['To'].update(visible=True)
                win_homePage['search_key2a'].update(visible=True)
                win_homePage['colon2'].update(visible=True)
                win_homePage['search_key2b'].update(visible=True)
                
            else:  
                win_homePage['search_key3'].update(visible=True)

        

        if ev2 == sg.WIN_CLOSED or ev2 == 'Exit'  or ev2 == None: #Close homepage and back to login page
            win_homePage_active  = False
            win_homePage.close()
            win_userPage.un_hide()  #back to login page
 
win_userPage.close()
print("End")


# %%
