import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
import json

# Page configuration
st.set_page_config(
    page_title="Program Impact Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        padding: 1.5rem;
        border-radius: 8px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s ease;
    }
    .metric-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .status-on-track { 
        color: #00cc00; 
        font-weight: bold; 
    }
    .status-at-risk { 
        color: #ff9900; 
        font-weight: bold; 
    }
    .status-off-track { 
        color: #cc0000; 
        font-weight: bold; 
    }
    .metric-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 0.5rem;
    }
    .metric-value-row {
        display: flex;
        justify-content: space-between;
        margin: 0.75rem 0;
    }
    .category-header {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(expectations_file, performance_file, evidence_file):
    """Load data from CSV files"""
    try:
        expectations = pd.read_csv(expectations_file)
        performance = pd.read_csv(performance_file)
        evidence = pd.read_csv(evidence_file)
        return expectations, performance, evidence
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

@st.cache_data
def load_metric_rationale():
    """Load metric rationale from JSON file"""
    try:
        if os.path.exists("metric_rationale.json"):
            with open("metric_rationale.json", "r") as f:
                return json.load(f)
        return {}
    except:
        return {}

def get_metric_rationale(metric_name, rationale_dict):
    """Get rationale for a metric"""
    return rationale_dict.get(metric_name, {
        "rationale": "No rationale available.",
        "target_rationale": "No target rationale available.",
        "data_availability": "Data availability information not specified."
    })

def is_lower_better_metric(metric_name):
    """Detect if a metric should use 'lower is better' logic"""
    lower_is_better_keywords = ['gap', 'cost', 'ratio', 'debt', 'time to', 'wait']
    metric_lower = metric_name.lower()
    return any(keyword in metric_lower for keyword in lower_is_better_keywords)

def format_value(value, metric_name=""):
    """Format value for display based on metric type"""
    if pd.isna(value):
        return "N/A"
    
    metric_lower = metric_name.lower()
    
    # Check if it's a currency metric
    if any(keyword in metric_lower for keyword in ['cost', 'salary', 'price', 'revenue', 'budget']):
        return f"${value:,.0f}"
    # Check if it's a percentage metric
    elif any(keyword in metric_lower for keyword in ['rate', 'percent', '%']):
        return f"{value:.1f}%"
    # Check if it's a score metric
    elif 'score' in metric_lower:
        return f"{value:.1f}"
    # Default: number with commas
    else:
        return f"{value:,.0f}"

def calculate_progress(baseline, actual, target, lower_is_better=False):
    """Calculate progress percentage"""
    if pd.isna(baseline) or pd.isna(target):
        return None, None, None
    
    if lower_is_better:
        # For metrics where lower is better (e.g., equity gaps, cost)
        if actual <= target:
            progress = 100
        else:
            denominator = baseline - target
            if denominator == 0:
                return None, None, None
            progress = max(0, min(100, ((baseline - actual) / denominator) * 100))
    else:
        # Standard calculation
        denominator = target - baseline
        if denominator == 0:
            return None, None, None
        progress = max(0, min(100, ((actual - baseline) / denominator) * 100))
    
    # Classify status
    if progress >= 80:
        status = "On Track"
        color = "green"
    elif progress >= 50:
        status = "At Risk"
        color = "orange"
    else:
        status = "Off Track"
        color = "red"
    
    return progress, status, color

def get_latest_performance(performance_df, initiative_id, metric):
    """Get the most recent performance data for an initiative/metric"""
    filtered = performance_df[
        (performance_df['Initiative ID'] == initiative_id) & 
        (performance_df['Metric'] == metric)
    ]
    if filtered.empty:
        return None
    # Sort by year and get the latest
    filtered = filtered.sort_values('Year', ascending=False)
    return filtered.iloc[0]

def get_evidence_grade(evidence_df, initiative_id, metric=None):
    """Get evidence summary and grade for an initiative/metric"""
    filtered = evidence_df[evidence_df['Initiative ID'] == initiative_id]
    
    # If evidence has Metric column, filter by it
    if 'Metric' in evidence_df.columns and metric is not None:
        filtered = filtered[filtered['Metric'] == metric]
    if filtered.empty:
        return None, None, None
    
    # Calculate average confidence score
    avg_confidence = filtered['Confidence Score'].mean()
    
    # Grade based on confidence and evidence types
    if avg_confidence >= 2.5:
        grade = "A"
    elif avg_confidence >= 2.0:
        grade = "B"
    elif avg_confidence >= 1.5:
        grade = "C"
    else:
        grade = "D"
    
    return grade, filtered, avg_confidence

def create_trend_chart(performance_df, initiative_id, metric, baseline, target_2030, lower_is_better=False):
    """Create trend and projection chart"""
    filtered = performance_df[
        (performance_df['Initiative ID'] == initiative_id) & 
        (performance_df['Metric'] == metric)
    ].sort_values('Year')
    
    if filtered.empty:
        return None
    
    fig = go.Figure()
    
    # Add actual data points
    fig.add_trace(go.Scatter(
        x=filtered['Year'],
        y=filtered['Actual Value'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    
    # Add baseline line
    if not pd.isna(baseline):
        fig.add_hline(
            y=baseline,
            line_dash="dash",
            line_color="gray",
            annotation_text="Baseline",
            annotation_position="right"
        )
    
    # Add target line
    if not pd.isna(target_2030):
        fig.add_hline(
            y=target_2030,
            line_dash="dash",
            line_color="green",
            annotation_text="Target 2030",
            annotation_position="right"
        )
        
        # Simple linear projection (if we have at least 2 data points)
        if len(filtered) >= 2:
            latest_year = filtered['Year'].max()
            latest_value = filtered[filtered['Year'] == latest_year]['Actual Value'].iloc[0]
            prev_year = filtered['Year'].sort_values().iloc[-2]
            prev_value = filtered[filtered['Year'] == prev_year]['Actual Value'].iloc[0]
            
            # Calculate trend
            if latest_year != prev_year:
                slope = (latest_value - prev_value) / (latest_year - prev_year)
                
                # Project to 2030
                projection_years = list(range(int(latest_year) + 1, 2031))
                if projection_years:
                    projection_values = [latest_value + slope * (year - latest_year) for year in projection_years]
                    projection_years = [latest_year] + projection_years
                    projection_values = [latest_value] + projection_values
                    
                    fig.add_trace(go.Scatter(
                        x=projection_years,
                        y=projection_values,
                        mode='lines',
                        name='Projected (No Intervention)',
                        line=dict(color='#ff7f0e', width=2, dash='dot'),
                        opacity=0.7
                    ))
    
    fig.update_layout(
        title=f"{metric} - Trend and Projection",
        xaxis_title="Year",
        yaxis_title="Value",
        hovermode='x unified',
        height=400,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig

def render_methodology_page():
    """Render the methodology and rationale explanation page"""
    st.header("Methodology & Metric Rationale")
    
    st.markdown("""
    ### Overview
    
    This dashboard tracks key initiatives' performance against Ambition 2045 target sheets, focusing on 
    **Pillar 2: BMGF Impact** of the Impact Accounting Framework. The tool enables teams to visualize how 
    initiatives are performing against expectations and identify evidence supporting observed progress.
    
    ---
    
    ### Core Questions
    
    1. **Are we meeting the goals we set for 2030 and beyond?**
    2. **What evidence supports the observed progress?**
    3. **Where are the biggest gaps between targets and actuals?**
    
    ---
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Progress Calculation")
        st.markdown("""
        For each metric, progress is calculated using the formula:
        
        **For higher-is-better metrics:**
        ```
        Progress % = (Actual - Baseline) / (Target - Baseline) × 100
        ```
        
        **For lower-is-better metrics** (equity gaps, costs):
        ```
        Progress % = (Baseline - Actual) / (Baseline - Target) × 100
        ```
        
        **Status Classification:**
        - **On Track** (Green): ≥80% progress toward target
        - **At Risk** (Orange): 50-79% progress toward target  
        - **Off Track** (Red): <50% progress toward target
        """)
    
    with col2:
        st.subheader("Trend Projections")
        st.markdown("""
        Simple linear projections are calculated based on the most recent two data points:
        
        ```
        Projection = Latest Value + (Trend Slope × Years to Target)
        ```
        
        This provides a "business-as-usual" projection showing what would happen without intervention.
        
        The projection line (orange dashed) shows the expected trajectory if current trends continue, 
        helping to distinguish impact that can be attributed to the proposed solution.
        """)
    
    st.markdown("---")
    
    st.subheader("Evidence Grading")
    st.markdown("""
    Evidence is graded based on confidence scores (1-3 scale):
    
    | Grade | Confidence Range | Description |
    |-------|-----------------|-------------|
    | **A** | ≥2.5 | Strong evidence (RCT, multiple high-quality studies) |
    | **B** | 2.0-2.49 | Moderate evidence (QED, descriptive with strong methodology) |
    | **C** | 1.5-1.99 | Weak evidence (Limited studies, descriptive) |
    | **D** | <1.5 | Limited evidence (Preliminary, anecdotal) |
    
    Evidence types tracked:
    - **RCT (Randomized Controlled Trial)**: Highest confidence (3/3)
    - **QED (Quasi-Experimental Design)**: Moderate confidence (2/3)
    - **Descriptive**: Lower confidence (1/3), but valuable for context
    """)
    
    st.markdown("---")
    
    st.subheader("Metric-Specific Rationale")
    st.markdown("""
    Below are detailed explanations for key metrics tracked in the Learnvia initiative:
    """)
    
    rationale_dict = load_metric_rationale()
    
    if rationale_dict:
        for metric_name, rationale_info in rationale_dict.items():
            with st.expander(f"**{metric_name}**"):
                st.markdown(f"""
                **Rationale:** {rationale_info.get('rationale', 'N/A')}
                
                **Target Rationale:** {rationale_info.get('target_rationale', 'N/A')}
                
                **Data Availability:** {rationale_info.get('data_availability', 'N/A')}
                """)
    else:
        st.info("Metric rationale file not found. Create metric_rationale.json for detailed explanations.")
    
    st.markdown("---")
    
    st.subheader("Data Sources & Quality")
    st.markdown("""
    - **Learnvia Platform**: User counts, adoption data, platform metrics
    - **Institution Records**: Course success rates, equity gap data (disaggregated by race/ethnicity, Pell status)
    - **Research Database**: Efficacy studies, peer-reviewed publications
    - **Survey Data**: Faculty and student satisfaction (CSAT)
    - **Finance Records**: Development costs, operational expenditures
    
    **Reporting Frequency**: 
    - User/adoption metrics: Real-time or quarterly
    - Course success: Per term (Fall/Spring semesters)
    - Research: Annual or upon publication
    """)

def main():
    st.title("Program Impact Dashboard MVP")
    st.markdown("**Pillar 2: BMGF Impact** - Visualizing initiative performance against Ambition 2045 targets")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Dashboard", "Methodology"])
    
    # Sidebar for file uploads
    st.sidebar.header("Data Input")
    
    upload_mode = st.sidebar.radio(
        "Data Source",
        ["Use Sample Data", "Upload CSV Files"]
    )
    
    if upload_mode == "Upload CSV Files":
        expectations_file = st.sidebar.file_uploader(
            "Expectations.csv",
            type=['csv'],
            help="Columns: Initiative ID, Metric, Baseline, Target 2030, Target 2045, Expectation Type"
        )
        performance_file = st.sidebar.file_uploader(
            "Performance.csv",
            type=['csv'],
            help="Columns: Initiative ID, Metric, Year, Actual Value, Data Source, Quality"
        )
        evidence_file = st.sidebar.file_uploader(
            "Evidence.csv",
            type=['csv'],
            help="Columns: Initiative ID, Evidence Type, Confidence Score, Link / Summary"
        )
        
        if expectations_file and performance_file and evidence_file:
            expectations, performance, evidence = load_data(expectations_file, performance_file, evidence_file)
        else:
            st.info("Please upload all three CSV files to begin.")
            st.stop()
    else:
        # Use sample data files if they exist
        if os.path.exists("Expectations.csv") and os.path.exists("Performance.csv") and os.path.exists("Evidence.csv"):
            expectations, performance, evidence = load_data("Expectations.csv", "Performance.csv", "Evidence.csv")
        else:
            st.error("Sample data files not found. Please create Expectations.csv, Performance.csv, and Evidence.csv files, or use the upload option.")
            st.stop()
    
    if expectations is None or performance is None or evidence is None:
        st.error("Failed to load data. Please check your CSV files.")
        st.stop()
    
    # Load metric rationale
    rationale_dict = load_metric_rationale()
    
    # Main dashboard
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")
    
    # Initiative filter
    initiatives = sorted(expectations['Initiative ID'].unique())
    selected_initiative = st.sidebar.selectbox(
        "Select Initiative",
        ["All"] + list(initiatives)
    )
    
    # Filter data
    if selected_initiative != "All":
        filtered_expectations = expectations[expectations['Initiative ID'] == selected_initiative]
    else:
        filtered_expectations = expectations
    
    with tab1:
        # KPI Overview Section
        st.header("KPI Overview")
        
        # Group metrics by category/bucket
        # Debug: show what columns we have
        if st.sidebar.checkbox("Show Debug Info", False):
            st.sidebar.write("Columns:", list(filtered_expectations.columns))
            st.sidebar.write("Has Category:", 'Category' in filtered_expectations.columns)
            if 'Category' in filtered_expectations.columns:
                st.sidebar.write("Categories:", filtered_expectations['Category'].unique().tolist())
        
        if 'Category' in filtered_expectations.columns:
            # Define bucket order and colors
            buckets = {
                'Adoption': {'emoji': '', 'color': '#1f77b4', 'description': 'Platform reach and user adoption metrics'},
                'Continuity': {'emoji': '', 'color': '#2ca02c', 'description': 'Course completion, success rates, and equity outcomes'},
                'Social ROI': {'emoji': '', 'color': '#ff7f0e', 'description': 'Efficacy, satisfaction, and cost-effectiveness metrics'}
            }
            
            # Get unique categories, preserving order
            categories = []
            for bucket in buckets.keys():
                if bucket in filtered_expectations['Category'].values:
                    categories.append(bucket)
            
            # Display metrics grouped by bucket
            for category in categories:
                category_metrics = filtered_expectations[filtered_expectations['Category'] == category]
                
                if not category_metrics.empty:
                    # Category header with cleaner style
                    bucket_info = buckets.get(category, {'emoji': '', 'color': '#808080', 'description': ''})
                    st.markdown(f"""
                    <div style='background: linear-gradient(90deg, {bucket_info['color']}15 0%, {bucket_info['color']}05 100%); 
                                 padding: 1.25rem 1.5rem; 
                                 border-radius: 8px; 
                                 border-left: 5px solid {bucket_info['color']}; 
                                 margin: 2rem 0 1.5rem 0;
                                 box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                        <h2 style='color: {bucket_info['color']}; 
                                    margin: 0 0 0.5rem 0; 
                                    font-size: 1.4rem;
                                    font-weight: 700;'>{category}</h2>
                        <p style='margin: 0; 
                                   color: #666; 
                                   font-size: 0.95rem;'>{bucket_info['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display metrics in this category
                    num_metrics = len(category_metrics)
                    cols_per_row = 3
                    rows = (num_metrics + cols_per_row - 1) // cols_per_row
                    
                    for row in range(rows):
                        cols = st.columns(cols_per_row)
                        for col_idx in range(cols_per_row):
                            metric_idx = row * cols_per_row + col_idx
                            if metric_idx < num_metrics:
                                metric_row = category_metrics.iloc[metric_idx]
                                initiative_id = metric_row['Initiative ID']
                                metric = metric_row['Metric']
                                baseline = metric_row['Baseline']
                                target_2030 = metric_row['Target 2030']
                                
                                # Get latest performance
                                latest_perf = get_latest_performance(performance, initiative_id, metric)
                                
                                with cols[col_idx]:
                                    # Get rationale for this metric
                                    metric_rationale = get_metric_rationale(metric, rationale_dict)
                                    
                                    # Metric card container with clean styling
                                    st.markdown(f"""
                                    <div class="metric-card" style="padding: 1.25rem; border-radius: 8px; background-color: #ffffff; border: 1px solid #e0e0e0; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.08);">
                                    """, unsafe_allow_html=True)
                                    
                                    # Metric header
                                    st.markdown(f'<div class="metric-header">{metric}</div>', unsafe_allow_html=True)
                                    st.caption(f"Initiative: {initiative_id}")
                                    
                                    # Show rationale as expandable info
                                    if metric_rationale.get('rationale') != "No rationale available.":
                                        with st.expander("Metric Rationale", expanded=False):
                                            st.markdown(f"**Why this metric?** {metric_rationale['rationale']}")
                                            if metric_rationale.get('target_rationale'):
                                                st.markdown(f"**Target rationale:** {metric_rationale['target_rationale']}")
                                            if metric_rationale.get('data_availability'):
                                                st.caption(f"Data: {metric_rationale['data_availability']}")
                                    
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    
                                    if latest_perf is not None:
                                        actual = latest_perf['Actual Value']
                                        lower_is_better = is_lower_better_metric(metric)
                                        progress, status, color = calculate_progress(baseline, actual, target_2030, lower_is_better)
                                        
                                        if progress is not None:
                                            # Display values in clean grid
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.metric("Baseline", format_value(baseline, metric), help="Starting value")
                                                st.metric("Actual", format_value(actual, metric), help="Current value")
                                            with col2:
                                                st.metric("Target 2030", format_value(target_2030, metric), help="Target value")
                                                # Progress percentage
                                                st.metric("Progress", f"{progress:.1f}%", help="Progress toward target")
                                            
                                            # Progress bar with cleaner style
                                            st.markdown("<br>", unsafe_allow_html=True)
                                            progress_color = "#00cc00" if progress >= 80 else "#ff9900" if progress >= 50 else "#cc0000"
                                            st.markdown(f"""
                                            <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; margin: 0.5rem 0;">
                                                <div style="background-color: {progress_color}; width: {progress}%; height: 100%; border-radius: 10px; transition: width 0.3s ease;"></div>
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
                                            # Status badge
                                            st.markdown(f"""
                                            <div style="margin: 0.75rem 0; padding: 0.5rem; background-color: {progress_color}20; border-left: 3px solid {progress_color}; border-radius: 4px;">
                                                <strong>Status:</strong> <span class='status-{status.lower().replace(' ', '-')}'>{status}</span> ({progress:.1f}%)
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
                                            # Delta to target
                                            delta = actual - target_2030
                                            if lower_is_better:
                                                # For lower-is-better metrics, negative delta is good
                                                if delta <= 0:
                                                    delta_text = f"{format_value(abs(delta), metric)} below target"
                                                    delta_color = "#00cc00"
                                                else:
                                                    delta_text = f"{format_value(delta, metric)} above target"
                                                    delta_color = "#cc0000"
                                            else:
                                                # For higher-is-better metrics, positive delta is good
                                                if delta >= 0:
                                                    delta_text = f"+{format_value(delta, metric)} above target"
                                                    delta_color = "#00cc00"
                                                else:
                                                    delta_text = f"{format_value(abs(delta), metric)} below target"
                                                    delta_color = "#cc0000"
                                            
                                            st.markdown(f"""
                                            <div style="margin-top: 0.5rem; padding: 0.5rem; background-color: #f8f9fa; border-radius: 4px; font-size: 0.9rem;">
                                                <strong>Gap to Target:</strong> <span style="color: {delta_color}">{delta_text}</span>
                                            </div>
                                            """, unsafe_allow_html=True)
                                        else:
                                            st.warning("Unable to calculate progress (missing baseline or target)")
                                    else:
                                        st.warning("No performance data available")
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Baseline", format_value(baseline, metric))
                                        with col2:
                                            st.metric("Target 2030", format_value(target_2030, metric))
                                    
                                    # Close metric card div
                                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
        
        else:
            # Fallback to original display if no Category column
            num_metrics = len(filtered_expectations)
            cols_per_row = 3
            rows = (num_metrics + cols_per_row - 1) // cols_per_row
            
            for row in range(rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    metric_idx = row * cols_per_row + col_idx
                    if metric_idx < num_metrics:
                        metric_row = filtered_expectations.iloc[metric_idx]
                        initiative_id = metric_row['Initiative ID']
                        metric = metric_row['Metric']
                        baseline = metric_row['Baseline']
                        target_2030 = metric_row['Target 2030']
                        
                        # Get latest performance
                        latest_perf = get_latest_performance(performance, initiative_id, metric)
                        
                        with cols[col_idx]:
                            # Get rationale for this metric
                            metric_rationale = get_metric_rationale(metric, rationale_dict)
                            
                            # Metric card container with clean styling
                            st.markdown(f"""
                            <div class="metric-card" style="padding: 1.25rem; border-radius: 8px; background-color: #ffffff; border: 1px solid #e0e0e0; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.08);">
                            """, unsafe_allow_html=True)
                            
                            # Metric header
                            st.markdown(f'<div class="metric-header">{metric}</div>', unsafe_allow_html=True)
                            st.caption(f"Initiative: {initiative_id}")
                            
                            # Show rationale as expandable info
                            if metric_rationale.get('rationale') != "No rationale available.":
                                with st.expander("Metric Rationale", expanded=False):
                                    st.markdown(f"**Why this metric?** {metric_rationale['rationale']}")
                                    if metric_rationale.get('target_rationale'):
                                        st.markdown(f"**Target rationale:** {metric_rationale['target_rationale']}")
                                    if metric_rationale.get('data_availability'):
                                        st.caption(f"Data: {metric_rationale['data_availability']}")
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            if latest_perf is not None:
                                actual = latest_perf['Actual Value']
                                lower_is_better = is_lower_better_metric(metric)
                                progress, status, color = calculate_progress(baseline, actual, target_2030, lower_is_better)
                                
                                if progress is not None:
                                    # Display values in clean grid
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.metric("Baseline", format_value(baseline, metric), help="Starting value")
                                        st.metric("Actual", format_value(actual, metric), help="Current value")
                                    with col2:
                                        st.metric("Target 2030", format_value(target_2030, metric), help="Target value")
                                        # Progress percentage
                                        st.metric("Progress", f"{progress:.1f}%", help="Progress toward target")
                                    
                                    # Progress bar with cleaner style
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    progress_color = "#00cc00" if progress >= 80 else "#ff9900" if progress >= 50 else "#cc0000"
                                    st.markdown(f"""
                                    <div style="background-color: #f0f0f0; border-radius: 10px; height: 20px; margin: 0.5rem 0;">
                                        <div style="background-color: {progress_color}; width: {progress}%; height: 100%; border-radius: 10px; transition: width 0.3s ease;"></div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Status badge
                                    st.markdown(f"""
                                    <div style="margin: 0.75rem 0; padding: 0.5rem; background-color: {progress_color}20; border-left: 3px solid {progress_color}; border-radius: 4px;">
                                        <strong>Status:</strong> <span class='status-{status.lower().replace(' ', '-')}'>{status}</span> ({progress:.1f}%)
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Delta to target
                                    delta = actual - target_2030
                                    if lower_is_better:
                                        # For lower-is-better metrics, negative delta is good
                                        if delta <= 0:
                                            delta_text = f"{format_value(abs(delta), metric)} below target"
                                            delta_color = "#00cc00"
                                        else:
                                            delta_text = f"{format_value(delta, metric)} above target"
                                            delta_color = "#cc0000"
                                    else:
                                        # For higher-is-better metrics, positive delta is good
                                        if delta >= 0:
                                            delta_text = f"+{format_value(delta, metric)} above target"
                                            delta_color = "#00cc00"
                                        else:
                                            delta_text = f"{format_value(abs(delta), metric)} below target"
                                            delta_color = "#cc0000"
                                    
                                    st.markdown(f"""
                                    <div style="margin-top: 0.5rem; padding: 0.5rem; background-color: #f8f9fa; border-radius: 4px; font-size: 0.9rem;">
                                        <strong>Gap to Target:</strong> <span style="color: {delta_color}">{delta_text}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.warning("Unable to calculate progress (missing baseline or target)")
                            else:
                                st.warning("No performance data available")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Baseline", format_value(baseline, metric))
                                with col2:
                                    st.metric("Target 2030", format_value(target_2030, metric))
                            
                            # Close metric card div
                            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed View Section
        if selected_initiative != "All":
            st.header("Detailed Analysis")
            
            selected_metric = st.selectbox(
                "Select Metric for Detailed View",
                filtered_expectations['Metric'].unique()
            )
            
            metric_row = filtered_expectations[filtered_expectations['Metric'] == selected_metric].iloc[0]
            initiative_id = metric_row['Initiative ID']
            baseline = metric_row['Baseline']
            target_2030 = metric_row['Target 2030']
            target_2045 = metric_row.get('Target 2045', None)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Trend and Projection Chart")
                lower_is_better = is_lower_better_metric(selected_metric)
                chart = create_trend_chart(performance, initiative_id, selected_metric, baseline, target_2030, lower_is_better)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                else:
                    st.info("No performance data available for this metric")
            
            with col2:
                st.subheader("Evidence & Narrative")
                
                # Get evidence
                grade, evidence_data, avg_confidence = get_evidence_grade(evidence, initiative_id, selected_metric)
                
                if evidence_data is not None and not evidence_data.empty:
                    st.markdown(f"**Evidence Grade: {grade}**")
                    st.caption(f"Average Confidence: {avg_confidence:.1f}/3.0")
                    
                    st.markdown("**Supporting Evidence:**")
                    for idx, row in evidence_data.iterrows():
                        with st.expander(f"{row.get('Evidence Type', 'Evidence')} (Confidence: {row['Confidence Score']}/3)"):
                            st.write(row.get('Link / Summary', 'No summary available'))
                            if 'Link / Summary' in row and str(row['Link / Summary']).startswith('http'):
                                st.markdown(f"[View Source]({row['Link / Summary']})")
                else:
                    st.warning("No evidence data available for this metric")
                
                # Narrative insights
                st.markdown("**Key Learnings & Drivers:**")
                narrative_key = f"narrative_{initiative_id}_{selected_metric}"
                narrative_text = st.text_area(
                    "Add qualitative notes describing key learnings and drivers:",
                    key=narrative_key,
                    height=150,
                    help="Document insights about what's driving performance, challenges, and opportunities"
                )
            
            # Additional metrics table
            st.subheader("Performance Data Table")
            metric_performance = performance[
                (performance['Initiative ID'] == initiative_id) & 
                (performance['Metric'] == selected_metric)
            ].sort_values('Year')
            
            if not metric_performance.empty:
                st.dataframe(
                    metric_performance[['Year', 'Actual Value', 'Data Source', 'Quality']],
                    use_container_width=True
                )
            else:
                st.info("No performance data available for this metric")
        
        # Summary Statistics
        st.markdown("---")
        st.header("Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate overall stats
        total_metrics = len(filtered_expectations)
        metrics_with_data = 0
        on_track_count = 0
        at_risk_count = 0
        off_track_count = 0
        
        for idx, row in filtered_expectations.iterrows():
            initiative_id = row['Initiative ID']
            metric = row['Metric']
            baseline = row['Baseline']
            target_2030 = row['Target 2030']
            
            latest_perf = get_latest_performance(performance, initiative_id, metric)
            if latest_perf is not None:
                metrics_with_data += 1
                actual = latest_perf['Actual Value']
                lower_is_better = is_lower_better_metric(metric)
                progress, status, _ = calculate_progress(baseline, actual, target_2030, lower_is_better)
                if progress is not None:
                    if status == "On Track":
                        on_track_count += 1
                    elif status == "At Risk":
                        at_risk_count += 1
                    else:
                        off_track_count += 1
        
        with col1:
            st.metric("Total Metrics", total_metrics)
        with col2:
            st.metric("On Track", on_track_count)
        with col3:
            st.metric("At Risk", at_risk_count)
        with col4:
            st.metric("Off Track", off_track_count)
    
    with tab2:
        render_methodology_page()

if __name__ == "__main__":
    main()

