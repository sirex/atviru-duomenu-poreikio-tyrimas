import collections
import inspect
import re
import operator

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import yaml

import data as models


def is_object(obj):
    return (
        inspect.isclass(obj) and
        issubclass(obj, models.Objektas) and
        obj is not models.Objektas
    )


def get_objects():
    return {
        Objektas.__name__: Objektas()
        for _, Objektas in inspect.getmembers(models, is_object)
    }


def split_camel_case(identifier):
    matches = re.finditer('.+?(?:(?<=[a-ząčęėįšųūž])(?=[A-ZĄČĘĖĮŠŲŪŽ])|(?<=[A-ZĄČĘĖĮŠŲŪŽ])(?=[A-ZĄČĘĖĮŠŲŪŽ][a-ząčęėįšųūž])|$)', identifier)
    words = [m.group(0) for m in matches]
    words = words[:1] + [w.lower() for w in words[1:]]
    return ' '.join(words)


def sunburst(nodes, total=np.pi * 2, offset=0, depth=0, ax=None):
    ax = ax or plt.subplot(111, projection='polar')

    if depth == 0 and len(nodes) == 1:
        node = nodes[0]
        ax.bar([0], [0.2], [np.pi * 2])
        ax.text(0, 0, node.label, ha='center', va='center')
        sunburst(node.children, total=node.size, depth=depth + 1, ax=ax)
    elif nodes:
        d = np.pi * 2 / total
        labels = []
        widths = []
        levels = collections.defaultdict(list)
        local_offset = offset

        for node in nodes:
            labels.append(node.label)
            widths.append(node.size * d)
            for level in range(6):
                levels[level].append(node.levels.get(level, 0) * d)
            sunburst(node.children, total=total, offset=local_offset, depth=depth + 1, ax=ax)
            local_offset += node.size

        values = np.cumsum([offset * d] + widths[:-1])
        heights = [1] * len(nodes)
        bottoms = [depth - 0.8] * len(nodes)
        rects = ax.bar(values, heights, widths, bottoms, linewidth=1, edgecolor='white', align='edge')

        for level, widths_ in levels.items():
            # Level marker
            heights = [0.0185] * len(nodes)
            bottoms = [depth - 0.8 + (0.0185 + 0.127) * level + 0.127] * len(nodes)
            ax.bar(values, heights, widths, bottoms, color='gray', alpha=0.5, align='edge')

            # Level value
            heights = [0.12] * len(nodes)
            bottoms = [depth - 0.8 + (0.12 + 0.04) * level + 0.04] * len(nodes)
            ax.bar(values, heights, widths_, bottoms, color='white', alpha=0.5, align='edge')

        for rect, label in zip(rects, labels):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            rotation = (90 + (360 - np.degrees(x) % 180)) % 360
            ax.text(x, y, label, rotation=rotation, ha='center', va='center')

    if depth == 0:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_axis_off()


TreeNode = collections.namedtuple('TreeNode', ('label', 'size', 'levels', 'children'))


def build_sunburst_tree(tree, usage, levels, parent):
    for node in tree.get(parent, []):
        children = sorted(build_sunburst_tree(tree, usage, levels, node), key=operator.itemgetter(1), reverse=True)
        size = sum(x[1] for x in children) + usage.get(node, 0)
        levels_ = {level: sum(x.levels.get(level, 0) for x in children) + levels.get(node, {}).get(level, 0) for level in range(6)}
        if size > 0:
            label = '%s (%d)' % (split_camel_case(node), size)
            yield TreeNode(label, size, levels_, children)


def main():
    mpl.style.use('seaborn-darkgrid')
    mpl.rc('figure', figsize=(40, 30))
    mpl.rc('font', size=8)

    objects = get_objects()

    with open('providers.yml') as f:
        providers = list(yaml.load_all(f))

    available = collections.defaultdict(int)

    for provider in providers:
        for data in (provider.get('provides') or []):
            for model, fields in (data['data'] or {}).items():
                for field in fields:
                    key = (model, field)
                    available[key] = max(available[key], data['level'])

    with open('projects.yml') as f:
        projects = list(yaml.load_all(f))

    usage = collections.defaultdict(int)
    levels = collections.defaultdict(collections.Counter)

    for project in projects:
        for model, fields in (project['data-needed'] or {}).items():
            usage[model] += 1
            levels[model].update([min(available[(model, field)] for field in fields)])

    tree = collections.defaultdict(list)
    tree[''] = ['Objektas']

    for name, instance in objects.items():
        tree[instance.__class__.__base__.__name__].append(instance.__class__.__name__)

    tree = list(build_sunburst_tree(tree, usage, levels, ''))

    sunburst([TreeNode('Objektas', tree[0].size, tree[0].levels, tree[0].children)])
    plt.savefig('sunburst.png')

    from subprocess import run
    run(['xdg-open', 'sunburst.png'])


if __name__ == "__main__":
    main()
