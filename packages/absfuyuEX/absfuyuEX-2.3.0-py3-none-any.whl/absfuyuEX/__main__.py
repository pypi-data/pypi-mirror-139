import click

@click.command()
def ver():
    import absfuyuEX as abx
    click.echo(abx.__version__)

@click.command()
def update():
    from absfuyu import version
    version.check_for_update("absfuyuEX", True)


@click.group()
def main():
    pass
main.add_command(update)
main.add_command(ver)

if __name__ == "__main__":
    main()