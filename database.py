#%%
import pandas as pd


class Data:

    def __init__(self, df: pd.DataFrame = pd.DataFrame()) -> None:
        self.__data = df.copy()
        
        if type(self.__data.DerectionTime_O[0]) == str:
            self.__data.DerectionTime_O = pd.to_datetime(self.__data.DerectionTime_O, format='%d/%m/%Y %H:%M')
            self.__data.DerectionTime_D = pd.to_datetime(self.__data.DerectionTime_D, format='%d/%m/%Y %H:%M')
    
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

        if (f3 is not None) and (f3 not in set(self.__data.Gantry_O)):
            return (0, 'Gantry_O', f3)
        
        if (f5 is not None) and (f5 not in set(self.__data.Gantry_D)):
            return (0, 'Gantry_D', f5)

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

        return (1, Data(res))

    def download(self):
        pass

    def head(self, max_row: int = 10):
        return self.__data.head(max_row)
    
    def get(self):
        return self.__data


class DataBase:
    def __init__(self) -> None:
        self.__data_list = {}
    
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
#%%

db = DataBase()
db.add('data/TDCS_M06A_20190830_080000.csv', 'taiwan_traffic_data')
working_sheet = db.access('taiwan_traffic_data')

col_name_list = ['VehicleType', 'DerectionTime_O']
ascending_list = [True, False]
working_sheet.sort(col_name_list, ascending_list).head()

filter_dict = {
    'VehicleType': [5, 31],
    'DerectionTime_D': (pd.to_datetime('2019-08-30 08:14:00'), pd.to_datetime('2019-08-30 08:17:00')), 
    'Gantry_O': '03F3307N',
    'TripLength': (5, 20),
    'TripEnd': ['Y']
}
test = working_sheet.search(filter_dict)[1]
test.get()
# db.delete('taiwan_traffic_data')
# db.access('taiwan_traffic_data')
# %%

# %%
