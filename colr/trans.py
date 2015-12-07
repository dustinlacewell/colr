#! /usr/bin/env python

""" Convert color code between hex value, terminal escape code, and rgb.

Original name: colortrans.py
Original author: Micah Elliott http://MicahElliott.com
Original version: 0.1

This module has been modified for use with Python 3 and the Colr library.
The original can be found here: https://gist.github.com/MicahElliott/719710
-Christopher Welborn 12-06-15

Resources:
* http://en.wikipedia.org/wiki/8-bit_color
* http://en.wikipedia.org/wiki/ANSI_escape_code
* /usr/share/X11/rgb.txt

-------------------------------------------------------------------------------


"""

from types import GeneratorType

# Original lookup table provided by Micah Elliott (colortrans.py).
# Modified to dict by Christopher Welborn.
term2hex_map = {
    #    8-bit, RGB hex
    # Primary 3-bit (8 colors). Unique representation!
    '00':  '000000',
    '01':  '800000',
    '02':  '008000',
    '03':  '808000',
    '04':  '000080',
    '05':  '800080',
    '06':  '008080',
    '07':  'c0c0c0',

    # Equivalent "bright" versions of original 8 colors.
    '08':  '808080',
    '09':  'ff0000',
    '10':  '00ff00',
    '11':  'ffff00',
    '12':  '0000ff',
    '13':  'ff00ff',
    '14':  '00ffff',
    '15':  'ffffff',

    # Strictly ascending.
    '16':  '000000',
    '17':  '00005f',
    '18':  '000087',
    '19':  '0000af',
    '20':  '0000d7',
    '21':  '0000ff',
    '22':  '005f00',
    '23':  '005f5f',
    '24':  '005f87',
    '25':  '005faf',
    '26':  '005fd7',
    '27':  '005fff',
    '28':  '008700',
    '29':  '00875f',
    '30':  '008787',
    '31':  '0087af',
    '32':  '0087d7',
    '33':  '0087ff',
    '34':  '00af00',
    '35':  '00af5f',
    '36':  '00af87',
    '37':  '00afaf',
    '38':  '00afd7',
    '39':  '00afff',
    '40':  '00d700',
    '41':  '00d75f',
    '42':  '00d787',
    '43':  '00d7af',
    '44':  '00d7d7',
    '45':  '00d7ff',
    '46':  '00ff00',
    '47':  '00ff5f',
    '48':  '00ff87',
    '49':  '00ffaf',
    '50':  '00ffd7',
    '51':  '00ffff',
    '52':  '5f0000',
    '53':  '5f005f',
    '54':  '5f0087',
    '55':  '5f00af',
    '56':  '5f00d7',
    '57':  '5f00ff',
    '58':  '5f5f00',
    '59':  '5f5f5f',
    '60':  '5f5f87',
    '61':  '5f5faf',
    '62':  '5f5fd7',
    '63':  '5f5fff',
    '64':  '5f8700',
    '65':  '5f875f',
    '66':  '5f8787',
    '67':  '5f87af',
    '68':  '5f87d7',
    '69':  '5f87ff',
    '70':  '5faf00',
    '71':  '5faf5f',
    '72':  '5faf87',
    '73':  '5fafaf',
    '74':  '5fafd7',
    '75':  '5fafff',
    '76':  '5fd700',
    '77':  '5fd75f',
    '78':  '5fd787',
    '79':  '5fd7af',
    '80':  '5fd7d7',
    '81':  '5fd7ff',
    '82':  '5fff00',
    '83':  '5fff5f',
    '84':  '5fff87',
    '85':  '5fffaf',
    '86':  '5fffd7',
    '87':  '5fffff',
    '88':  '870000',
    '89':  '87005f',
    '90':  '870087',
    '91':  '8700af',
    '92':  '8700d7',
    '93':  '8700ff',
    '94':  '875f00',
    '95':  '875f5f',
    '96':  '875f87',
    '97':  '875faf',
    '98':  '875fd7',
    '99':  '875fff',
    '100': '878700',
    '101': '87875f',
    '102': '878787',
    '103': '8787af',
    '104': '8787d7',
    '105': '8787ff',
    '106': '87af00',
    '107': '87af5f',
    '108': '87af87',
    '109': '87afaf',
    '110': '87afd7',
    '111': '87afff',
    '112': '87d700',
    '113': '87d75f',
    '114': '87d787',
    '115': '87d7af',
    '116': '87d7d7',
    '117': '87d7ff',
    '118': '87ff00',
    '119': '87ff5f',
    '120': '87ff87',
    '121': '87ffaf',
    '122': '87ffd7',
    '123': '87ffff',
    '124': 'af0000',
    '125': 'af005f',
    '126': 'af0087',
    '127': 'af00af',
    '128': 'af00d7',
    '129': 'af00ff',
    '130': 'af5f00',
    '131': 'af5f5f',
    '132': 'af5f87',
    '133': 'af5faf',
    '134': 'af5fd7',
    '135': 'af5fff',
    '136': 'af8700',
    '137': 'af875f',
    '138': 'af8787',
    '139': 'af87af',
    '140': 'af87d7',
    '141': 'af87ff',
    '142': 'afaf00',
    '143': 'afaf5f',
    '144': 'afaf87',
    '145': 'afafaf',
    '146': 'afafd7',
    '147': 'afafff',
    '148': 'afd700',
    '149': 'afd75f',
    '150': 'afd787',
    '151': 'afd7af',
    '152': 'afd7d7',
    '153': 'afd7ff',
    '154': 'afff00',
    '155': 'afff5f',
    '156': 'afff87',
    '157': 'afffaf',
    '158': 'afffd7',
    '159': 'afffff',
    '160': 'd70000',
    '161': 'd7005f',
    '162': 'd70087',
    '163': 'd700af',
    '164': 'd700d7',
    '165': 'd700ff',
    '166': 'd75f00',
    '167': 'd75f5f',
    '168': 'd75f87',
    '169': 'd75faf',
    '170': 'd75fd7',
    '171': 'd75fff',
    '172': 'd78700',
    '173': 'd7875f',
    '174': 'd78787',
    '175': 'd787af',
    '176': 'd787d7',
    '177': 'd787ff',
    '178': 'd7af00',
    '179': 'd7af5f',
    '180': 'd7af87',
    '181': 'd7afaf',
    '182': 'd7afd7',
    '183': 'd7afff',
    '184': 'd7d700',
    '185': 'd7d75f',
    '186': 'd7d787',
    '187': 'd7d7af',
    '188': 'd7d7d7',
    '189': 'd7d7ff',
    '190': 'd7ff00',
    '191': 'd7ff5f',
    '192': 'd7ff87',
    '193': 'd7ffaf',
    '194': 'd7ffd7',
    '195': 'd7ffff',
    '196': 'ff0000',
    '197': 'ff005f',
    '198': 'ff0087',
    '199': 'ff00af',
    '200': 'ff00d7',
    '201': 'ff00ff',
    '202': 'ff5f00',
    '203': 'ff5f5f',
    '204': 'ff5f87',
    '205': 'ff5faf',
    '206': 'ff5fd7',
    '207': 'ff5fff',
    '208': 'ff8700',
    '209': 'ff875f',
    '210': 'ff8787',
    '211': 'ff87af',
    '212': 'ff87d7',
    '213': 'ff87ff',
    '214': 'ffaf00',
    '215': 'ffaf5f',
    '216': 'ffaf87',
    '217': 'ffafaf',
    '218': 'ffafd7',
    '219': 'ffafff',
    '220': 'ffd700',
    '221': 'ffd75f',
    '222': 'ffd787',
    '223': 'ffd7af',
    '224': 'ffd7d7',
    '225': 'ffd7ff',
    '226': 'ffff00',
    '227': 'ffff5f',
    '228': 'ffff87',
    '229': 'ffffaf',
    '230': 'ffffd7',
    '231': 'ffffff',

    # Gray-scale range.
    '232': '080808',
    '233': '121212',
    '234': '1c1c1c',
    '235': '262626',
    '236': '303030',
    '237': '3a3a3a',
    '238': '444444',
    '239': '4e4e4e',
    '240': '585858',
    '241': '626262',
    '242': '6c6c6c',
    '243': '767676',
    '244': '808080',
    '245': '8a8a8a',
    '246': '949494',
    '247': '9e9e9e',
    '248': 'a8a8a8',
    '249': 'b2b2b2',
    '250': 'bcbcbc',
    '251': 'c6c6c6',
    '252': 'd0d0d0',
    '253': 'dadada',
    '254': 'e4e4e4',
    '255': 'eeeeee',
}

# Create a map from hex to escape codes.
hex2term_map = {v: k for k, v in term2hex_map.items()}


def fix_hex(hexval):
    hexval = hexval.strip().lstrip('#').lower()
    hexlen = len(hexval)
    if hexlen == 3:
        rgbvals = {'r': hexval[0], 'g': hexval[1], 'b': hexval[2], }
        hexval = '{r}{r}{g}{g}{b}{b}'.format(**rgbvals)
    elif hexlen != 6:
        raise ValueError(
            'Expecting a hex string (#RGB, #RRGGBB), got: {}'.format(
                hexval))
    return hexval


def hex2rgb(hexval, allow_short=False):
    """ Return a tuple of (R, G, B) from a hex color. """
    if not hexval:
        raise ValueError(
            'Expecting a hex string (#RGB, #RRGGBB), got: {}'.format(
                hexval))
    hexval = hexval.strip().lstrip('#')
    if allow_short:
        hexval = fix_hex(hexval)
    try:
        val = tuple(
            int(''.join(hexval[i:i + 2]), 16)
            for i in range(0, len(hexval), 2)
        )
    except ValueError:
        # Bad hex string.
        raise ValueError('Invalid hex value: {}'.format(hexval))
    return val


def hex2term(hexval, allow_short=False):
    """ Convert a hex value into the nearest terminal code number. """
    return rgb2term(*hex2rgb(hexval, allow_short=allow_short))


def hex2termhex(hexval, allow_short=False):
    """ Convert a hex value into the nearest terminal color matched hex. """
    return rgb2termhex(*hex2rgb(hexval, allow_short=allow_short))


def print_all():
    """ Print all 256 xterm color codes. """
    for code in sorted(term2hex_map):
        print(' '.join((
            '\033[48;5;{code}m{code:<3}:{hexval:<6}\033[0m',
            '\033[38;5;{code}m{code:<3}:{hexval:<6}\033[0m'
        )).format(code=code, hexval=term2hex_map[code]))


def rgb2hex(r, g, b):
    """ Convert rgb values to a hex code. """
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def rgb2term(r, g, b):
    """ Convert an rgb value to a terminal code. """
    return hex2term_map[rgb2termhex(r, g, b)]


def rgb2termhex(r, g, b):
    """ Convert an rgb value to the nearest hex value that matches a term code.
        The hex value will be one in `hex2term_map`.
    """
    incs = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)

    res = []
    for part in (r, g, b):
        i = 0
        while i < len(incs) - 1:
            s, b = incs[i], incs[i + 1]  # smaller, bigger
            if s <= part <= b:
                s1 = abs(s - part)
                b1 = abs(b - part)
                if s1 < b1:
                    closest = s
                else:
                    closest = b
                res.append(closest)
                break
            i += 1

    # Convert back into nearest hex value.
    return rgb2hex(*res)


def term2hex(code, default=None):
    """ Convenience function for term2hex_map.get(code, None).
        Accepts strs or ints in the form of: 1, 01, 123.
        Returns `default` if the code is not found.
    """
    return term2hex_map.get('{:02}'.format(code), default)


def term2rgb(code):
    """ Convert a terminal code to an rgb value. """
    return hex2rgb(term2hex(code))


class ColorCode(object):
    """ A color code value that automatically converts from/to hex, term, rgb.
        Initialize with a hex str, code str/int, or rgb tuple/list/generator,
        and the other codes are automatically generated and made available
        through the attributes:
            code   : Terminal code number as a string.
            hexval : Nearest matching hex value.
            rgb    : Tuple of nearest matching (Red, Green, Blue) values.
    """
    __slots__ = ['code', 'hexval', 'rgb']

    def __init__(self, code=None):
        self.rgb = tuple()
        self.hexval = None
        self.code = None

        if isinstance(code, (list, tuple, GeneratorType)):
            self._init_rgb(*code)
        elif isinstance(code, str):
            try:
                # Try hex str.
                rgb = hex2rgb(code)
                self._init_rgb(*rgb)
            except (TypeError, ValueError):
                # Int as str.
                try:
                    termcode = int(code)
                except (TypeError, ValueError):
                    # Must be hex value.
                    self._init_hex(code)
                else:
                    # Term code was passed by str.
                    self._init_code(termcode)
        elif isinstance(code, int):
            # Term code was passed.
            self._init_code(code)
        else:
            raise TypeError('Expecting hex, term-code, or rgb. Got: {}'.format(
                getattr(code, '__class__', type(code)).__name__)
            )

    def __format__(self, fmt):
        """ Pass on any format calls to str(self). """
        return str(self).__format__(fmt)

    def __str__(self):
        """ A console friendly representation. """
        return ', '.join((
            'Terminal: {s.code:>3}',
            'Hex: {s.hexval:<6}',
            'RGB: {rgb}'
        )).format(s=self, rgb=', '.join('{:>3}'.format(i) for i in self.rgb))

    def _init_code(self, code):
        """ Initialize from an int terminal code. """
        if -1 < code < 256:
            self.code = '{:02}'.format(code)
            self.hexval = term2hex(code)
            self.rgb = hex2rgb(self.hexval)
        else:
            raise ValueError(' '.join((
                'Code must be in the range 0-255, inclusive.',
                'Got: {} ({})'
            )).format(code, getattr(code, '__class__', type(code)).__name__))

    def _init_hex(self, hexval):
        """ Initialize from a hex value string. """
        self.hexval = hex2termhex(fix_hex(hexval))
        self.code = hex2term(self.hexval)
        self.rgb = hex2rgb(self.hexval)

    def _init_rgb(self, r, g, b):
        """ Initialize from red, green, blue args. """
        self.rgb = (r, g, b)
        self.hexval = rgb2hex(r, g, b)
        self.code = hex2term(self.hexval)

    def example(self):
        """ Same as str(self), except the color codes are actually used. """

        return '\033[38;5;{s.code}m{s}\033[0m'.format(s=self)

    @classmethod
    def from_code(cls, code):
        """ Return a ColorCode from a terminal code. """
        c = cls()
        c._init_code(code)
        return c

    @classmethod
    def from_hex(cls, hexval):
        """ Return a ColorCode from a hex string. """
        c = cls()
        c._init_hex(hexval)
        return c

    @classmethod
    def from_rgb(cls, r, g, b):
        """ Return a ColorCode from a RGB tuple. """
        c = cls()
        c._init_rgb(r, g, b)
        return c

if __name__ == '__main__':
    from sys import exit, stderr
    print(
        ' '.join((
            'This module is part of the Colr package,'
            'and is meant to be imported.'
        )),
        file=stderr)
    exit(1)
