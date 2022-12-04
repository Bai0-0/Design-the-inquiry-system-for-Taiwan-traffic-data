#%%
import pandas as pd
import os
import shutil


class Data:

    def __init__(self, df: pd.DataFrame = pd.DataFrame()) -> None:
        self.__data = df.copy()
        
        if not self.__data.empty:
            if type(self.__data.DerectionTime_O[0]) == str:
                self.__data.DerectionTime_O = pd.to_datetime(self.__data.DerectionTime_O)
                self.__data.DerectionTime_D = pd.to_datetime(self.__data.DerectionTime_D)
    
    def sort(self, col_name_list: list, ascending_list: list):
        """Sort data

        Args:
            col_name_list (list): column names to sort by
            ascending_list (list): True for ascending and False for descending

        Returns:
            Data
        """
        assert len(col_name_list) == len(ascending_list), 'Length not match for input arguments'
        res = self.__data.sort_values(col_name_list, ascending=ascending_list)
        return Data(res)

    def search(self, filter_dict: dict):
        """Search data

        Args:
            filter_dict (dict): filter dict

        Returns:
            Data
        """

        # f1: list[int]
        f1 = filter_dict.get('VehicleType', None)
        # f2: tuple(datetime1, datetime2)
        f2 = filter_dict.get('DerectionTime_O', None)
        # f3: str
        f3 = filter_dict.get('Gantry_O', None)
        # f4: tuple(datetime1, datetime2)
        f4 = filter_dict.get('DerectionTime_D', None)
        # f5: str
        f5 = filter_dict.get('Gantry_D', None)
        # f6: tuple(int1, int2)
        f6 = filter_dict.get('TripLength', None)
        # f7: list[str]
        f7 = filter_dict.get('TripEnd', None)

        # if (f3 is not None) and (f3 not in set(self.__data.Gantry_O)):
        #     return (0, 'Gantry_O', f3)
        
        # if (f5 is not None) and (f5 not in set(self.__data.Gantry_D)):
        #     return (0, 'Gantry_D', f5)

        res = self.__data.copy()
        if f1 is not None:
            res = res[res.VehicleType.isin(f1)]

        if f2 is not None:
            res = res[(f2[0] <= res.DerectionTime_O) & (res.DerectionTime_O <= f2[1])]

        if f3 is not None:
            res = res[res.Gantry_O == f3]
        
        if f4 is not None:
            res = res[(f4[0] <= res.DerectionTime_D) & (res.DerectionTime_D <= f4[1])]
        
        if f5 is not None:
            res = res[res.Gantry_D == f5]

        if f6 is not None:
            res = res[(f6[0] <= res.TripLength) & (res.TripLength <= f6[1])]
        
        if f7 is not None:
            res = res[res.TripEnd.isin(f7)]

        return Data(res)

    def download(self, path):
        self.__data.to_csv(path, index=False)
    
    def get(self):
        return self.__data


class DataBase:
    def __init__(self, data_path) -> None:
        self.__data_list = {}
        self.__data_path = data_path
        file_list = os.listdir(self.__data_path)
        file_list = [f for f in file_list if f != '.DS_Store']
        if len(file_list) > 0:
            for f in file_list:
                self.add(os.path.join(self.__data_path, f), f.rstrip('.csv'))
    
    def add(self, data_path: str, sheet_name: str):
        """Add sheet to the database

        Args:
            data_path (str): path of data sheet
            sheet_name (str): sheet name
        """
        df = pd.read_csv(data_path)
        self.__data_list[sheet_name] = Data(df)

    def access(self, sheet_name: str) -> Data:
        """Access sheet in the database

        Args:
            sheet_name (str): sheet name

        Returns:
            Data: data sheet
        """
        if sheet_name in self.__data_list:
            return self.__data_list[sheet_name]
        else:
            print('Data sheet does not exist in the database.')

    def delete(self, sheet_name: str):
        """Delete sheet from the database

        Args:
            sheet_name (str): sheet name
        """
        if sheet_name in self.__data_list:
            self.__data_list.pop(sheet_name)
        else:
            print('Data sheet does not exist in the database.')

    def save_to_local(self):
        shutil.rmtree(self.__data_path)
        self.generate_folder(self.__data_path)
        for k in self.__data_list:
            path = os.path.join(self.__data_path, k + '.csv')
            self.__data_list[k].download(path)

    def show_content(self):
        return self.__data_list.keys()

    @staticmethod
    def generate_folder(path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
        return None


# %%
