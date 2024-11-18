# 1.1 nl

## Задание
Написать упрощенный вариант утилиты `nl` -- скрипт, который выдает в `stdout` пронумерованные строки из файла.
Если файл не передан, то скрипт читает строки из `stdin`.

Он должен работать так же, как `nl -b a`.

## Запуск

### Stdin 
```
$ echo "hello\n\nworld" | python -m nl
     1 hello
     2 
     3 world
```

### Файл
```
$ python -m nl nl/__main__.py
     1 import click
     2 import sys
     3 
     4 @click.command()
     5 @click.option("-w", '--width', required=False, default=6,
     6             help="the number of characters to be occupied by the line number. Default is 6")
     7 @click.argument("file", type=click.File("r"), required=False)
     8 def _cli(width, file):
     9     """The same as wl -b a: line numbering of file or stdin
    10     
    11     If file is absent - reads from stdin.
    12     """
    13     if file is None:
    14         file = sys.stdin
    15 
    16     number_input(file, width)
    17 
    18 def number_input(input, width):
    19     i = 1
    20     while line := input.readline():
    21         print(f"{str(i) : >{width}} {line}", end="")
    22         i += 1
    23 
    24 if __name__ == "__main__":
    25     _cli()
```

# 1.2 tail

Написать упрощенный вариант утилиты `tail` -- скрипт, выводящий в `stdout` последние 10 строк каждого из переданных файлов.

если передано больше одного файла, то перед обработкой очередного файла необходимо вывести его имя. Подробности смотрите в оригинальной утилите `tail`, ваш скрипт должен повторять форматирование.
если не передано ни одного файла, то нужно вывести последние 17 строк из `stdin`.

## Запуск

### Stdin
```
$ cat nl/__main__.py | python -m tail | nl -b a 
     1      number_input(file, width)
     2
     3  def number_input(input, width):
     4      i = 1
     5      while line := input.readline():
     6          print(f"{str(i) : >{width}} {line}", end="")
     7          i += 1
     8
     9  if __name__ == "__main__":
    10      _cli()
```

### Один файл

```
$ python -m tail nl/__main__.py | nl -b a
     1      number_input(file, width)
     2
     3  def number_input(input, width):
     4      i = 1
     5      while line := input.readline():
     6          print(f"{str(i) : >{width}} {line}", end="")
     7          i += 1
     8
     9  if __name__ == "__main__":
    10      _cli()
```

### Несколько файлов
```
$ python -m tail nl/__main__.py tail/__main__.py | nl -b a
     1  ==> nl/__main__.py <==
     2      number_input(file, width)
     3
     4  def number_input(input, width):
     5      i = 1
     6      while line := input.readline():
     7          print(f"{str(i) : >{width}} {line}", end="")
     8          i += 1
     9
    10  if __name__ == "__main__":
    11      _cli()
    12
    13  ==> tail/__main__.py <==
    14      queue = []
    15      for line in input:
    16          queue.append(line.rstrip())
    17          if len(queue) > lines_number:
    18              queue.pop(0)
    19
    20      print(*queue, sep="\n")
    21
    22  if __name__ == "__main__":
    23      _cli()
```

# 1.3 wc

## Задание

Написать скрипт, работающий так же, как утилита `wc`, вызванная без дополнительных опций.
Т.е. для каждого переданного файла утилита выводит статистику (3 числа) и имя файла.

При этом

если передано больше одного файла, то в самом конце утилита выводит суммарную статистику (total),
если ни одного файла не передано, то утилита считывает весь вход и печатает для него статистику без имени.

## Запуск

## Stdin

```
✗ echo "hello\nworld!   \n\nlalala\n" | python -m wc
       5       3      25
```

## Несколько файлов
```
$ python -m wc tail/__main__.py wc/__main__.py
      37      90     935 tail/__main__.py
      43     112    1041 wc/__main__.py
      80     202    1976 total
```

## Сравнение с выхлопом wc
```
$ diff <(python -m wc tail/__main__.py wc/__main__.py) <(wc tail/__main__.py wc/__main__.py)
$ echo $?
0

$diff <(echo "hello\nworld!   \n\nlalala\n" | wc) <(echo "hello\nworld!   \n\nlalala\n" | python -m wc)
$ echo $?
0
```