"""Current-paper compatibility entry; old verifier is archived."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("verify_argument_v2.py")),run_name="__main__")
