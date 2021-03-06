# Colr

A python module for using terminal colors in linux. It contains a simple
`color` function that accepts style and color names, and outputs a string
with escape codes, but also has all colors and styles as chainable methods
on the `Colr` object.

_______________________________________________________________________________

## Dependencies:

### System

* **Python 3.5+** -
    This library uses `yield from` and the `typing` module.
    [Python 2 support is not planned.](#python-2)

### Modules

*There are no dependencies required for importing this library on Linux*, however:

* [Docopt](https://github.com/docopt/docopt) -
    Only required for the [command line tool](#colr-tool)
    and the [colr.docopt wrapper](#colrdocopt), not the library itself.
* [Colorama](https://github.com/tartley/colorama) -
    [Windows only](#windows).
    This is not required on linux.
    It provides a helper for basic color support for Windows.

## Installation:

Colr is listed on [PyPi](https://pypi.python.org/pypi/Colr),
and can be installed using [pip](https://pip.pypa.io/en/stable/installing/):

```
pip install colr
```

Or you can clone the repo on [GitHub](https://github.com/welbornprod/colr)
and install it from the command line:

```
git clone https://github.com/welbornprod/colr.git
cd colr
python3 setup.py install
```

## Examples:

### Simple:

```python
from colr import color
print(color('Hello world.', fore='red', style='bright'))
```

### Chainable:
```python
from colr import Colr as C
print(
    C()
    .bright().red('Hello ')
    .normal().blue('World')
)

# Background colors start with 'bg', and AttributeError will be raised on
# invalid method names.
print(C('Hello ', fore='red').bgwhite().blue('World'))

```

## Examples (256 Colors):

### Simple:

```python
from colr import color
# Invalid color names/numbers raise a ValueError.
print(color('Hello world', fore=125, back=80))
```

### Chainable:

```python
from colr import Colr as C
# Foreground colors start with 'f_'
# Background colors start with 'b_'
print(C().f_125().b_80('Hello World'))
```

## Examples (True Color):

### Simple:

```python
from colr import color
print(color('Hello there.', fore=(255, 0, 0), back=(0, 0, 0)))
```

### Chainable:

```python
from colr import Colr as C
# Foreground colors are set with the `rgb()` method.
# Background colors are set with the `b_rgb()` method.
# Text for the chained methods should be chained after or during
# the call to the methods.
print(C().b_rgb(0, 0, 0).rgb(255, 0, 0, 'Hello there.'))
```

## Examples (Hex):

### Simple:

```python
from colr import color
# When not using the Colr.hex method, the closest matching extended code
# is used. For true color, just use:
#     fore=hex2rgb('ff0000')
# or
#     Colr.hex('ff0000', rgb_mode=True)
print(color('Hello there.', fore='ff0000', back='000'))
```

### Chainable:

```python
from colr import Colr as C
# Foreground colors are set with the `hex()` method.
# Background colors are set with the `b_hex()` method.
# Text for the chained methods should be chained after or during
# the call to the methods.
print(C().b_hex('#000').hex('ff0000', 'Hello there.'))

# With rgb_mode set, these are the same:
print(C().hex('ff0000', 'test', rgb_mode=True))
print(C().rgb(255, 0, 0, 'test'))
```

_______________________________________________________________________________


## Other methods:

The `Colr` object has several helper methods.
The `color()` method returns a `str`, but the rest return a `Colr` instance
so they can be chained.
A chainable version of `color()` does exist (`chained()`), but it's not really
needed outside of the `colr` module itself.

### Colr.center

Like `str.center`, except it ignores escape codes.

```python
Colr('Hello', fore='green').center(40)

# This also ignores escape codes:
'{:^40}'.format(Colr('Hello', fore='green'))
```

### Colr.format

Like `str.format`, except it operates on `Colr.data`.

```python
Colr('Hello').blue(' {}').red(' {}').format('my', 'friend').center(40)
```

### Colr.gradient

Like `rainbow()`, except a known name can be passed to choose the color
(same names as the basic fore colors).

```python
(Colr('Wow man, ').gradient(name='red')
.gradient('what a neat feature that is.', name='blue'))
```

### Colr.gradient_black

Builds a black and white gradient. The default starting color is black, but
white will be used if `reverse=True` is passed. Like the other `gradient/rainbow`
functions, if you pass a `fore` color, the background will be gradient.

```python
(C('Why does it have to be black or white?').gradient_black(step=3)
.gradient_black(' ' * 10, fore='reset', reverse=True))
```

### Colr.gradient_rgb

Uses true color (rgb codes) to build a gradient from one rgb value to another.
Just like the other `gradient/rainbow` methods, passing a `fore` color means
the background is gradient.

When using `linemode=True` (where each line is a separate gradient), you can
"shift" the gradient left or right for each line using `movefactor=N`. `N` can
be positive or negative to change the direction of the shift, or `None` / `0`
to not shift at all (the default is `None`).

```python
C('This is pretty fancy.').gradient_rgb((0, 0, 255), (255, 0, 0), step=5)
```

### Colr.hex

This will set the fore color using hex values. It accepts
the same args as the other chained methods, except the hex value should be the
first argument. With `rgb_mode=True`, the value is converted straight to
a true color (rgb) code.

```python
# This will use true color (rgb) codes, equivalent to Colr.rgb(255, 55, 55).
Colr().hex('ff3737', rgb_mode=True).bgwhite('Test')
# Without `rgb_mode`, it finds the nearset extended terminal color.
# This is equivalent to extended code 203, or rgb(255, 95, 95).
Colr().hex('ff3737').bgwhite('Test')
```

### Colr.join

Joins `Colr` instances or other types together.
If anything except a `Colr` is passed, `str(thing)` is called before
joining. `join` accepts multiple args, and any list-like arguments are
flattened at least once (simulating str.join args).

```python
Colr('alert', 'red').join('[', ']').yellow(' This is neat.')
```

### Colr.ljust

Like `str.ljust`, except it ignores escape codes.

```python
Colr('Hello', 'blue').ljust(40)

# This also ignores escape codes:
'{:<40}'.format(Colr('Hello', 'blue'))
```

### Colr.rainbow

Beautiful rainbow gradients in the same style as [lolcat](https://github.com/busyloop/lolcat).
This method is incapable of doing black and white gradients. That's what
`gradient_black()` is for.

```python
Colr('This is really pretty.').rainbow(freq=.5)
```

If your terminal supports it, you can use true color (rgb codes) by using
`rgb_mode=True`:

```python
Colr('This is even prettier.').rainbow(rgb_mode=True)
```

### Colr.rgb

This will set the fore color using true color (rgb codes). It accepts
the same args as the other chained methods, except the `r`, `g`, and `b`
values should be the first arguments.

```python
Colr().rgb(255, 55, 55).bgwhite('Test')
```

It has a background version called `b_rgb`.

```python
Colr().b_rgb(255, 255, 255).rgb(255, 55, 55, 'Test')
```

### Colr.rjust

Like `str.rjust`, except it ignores escape codes.

```python
Colr('Hello', 'blue').rjust(40)

# This also ignores escape codes:
'{:>40}'.format(Colr('Hello', 'blue'))
```

### Colr.str

The same as calling `str()` on a `Colr` instance.
```python
Colr('test', 'blue').str() == str(Colr('test', 'blue'))
```

### Colr.stripped

The same as calling `strip_codes(Colr().data)`.
```python
data = 'Testing this.'
colored = Colr(data, fore='red')
data == colored.stripped()
```

### Colr.\_\_add\_\_

Strings can be added to a `Colr` and the other way around.
Both return a `Colr` instance.

```python
Colr('test', 'blue') + 'this' == Colr('').join(Colr('test', 'blue'), 'this')
'test' + Colr('this', 'blue') == Colr('').join('test', Colr(' this', 'blue'))

```

### Colr.\_\_bytes\_\_

Calling `bytes()` on a `Colr` is like calling `Colr().data.encode()`. For
custom encodings, you can use `str(Colr()).encode(my_encoding)`.

```python
bytes(Colr('test')) = 'test'.encode()
```

### Colr.\_\_call\_\_

`Colr` instances are callable themselves.
Calling a `Colr` will append text to it, with the same arguments as `color()`.

```python
Colr('One', 'blue')(' formatted', 'red')(' string.', 'blue')
```

### Colr.\_\_eq\_\_, \_\_ne\_\_

`Colr` instances can also be compared with other `Colr` instances.
They are equal if `self.data` is equal to `other.data`.

```python
Colr('test', 'blue') == Colr('test', 'blue')
Colr('test', 'blue') != Colr('test', 'red')
```

### Colr.\_\_lt\_\_, \_\_gt\_\_, \_\_le\_\_, \_\_ge\_\_
Escape codes are stripped for less-than/greater-than comparisons.

```python
Colr('test', 'blue') < Colr('testing', 'blue')
```

### Colr.\_\_getitem\_\_

Escape codes are stripped when subscripting/indexing.

```python
Colr('test', 'blue')[2] == Colr('s')
Colr('test', 'blue')[1:3] == Colr('es')
```

### Colr.\_\_hash\_\_

Hashing a `Colr` just means hashing `Colr().data`, but this works:
```python
hash(Colr('test', 'blue')) == hash(Colr('test', 'blue'))
```

### Colr.\_\_mul\_\_

`Colr` instances can be multiplied by an `int` to build color strings.
These are all equal:

```python
Colr('*', 'blue') * 2
Colr('*', 'blue') + Colr('*', 'blue')
Colr('').join(Colr('*', 'blue'), Colr('*', 'blue'))
```

_______________________________________________________________________________

## Color Translation:

The `colr` module also includes several tools for converting from one color
value to another:

### ColorCode

A class that automatically converts hex, rgb, or terminal codes to the other
types. They can be accessed through the attributes `code`, `hexval`, and `rgb`.

```python
from colr import ColorCode
print(ColorCode(30))
# Terminal:  30, Hex: 008787, RGB:   0, 135, 135

print(ColorCode('de00fa'))
# Terminal: 165, Hex: de00fa, RGB: 222,   0, 250

print(ColorCode((75, 50, 178)))
# Terminal:  61, Hex: 4b32b2, RGB:  75,  50, 178
```

Printing `ColorCode(45).example()` will show the actual color in the terminal.

### hex2rgb

Converts a hex color (`#000000`) to RGB `(0, 0, 0)`.

### hex2term

Converts a hex color to terminal code number.

```python
from colr import color, hex2term
print(color('Testing', hex2term('#FF0000')))
```
### hex2termhex

Converts a hex color to it's closest terminal color in hex.

```python
from colr import hex2termhex
hex2termhex('005500') == '005f00'
```

### rgb2hex

Converts an RGB value `(0, 0, 0)` to it's hex value (`000000`).

### rgb2term

Converts an RGB value to terminal code number.

```python
from colr import color, rgb2term
print(color('Testing', rgb2term(0, 255, 0)))
```

### rgb2termhex

Converts an RGB value to it's closest terminal color in hex.

```python
from colr import rgb2termhex
rgb2termhex(0, 55, 0) == '005f00'
```

### term2hex

Converts a terminal code number to it's hex value.

```python
from colr import term2hex
term2hex(30) == '008787'
```

### term2rgb

Converts a terminal code number to it's RGB value.

```python
from colr import term2rgb
term2rgb(30) == (0, 135, 135)
```
_______________________________________________________________________________


## Colr Tool:

The `colr` package can be used as a command line tool. An entry point script
named `colr` is created when installed with pip. Otherwise it can be executed
using the `python -m colr` method.
```bash
colr --help
```

Basic usage involves passing text, or piping stdin data and setting the colors
by position or flag.

```bash
# These all do the same thing:
colr "Test" "red" "white" "bright"
colr "Test" -f "red" -b "white" -s "bright"
printf "Test" | colr -f "red" -b "white" -s "bright"
```

Using the positional arguments is faster for just setting fore colors, but
the flag method is needed for stdin data, or for picking just the background
color or style:

```bash
colr "Test" -s "bright"
```

Extended and True colors are supported:
```bash
colr "Test" 124 255
colr "Test" "255, 0, 0" "255, 255, 255"
# Use true color (rgb) escape codes to generate a gradient, and then
# center it in the terminal (0 means use terminal width).
colr "Test" -G "255,0,0" -G "0,0,255" -c 0
```

It will do fore, back, style, gradients, rainbows, justification,
and translation.
It can strip codes from text (as an argument or stdin), or explain the
codes found in the text.

[lolcat](https://github.com/busyloop/lolcat) emulation:
```bash
fortune | colr --rainbow
```

The colr tool does not read files, but it's not a problem:
```bash
cat myfile.txt | colr --gradient red
```

Also see [ccat](https://github.com/welbornprod/ccat).


## Colr.docopt:

Colr provides a wrapper for docopt that will automatically colorize usage
strings. If you provide it a script name it will add a little more color by
colorizing the script name too.
```python
from colr import docopt
argd = docopt(USAGE, script='mycommand')
```

_______________________________________________________________________________

## Contributing:

As always contributions are welcome here. If you think you can improve something,
or have a good idea for a feature, please file an
[issue](https://github.com/welbornprod/colr/issues/new) or a
[pull request](https://github.com/welbornprod/colr/compare).

_______________________________________________________________________________

## Notes:

### Reasons

In the past, I used a simple `color()` function because I'm not fond of the
string concatenation style that other libraries use. The 'clor' javascript
library uses method chaining because that style suits javascript, but I wanted
to make it available to Python also, at least as an option.

### Reset Codes

The reset code is appended only if some kind of text was given, and
colr/style args were used. The only values that are considered 'no text'
values are `None` and `''` (empty string). `str(val)` is called on all other
values, so `Colr(0, 'red')` and `Colr(False, 'blue')` will work, and the reset
code will be appended.

This makes it possible to build background colors and styles, but
also have separate styles for separate pieces of text.

### Python 2

I don't really have the desire to back-port this to Python 2.
It wouldn't need too many changes, but I like the Python 3 features
(`yield from`, `str/bytes`).

### Windows

Basic colors are supported on Windows through the
[colorama](https://github.com/tartley/colorama) library.
It is only imported if `platform.system() == 'Windows'`.
It provides a wrapper around `stdout` and `stderr` to make basic ansi codes
work. If the import fails, then all color codes are disabled
(as if `colr.disable()` was called).
I booted into Windows 8 for the first time in months to make this little
feature happen, only to discover that the color situation for CMD and
PowerShell really sucks. If you think you can help improve the `colr` package
for windows, please see the [contributing](#contributing) section.

### Misc.
This library may be a little too flexible:

```python
from colr import Colr as C
warnmsg = lambda s: C('warning', 'red').join('[', ']')(' ').green(s)
print(warnmsg('The roof is on fire again.'))
```

![The possibilities are endless.](https://welbornprod.com/static/media/img/colr-warning.png)
