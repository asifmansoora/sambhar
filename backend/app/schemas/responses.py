from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ColumnProfile(BaseModel):
    data_type: str
    missing_count: int
    missing_percentage: float
    unique_count: int
    top_values: List[Any]
    numeric_stats: Optional[Dict[str, float]] = None
    temporal_stats: Optional[Dict[str, Any]] = None

class ProfileResponse(BaseModel):
    profile: Dict[str, ColumnProfile]
    visualizations: Dict[str, Dict[str, Any]]
    summary: str

class VisualizationResponse(BaseModel):
    plot_data: Dict[str, Any]
    viz_type: str 