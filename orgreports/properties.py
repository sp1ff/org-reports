"""Report on tasks by properties."""
import PyOrgMode
import click
import codecs
import itertools
import unicodedata


from . import help


from operator import itemgetter


from jinja2 import Template
from PyOrgMode.PyOrgMode import OrgDataStructure


def find_by_property(files, property, states):
    """Categorize all tasks in `files' by Org property `property'.

    :param files iterable(str): list of files to process
    :param property str: Org property by which to categorize
    :param states iterable(str): todo states to be categorized
    :return dict: a dict mapping `property' values to lists of tasks (on
                  which more below)

    This method will return a dict whose keys are values of the Org property
    `property' (expressed as a string) and whose values are lists of two-tuples
    containing the task headline & filename for tasks having that value.

    key 0 will return a list of the tasks that do not define the Org property
    `property' and 1 the list of tasks that define `property' multiple times.
    """

    def _is_drawer(x):
        return isinstance(x, PyOrgMode.PyOrgMode.OrgElement) and \
            x.TYPE == 'DRAWER_ELEMENT'

    props = {0: [], 1: []}  # 0 => no context, 1 => multiple contexts

    for f in files:

        # TODO(sp1ff): Look for a property_all field

        base = OrgDataStructure()
        for s in states:
            base.add_todo_state(s)

        with codecs.open(f, encoding='utf-8') as fh:
            base.load_from_string(fh.read())

        todos = base.extract_todo_list()
        for todo in todos:

            # No node, no node content => no context
            if todo.node is None or todo.node.content is None:
                props[0].append((unicode(todo.heading), unicode(f)))
                continue

            # todo.node.content is a list. The elements may be
            # strings, or Element instances. Fortunately, Element
            # and its subclasses have a member named TYPE.
            drawers = filter(_is_drawer, todo.node.content)
            if len(drawers) == 0:
                # no drawers => no contexts
                props[0].append((unicode(todo.heading), unicode(f)))
                continue

            matches = set()
            for drawer in drawers:
                for x in drawer.content:
                    if isinstance(x, PyOrgMode.PyOrgMode.OrgDrawer.Property):
                        if x.name == property:
                            matches.add(x)

            # `matches' is the list of properties matching `property'.
            # no matches => no context
            if len(matches) == 0:
                props[0].append((unicode(todo.heading), unicode(f)))
                continue
            elif len(matches) > 1:
                # multiple contexts (?)
                props[1].append((unicode(todo.heading), unicode(f)))
                continue
            else:
                val = matches.pop().value
                if val not in props:
                    props[val] = [ ]
                props[val].append((unicode(todo.heading), unicode(f)))

    return props


def form_product(files, properties, states, elide_empty=False):
    """Form the product over all properties."""

    def _make_key(vals):
        key = [ ]
        for p in vals:
            if 0 == p:
                key.append('nil')
            elif 1 == p:
                key.append('*')
            else:
                key.append(p)
        return unicode(','.join(key))

    # property => { value: set(tasks) }
    sets = { }
    # Make a list of keys which I can feed to `product', below
    keys = [ ]
    for prop in properties:
        D = find_by_property(files, prop, states)
        sets[prop] = { }
        for k in D:
            # TODO(sp1ff): This will fail on duplicate headlines
            sets[prop][k] = set(D[k])
        keys.append(sorted(D.keys()))

    counts = { }  # key => # tasks
    for p in itertools.product(*keys):
        key = _make_key(p)
        s = sets[properties[0]][p[0]]
        i = 1
        for k in p[1:]:
            s = s & sets[properties[i]][k]
            i += 1

        n = len(s)
        if elide_empty and n == 0:
            continue
        counts[key] = n

    return counts


# TODO(sp1ff): Generalize this
def _make_2col_table(properties, rows):
    """Print a nice table."""

    from click.termui import get_terminal_size

    T = Template("""
| {{   ('{0: <%d}'%max_len).format(Properties) }} | # Tasks |
|{{ '-'*max_len }}--+---------|
{% for x in rows -%}
| {{ unicode('{{0: <{0}}}'.format(max_len-uw(x[0]))).format(x[0]) }} | {{ '{0: >7}'.format(x[1]) }} |
{% endfor -%}
|{{ '-'*max_len }}--+---------|
""")

    def _uw(s):
        """Return the # of wide characters"""

        # A  ; Ambiguous
        # F  ; Fullwidth
        # H  ; Halfwidth
        # N  ; Neutral
        # Na ; Narrow
        # W  ; Wide
        return map(lambda x: unicodedata.east_asian_width(x), s).count('W')

    max_len = max(32, max([len(x[0]) for x in rows]))

    return T.render(unicode=unicode, Properties=properties, max_len=max_len,
                    rows=rows, uw=_uw)


PROPS_HEADER = 'org-reports properties'

PROPS_SYNOPSIS = 'Report tasks by properties'

PROPS_DISCUSS = """org-reports properties will print a report of your
tasks by a given property or properties.

This command will partition the tasks found in the [2mFILES[0m arguments
(as identified by heading [2mSTATES[0m) by [2mPROPERTY[0m for each
value of [2mPROPERTY[0m. For each combination of property values, it
will count the tasks having that combination & print a simple report. Empty
partitions aren't printed.
"""


@click.command(add_help_option=False)
@click.option('--property', '-p', type=str, default=['Context'], help='Org property on'
              'which to partition tasks (may be given more than once)',
              multiple=True)
@click.option('--state', '-s', multiple=True, help='Task states to be counted ("TODO", "PENDING", &c); this '
              'option may be given more than once-- the default is simply "TODO"')
@click.option('--sort', '-o', type=click.Choice(['alpha', 'numeric']), default='numeric',
              help='order in which output will be sorted')
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@help(header=PROPS_HEADER, synopsis=PROPS_SYNOPSIS, discussion=PROPS_DISCUSS)
def main(property, state, sort, files):
    """Print a report of the number of open tasks by arbitrary properties"""

    X = form_product(files, property, state, True)

    rows = [(x, X[x]) for x in X]
    if sort == 'alpha':
        rows = sorted(rows, key=itemgetter(0))
    else:
        rows = sorted(rows, key=itemgetter(1), reverse=True)

    print(_make_2col_table(','.join(property), rows))
