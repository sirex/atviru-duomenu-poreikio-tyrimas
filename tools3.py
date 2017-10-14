import yaml
import inspect
import collections

import data


class Error(Exception):

    def __init__(self, obj, msg):
        super().__init__('%s\n\n%s' % (msg, yaml.dump(obj, default_flow_style=False)))


def _is_object(obj):
    return (
        inspect.isclass(obj) and
        issubclass(obj, data.Objektas) and
        obj is not data.Objektas
    )


def _get_objects():
    return {
        Objektas.__name__: Objektas()
        for _, Objektas in inspect.getmembers(data, _is_object)
    }


def main():
    objects = _get_objects()

    with open('projects.yml') as f:
        projects = list(yaml.load_all(f))

    for project in projects:
        for thing, props in project['data-needed'].items():
            obj = objects[thing]
            for path in props:
                for i, name in enumerate(path.split('.')):
                    if i == 0:
                        try:
                            prop = obj[name]
                        except AttributeError as e:
                            raise Error(project, e)
                    else:
                        if _is_object(prop.type):
                            prop = prop.type()[name]
                        elif isinstance(prop.type, data.Objektas):
                            prop = prop.type[name]
                        else:
                            raise Error(project, "%s field is not an object" % path)

                print(project['title'], obj.meta.title, prop.title)


if __name__ == "__main__":
    yaml.Dumper.add_representer(
        collections.OrderedDict,
        lambda dumper, data: dumper.represent_dict(data.items())
    )
    yaml.Loader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        lambda loader, node: collections.OrderedDict(loader.construct_pairs(node))
    )
    main()
