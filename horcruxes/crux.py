import click
import secrets

@click.group()
def cli():
    pass


@cli.command()
@click.option('-n', type=int, required=True, help='Number of horcruxes to create')
@click.option('-k', type=int, required=True, help='Number of horcruxes to recover original')
@click.option('-o', default='./output', type=click.Path(exists=False), help='Destination directory')
@click.option('--block-size', type=int, help="Size of block to operate on. Larger values are faster, but may result in horcruxes of different sizes. Defaults to 1/10th of file size")
@click.argument('file', type=click.Path(exists=True, readable=True))
def split(file, n: int, k: int, o, block_size):
    """Splits a file into horcruxes"""
    import os
    import shamir
    os.makedirs(o, exist_ok=True)

    from cruxcreator import HorcruxCreateManager
    hcm = HorcruxCreateManager(file, n, k, block_size, o)
    hcm.write_headers()
    hcm.write()

    print("Operation successful.")

@cli.command()
@click.option('-o', type=click.Path(exists=False), required=True, help='Destination directory')
@click.argument('files-or-dir', type=click.Path(exists=True, readable=True), nargs=-1)
def bind(files_or_dir, o):
    """Binds horcruxes back into the original. files-or-dir may be a list of files or a directory containing a list of horcrux files"""
    import os
    if os.path.dirname(o): os.makedirs(os.path.dirname(o), exist_ok=True)

    from cruxreverser import HorcruxReverseManager
    files = files_or_dir
    if len(files_or_dir) == 1 and os.path.isdir(files_or_dir[0]):
        files = [os.path.join(files_or_dir[0], file) for file in os.listdir(files_or_dir[0])]

    try:
        hrm = HorcruxReverseManager(files, o)
        hrm.decrypt()
    except ValueError as e:
        import sys
        print(f"Invalid arguments: {e}", file=sys.stderr)
    else:
        print("Operation successful.")

if __name__ == '__main__':
    cli()