import click
from gopublic.cli.cli import pass_context, json_loads
from gopublic.cli.decorators import custom_exception, dict_output


@click.command('view')
@click.argument("file_id", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_id):
    """Show a file

Output:

    Dict with file info
    """
    return ctx.gi.file.view(file_id)
