"""
Impact Metrics - Core module for tracking and analyzing impact metrics
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class ImpactMetrics:
    """
    Main class for managing and analyzing impact metrics.
    """
    
    def __init__(self):
        """Initialize the Impact Metrics system."""
        self.metrics = {}
        self.history = []
    
    def add_metric(self, name: str, value: float, timestamp: Optional[datetime] = None):
        """
        Add a metric to track.
        
        Args:
            name: Name of the metric
            value: Value of the metric
            timestamp: Optional timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        metric_entry = {
            "name": name,
            "value": value,
            "timestamp": timestamp.isoformat()
        }
        
        self.metrics[name] = value
        self.history.append(metric_entry)
        
        return metric_entry
    
    def get_metric(self, name: str) -> Optional[float]:
        """
        Get the current value of a metric.
        
        Args:
            name: Name of the metric
            
        Returns:
            Current value of the metric or None if not found
        """
        return self.metrics.get(name)
    
    def get_history(self, name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get metric history.
        
        Args:
            name: Optional metric name to filter by
            
        Returns:
            List of metric entries
        """
        if name:
            return [entry for entry in self.history if entry["name"] == name]
        return self.history
    
    def calculate_average(self, name: str) -> Optional[float]:
        """
        Calculate average value for a metric.
        
        Args:
            name: Name of the metric
            
        Returns:
            Average value or None if no data
        """
        history = self.get_history(name)
        if not history:
            return None
        
        values = [entry["value"] for entry in history]
        return sum(values) / len(values)
    
    def export_data(self, filepath: str) -> bool:
        """
        Export metrics data to a JSON file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                "metrics": self.metrics,
                "history": self.history,
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False


def main():
    """Main function for testing."""
    metrics = ImpactMetrics()
    
    # Example usage
    metrics.add_metric("users", 100)
    metrics.add_metric("users", 150)
    metrics.add_metric("revenue", 5000.0)
    
    print("Current metrics:", metrics.metrics)
    print("Average users:", metrics.calculate_average("users"))
    print("History:", metrics.get_history())


if __name__ == "__main__":
    main()

