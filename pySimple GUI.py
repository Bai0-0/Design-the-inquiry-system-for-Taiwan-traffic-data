
# %%
import PySimpleGUI as sg

class UI:

    def __init__(self, system) -> None: #system:System
        self.system = system
    
        '''Layout design'''
        #header = ("VehicleType",'DerectionTime_O','Gantry_O','DerectionTime_D','Gantry_D','TripLength',"TripEnd")
        vehicle_list = ('5','31','32','41','42')
        layout_userPage =[[sg.Text("Please enter your ID and Password:")],
                        [sg.Text("User ID  :"), sg.InputText(key = "userID")],
                        [sg.Text("Password :"), sg.InputText(key = "pwd", password_char='*')],
                        [sg.Button("Login"), sg.Button('Exit')]]

        frame_search =sg.Frame(title ='Search',layout =[[sg.Text('Select columns and input corresponding keywords to search:')],

                    #Column 1 
                    [sg.Checkbox('VehicleType', k='-CB_Vehicle-'),sg.Listbox(size=(10,5),values = vehicle_list, select_mode = 'multiple',key = "-LB_Vehicle-")],
                    [sg.Text('*5-semi-trailer truck, 31-minibus, 32-van, 41-large van, 42-large truck',size = [10,1])],

                    #Column 2
                    [sg.Checkbox('DerectionTime_O', k='-CB_TimeO-'), sg.Text("From 2019-08-30 08:"), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_OMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_OSec-'),
                    sg.Text('To 2019-08-30 08:'), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_OMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_OSec-')],
                    [sg.Text('*Time for the vehicle to arrive the first station')],
                
                    #Col 3
                    [sg.Checkbox('Gantry_O', k='-CB_GO-'),sg.InputText(key = '-Input_GO-',size = [10,1])],
                    [sg.Text('*ID of the vehicle to arrive the first station')],

                    #col4
                    [sg.Checkbox('DerectionTime_D', k='-CB_TimeD-'), sg.Text("From 2019-08-30 08:"), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_DMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-From_DSec-'),
                    sg.Text('To 2019-08-30 08:'), sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_DMin-'),sg.Text(':'),sg.Combo(values=[i for i in range(61)],size =(5,5), key = '-To_DSec-')],
                    [sg.Text('*Time for the vehicle to arrive the last station')],

                    #col5
                    [sg.Checkbox('Gantry_D', k='-CB_GD-'),sg.InputText(key = '-Input_GD-',size = [10,1])],
                    [sg.Text('*ID of the vehicle to arrive the last station')],

                    #col6
                    [sg.Checkbox('TripLength', k='-CB_TripLen-'),sg.InputText(key = '-Input_TripLen-',size = [10,1])],
                    [sg.Text('*Travel distance')],

                    #col7
                    [sg.Checkbox('TripEnd', k='-CB_TripE-'),sg.Radio('Y-Normal', "Radio", size=(10,1), k='-TripE_Y-'),sg.Radio('N-Abnormal', "Radio",size=(10,1), k='-TripE_N-')],

                    [sg.Button('SEARCH',key = "-Search-")]])

        frame_show = sg.Frame
        layout_homePage = [[frame_search]]

        self.win_userPage = sg.Window('Login Page',layout_userPage)
        self.win_homePage = sg.Window('HomePage', layout_homePage,finalize=True)
        self.win_homePage.hide()
        self.win_homePage_active = False

    def run(self): 

        while True:
            ev1, vals1 = self.win_userPage.read()

            
            if ev1 == sg.WIN_CLOSED or ev1 == 'Exit' or ev1 == None:
                break

            '''-------------step 1: login page manipulation-----------'''
            if not self.win_homePage_active and ev1 == 'Login':  

                # ---------------call user class , read userID and pwd-----------------
                #(vals1["userID"], vals1["pwd"])

                self.win_homePage_active = True
                self.win_homePage.un_hide()
                self.win_userPage.hide()

                self.system.sign_up(vals1['userID'], vals1['pwd'], None)
            
            


            '''---------step2: Homepage manipulation----------'''
            if self.win_homePage_active:

                while self.win_homePage_active:
                
                    ev2, vals2 = self.win_homePage.read()
                    
                    '''-----------------Search frame---------------------'''

                    if ev2 == '-Search-': #press search button

                        filter_dict = {}

                        if vals2['-CB_Vehicle-']:
                            filter_dict['VehicleType'] = vals2['-LB_Vehicle-']
                        if vals2['-CB_TimeO-']:
                            filter_dict['DerectionTime_O']
                        if vals2['-CB_GO-']:
                            pass
                        if vals2['']
                    
                    if ev2 == "sort":
                        pass

                    if ev2 == sg.WIN_CLOSED or ev2 == 'Exit'  or ev2 == None: #Close homepage and back to login page
                        win_homePage_active  = False
                        self.win_homePage.close()
                        self.win_userPage.un_hide()  #back to login page
        
        self.win_userPage.close()
        print("End")


# %%
