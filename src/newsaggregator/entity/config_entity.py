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
class DataCategorizingConfig:
    root_dir: Path
    input_path: Path
    output_path: Path
    categories_keywords: Dict[str, List[str]]
   


@dataclass
class DataLabellingConfig:
    root_dir:Path
    input_path : Path
    output_path: Path
    reputable_sources: List[str]
    suspicious_domain_patterns: List[str]
    sensational_keywords: List[str]
    thresholds: Dict[str, float]
    model_path : Path
@dataclass
class DataCleaningConfig:
    root_dir:Path
    input_path : Path
    output_path: Path
    date_column : str
    text_columns : List[str]
    
