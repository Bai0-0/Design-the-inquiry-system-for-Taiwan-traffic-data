#%%
import os
import pandas as pd
from os.path import dirname, abspath, join

class UserBase:
    
    def __init__(self, lib_path) -> None:
        self.user_file_path = os.path.join(lib_path, 'account_info.csv')
        if os.path.exists(self.user_file_path):
            self.__account_info = pd.read_csv(self.user_file_path, index_col=0)
            self.__account_info = self.__account_info.astype(str)
            self.__account_info.reset_index(drop=True, inplace=True)
        else:
            self.__account_info = pd.DataFrame(columns=['uid', 'password'])
    
    def sign_up(self, uid: str, pw: str) -> tuple:
        """Sign up

        Args:
            uid (str): user name
            pw (str): password

        Returns:
            tuple: (True) for success
        """
        if uid not in set(self.__account_info.uid):
            tmp = pd.DataFrame({'uid': [uid], 'password': [pw]})
            self.__account_info = pd.concat([self.__account_info, tmp])
            self.__account_info.reset_index(drop=True, inplace=True)
        else:
            self.__account_info.loc[self.__account_info.uid == uid, 'password'] = pw
        
        return (True)
    
    def sign_in(self, uid: str, pw: str) -> tuple:
        """Sign in

        Args:
            uid (str): user name
            pw (str): password

        Returns:
            tuple: (True, '') for success, (False, Error) for failure
        """
        if uid in set(self.__account_info.uid):
            pw_list = list(self.__account_info.loc[self.__account_info.uid == uid, 'password'])
            if pw in pw_list:
                return (True, '')
            else:
                print('Incorrect Password.')
                return (False, 'Incorrect Password.')
        else:
            print('Invalid Username.')
            return (False, 'Invalid Username.')

    def save_to_local(self):
        if os.path.exists(self.user_file_path):
            os.remove(self.user_file_path)
        self.__account_info = self.__account_info.astype(str)
        self.__account_info.to_csv(self.user_file_path)


if __name__ == '__main__':
    root_path = dirname(abspath(__file__))
    lib_path = join(root_path, 'lib')
    ub = UserBase(lib_path)
    ub.sign_in('1', 476)
    ub.sign_up('123', 123)
    ub.sign_up('CZZ', 456)
    print(ub.sign_in('CZZ', 456))
    ub.sign_in('CZZ', 476)
    ub.sign_in('XYS', 476)
    ub.save_to_local()
    test = ub._UserBase__account_info.values.tolist()
# %%
