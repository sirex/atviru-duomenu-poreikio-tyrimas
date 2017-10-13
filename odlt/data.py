from collections import namedtuple

from odlt.lib import Container, Model, Project


models, projects = tables = (
    Container(Model, 'odlt/models/*.py'),
    Container(Project, 'odlt/projects/*.py'),
)


db = namedtuple('db', ('models', 'projects'))(*tables)
for table in tables:
    table._prep(db)
