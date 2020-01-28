

class Users:
    def __init__(self,name,password):
        self.User_name=name
        self.Password=password

    def change_user(self,name,password):
        self.User_name=(name if name else self.User_name)
        self.Password=(password if password else self.Password)

    #def table_name(self):
