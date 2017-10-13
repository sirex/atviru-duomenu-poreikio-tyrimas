import logging
import yaml


log = logging.getLogger()


def wrap(v):
    if isinstance(v, (list, tuple)):
        return Container(v)
    elif isinstance(v, dict):
        return Object(v)
    else:
        return v


class Container:

    def __init__(self, objects):
        self.objects = list(map(wrap, objects))

    def __iter__(self):
        yield from self.objects

    def _find(self, **kw):
        for o in self.objects:
            if all(o[k] == v for k, v in kw.items()):
                yield o

    def _get(self, **kw):
        found = self._find(**kw)
        o = next(found, None)
        if o is not None and next(found, None):
            raise MultipleObjectsFound()
        return o


class Object:

    def __init__(self, attrs):
        self._attrs = attrs

    def __getattr__(self, key):
        return wrap(self._attrs[key])

    def __getitem__(self, key):
        return wrap(self._attrs[key])

    def _aslist(self, key='key', value='value'):
        return Container(
            dict(v, key=k) if isinstance(v, dict) else {key: k, value: v}
            for k, v in self._attrs.items()
        )

    def _extend(self, ref, key, objects):
        o = objects._get(**{key: self[ref]}) if ref in self._attrs else None
        if o:
            return Object(dict(self._attrs, *o._attrs))._extend(ref, key, objects)
        else:
            return self


class MultipleObjectsFound(Exception):
    pass


def main():
    logging.basicConfig(format='%(levelname)s %(message)s', level=logging.DEBUG)

    with open('data.yml') as f:
        models = wrap(list(yaml.load_all(f)))

    with open('projects.yml') as f:
        projects = wrap(list(yaml.load_all(f)))

    for project in projects:
        for model in project.data._aslist('name', 'fields'):
            if models._get(name=model.name) is None:
                log.error("model %r specified for %r project, does not exist",
                          model.name, project.title)
            model = model._extend('extends', 'name', models)
            for field in model.fields:
                print(project.title, model.name, field)


if __name__ == "__main__":
    main()
