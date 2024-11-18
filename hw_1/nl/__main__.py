import click
import sys

@click.command()
@click.option("-w", '--width', required=False, default=6,
            help="the number of characters to be occupied by the line number. Default is 6")
@click.argument("file", type=click.File("r"), required=False)
def _cli(width, file):
    """The same as wl -b a: line numbering of file or stdin
    
    If file is absent - reads from stdin.
    """
    if file is None:
        file = sys.stdin

    number_input(file, width)

def number_input(input, width):
    i = 1
    while line := input.readline():
        print(f"{str(i) : >{width}} {line}", end="")
        i += 1

if __name__ == "__main__":
    _cli()
