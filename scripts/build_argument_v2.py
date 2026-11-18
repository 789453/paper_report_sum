"""Export sources; optionally compile or regenerate DOCX on explicit request."""
from pathlib import Path
import subprocess
import sys
from argument_v2_content import load_slides

ROOT = Path(__file__).resolve().parents[1]
load_slides()
subprocess.run([sys.executable, str(ROOT / 'scripts/build_argument_v2_generated.py'), *sys.argv[1:]],
               cwd=ROOT, check=True)
