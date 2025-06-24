import os
import pathlib
import sys

NOTEBOOKS_DIR = pathlib.Path(__file__).parent
REPO_DIR = NOTEBOOKS_DIR.parent
PROJECT_ROOT = REPO_DIR / "src"


def init(verbose=False):
    # Apply nest_asyncio patch to allow nested event loops in Jupyter
    try:
        import nest_asyncio

        nest_asyncio.apply()
        if verbose:
            print("Applied nest_asyncio patch for Jupyter compatibility")
    except ImportError:
        if verbose:
            print("nest_asyncio not available, skipping patch")

    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, str(PROJECT_ROOT))
    if verbose:
        print(f"Changed working directory to: {PROJECT_ROOT}")