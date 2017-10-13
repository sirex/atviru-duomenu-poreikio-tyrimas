from odlt.lib import Data


def main():
    data = Data()

    for project in data.projects:
        for data in project.data:
            print(project.title, data.model.title, data.field.title)

    for model in data.models:
        for field in model.fields:
            print(model.title, field.title, model.projects)


if __name__ == "__main__":
    main()
