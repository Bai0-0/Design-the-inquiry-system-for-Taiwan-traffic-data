
# %%
import PySimpleGUI as sg
import pandas as pd
from pandas import Timestamp
from database import Data, DataBase
import copy
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

        header = ("VehicleType",'DerectionTime_O','Gantry_O','DerectionTime_D','Gantry_D','TripLength',"TripEnd",'TripInformation')
        vehicle_list = ('5','31','32','41','42')
        layout_userPage =[[sg.Text("Please enter your ID and Password:")],
                        [sg.Text("User ID:")],
                        [sg.Input(key = "userID")],
                        [sg.Text("Password:")],
                        [sg.Input(key = "pwd", password_char='*')],
                        [sg.Button("Sign Up"), sg.Button('Log In'), sg.Button('Exit')],
                        [sg.Text('Sucessfully sign up, please log in', k = '-end_signup-', text_color = 'red', visible=False), sg.Text(' ',k = '-warn_user-', text_color='red')]]

        frame_search =sg.Frame(title ='Search',layout =[[sg.Text('Select columns and input corresponding keywords to search:')],

                    #Column 1 
                    [sg.Checkbox('VehicleType', k='-CB_Vehicle-'),sg.Listbox(size=(10,5),values = vehicle_list, select_mode = 'multiple',key = "-LB_Vehicle-")],
                    [sg.Text('*5-semi-trailer truck, 31-minibus, 32-van, 41-large van, 42-large truck')],

                    #Column 2
                    [sg.Checkbox('DerectionTime_O', k='-CB_TimeO-'), sg.Text("From 2019-08-30 08:"), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_OMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_OSec-'),
                    sg.Text('To 2019-08-30 08:'), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_OMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_OSec-')],
                    [sg.Text('*Time for the vehicle to arrive the first station')],
                
                    #Col 3
                    [sg.Checkbox('Gantry_O', k='-CB_GO-'),sg.Input(key = '-Input_GO-',size = [10,1])],
                    [sg.Text('*ID of the vehicle to arrive the first station')],

                    #col4
                    [sg.Checkbox('DerectionTime_D', k='-CB_TimeD-'), sg.Text("From 2019-08-30 08:"), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_DMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_DSec-'),
                    sg.Text('To 2019-08-30 08:'), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_DMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_DSec-')],
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

                    [sg.Text('Number of entry to show:'),sg.Input(default_text = '20',k = '-Input_head-',size=[7,1]), sg.Button('SEARCH',key = "-Search-"),], 
                    [sg.Text('No record founded',text_color = 'red', k = '-warning-',visible = False)]])

        frame_res = sg.Frame(title='Result Display', layout = [[sg.Table([[0,0,0,0,0,0,0,0]], headings = header,num_rows = 10,k = '-res-')]])
        self.layout_homePage = [[sg.Button('Back')],
                            [frame_search],
                            [frame_res]]

        self.win_userPage = sg.Window('Login Page',layout_userPage)
        self.win_homePage_active = False

    def search(self, working_sheet: Data, vals2): 
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

        res_table = working_sheet.search(filter_dict).get()
       
        if len(res_table) == 0: # empty search result

            self.win_homePage['-warning-'].update(visible = True) #show warning message
            self.win_homePage['-res-'].update([[0]])

        else:

            res_table['DerectionTime_D'] = res_table['DerectionTime_D'].astype(str)
            res_table['DerectionTime_O'] = res_table['DerectionTime_O'].astype(str)

            num_row = int(vals2['-Input_head-'])
            res_table = res_table.head(num_row)
            res_table = res_table.values.tolist()

            self.win_homePage['-res-'].update(res_table)
            self.win_homePage['-warning-'].update(visible = False)
    
    def run(self): 
        

        while True:
            ev1, vals1 = self.win_userPage.read()

            if ev1 == sg.WIN_CLOSED or ev1 == 'Exit' or ev1 == None:
                break

            '''-------------step 1: login page manipulation-----------'''
            if ev1 == 'Sign Up':
                # not self.win_homePage_active and 
                self.win_userPage['-warn_user-'].update('')
                self.system.userbase.sign_up(vals1['userID'],vals1['pwd'])
                self.win_userPage['-end_signup-'].update(visible = True)

            if  ev1 == 'Log In' : 
                #not self.win_homePage_active and

                self.win_userPage['-end_signup-'].update(visible = False)  
                print('invisible end sign up')

                temp = self.system.userbase.sign_in(vals1['userID'],vals1['pwd'])

                if temp[0] is False:  # (False, message)

                    self.win_userPage['-warn_user-'].update(temp[1])

                else: #sucessfully log in

                    #create home page
                    self.win_homePage_active = True
                    temp_layout = copy.deepcopy(self.layout_homePage)
                    
                    self.win_homePage = sg.Window('HomePage', temp_layout, finalize=True)
                    self.working_sheet = self.system.database.access('taiwan_traffic_data') 
                    
                    #hide user page
                    self.win_userPage.hide()
                    self.win_userPage['-warn_user-'].update(' ')
                               
           
            '''---------step 3: Homepage manipulation----------'''
            

            while self.win_homePage_active == True:
            
                ev2, vals2 = self.win_homePage.read()
                
                '''-----------------Search frame---------------------'''
                

                if ev2 == '-Search-': #press search button
                    self.search(self.working_sheet, vals2)

                if ev2 == 'sort':
                    pass

                if ev2 == sg.WIN_CLOSED or ev2 == None or ev2 == 'Back': #Close homepage and back to login page
                    win_homePage_active  = False
                    self.win_homePage.close()
                    self.win_userPage.un_hide()  #back to login page
                    break
        
        self.win_userPage.close()
        print("End")


# %%
