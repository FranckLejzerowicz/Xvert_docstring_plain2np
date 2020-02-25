# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click

from Xvert_docstring_plain2np import __version__
from Xvert_docstring_plain2np._xvert import xvert


@click.command()
@click.option(
    "-i", "--i-folder", required=True,
    help="Folder to walk through to find files for conversion."
)
@click.option(
    "-o", "--o-mv", required=False, show_default=True, default=None,
    help="File path to the script to run to replace the non-converted "
         "files with the converted files (after checking)."
)
@click.version_option(__version__, prog_name="Xvert_docstring_plain2np")


def standalone_xvert(i_folder, o_mv):
    xvert(i_folder, o_mv)


if __name__ == "__main__":
    standalone_xvert()