#%%
import os
from os.path import dirname, abspath, join
import pandas as pd

from database import DataBase
from userbase import UserBase
from user_interface import UI
# from search import UI_cls as UI


class System:

    def __init__(self) -> None:
        
        root_path = dirname(abspath(__file__))
        lib_path = join(root_path, 'lib')
        data_path = join(root_path, 'lib', 'data')
        test_path = join(root_path, 'test')
        self.generate_folder(lib_path)
        self.generate_folder(data_path)

        self.userbase = UserBase(lib_path)
        self.database = DataBase(data_path)

        self.database.add(join(test_path, 'TDCS_M06A_20190830_080000.csv'), 'taiwan_traffic_data')
        self.user_interface = UI(self)
        self.user_interface.run()

        self.userbase.save_to_local()
        self.database.save_to_local()



    @staticmethod
    def generate_folder(path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        return None


if __name__ == '__main__':
    system = System()


# %%
