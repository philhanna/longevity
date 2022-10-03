from pathlib import Path

project_root_dir = Path(__file__).parent.parent
testdata = project_root_dir / "testdata"

__all__ = [
    'project_root_dir',
    'testdata',
]
