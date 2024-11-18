import click
import sys

@click.command()
@click.option("-n", "--lines", required=False, default=10,
            help="The location is number lines")
@click.argument("file", nargs=-1, type=click.Path(exists=True), required=False)
def _cli(lines, file):
    """tail - display the last part of a file"""

    if len(file) == 0:
        file = ("-",)
    
    return tail(file, lines)

def tail(filenames, lines_number):
    for i, filename in enumerate(filenames):
        input = click.open_file(filename)
        if len(filenames) > 1:
            print(f"==> {filename} <==")
        
        _tail_one(input, lines_number)
        
        if i < len(filenames) - 1:
            print()

def _tail_one(input, lines_number):
    queue = []
    for line in input:
        queue.append(line.rstrip())
        if len(queue) > lines_number:
            queue.pop(0)
    
    print(*queue, sep="\n")

if __name__ == "__main__":
    _cli()
