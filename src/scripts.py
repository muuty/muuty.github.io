import click

from builder import PageBuilder


@click.group()
def cli() -> None:
    pass


@cli.command()
def build() -> None:
    click.echo("Running build...")
    PageBuilder().build_posts()


@cli.command()
def dev() -> None:
    click.echo("Running dev server...")


if __name__ == "__main__":
    cli()
