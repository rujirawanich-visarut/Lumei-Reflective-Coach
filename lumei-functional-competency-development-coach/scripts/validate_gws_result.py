"""Portable local validator; host execution is external."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'shared/runtime'))
from gws_runtime import cli
if __name__ == '__main__': raise SystemExit(cli('WorkplaceSkillsResult'))
