#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test_colr.py
    Run a few tests for the Colr library.
    -Christopher Welborn 08-30-2015
"""

from docopt import docopt
import os
import sys

from colr import __version__, color, Colr

NAME = 'Test Colr'
VERSIONSTR = '{} v. {}'.format(NAME, __version__)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

USAGESTR = """{versionstr}
    Usage:
        {script} [-h | -v]

    Options:
        -h,--help     : Show this help message.
        -v,--version  : Show version.
""".format(script=SCRIPT, versionstr=VERSIONSTR)


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    print('Running {}'.format(color(VERSIONSTR, fore='red', style='bright')))
    maxwidth = 78
    chunkwidth = maxwidth / 3
    # Gradient back color.
    print(Colr().gradient(' ' * maxwidth, start=232, fore='reset'))
    # Explicit gradient fore color.
    print(Colr().gradient('-' * maxwidth, start=232, step=2, back='blue'))
    # Implicit gradient fore color.
    print(Colr().gradient('_' * maxwidth, start=235), end='\n\n')

    try:
        # Both fore and back are not allowed in a gradient.
        print(
            Colr().gradient(
                ' ' * maxwidth,
                start=232,
                fore='white',
                back='white'))
    except ValueError:
        pass

    # Justified text should be chainable.
    print(
        Colr()
        .ljust(chunkwidth, text='Left', fore=255, back='green', style='b')
        .center(chunkwidth, text='Middle', fore=255, back='blue', style='b')
        .rjust(chunkwidth, text='Right', fore=255, back='red', style='b')
    )
    # Chained formatting must provide the 'text' argument,
    # otherwise the string is built up and the entire string width grows.
    # This built up string would then be padded, instead of each individual
    # string.
    print(
        Colr()
        # 256 color methods can be called with bg_<num>, b_<num>, b256_<num>.
        .b_82().b().f_255().ljust(chunkwidth, text='Left')
        .b256_56().b().f_255().center(chunkwidth, text='Middle')
        # Named background color start with 'bg' or 'b_'
        .bgred().b().f_255().rjust(chunkwidth, text='Right')
    )
    # Width should be calculated without color codes.
    print(Colr('True Middle').center(maxwidth, fore='magenta'))

    # Squeezed justification should account for existing text width.
    # But if text was previously justified, don't ruin it.
    print(Colr('Lefty', fore=232, back=255).center(
        maxwidth,
        text='Center',
        fore=232,
        back='blue',
        style='bright',
        squeeze=True))
    print(
        Colr('LeftyCenter'.center(maxwidth // 2), fore=232, back=255)
        .center(
            maxwidth / 2,
            text='Center',
            fore=232,
            back='blue',
            style='bright',
            squeeze=True
        )
    )

    def fancy_log(label, msg, tag):
        """ Squeezed justification with complex joins should account for
            existing text width.
        """
        return (
            Colr(label, fore='green')
            .center(
                # Centering on maxwidth would ruin the next rjust because
                # the spaces created by .center will not be overwritten.
                maxwidth - (len(tag) + 2),
                text=msg,
                fore='yellow',
                squeeze=True
            )
            .rjust(
                maxwidth,
                text=Colr(tag, fore='red').join(
                    '[', ']',
                    fore='blue'
                ),
                squeeze=True)
        )
    print(fancy_log('This is a label:', 'This is centered.', 'Status: Okay'))

    print(Colr('|', fore='blue').join(
        'This is regular text.'.ljust(maxwidth // 2 - 1),
        Colr('This is colored.', fore='red').rjust(maxwidth // 2)
    ))
    return 0

if __name__ == '__main__':
    mainret = main(docopt(USAGESTR, version=VERSIONSTR))
    sys.exit(mainret)