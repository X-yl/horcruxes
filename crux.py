import click

@click.group()
def cli():
    pass


@cli.command()
@click.option('-n', type=int, required=True, help='Number of horcruxes to create')
@click.option('-k', type=int, required=True, help='Number of horcruxes to recover original')
@click.argument('file', type=click.Path(exists=True, readable=True))
def encrypt(file, n: int, k: int):
    print(f"{file}, {n}, {k}")


if __name__ == '__main__':
    cli()