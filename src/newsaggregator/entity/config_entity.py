from dataclasses import dataclass
from typing import List
from pathlib import Path
from typing import Dict

@dataclass
class DataIngestionConfig:
    root_dir:Path
    input_path : Path
    output_path: Path
    
@dataclass
class DataCleaningConfig:
    root_dir:Path
    input_path : Path
    output_path: Path
    date_column : str
    text_columns : List[str]
    
