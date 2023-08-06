import sys
import os

# If we are not running as a package, add project root to path
if not __package__:
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

if __name__ == "__main__":
    from tat.gui.main import main as _main
    sys.exit(_main())
