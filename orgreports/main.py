"""org-reports implementation of main"""
import click


from . import help
from contexts import main as context_main
from projects import main as projects_main
from files import main as files_main


ORG_REPORTS_HEADING = 'org-reports'

ORG_REPORTS_HELP = """
Generate a variety of reports on Emacs org-mode files. For help
on a specific sub-command, do:

    \b
    org-reports SUB-COMMAND --help

See also the discussion below.
"""

ORG_REPORTS_DISCUSSION = """This is a personal script that I may (or may not)
generalize. At present, it lets me generate some very basic reports about my
org-mode planner:

[1mTasks by Context[0m

org-reports contexts prints a report on the number of tasks per context.
Useful for seeing how well my contexts are working for me.

[1mOpen Projects[0m

org-reports projects prints a report of the number of open projects. Useful
for keeping a lid on my commitments.

[1mFile Structure[0m

Really more of a debugging tool at this point, org-reports files prints an
outline of its arguments.
"""


@click.group(add_help_option=False)
@click.version_option()
@help(header=ORG_REPORTS_HEADING, synopsis=ORG_REPORTS_HELP,
      discussion=ORG_REPORTS_DISCUSSION)
def cli():
    pass


cli.add_command(context_main, name='contexts')
cli.add_command(projects_main, name='projects')
cli.add_command(files_main, name='files')


if __name__ == '__main__':
    cli()
