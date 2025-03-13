"""A Script to update notebook for colab compatibility.

This extensions adds a first cell to the notebook with the necessary
dependencies to run the notebook.
"""

import os
from pathlib import Path
import argparse
import glob

import nbformat as nbf


def _arg2path(p:str) -> Path:
    return Path(p).absolute()

if __name__ == "__main__":
    # Get all the notebooks in the src directory
    parser = argparse.ArgumentParser()
    parser.add_argument("--header_notebook", type=_arg2path, default=Path(__file__).parent / "header_colab.ipynb")
    parser.add_argument("--notebook_dir", type=_arg2path, default=Path(__file__).parent.parent / 'src')
    parser.add_argument("--inplace", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()
    os.chdir(args.notebook_dir)


    header_nbk = nbf.read(args.header_notebook, as_version=4)
    for notebook_file in glob.glob("*.ipynb"):
        nbk = nbf.read(notebook_file, as_version=4)
        nbk.cells = [nbk.cells[0], *header_nbk.cells, *nbk.cells[1:]]

        if args.inplace:
            nbf.write(nbk, notebook_file)
        else:
            nbf.write(nbk, Path(notebook_file).stem + "_updated.ipynb")

    # in the CI pipeline, these new notebook will be uploaded to a new branch
