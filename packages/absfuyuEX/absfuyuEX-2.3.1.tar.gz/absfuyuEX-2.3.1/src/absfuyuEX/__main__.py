import click

@click.command()
def ver():
    import absfuyuEX as abx
    click.echo(abx.__version__)

@click.command()
def update():
    from absfuyu import version
    version.check_for_update("absfuyuEX", True)


@click.command(name="wgs")
def wgscli():
    from absfuyuEX.tool import WGS
    click.echo(WGS.wgs())


@click.group()
def main():
    pass
main.add_command(update)
main.add_command(ver)
main.add_command(wgscli)

if __name__ == "__main__":
    main()