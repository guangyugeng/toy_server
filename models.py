from utils import log
import json


class Model(object):
    def __init__(self):
        path = self.__class__._get_path()
        model_dict = self.__class__._load(path)
        self.id = len(model_dict) + 1

    @classmethod
    def all(cls):
        path = cls._get_path()
        model_list = cls._load(path)
        return model_list

    def save(self):
        model_list = self.all()
        # log(model_list)
        model_list.append(self.__dict__)
        path = self._get_path()
        self._save(model_list, path)

    def delete(self):
        model_list = self.all()
        m = filter(lambda m: m['id'] == self.id, model_list).__next__()
        model_list.remove(m)
        path = self._get_path()
        self._save(model_list, path)

    @classmethod
    def _get_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def _load(cls, path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            # log('load', s)
            return json.loads(s)

    @classmethod
    def _save(cls, model_list, path):
        d = json.dumps(model_list, indent=2, ensure_ascii=False)
        with open(path, 'w+', encoding='utf-8') as f:
            # log('save', path, d)
            f.write(d)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        super().__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def valid_login(self):
        users = self.all()
        for u in users:
            if u.get('username') == self.username \
                    and u.get('password') == self.password:
                return True
        return False

    def valid_register(self):
        users = self.all()
        for u in users:
            if u.get('username') == self.username:
                raise ValueError("same username")
        return len(self.username) > 2 and len(self.password) > 2

