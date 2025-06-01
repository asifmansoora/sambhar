import pytest
import pandas as pd
import numpy as np
from app.utils.data_profiler import DataProfiler
import json
from datetime import datetime, timedelta

@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe with various data types for testing."""
    return pd.DataFrame({
        'numeric': [1, 2, 3, 4, 5, np.nan],
        'categorical': ['A', 'B', 'A', 'C', 'B', None],
        'datetime': pd.date_range(start='2024-01-01', periods=6),
        'boolean': [True, False, True, True, False, None],
        'float': [1.1, 2.2, 3.3, np.nan, 5.5, 6.6]
    })

@pytest.fixture
def edge_case_dataframe():
    """Create a dataframe with edge cases."""
    # Create a DataFrame with all columns having the same length
    df = pd.DataFrame({
        'all_null': [None] * 3,
        'extreme_values': [np.inf, -np.inf, np.nan],
        'mixed_types': ['1', 'text', '3.14'],  # Strings that look like numbers
        'special_chars': ['%$#@', '한글', '🌟'],
        'long_text': ['a' * 1000, 'b' * 500, 'c' * 100],
        'timestamps': [
            pd.Timestamp('2024-01-01'),
            pd.Timestamp('1970-01-01'),
            pd.Timestamp('2099-12-31')
        ]
    })
    
    # Create an empty column with no data
    df['empty_col'] = pd.Series([], dtype=object)
    
    return df

@pytest.fixture
def data_profiler(sample_dataframe):
    """Create a DataProfiler instance with the sample dataframe."""
    return DataProfiler(sample_dataframe)

@pytest.fixture
def edge_case_profiler(edge_case_dataframe):
    """Create a DataProfiler instance with edge case dataframe."""
    return DataProfiler(edge_case_dataframe)

def test_initialization(data_profiler, sample_dataframe):
    """Test if DataProfiler initializes correctly."""
    assert len(data_profiler.numeric_cols) == 2  # numeric and float
    assert len(data_profiler.categorical_cols) == 2  # categorical and boolean
    assert len(data_profiler.datetime_cols) == 1
    assert isinstance(data_profiler.df, pd.DataFrame)
    assert data_profiler.df.equals(sample_dataframe)

def test_edge_case_initialization(edge_case_profiler):
    """Test initialization with edge case data."""
    assert len(edge_case_profiler.numeric_cols) == 0  # No pure numeric columns
    assert len(edge_case_profiler.categorical_cols) >= 4  # mixed_types, special_chars, etc.
    assert len(edge_case_profiler.datetime_cols) == 1  # timestamps
    assert edge_case_profiler.df.shape[1] == 7  # Total number of columns

def test_convert_to_serializable(data_profiler):
    """Test conversion of various types to JSON serializable format."""
    # Test numpy types
    assert data_profiler._convert_to_serializable(np.int32(5)) == 5
    assert data_profiler._convert_to_serializable(np.float64(3.14)) == 3.14
    assert data_profiler._convert_to_serializable(np.array([1, 2, 3])) == [1, 2, 3]
    assert data_profiler._convert_to_serializable(pd.Series([1, 2, 3])) == [1, 2, 3]
    
    # Test None/NaN
    assert data_profiler._convert_to_serializable(np.nan) is None
    assert data_profiler._convert_to_serializable(None) is None
    
    # Test datetime
    test_date = pd.Timestamp('2024-01-01')
    assert isinstance(data_profiler._convert_to_serializable(test_date), str)

def test_edge_case_serialization(edge_case_profiler):
    """Test serialization of edge cases."""
    # Test infinite values
    assert edge_case_profiler._convert_to_serializable(np.inf) == float('inf')
    assert edge_case_profiler._convert_to_serializable(-np.inf) == float('-inf')
    
    # Test empty structures
    assert edge_case_profiler._convert_to_serializable(np.array([])) == []
    assert edge_case_profiler._convert_to_serializable(pd.Series([])) == []
    
    # Test special characters
    special_series = pd.Series(['%$#@', '한글', '🌟'])
    converted = edge_case_profiler._convert_to_serializable(special_series)
    assert all(isinstance(x, str) for x in converted)
    assert '한글' in converted  # Ensure Unicode is preserved
    assert '🌟' in converted  # Ensure emoji is preserved
    
    # Test large numbers
    assert edge_case_profiler._convert_to_serializable(np.float64(1e308)) == float(1e308)
    
    # Test nested structures
    nested = {
        'array': np.array([1, 2, 3]),
        'series': pd.Series([4, 5, 6]),
        'timestamp': pd.Timestamp('2024-01-01'),
        'special': '한글'
    }
    converted = edge_case_profiler._convert_to_serializable(nested)
    assert isinstance(converted, dict)
    assert isinstance(converted['array'], list)
    assert isinstance(converted['series'], list)
    assert isinstance(converted['timestamp'], str)
    assert converted['special'] == '한글'

def test_profile_generation(data_profiler):
    """Test if profile generation works and is JSON serializable."""
    profile = data_profiler.generate_profile()
    
    # Test if profile contains expected columns
    assert set(profile.keys()) == {'numeric', 'categorical', 'datetime', 'boolean', 'float'}
    
    # Test if profile is JSON serializable
    try:
        json.dumps(profile)
    except TypeError as e:
        pytest.fail(f"Profile is not JSON serializable: {e}")
    
    # Test numeric column profile
    numeric_profile = profile['numeric']
    assert 'numeric_stats' in numeric_profile
    assert numeric_profile['missing_count'] == 1
    assert numeric_profile['data_type'] == 'float64'
    
    # Test categorical column profile
    cat_profile = profile['categorical']
    assert 'top_values' in cat_profile
    assert cat_profile['unique_count'] == 3
    
    # Test datetime column profile
    datetime_profile = profile['datetime']
    assert 'temporal_stats' in datetime_profile

def test_edge_case_profile(edge_case_profiler):
    """Test profile generation with edge case data."""
    profile = edge_case_profiler.generate_profile()
    
    # Test all null column
    null_profile = profile['all_null']
    assert null_profile['missing_count'] == 3
    assert null_profile['missing_percentage'] == 100.0
    assert null_profile['unique_count'] == 0
    
    # Test extreme values
    extreme_profile = profile['extreme_values']
    assert extreme_profile['missing_count'] == 1  # np.nan
    assert 'numeric_stats' in extreme_profile
    assert np.isinf(extreme_profile['numeric_stats']['max'])
    assert np.isinf(extreme_profile['numeric_stats']['min'])
    
    # Test mixed types
    mixed_profile = profile['mixed_types']
    assert mixed_profile['unique_count'] == 3
    assert len(mixed_profile['top_values']) > 0
    
    # Test special characters
    special_profile = profile['special_chars']
    assert special_profile['unique_count'] == 3
    assert all(isinstance(k, str) for k in special_profile['top_values'].keys())
    assert any('한글' in k for k in special_profile['top_values'].keys())
    assert any('🌟' in k for k in special_profile['top_values'].keys())
    
    # Test long text
    long_profile = profile['long_text']
    assert long_profile['unique_count'] == 3
    assert all(len(k) <= 100 for k in long_profile['top_values'].keys())  # Check if truncated

def test_visualization_generation(data_profiler):
    """Test if visualization generation works and is JSON serializable."""
    visualizations = data_profiler.generate_visualizations()
    
    # Test if expected visualizations are present
    expected_viz = {
        'numeric_histogram', 'float_histogram',
        'categorical_bar', 'boolean_bar',
        'datetime_line', 'correlation_heatmap'
    }
    assert set(visualizations.keys()) >= expected_viz
    
    # Test if visualizations are JSON serializable
    try:
        json.dumps(visualizations)
    except TypeError as e:
        pytest.fail(f"Visualizations are not JSON serializable: {e}")
    
    # Test visualization content
    for viz_name, viz_data in visualizations.items():
        assert 'data' in viz_data
        assert 'layout' in viz_data

def test_edge_case_visualization(edge_case_profiler):
    """Test visualization generation with edge case data."""
    visualizations = edge_case_profiler.generate_visualizations()
    
    # Test visualization for empty column
    assert 'empty_col_bar' not in visualizations
    
    # Test visualization for all null column
    assert 'all_null_bar' not in visualizations
    
    # Test visualization for mixed types
    assert 'mixed_types_bar' in visualizations
    viz = visualizations['mixed_types_bar']
    assert 'data' in viz
    assert 'layout' in viz
    
    # Test visualization for special characters
    assert 'special_chars_bar' in visualizations
    viz = visualizations['special_chars_bar']
    assert 'data' in viz
    assert 'layout' in viz
    
    # Test if all visualizations are JSON serializable
    try:
        json.dumps(visualizations)
    except TypeError as e:
        pytest.fail(f"Edge case visualizations are not JSON serializable: {e}")

def test_summary_generation(data_profiler):
    """Test if summary generation works."""
    summary = data_profiler.generate_summary()
    
    # Test if summary contains expected information
    assert isinstance(summary, str)
    assert "6 rows" in summary
    assert "5 columns" in summary
    assert "2 numeric columns" in summary
    assert "2 categorical columns" in summary
    assert "1 datetime columns" in summary

def test_edge_case_summary(edge_case_profiler):
    """Test summary generation with edge case data."""
    summary = edge_case_profiler.generate_summary()
    
    assert isinstance(summary, str)
    assert "3 rows" in summary  # Number of rows
    assert "7 columns" in summary  # Total number of columns
    
    # Test if summary contains information about data quality
    quality_terms = ['missing', 'null', 'empty']
    assert any(term in summary.lower() for term in quality_terms)
    
    # Test if summary mentions special data types
    type_terms = ['timestamp', 'text', 'special characters']
    assert any(term in summary.lower() for term in type_terms)

def test_specific_visualization(data_profiler):
    """Test generation of specific visualizations."""
    # Test histogram
    hist = data_profiler.generate_specific_visualization("histogram", ["numeric"])
    assert isinstance(hist, dict)
    assert 'data' in hist
    assert 'layout' in hist
    
    # Test bar chart
    bar = data_profiler.generate_specific_visualization("bar", ["categorical"])
    assert isinstance(bar, dict)
    assert 'data' in bar
    assert 'layout' in bar
    
    # Test correlation
    corr = data_profiler.generate_specific_visualization("correlation")
    assert isinstance(corr, dict)
    assert 'data' in corr
    assert 'layout' in corr
    
    # Test invalid type
    with pytest.raises(ValueError):
        data_profiler.generate_specific_visualization("invalid_type")

def test_edge_case_specific_visualization(edge_case_profiler):
    """Test specific visualization generation with edge cases."""
    # Test empty column
    with pytest.raises(RuntimeError):
        edge_case_profiler.generate_specific_visualization("bar", ["empty_col"])
    
    # Test all null column
    with pytest.raises(RuntimeError):
        edge_case_profiler.generate_specific_visualization("bar", ["all_null"])
    
    # Test mixed types column
    bar = edge_case_profiler.generate_specific_visualization("bar", ["mixed_types"])
    assert isinstance(bar, dict)
    assert 'data' in bar
    assert len(bar['data']) > 0
    
    # Test special characters
    bar = edge_case_profiler.generate_specific_visualization("bar", ["special_chars"])
    assert isinstance(bar, dict)
    assert 'data' in bar
    assert len(bar['data']) > 0
    
    # Test timestamps
    line = edge_case_profiler.generate_specific_visualization("line", ["timestamps"])
    assert isinstance(line, dict)
    assert 'data' in line
    assert len(line['data']) > 0

def test_error_handling(data_profiler):
    """Test error handling in visualization generation."""
    # Create a dataframe that will definitely cause visualization errors
    df = pd.DataFrame({
        'numeric': [1, 2, 3],
        'other': [1, 2, 3]
    })
    bad_profiler = DataProfiler(df)
    
    # Modify the dataframe after creation to introduce invalid data
    bad_profiler.df.loc[0, 'numeric'] = 'not_a_number'
    
    # Test if error is properly caught and logged
    with pytest.raises(RuntimeError):
        # This should fail because we have invalid data in a numeric column
        bad_profiler.generate_visualizations()

def test_empty_dataframe():
    """Test handling of empty dataframe."""
    empty_df = pd.DataFrame()
    empty_profiler = DataProfiler(empty_df)
    
    # Test profile generation
    profile = empty_profiler.generate_profile()
    assert isinstance(profile, dict)
    assert len(profile) == 0
    
    # Test visualization generation
    viz = empty_profiler.generate_visualizations()
    assert isinstance(viz, dict)
    assert len(viz) == 0
    
    # Test summary generation
    summary = empty_profiler.generate_summary()
    assert "0 rows" in summary
    assert "0 columns" in summary

def test_single_row_dataframe():
    """Test handling of single row dataframe."""
    single_row_df = pd.DataFrame({
        'numeric': [1],
        'text': ['test'],
        'date': [pd.Timestamp('2024-01-01')]
    })
    profiler = DataProfiler(single_row_df)
    
    # Test profile generation
    profile = profiler.generate_profile()
    assert len(profile) == 3
    
    # Test visualization generation
    viz = profiler.generate_visualizations()
    assert isinstance(viz, dict)
    
    # Ensure no correlation heatmap for single row
    assert 'correlation_heatmap' not in viz 