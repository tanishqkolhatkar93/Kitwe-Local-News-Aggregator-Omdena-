from dataclasses import dataclass
from typing import List
from pathlib import Path
from typing import Dict

@dataclass
class DataIngestionConfig:
    root_dir:Path
    News_websites : Dict[str,str]
    output_path: Path