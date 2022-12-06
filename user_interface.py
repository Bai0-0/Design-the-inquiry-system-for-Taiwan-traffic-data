
# %%
import PySimpleGUI as sg
import pandas as pd
from pandas import Timestamp
from database import Data, DataBase
import copy
from os.path import dirname, abspath, join
# from system import System


class UI:

    @staticmethod
    def int_tuple_to_datetime(M, S):
        strm = str(M)
        strs = str(S)
        if len(strm) < 2:
            strm = '0' + strm
        if len(strs) < 2:
            strs = '0' + strs
        date = '2019-08-30 08:' + strm + ':' + strs

        return pd.to_datetime(date)

    def __init__(self, system) -> None: #system:System obj
        self.system = system
    
        '''-------------Layout design-------------------'''

        # sg.theme('Reddit')
        sg.theme('default')
        # sg.theme('SystemDefault1')

        header = ("VehicleType",'DerectionTime_O','Gantry_O','DerectionTime_D','Gantry_D','TripLength',"TripEnd",'TripInformation')
        header_sort = ("VehicleType",'DerectionTime_O','Gantry_O','DerectionTime_D','Gantry_D','TripLength',"TripEnd",'TripInformation', '/')
        vehicle_list = ('5','31','32','41','42')

        layout_userPage =[[sg.Text("Please enter your ID and Password:")],
                        [sg.Text("User ID:")],
                        [sg.Input(key = "userID")],
                        [sg.Text("Password:")],
                        [sg.Input(key = "pwd", password_char='*')],
                        [sg.Button("Sign Up"), sg.Button('Log In'), sg.Button('Exit')],
                        [sg.Text('Sucessfully sign up, please log in', k = '-end_signup-', text_color = 'red', visible=False), sg.Text(' ',k = '-warn_user-', text_color='red')]]

        frame_search =sg.Frame(title ='Search', font = ("Helvetica", 15), size = [700,570],layout =[[sg.Text('Select columns and input corresponding keywords to search:', font = ("Helvetica", 12))],

                    #Column 1 
                    [sg.Checkbox('VehicleType', k='-CB_Vehicle-'),sg.Listbox(size=(10,5),values = vehicle_list, select_mode = 'multiple',key = "-LB_Vehicle-")],
                    [sg.Text('*5-semi-trailer truck, 31-minibus, 32-van, 41-large van, 42-large truck')],

                    #Column 2
                    [sg.Checkbox('DerectionTime_O', k='-CB_TimeO-'), sg.Text("From 2019-08-30 08:"), sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-From_OMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-From_OSec-'),
                    sg.Text('To 2019-08-30 08:'), sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-To_OMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-To_OSec-')],
                    [sg.Text('*Time for the vehicle to arrive the first station')],
                
                    #Col 3
                    [sg.Checkbox('Gantry_O', k='-CB_GO-'),sg.Input(key = '-Input_GO-',size = [10,1])],
                    [sg.Text('*ID of the vehicle to arrive the first station')],

                    #col4
                    [sg.Checkbox('DerectionTime_D', k='-CB_TimeD-'), sg.Text("From 2019-08-30 08:"), sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-From_DMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-From_DSec-'),
                    sg.Text('To 2019-08-30 08:'), sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-To_DMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(60)],size =(5,5), key = '-To_DSec-')],
                    [sg.Text('*Time for the vehicle to arrive the last station')],

                    #col5
                    [sg.Checkbox('Gantry_D', k='-CB_GD-'),sg.Input(key = '-Input_GD-',size = [10,1])],
                    [sg.Text('*ID of the vehicle to arrive the last station')],

                    #col6
                    [sg.Checkbox('TripLength', k='-CB_TripLen-'),sg.Input(key = '-Input_TripLen1-',size = [6,1]), 
                                sg.Text(':'),sg.Input(key = '-Input_TripLen2-',size = [6,1])],
                    [sg.Text('*Travel distance')],

                    #col7
                    [sg.Checkbox('TripEnd', k='-CB_TripE-'), sg.Listbox(values = ('Y','N'),size = [5,2],select_mode = 'multiple',key = "-LB_TripE-")],
                    [sg.Button('SEARCH',key = "-Search-",size = [7,1])],
                    [sg.Text('No record founded',text_color = 'red', k = '-warning-',visible = False)]

                    ])

        
        
        frame_sort =sg.Frame(title ='Sort',font = ("Helvetica", 15), size = [500,570], element_justification = 'left', layout =[
            [sg.Text('Select columns and order to sort:',font = ("Helvetica", 12))],
            [sg.Text('Select the first columns to sort:')],
            [sg.Combo(values=header_sort,key='-Sort_Col_1-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_1-')],
            [sg.Text('Select the second columns to sort:')],
            [sg.Combo(values=header_sort,key='-Sort_Col_2-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_2-')],
            [sg.Text('Select the third columns to sort:')],
            [sg.Combo(values=header_sort,key='-Sort_Col_3-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_3-')],
            [sg.Text('Select the fourth columns to sort:')],
            [sg.Combo(values=header_sort,key='-Sort_Col_4-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_4-')],
            [sg.Text('Select the fifth columns to sort:')],[sg.Combo(values=header_sort,key='-Sort_Col_5-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_5-')],
            [sg.Text('Select the sixth columns to sort:')],[sg.Combo(values=header_sort,key='-Sort_Col_6-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_6-')],
            [sg.Text('Select the seventh columns to sort:')],[sg.Combo(values=header_sort,key='-Sort_Col_7-',enable_events = True), sg.Listbox(size=(10,2), values=['Ascending', 'Descending'],key='-Sorting_Order_7-')],
            [sg.Button('SORT', key = '-Sort-',size = [7,1])],
            [sg.Text(k='search_output_list')]])
       
        layout_res = [[sg.Text('Number of entry to show:'), sg.Input(default_text = '20',k = '-Input_head-',size=[7,1]), 
                        sg.Button('Display', k = '-display-'), sg.Button('Reset', k = '-clear-')],
                        [sg.Table([[0]], headings = header, num_rows = 20, size = [1150, 30], expand_x = True, expand_y = True, justification='center', k = '-res-')]]

        frame_res = sg.Frame(title='Result Display',  font = ("Helvetica", 15),size = [1210,330],layout = layout_res)

        self.layout_homePage = [[sg.Text('Inquiry System for Taiwan Traffic Data',  font = ("Helvetica", 25), expand_x = True, justification = 'center', relief=sg.RELIEF_RIDGE)],
                            [sg.Button('Back', size = [7,1])],
                            [frame_search, frame_sort],
                            [frame_res]]
        self.layout_dashboardPage = [[sg.Text('Welcome to our System!')],
                        [sg.Text(f'current working directory: {self.system.test_path}')],
                        [sg.Text('file path'),sg.InputText(key = '-Input_Path-'),sg.Text('filename in database'), sg.InputText(key = '-Input_Name-'),sg.Button("Add Sheet", key = '-Action_add-')],
                        [sg.Text('Current sheets in database')],[sg.Combo(values = list(self.system.database.show_content()),key='-Sheet_To_Access-', enable_events=True), sg.Button('Access Sheet', key = '-Action_access-')],
                        [sg.Text('choose file to delete')],[sg.Combo(values = list(self.system.database.show_content()),key='-Sheet_To_Delete-', enable_events=True), sg.Button('Delete Sheet', key = '-Action_delete-')],
                        [sg.Button('Log out', key = '-Log_out-')]]
        
        self.win_userPage = sg.Window('Login Page', layout = layout_userPage)
        self.win_homePage_active = False
        self.win_dashboardPage_active = False

    def search(self, vals2): 

        '''
        store self.res_table  continously, reset to original when click '-clear-' button

        '''

        self.win_homePage['-warning-'].update(visible = False)

        filter_dict = { }

        if vals2['-CB_Vehicle-'] == True:
            
            filter_dict['VehicleType'] = [int(x) for x in vals2['-LB_Vehicle-']]
        
        if vals2['-CB_TimeO-'] == True:
            filter_dict['DerectionTime_O'] = (self.int_tuple_to_datetime(vals2['-From_OMin-'], vals2['-From_OSec-']),
                                                self.int_tuple_to_datetime(vals2['-To_OMin-'], vals2['-To_OSec-']))
        if vals2['-CB_GO-'] == True:
            filter_dict['Gantry_O'] = str(vals2['-Input_GO-'])

        if vals2['-CB_TimeD-'] == True:
            filter_dict['DerectionTime_D'] = (self.int_tuple_to_datetime(vals2['-From_DMin-'], vals2['-From_DSec-']),
                                                self.int_tuple_to_datetime(vals2['-To_DMin-'], vals2['-To_DSec-']))
            
        if vals2['-CB_GD-'] == True:
            filter_dict['Gantry_D'] = str(vals2['-Input_GD-'])

        if vals2['-CB_TripLen-'] == True:
            filter_dict['TripLength'] = (float(vals2['-Input_TripLen1-']),float(vals2['-Input_TripLen2-']))

        if vals2['-CB_TripE-'] == True:
            filter_dict['TripEnd'] = vals2['-LB_TripE-']  

        self.res_table = Data(self.origin_sheet.get().copy())  # reset self.res_table

        self.res_table = self.res_table.search(filter_dict)
       
        self.display(int(vals2['-Input_head-']))
    
    def sort(self,vals2): #working_sheet: Data 
        self.win_homePage['-warning-'].update(visible = False)
        
        ascending_order = []
        col_name = []
        
        for i in range(1,8):
            col = f'-Sort_Col_{i}-'
            sort_order = f'-Sorting_Order_{i}-'
            if vals2[col] and vals2[col] != '/':
                col_name.append(vals2[col])
                if len(vals2[sort_order])>0:
                    ascending_order.append(False if vals2[sort_order][0] == 'Descending' else True)
                else:
                    ascending_order.append(True)

        self.res_table = self.res_table.sort(col_name, ascending_order)
        self.display(int(vals2['-Input_head-']))
                      
    def display(self, num_row: int):

        self.res_table_data = self.res_table.get().copy()
        
        if len(self.res_table_data) == 0: # empty search result

            self.win_homePage['-warning-'].update(visible = True) #show warning message
            self.win_homePage['-res-'].update([[0]])

        else:
            self.res_table_data['DerectionTime_D'] = self.res_table_data['DerectionTime_D'].astype(str)
            self.res_table_data['DerectionTime_O'] = self.res_table_data['DerectionTime_O'].astype(str)

            temp = self.res_table_data.head(num_row)
            temp = temp.values.tolist()

            self.win_homePage['-res-'].update(temp)
            self.win_homePage['-warning-'].update(visible = False)
    
    
    def run(self): 
        

        while True:
            ev1, vals1 = self.win_userPage.read()

            if ev1 == sg.WIN_CLOSED or ev1 == 'Exit' or ev1 == None:
                break

            '''-------------step 1: login page manipulation-----------'''
            if not self.win_dashboardPage_active and ev1 == 'Sign Up':
                print(vals1['userID'], vals1['pwd'])
                self.win_userPage['-warn_user-'].update('')
                self.system.userbase.sign_up(vals1['userID'],vals1['pwd'])
                self.win_userPage['-end_signup-'].update(visible = True)
                
                
            if not self.win_dashboardPage_active and ev1 == 'Log In':
                self.win_userPage['-end_signup-'].update(visible = False)  

                temp = self.system.userbase.sign_in(vals1['userID'],vals1['pwd'])

                if temp[0] is False:  # (False, message)

                    self.win_userPage['-warn_user-'].update(temp[1])

                else: #sucessfully log in

                    #create home page
                    self.win_dashboardPage_active = True
                    temp_layout = copy.deepcopy(self.layout_dashboardPage)
                    
                    self.win_dashboardPage = sg.Window('Dashboard Panel', temp_layout)
                    #hide user page
                    self.win_userPage.hide()
                    self.win_userPage['-warn_user-'].update(' ')
                    
                    
                    while self.win_dashboardPage_active:
                        ev3, vals3 = self.win_dashboardPage.read()
                        
                        if ev3 == '-Action_access-':
                            if not vals3['-Sheet_To_Access-']:
                                sg.popup('Please select a sheet!')
                                continue
                            else:
                                data_sheet = vals3['-Sheet_To_Access-']
                                
                                self.origin_sheet = self.system.database.access(data_sheet) 
                                self.res_table = Data(self.origin_sheet.get().copy())
                                sg.popup(f'Access Data: {data_sheet}!')
                                
                                self.win_homePage_active = True
                                self.win_dashboardPage.hide()
                                temp_layout = copy.deepcopy(self.layout_homePage)
                                
                                self.win_homePage = sg.Window('HomePage', temp_layout, finalize=True)
                                
                                while self.win_homePage_active == True:
                                
                                    ev2, vals2 = self.win_homePage.read()
                                    
    
                                    if ev2 == '-Search-': #press search button
                                        self.search(vals2)
    
                                    if ev2 == '-Sort-':
    
                                        self.sort(vals2)
    
                                    if ev2 == '-display-':
    
                                        self.display(int(vals2['-Input_head-']))
    
                                    if ev2 == '-clear-': #rebuild homepage
                                        self.win_homePage.close()
                                        self.res_table = Data(self.origin_sheet.get().copy())
                                        temp_layout = copy.deepcopy(self.layout_homePage)
                                        self.win_homePage = sg.Window('HomePage', temp_layout, finalize=True)
    
                                    if ev2 == sg.WIN_CLOSED or ev2 == None or ev2 == 'Back': #Close homepage and back to login page
                                        self.win_homePage_active  = False
                                        self.win_homePage.close()
                                        self.win_dashboardPage.un_hide()  #back to login page
                                        break
                        
                        elif ev3 == '-Action_add-':
                            file_path = vals3['-Input_Path-']
                            file_name = vals3['-Input_Name-']
                            self.system.database.add(file_path,file_name)
                            sg.popup(f'Successfully add sheet: {file_name}')
                            
                            
                            self.win_dashboardPage['-Sheet_To_Delete-'].update(values =list(self.system.database.show_content())  )
                            self.win_dashboardPage['-Sheet_To_Access-'].update(values =list(self.system.database.show_content())  )
                        
                        
                        elif ev3 == '-Action_delete-':
                            file_name = vals3['-Sheet_To_Delete-']
                            deleted = self.system.database.delete(file_name)
                            if deleted:
                                sg.popup(f'Successfully delete sheet: {file_name}')
                            else:
                                sg.popup('Data sheet does not exist in the database.')
                            
                            self.win_dashboardPage['-Sheet_To_Delete-'].update(values =list(self.system.database.show_content())  )
                            self.win_dashboardPage['-Sheet_To_Access-'].update(values =list(self.system.database.show_content())  )
                        
                        elif ev3 == '-Log_out-' or ev3 == sg.WIN_CLOSED or ev3== None:
                            self.win_dashboardPage_active = False
                            self.win_dashboardPage.close()
                            self.win_userPage.un_hide()  #back to login page
                            
        self.win_userPage.close()
        print("End")
    

    
# %%
