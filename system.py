#%%
import os
from os.path import dirname, abspath, join
import pandas as pd

from database import DataBase
from userbase import UserBase


class System:

    def __init__(self) -> None:
        
        root_path = dirname(abspath(__file__))
        lib_path = join(root_path, 'lib')
        data_path = join(root_path, 'lib', 'data')
        self.generate_folder(lib_path)
        self.generate_folder(data_path)

        self.userbase = UserBase(lib_path)
        self.database = DataBase(data_path)

        self.user_interface = UI(self)
        self.user_interface.run()

        self.userbase.save_to_local()
        self.database.save_to_local()



    @staticmethod
    def generate_folder(path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        return None


        
#%%
if __name__ == '__main__':
    system = System()
    # system.database.add('test/TDCS_M06A_20190830_080000.csv', 'taiwan_traffic_data')

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
