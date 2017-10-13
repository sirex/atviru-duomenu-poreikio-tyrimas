import importlib
import inspect
import pathlib
import yaml


class Data:

    def __init__(self):
        with open('projects.yaml') as f:
            projects = yaml.load_all(f)



class Error(Exception):
    pass


class Container:

    def __init__(self, model, glob, *args, **kwargs):
        self.model = model
        self.objects = [
            Klass(name, *args, **kwargs)
            for name, Klass in _get_classes(model, glob)
        ]
        self.objects_by_name = {o.name: o for o in self.objects}

    def __getitem__(self, key):
        try:
            return self.objects_by_name[key]
        except KeyError:
            raise Error('%s object was not found in %s container.' %
                        (key, self.model.__name__))

    def __iter__(self):
        yield from self.objects

    def _prep(self, db):
        for obj in self.objects:
            obj._prep(db)
        return self


_item_id_seq = {}


class Item:

    def __hash__(self):
        global _item_id_seq
        if self.name not in _item_id_seq:
            _item_id_seq[self.name] = len(_item_id_seq)
        print(_item_id_seq[self.name], self.name)
        return _item_id_seq[self.name]

    def _prep(self, db):
        self._db = db


class Model(Item):
    title = None
    fields = None

    def __init__(self, name):
        self.name = name
        assert self.title
        self.fields_by_name = {}
        for field in self.fields:
            field.model = self
            self.fields_by_name[field.name] = field

    def __getitem__(self, key):
        return self.fields_by_name[key]

    @property
    def projects(self):
        return [p for p in self._db.projects if self in p.models]


class Field:

    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.model = None


class Project(Item):
    title = None
    data = None

    def __init__(self, name):
        self.name = name
        assert self.title
        assert self.data

    def _prep(self, db):
        self._db = db
        self.models = set()
        for data in self.data:
            data._prep(db)
            self.models.add(data.model)


class Data:

    def __init__(self, name):
        self.name = name

    def _prep(self, db):
        model, field = self.name.rsplit('.', 1)
        self.model = db.models[model]
        self.field = self.model[field]


def _get_classes(Klass, glob):
    def _is_class(obj):
        return (
            inspect.isclass(obj) and
            issubclass(obj, Klass) and
            obj is not Klass
        )

    for path in pathlib.Path().glob(glob):
        module_name = '.'.join(path.parent.parts + (path.stem,))
        model_name_prefix = module_name.split('.', 2)[2]
        module = importlib.import_module(module_name)
        for _, ProjectClass in inspect.getmembers(module, _is_class):
            yield model_name_prefix + '.' + ProjectClass.__name__, ProjectClass
