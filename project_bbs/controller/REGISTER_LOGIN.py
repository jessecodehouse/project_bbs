from model import MODEL

class RegisterAndLogin(object):

    def __init__(self):
        self.db = MODEL.ChangeInfoUser()

    def test_user_name_exist(self, user_name):    # 输入用户名，判断用户名是否在数据库中存在,存在返回True，不存在返回False
        exist_user_name = self.db.search_info(user_name)
        if not exist_user_name:
            return False
        else:
            return True

    def test_user_name_and_pwd(self, user_name, pwd):   # 输入用户名和密码，判断与数据库中的是否一致,一致返回True
        ret = self.db.search_info(user_name)
        if ret:
            if ret[0] == user_name and ret[1] == pwd:
                return True
        return False


