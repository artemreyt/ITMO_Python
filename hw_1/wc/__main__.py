import click

@click.command()
@click.argument("file", nargs=-1, type=click.Path(exists=True), required=False)
def _cli(file):
    """wc - word, line, character, and byte count"""

    if len(file) == 0:
        file = ("-",)
    
    return wc(file)

def _print_stat(word, line, char, filename):
    print(f"{line:>8}{word:>8}{char:>8}", end="")
    if filename != "-":
        print(f" {filename}")
    else:
        print()

def wc(filenames):
    total_word, total_line, total_char = 0,0,0
    for filename in filenames:
        input = click.open_file(filename)
        word, line, char = wc_one(input)
        _print_stat(word, line, char, filename)
        total_word += word
        total_line += line
        total_char += char

    if len(filenames) > 1:
        _print_stat(total_word, total_line, total_char, "total")

def wc_one(input):
    word, line, char = 0, 0, 0
    for l in input:
        line += 1
        char += len(l)
        word += len(l.split())

    return word, line, char

if __name__ == "__main__":
    _cli()
