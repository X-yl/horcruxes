import click
import secrets

@click.group()
def cli():
    pass


@cli.command()
@click.option('-n', type=int, required=True, help='Number of horcruxes to create')
@click.option('-k', type=int, required=True, help='Number of horcruxes to recover original')
@click.option('-o', type=click.Path(exists=False), required=True, help='Destination directory')
@click.option('--block-size', type=int, help="Size of block to operate on. Larger values are faster, but may result in horcruxes of different sizes. Defaults to 1/10th of file size")
@click.argument('file', type=click.Path(exists=True, readable=True))
def encrypt(file, n: int, k: int, o, block_size):
    import os
    import shamir
    os.makedirs(os.path.dirname(o), exist_ok=True)

    from cruxcreator import HorcruxCreateManager
    hcm = HorcruxCreateManager(file, n, k, block_size, o)
    hcm.write_headers()
    hcm.write()

    print("Operation successful.")

@click.option('-o', type=click.Path(exists=False), required=True, help='Destination directory')
@click.argument('files', type=click.Path(exists=True, readable=True), nargs=-1)
def decrypt(files, o):
    import os
    os.makedirs(os.path.dirname(o), exist_ok=True)

    from cruxreverser import HorcruxReverseManager
    hrm = HorcruxReverseManager(files, o)
    hrm.decrypt()

if __name__ == '__main__':
    cli()