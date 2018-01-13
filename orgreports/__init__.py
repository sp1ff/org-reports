"""org-reports utilities"""
import click


def _org_reports_help(ctx, value, header, synopsis, discussion=None, paged=True):
    """Print a nicely formatted help message.

    :param ctx click.Context: The current click Context instance
    :param header str: Heading for this help page
    :param synopsis str: A brief description of this command
    :param discussion str: A discussion of this command of arbitrary length

    Print a help page in a nicer format using ANSI escape codes.
    """
    from click.formatting import HelpFormatter
    from click.termui import echo, echo_via_pager

    if not value or ctx.resilient_parsing:
        return

    fmt = HelpFormatter()
    fmt.write_text('[1m' + header + '[0m')
    fmt.write_paragraph()
    pieces = ctx.command.collect_usage_pieces(ctx)
    fmt.write_usage(ctx.command_path, ' '.join(pieces), '[1mUsage[0m\n\n')
    fmt.write_paragraph()
    with fmt.indentation():
        fmt.write_text(synopsis)
    ctx.command.format_options(ctx, fmt)
    fmt.write_paragraph()
    if discussion:
        fmt.write_text('[1mDiscussion[0m')
        fmt.write_paragraph()
        with fmt.indentation():
            fmt.write_text(discussion)

    if paged:
        echo_via_pager(fmt.getvalue(), ctx.color)
    else:
        echo(fmt.getvalue(), ctx.color)

    ctx.exit()


def help(**attrs):

    from click.decorators import _param_memo

    header = attrs.pop('header')
    synopsis = attrs.pop('synopsis')
    discussion = attrs.pop('discussion', None)
    paged = attrs.pop('paged', False)

    def _shim(ctx, param, value):
        _org_reports_help(ctx, value, header, synopsis, discussion, paged)

    def decorator(f):
        _param_memo(f, click.Option(['-h', '--help'],
                                    help='Print this message & exit with status zero',
                                    is_flag=True, is_eager=True, expose_value=False,
                                    callback=_shim))
        return f

    return decorator
