import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class DataProfiler:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Don't consider columns with infinite values or all-null as numeric
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        self.numeric_cols = [col for col in numeric_cols 
                           if not (df[col].isna().all() or 
                                 any(np.isinf(df[col].dropna())))]
        self.categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns

    def _convert_to_serializable(self, obj: Any) -> Any:
        """Convert numpy types to Python native types."""
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8, np.uint16,
            np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            if np.isnan(obj) or pd.isna(obj):
                return None
            elif np.isinf(obj):
                return str(obj)  # Convert infinity to string representation
            return float(obj)
        elif isinstance(obj, (np.bool_)):
            return bool(obj)
        elif isinstance(obj, (np.ndarray,)):
            return [self._convert_to_serializable(x) for x in obj.tolist()]
        elif isinstance(obj, pd.Series):
            return [self._convert_to_serializable(x) for x in obj.tolist()]
        elif isinstance(obj, pd.DataFrame):
            return {col: [self._convert_to_serializable(x) for x in obj[col].tolist()] for col in obj.columns}
        elif isinstance(obj, dict):
            return {str(k): self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._convert_to_serializable(x) for x in obj]
        elif isinstance(obj, (datetime, pd.Timestamp)):
            return obj.isoformat()
        elif pd.isna(obj):
            return None
        elif isinstance(obj, (complex, np.complex64, np.complex128)):
            return str(obj)
        return str(obj) if not isinstance(obj, (str, int, float, bool, type(None))) else obj

    def _ensure_json_serializable(self, obj: Any) -> Any:
        """Ensure an object is JSON serializable by testing it."""
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            return self._convert_to_serializable(obj)

    def generate_profile(self) -> Dict[str, Any]:
        """Generate comprehensive profile for all columns."""
        profile = {}
        
        for col in self.df.columns:
            profile[col] = self._profile_column(col)
            
        return profile

    def _truncate_string(self, s: str, max_length: int = 100) -> str:
        """Truncate a string to a maximum length."""
        return s[:max_length] + '...' if len(s) > max_length else s

    def _profile_column(self, column: str) -> Dict[str, Any]:
        """Generate profile for a single column."""
        series = self.df[column]
        
        # Handle empty or all-null columns
        if series.empty or series.isna().all():
            return {
                "data_type": str(series.dtype),
                "missing_count": len(series),
                "missing_percentage": 100.0,
                "unique_count": 0,
                "top_values": {}
            }
        
        missing_count = series.isna().sum()
        total_count = len(series)
        
        # Handle value counts with truncation for string values
        value_counts = series.value_counts()
        top_values = {}
        for k, v in value_counts.head(5).items():
            key = str(k)
            if isinstance(k, str) and len(k) > 100:
                key = self._truncate_string(k)
            top_values[key] = self._convert_to_serializable(v)
        
        profile = {
            "data_type": str(series.dtype),
            "missing_count": self._convert_to_serializable(missing_count),
            "missing_percentage": self._convert_to_serializable(missing_count / total_count * 100 if total_count > 0 else 0),
            "unique_count": self._convert_to_serializable(series.nunique() or 0),
            "top_values": top_values
        }
        
        if column in self.numeric_cols:
            non_null = series.dropna()
            if len(non_null) > 0:
                profile["numeric_stats"] = {
                    "mean": self._convert_to_serializable(non_null.mean()),
                    "std": self._convert_to_serializable(non_null.std()),
                    "min": self._convert_to_serializable(non_null.min()),
                    "max": self._convert_to_serializable(non_null.max()),
                    "median": self._convert_to_serializable(non_null.median()),
                    "skewness": self._convert_to_serializable(stats.skew(non_null) if len(non_null) > 2 else 0),
                    "kurtosis": self._convert_to_serializable(stats.kurtosis(non_null) if len(non_null) > 2 else 0)
                }
        
        if column in self.datetime_cols:
            non_null = series.dropna()
            if len(non_null) > 0:
                profile["temporal_stats"] = {
                    "min_date": self._convert_to_serializable(non_null.min()),
                    "max_date": self._convert_to_serializable(non_null.max()),
                    "date_range_days": (non_null.max() - non_null.min()).days
                }
            
        return profile

    def generate_visualizations(self) -> Dict[str, Dict[str, Any]]:
        """Generate appropriate visualizations for all columns."""
        visualizations = {}
        
        try:
            # Numeric columns
            for col in self.numeric_cols:
                if self.df[col].nunique() > 1:  # Only visualize if there's variation
                    fig = px.histogram(self.df, x=col, nbins=30)
                    viz_dict = self._ensure_json_serializable(fig.to_dict())
                    visualizations[f"{col}_histogram"] = viz_dict
                
            # Categorical columns
            for col in self.categorical_cols:
                value_counts = self.df[col].value_counts()
                if len(value_counts) > 0 and len(value_counts) <= 20:  # Only for reasonable number of categories
                    df_plot = pd.DataFrame({
                        'category': value_counts.index,
                        'count': value_counts.values
                    })
                    fig = px.bar(df_plot, x='category', y='count')
                    viz_dict = self._ensure_json_serializable(fig.to_dict())
                    visualizations[f"{col}_bar"] = viz_dict
                    
            # Time series
            for col in self.datetime_cols:
                if self.df[col].nunique() > 1:  # Only visualize if there's variation
                    df_plot = self.df.copy()
                    df_plot[col] = df_plot[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
                    fig = px.line(df_plot, x=col)
                    viz_dict = self._ensure_json_serializable(fig.to_dict())
                    visualizations[f"{col}_line"] = viz_dict
                
            # Correlation matrix for numeric columns
            if len(self.numeric_cols) > 1 and len(self.df) > 1:  # Need at least 2 numeric columns and 2 rows
                corr_matrix = self.df[self.numeric_cols].corr()
                fig = px.imshow(
                    corr_matrix.values,
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns
                )
                viz_dict = self._ensure_json_serializable(fig.to_dict())
                visualizations["correlation_heatmap"] = viz_dict
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")
            raise RuntimeError(f"Failed to generate visualizations: {str(e)}")
                
        return visualizations

    def generate_summary(self) -> str:
        """Generate natural language summary of the dataset."""
        summary_parts = []
        
        # Basic dataset information
        summary_parts.append(
            f"This dataset has {len(self.df)} rows and {len(self.df.columns)} columns."
        )
        
        # Data types summary
        type_counts = []
        if len(self.numeric_cols) > 0:
            type_counts.append(f"{len(self.numeric_cols)} numeric columns")
        if len(self.categorical_cols) > 0:
            type_counts.append(f"{len(self.categorical_cols)} categorical columns")
        if len(self.datetime_cols) > 0:
            type_counts.append(f"{len(self.datetime_cols)} datetime columns")
        
        if type_counts:
            summary_parts.append(f"It contains {', '.join(type_counts)}.")
        
        # Special data types
        special_types = []
        if any('text' in str(self.df[col].dtype).lower() for col in self.df.columns):
            special_types.append("text")
        if any(self.df[col].astype(str).str.contains('[^\x00-\x7F]').any() for col in self.df.columns):
            special_types.append("special characters")
        if special_types:
            summary_parts.append(f"The dataset includes {' and '.join(special_types)} data.")
        
        # Missing values
        total_missing = self.df.isna().sum().sum()
        if total_missing > 0:
            summary_parts.append(
                f"There are {total_missing} missing values across all columns."
            )
            
        # Empty columns
        empty_cols = [col for col in self.df.columns if self.df[col].empty]
        if empty_cols:
            summary_parts.append(f"There are {len(empty_cols)} empty columns.")
            
        # Correlation insights
        if len(self.numeric_cols) > 1 and len(self.df) > 1:
            corr_matrix = self.df[self.numeric_cols].corr()
            high_corr = np.where(np.abs(corr_matrix) > 0.8)
            high_corr_pairs = [(corr_matrix.index[x], corr_matrix.columns[y], corr_matrix.iloc[x, y])
                              for x, y in zip(*high_corr) if x != y]
            
            if high_corr_pairs:
                pair = high_corr_pairs[0]
                summary_parts.append(
                    f"There is a strong correlation ({float(pair[2]):.2f}) between {pair[0]} and {pair[1]}."
                )
        
        return " ".join(summary_parts)

    def generate_specific_visualization(self, viz_type: str, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate a specific type of visualization."""
        try:
            # First check if visualization type is supported
            if viz_type not in ["histogram", "bar", "line", "correlation"]:
                raise ValueError(f"Unsupported visualization type: {viz_type}")
            
            # Then check for required columns
            if viz_type != "correlation":
                if not columns or not columns[0] in self.df.columns:
                    raise ValueError("Invalid column specified")
                
            if viz_type == "histogram" and columns:
                if self.df[columns[0]].nunique() <= 1:
                    raise RuntimeError("Insufficient variation for visualization")
                fig = px.histogram(self.df, x=columns[0], nbins=30)
                return self._ensure_json_serializable(fig.to_dict())
                
            elif viz_type == "bar" and columns:
                value_counts = self.df[columns[0]].value_counts()
                if len(value_counts) == 0:
                    raise RuntimeError("No data available for visualization")
                df_plot = pd.DataFrame({
                    'category': value_counts.index,
                    'count': value_counts.values
                })
                fig = px.bar(df_plot, x='category', y='count')
                return self._ensure_json_serializable(fig.to_dict())
                
            elif viz_type == "line" and columns:
                if self.df[columns[0]].nunique() <= 1:
                    raise RuntimeError("Insufficient variation for visualization")
                df_plot = self.df.copy()
                if columns[0] in self.datetime_cols:
                    df_plot[columns[0]] = df_plot[columns[0]].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
                fig = px.line(df_plot, x=columns[0])
                return self._ensure_json_serializable(fig.to_dict())
                
            elif viz_type == "correlation":
                if len(self.numeric_cols) <= 1:
                    raise RuntimeError("Insufficient numeric columns for correlation")
                if len(self.df) <= 1:
                    raise RuntimeError("Insufficient data for correlation")
                corr_matrix = self.df[self.numeric_cols].corr()
                fig = px.imshow(
                    corr_matrix.values,
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns
                )
                return self._ensure_json_serializable(fig.to_dict())
            
        except ValueError as e:
            # Re-raise ValueError exceptions directly
            raise e
        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
            raise RuntimeError(f"Failed to generate visualization: {str(e)}") 