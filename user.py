class User:
    
    def __init__(self, uid, pw, acc_lvl=None) -> None:
        self.user_id = uid
        self.password = pw
        self.access_level = acc_lvl

    def __eq__(self, __o: object) -> bool:
        if (self.user_id == __o.user_id) and (self.password == __o.password):
            return True
        else:
            return False