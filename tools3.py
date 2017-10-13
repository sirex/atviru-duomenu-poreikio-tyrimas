import yaml
import inspect

import data


def _get_objects():
    def _is_thing(obj):
        return (
            inspect.isclass(obj) and
            issubclass(obj, data.Thing) and
            obj is not data.Thing
        )

    return {
        Thing.__name__: Thing()
        for _, Thing in inspect.getmembers(data, _is_thing)
    }


def main():
    objects = _get_objects()

    with open('projects.yml') as f:
        projects = list(yaml.load_all(f))

    for project in projects:
        for thing, props in project['data-needed'].items():
            obj = objects[thing]
            for prop in props:
                prop = obj[prop]
                print(project['title'], obj.meta.title, prop.title)


if __name__ == "__main__":
    main()
