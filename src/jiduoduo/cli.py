import os
import sys

import click


@click.group()
@click.option('--dry_run', type=bool, default=True)
@click.pass_context
def cli(ctx, dry_run: bool):
    ctx.ensure_object(dict)
    ctx.obj['dry_run'] = dry_run

    click.echo(f'os.getcwd()={os.getcwd()}')
    click.echo(f'sys.executable={sys.executable}')
    click.echo(f'dry_run={dry_run}')


@cli.command()
@click.argument('name', required=True)
@click.pass_context
def test(ctx, name: str):
    from jiduoduo.app import app
    from jiduoduo.models import VPS
    with app.app_context():
        vps = VPS.get_by_name(name)
        if not vps:
            click.echo(f'No such VPS: {name}')
            return
        vps.run('echo test')


if __name__ == '__main__':
    cli()
