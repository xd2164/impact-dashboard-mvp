"""
Basic Impact Metrics Example
Demonstrates basic usage of the Impact Metrics system.
"""

from src.impact_metrics import ImpactMetrics


def main():
    """Basic example of using Impact Metrics."""
    
    # Initialize metrics tracker
    metrics = ImpactMetrics()
    
    # Add some metrics
    print("Adding metrics...")
    metrics.add_metric("daily_active_users", 1250)
    metrics.add_metric("daily_active_users", 1350)
    metrics.add_metric("daily_active_users", 1420)
    
    metrics.add_metric("revenue", 10000.50)
    metrics.add_metric("revenue", 10500.75)
    
    # Display current metrics
    print("\nCurrent Metrics:")
    for name, value in metrics.metrics.items():
        print(f"  {name}: {value}")
    
    # Calculate averages
    print("\nAverages:")
    print(f"  Average daily active users: {metrics.calculate_average('daily_active_users')}")
    print(f"  Average revenue: {metrics.calculate_average('revenue')}")
    
    # Get history
    print("\nMetric History:")
    history = metrics.get_history()
    for entry in history:
        print(f"  {entry['name']}: {entry['value']} at {entry['timestamp']}")
    
    # Export data
    print("\nExporting data...")
    if metrics.export_data("metrics_export.json"):
        print("✅ Data exported successfully!")
    else:
        print("❌ Failed to export data")


if __name__ == "__main__":
    main()

