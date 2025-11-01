"""
Tests for Impact Metrics core functionality
"""

import pytest
from src.impact_metrics import ImpactMetrics
from datetime import datetime


def test_add_metric():
    """Test adding a metric."""
    metrics = ImpactMetrics()
    result = metrics.add_metric("test_metric", 100.0)
    
    assert result["name"] == "test_metric"
    assert result["value"] == 100.0
    assert metrics.get_metric("test_metric") == 100.0


def test_get_history():
    """Test getting metric history."""
    metrics = ImpactMetrics()
    metrics.add_metric("test_metric", 100.0)
    metrics.add_metric("test_metric", 200.0)
    
    history = metrics.get_history("test_metric")
    assert len(history) == 2
    assert history[0]["value"] == 100.0
    assert history[1]["value"] == 200.0


def test_calculate_average():
    """Test calculating average."""
    metrics = ImpactMetrics()
    metrics.add_metric("test_metric", 100.0)
    metrics.add_metric("test_metric", 200.0)
    metrics.add_metric("test_metric", 300.0)
    
    average = metrics.calculate_average("test_metric")
    assert average == 200.0


def test_export_data(tmp_path):
    """Test exporting data."""
    metrics = ImpactMetrics()
    metrics.add_metric("test_metric", 100.0)
    
    filepath = tmp_path / "test_export.json"
    result = metrics.export_data(str(filepath))
    
    assert result is True
    assert filepath.exists()

