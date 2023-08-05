# rainbowprint
A Python 3 module that allows you to print your Python3 command line output in pretty colors.  Print the rainbow!

## Prerequisites
This module requires python3 (version 3.6 or later) and python3-pip.

These prerequisites can be installed on a Debian based linux machine, like so:

`sudo apt-get install python3 python3-pip`

## Installing

Via Python pip:

`pip install rainbowprint`

## Usage
Import the rprint function, like so:

`from rainbowprint import rprint`

Use the rprint() function to print any object you want (string, boolean, integer, etc.):

```python
from rainbowprint import rprint

example_object = 'An example string\n' * 24
rprint(example_object)
```

You can select a color sequence by passing the 'seq' argument, like so:

`rprint('Some example text', seq=1)`

There are currently only two gradients to choose from [0 or 1].  More will be added in future releases.  If no seq argument is passed, then rprint will default to sequence 0.

If seq=1, you can also pass a start and end color as well:

`rprint('Some example text', seq=1, start='blue', end='white')`

'start' and 'end' are optional, and their defaults are 'red' and 'blue' respectively.

The optional arguments for python's print() can also be passed to rprint():

`rprint('Some example text', seq=1, sep=None, end='', file=None, flush=True)`

#### rprint(text: object, seq: int = 0, **kwargs) -> None
Prints text in color pattern, based on the selected sequence (seq).
This function can also take the same arguments as Python's print()
via **kwargs.

#### magenta_gradient() -> Generator[int, None, None]
Generates an integer that corresponds to a color in this gradient.

#### basic_gradient(start: str='', end: str='') -> Generator[int, None, None]
Generates an integer that corresponds to a color in this gradient.
A start color and an end color can be specified via the start and
end parameters.  The default start and end are 'red'
and 'blue' respectively.