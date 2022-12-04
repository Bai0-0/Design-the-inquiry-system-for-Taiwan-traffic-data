
# %%
import PySimpleGUI as sg
import pandas as pd
from pandas import Timestamp
from system import System

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

    def __init__(self, system) -> None: #system:System
        self.system = system
    
        '''Layout design'''
        #header = ("VehicleType",'DerectionTime_O','Gantry_O','DerectionTime_D','Gantry_D','TripLength',"TripEnd")
        vehicle_list = ('5','31','32','41','42')
        layout_userPage =[[sg.Text("Please enter your ID and Password:")],
                        [sg.Text("User ID:"), sg.Input(key = "userID")],
                        [sg.Text("Password :"), sg.Input(key = "pwd", password_char='*')],
                        [sg.Button("Sign In"), sg.Button('Sign Up'), sg.Button('Exit')]]

        frame_search =sg.Frame(title ='Search',layout =[[sg.Text('Select columns and input corresponding keywords to search:')],

                    #Column 1 
                    [sg.Checkbox('VehicleType', k='-CB_Vehicle-'),sg.Listbox(size=(10,5),values = vehicle_list, select_mode = 'multiple',key = "-LB_Vehicle-")],
                    [sg.Text('*5-semi-trailer truck, 31-minibus, 32-van, 41-large van, 42-large truck',size = [10,1])],

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
                    [sg.Checkbox('TripLength', k='-CB_TripLen-'),sg.Input(key = '-Input_TripLen-',size = [10,1])],
                    [sg.Text('*Travel distance')],

                    #col7
                    [sg.Checkbox('TripEnd', k='-CB_TripE-'), sg.Listbox(values = ('Y','N'),size = [2,1],select_mode = 'multiple',key = "-LB_TripE-")],

                    [sg.Text('Number of entry to show:'),sg.Input(k = '-Input_head-'), sg.Button('SEARCH',key = "-Search-"),], 
                    [sg.Text('No record founded',text_color = 'red', k = '-warning-',visible = False)]])

        frame_res = sg.Frame(title='Result Display', layout = [[sg.Table(k = '-res-')]] )
        self.layout_homePage = [[sg.Button('Back')],
                            [frame_search],
                            [frame_res]]

        self.win_userPage = sg.Window('Login Page',layout_userPage)
        self.win_homePage_active = False

    def search(self, working_sheet, vals2): #working_sheet: Data 
        
        self.win_homePage['-warning-'].update(visible = False)

        filter_dict = {}

        if vals2['-CB_Vehicle-']:
            filter_dict['VehicleType'] = vals2['-LB_Vehicle-']
        if vals2['-CB_TimeO-']:
            filter_dict['DerectionTime_O'] = tuple(self.int_tuple_to_datetime(vals2['-From_OMin-'], vals2['-From_OSec-']),
                                                self.int_tuple_to_datetime(vals2['-To_OMin-'], vals2['-To_OSec-']))
        if vals2['-CB_GO-']:
            filter_dict['Gantry_O'] = str(vals2['-Input_GO-'])

        if vals2['-CB_TimeD-']:
            filter_dict['DerectionTime_D'] = tuple(self.int_tuple_to_datetime(vals2['-From_DMin-'], vals2['-From_DSec-']),
                                                self.int_tuple_to_datetime(vals2['-To_DMin-'], vals2['-To_DSec-']))
            
        if vals2['-CB_GD-']:
            filter_dict['Gantry_D'] = str(vals2['-Input_GD-'])

        if vals2['-CB_TripLen-']:
            filter_dict['TripLength'] = tuple(vals2['-Input_TripLen-'])

        if vals2['-CB_TripE-']:
            filter_dict['TripEnd'] = vals2['-LB_TripE-']  

        temp = working_sheet.search(filter_dict).get()

        if len(temp) == 0: # no search result

            self.win_homePage['-warning-'].update(visible = True) #show warning message

        else:
            temp['DerectionTime_D'] = temp['DerectionTime_D'].apply(lambda df: str(df))
            temp['DerectionTime_O'] = temp['DerectionTime_O'].apply(lambda df: str(df))
            temp.values.tolist()
            self.win_homePage['-res-'].update(values = temp)
            self.win_homePage['-warning-'].update(visible = False)
    
    def run(self): 

        while True:
            ev1, vals1 = self.win_userPage.read()

            
            if ev1 == sg.WIN_CLOSED or ev1 == 'Exit' or ev1 == None:
                break

            '''-------------step 1: login page manipulation-----------'''
            if not self.win_homePage_active and (ev1 == 'Sign In' or ev1 == 'Sign Up'):  

                self.win_homePage_active = True

                # self.system.sign_up(vals1['userID'], vals1['pwd'], None)
                # self.system.sign_in()

                ## create homepage
                self.win_homePage = sg.Window('HomePage', self.layout_homePage,finalize=True)
                
            
            '''---------step2: Homepage manipulation----------'''
            if self.win_homePage_active:

                while self.win_homePage_active:
                
                    ev2, vals2 = self.win_homePage.read()
                    
                    '''-----------------Search frame---------------------'''

                    if ev2 == '-Search-': #press search button
                        working_sheet = self.system.database.access('taiwan_traffic_data')

                        self.search(working_sheet, vals2)


                    if ev2 == sg.WIN_CLOSED or ev2 == None or ev2 == 'Back': #Close homepage and back to login page
                        win_homePage_active  = False
                        self.win_homePage.close()

                        #self.win_userPage.un_hide()  #back to login page
        
        self.win_userPage.close()
        print("End")


# %%
