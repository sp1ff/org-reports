"""Report on tasks by context."""
import PyOrgMode
import click
import codecs
import sys
import unicodedata


from . import help
from properties import find_by_property


from operator import itemgetter


from jinja2 import Template
from PyOrgMode.PyOrgMode import OrgDataStructure


CTX_HEADER = 'org-reports contexts'

CTX_SYNOPSIS = 'Report tasks by property.'

CTX_DISCUSS = """org-reports contexts will print a report of your todos
broken out by a given property ([2mContext[0m, by default).

This command will partition the tasks found in the [2mFILES[0m arguments
(as identified by heading [2mSTATES[0m) and count the number of tasks in
each partition. Tasks that are lacking the given property, or that specify that
property more than once will also be listed (if any).
"""


@click.command(add_help_option=False)
@click.option('--property', '-p', type=str, default='Context', help='Org property on'
              'which to partition tasks')
@click.option('--state', '-s', multiple=True, help='Task states to be counted ("TODO", "PENDING", &c); this '
              'option may be given more than once-- the default is simply "TODO"')
@click.option('--sort', '-o', type=click.Choice(['alpha', 'numeric']), default='numeric',
              help='order in which output will be sorted')
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@help(header=CTX_HEADER, synopsis=CTX_SYNOPSIS, discussion=CTX_DISCUSS)
def main(property, state, sort, files):
    """Print a report of the number of open tasks by context.

    This is really just a special case of the `properties' sub-command, but
    I've kept it separate because I like the extended report format used here.
    """

    from click.termui import get_terminal_size

    T = Template("""
{{ total_tasks }} tasks in {{ num_ctxes }} {{ Property }}s:

| {{   ('{0: <%d}'%max_len).format(Property) }} | # Tasks |        |
|{{ '-'*max_len }}--+---------+--------|
{% for x in contexts -%}
| {{ unicode('{{0: <{0}}}'.format(max_len-uw(x[0]))).format(x[0]) }} | {{ '{0: >7}'.format(x[1]) }} | {{ '{0: >5.1f}'.format(x[2]) }}% |
{% endfor -%}
|{{ '-'*max_len }}--+---------+--------|
""")

    S = Template("""
{{ len(contexts) }} tasks with {{ headline }}:

| Task {{ ' '*(max_todo_len-6) }} | File {{ ' '*(max_file_len-6)}} |
|{{ '-'*max_todo_len }}-+{{ '-'*max_file_len }}-|
{% for x in contexts -%}
| {{ unicode('{{0: <{0}}}'.format(max_todo_len-uw(x[0]))).format(x[0]) }}|{{ unicode('{{0: <{0}}}'.format(max_file_len-uw(x[1]))).format(x[1]) }} |
{% endfor -%}
|{{ '-'*max_todo_len }}-+{{ '-'*max_file_len }}-|
""")

    def _handle_unexp(ctxes, headline):
        max_todo_len = max(32, max([len(x[0]) for x in ctxes]))
        max_file_len = max(32, max([len(x[1]) for x in ctxes]))
        twidth, _ = get_terminal_size()
        # The seven is for | & extra spaces in each column
        if max_todo_len + max_file_len + 7 > twidth:
            xT = float(max_todo_len + max_file_len + 7)
            xt = float(twidth)
            xo = float(max_todo_len)
            xf = float(max_file_len)
            max_todo_len = int(xo/xT*xt)
            max_file_len = int(xf/xT*xt)
            ctxes = map(lambda x: (_ell(x[0], max_todo_len),
                                      _ell(x[1], max_file_len, False)),
                           ctxes)

        sorted(ctxes, key=lambda x: u'%s-%s' % x)
        print(S.render(unicode=unicode, Property=property,
                       max_todo_len=max_todo_len,
                       contexts=ctxes, max_file_len=max_file_len,
                       uw=_uw, len=len, headline=headline))

    contexts = find_by_property(files, property, state)

    no_ctxes = []
    mt_ctxes = []
    if 0 in contexts:
        no_ctxes = contexts[0]
        del contexts[0]
    if 1 in contexts:
        mt_ctxes = contexts[1]
        del contexts[1]

    max_len = max(32, max([len(x) for x in contexts.keys()]))

    def _uw(s):
        """Return the # of wide characters"""

        # A  ; Ambiguous
        # F  ; Fullwidth
        # H  ; Halfwidth
        # N  ; Neutral
        # Na ; Narrow
        # W  ; Wide
        return map(lambda x: unicodedata.east_asian_width(x), s).count('W')

    def _ell(s, cc, append=True):
        """Truncate `s' to `cc', appending or prepending ellipses as needed"""
        if len(s) <= cc:
            return s
        if append:
            return s[:cc-3] + '...'
        else:
            return '...' + s[-cc+3:]

    total_tasks = sum([len(x) for x in contexts.values()])
    contexts = [(x, len(contexts[x]), 100*float(len(contexts[x]))/float(total_tasks)) for x in contexts.keys()]

    if sort == 'alpha':
        contexts = sorted(contexts, key=itemgetter(0))
    else:
        contexts = sorted(contexts, key=itemgetter(1), reverse=True)

    print(T.render(unicode=unicode, Property=property, max_len=max_len,
                   contexts=contexts, uw=_uw, num_ctxes=len(contexts)-2,
                   total_tasks=total_tasks))

    if no_ctxes:
        _handle_unexp(no_ctxes, 'no contexts')

    if mt_ctxes:
        _handle_unexp(mt_ctxes, 'multiple contexts')
