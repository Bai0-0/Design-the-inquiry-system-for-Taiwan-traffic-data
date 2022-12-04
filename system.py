#%%
from database import DataBase
from user import User


class System:

    def __init__(self) -> None:
        self.user_list = []
        self.database = DataBase()
        self.user_interface = UserInterface(self)
    
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

class UserInterface:
    def __init__(self, system) -> None:
        self.system = system

        print(self.system.database)
#%%
system = System()

# %%
