"""Report on org files."""
import PyOrgMode
import click
import sys


from PyOrgMode.PyOrgMode import OrgElement


def outline(f):
    """Print the outline of an org file."""

    base = PyOrgMode.PyOrgMode.OrgDataStructure()
    base.load_from_file(f)

    # import pdb; pdb.set_trace()

    def _process_node(n):
        if isinstance(n, OrgElement):
            if n.TYPE in ['SCHEDULE_ELEMENT', 'DRAWER_ELEMENT', 'TABLE_ELEMENT']:
                return
            print('%s %s' % ('*'*n.level, n.heading))
            for child in n.content:
                if isinstance(child, OrgElement):
                    _process_node(child)

    _process_node(base.root)


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
def main(files):
    """For now, just print an outline of each file in FILES."""
    map(outline, files)
