"""Report on open projects."""
import PyOrgMode
import click


from . import help


from jinja2 import Template
from PyOrgMode.PyOrgMode import OrgDataStructure


HEADER = 'org-reports projects'

SYNOPSIS = 'Report on open projects'

DISCUSSION = """org-reports projects will print a report of my outstanding
projects, broken out by parent nodes.

This is a command that needs to be made more general. In my Org system, a
project is a task at level 2, not marked done, with the the [2mprojectt[0m
tag, lacking the [2minactive[0m. Others presumably do something different,
and I'm not sure how to make this more general.
 """


@click.command()
@click.option('--brief', '-b', is_flag=True, default=False,
              help='Just summarize the results.')
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@help(header=HEADER, synopsis=SYNOPSIS, discussion=DISCUSSION)
def main(brief, files):
    """Print a report of the number of open projects."""

    # Look for nodes at level 2, with the tag 'project', missing
    # the tag 'inactive'; group them by their parentage

    projects = { }

    def extract_from_level(content):
        for node in content:
            if not hasattr(node, 'level'):
                continue
            if node.level == 2:
                tags = set(node.get_all_tags())
                todo = node.todo if hasattr(node, 'todo') else None
                if 'PROJECT' in tags and 'inactive' not in tags and \
                   (todo is None or todo not in ['DONE', 'CANCELLED']):
                    parent = node.parent.heading.strip()
                    if parent in projects:
                        projects[parent].append(node)
                    else:
                        projects[parent] = [node]
            elif node.level == 1 and node.content is not None:
                extract_from_level(node.content)

    for f in files:
        base = OrgDataStructure()
        base.add_done_state('CANCELLED')
        base.load_from_file(f)
        extract_from_level(base.root.content)

    if brief:
        for h in projects:
            print '%d %s' % (len(projects[h]), h)
    else:
        for h in projects:
            print '%d %s:' % (len(projects[h]), h)
            for p in projects[h]:
                print '    %s' % p.heading
