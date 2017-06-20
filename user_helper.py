class SignUpCredential(object):
    username = None
    email = None
    fullname = None
    password = None

    def __init__(self, username, email, fullname, password):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.password = password


class LoginCredential(object):

    password = None
    username = None

    def __init__(self, username1, password1):
        self.username = username1
        self.password = password1



class User(object):
    username = None
    fullname = None
    email = None
    liftmaxes = {}
    programs = list()

    def __init__(self, username, fullname, email,  liftmaxes, programs):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.liftmaxes = liftmaxes
        self.programs = programs

    def to_dict(self):
        user_dict = {'Username': self.username, 'fullname': self.fullname, 'email': self.email,
                     'liftmaxes': self.liftmaxes, 'programs': self.programs}
        return user_dict


