from utils import log
import json

class User(object):
    def __init__(self, form):
        self.id = len(self.all()) + 1
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    @classmethod
    def all(cls):
        path = cls._get_path()
        model_dict = cls._load(path)
        models = [cls(m) for m in model_dict]
        return models

    def save(self):
        path = self._get_path()
        models = self.all()
        models.append(self)
        model_dict = [m.__dict__ for m in models]
        self._save(model_dict, path)

    # def delete(self):
    #     path = self._get_path()
    #     models = self.all()
    #     models.remove(self.id)
    #     model_dict = [m.__dict__ for m in models]
    #     self._save(model_dict, path)

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
    def _save(cls, model_dict, path):
        d = json.dumps(model_dict, indent=2, ensure_ascii=False)
        with open(path, 'w+', encoding='utf-8') as f:
            log('save', path, d, model_dict)
            f.write(d)

#
# class User(Model):
#     def __init__(self, form):
#         self.username = form.get('username', '')
#         self.password = form.get('password', '')
#
