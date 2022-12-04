#%%
import os
from os.path import dirname, abspath, join
import pandas as pd

from database import DataBase
from user import User, UserBase


class System:

    def __init__(self) -> None:
        root_path = dirname(abspath(__file__))
        lib_path = join(root_path, 'lib')
        data_path = join(root_path, 'lib', 'data')
        self.generate_folder(lib_path)
        self.generate_folder(data_path)

        self.userbase = UserBase()
        self.database = DataBase(data_path)
        
        self.user_interface = None

    def sign_up(self, uid, pw, acc_lvl):
        user = User(uid, pw, acc_lvl)
        self.user_list.append(user)
        return None

    def sign_in(self, uid, pw):
        user = User(uid, pw)
        for exist_user in self.user_list:
            if exist_user == user:
                user.access_level = exist_user.access_level
                print('Successfully Logged In')
                return True
        print('Incorrect User Name or Password')
        return False

    @staticmethod
    def generate_folder(path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        return None


        
#%%
if __name__ == '__main__':
    system = System()
    system.database.add('test/TDCS_M06A_20190830_080000.csv', 'taiwan_traffic_data')

    working_sheet = system.database.access('taiwan_traffic_data')
    col_name_list = ['VehicleType', 'DerectionTime_O']
    ascending_list = [True, False]
    working_sheet.sort(col_name_list, ascending_list)
    filter_dict = {
        'VehicleType': [5, 31],
        'DerectionTime_D': (pd.to_datetime('2019-08-30 08:14:00'), pd.to_datetime('2019-08-30 08:17:00')), 
        'Gantry_O': '03F3307N',
        'TripLength': (5, 20),
        'TripEnd': ['Y']
    }
    test = working_sheet.search(filter_dict)

    # system.database.delete('taiwan_traffic_data')
    system.database.save_to_local()
    print(system.database.show_content())
    print(test.get().shape)
# %%
