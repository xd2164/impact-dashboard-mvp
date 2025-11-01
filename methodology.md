# Program Impact Dashboard Methodology

## Overview

This dashboard tracks key initiatives' performance against Ambition 2045 target sheets, focusing on **Pillar 2: BMGF Impact** of the Impact Accounting Framework. The tool enables teams to visualize how initiatives are performing against expectations and identify evidence supporting observed progress.

## Core Questions

1. **Are we meeting the goals we set for 2030 and beyond?**
2. **What evidence supports the observed progress?**
3. **Where are the biggest gaps between targets and actuals?**

## Methodology

### Progress Calculation

For each metric, progress is calculated using the formula:

```
Progress % = (Actual - Baseline) / (Target - Baseline) × 100
```

**Status Classification:**
- **On Track (Green)**: ≥80% progress toward target
- **At Risk (Orange)**: 50-79% progress toward target  
- **Off Track (Red)**: <50% progress toward target

### Lower-is-Better Metrics

For metrics where lower values are better (e.g., equity gaps, costs, ratios), the calculation is automatically inverted:

```
Progress % = (Baseline - Actual) / (Baseline - Target) × 100
```

The system automatically detects these metrics based on keywords in the metric name (gap, cost, ratio, debt, etc.).

### Trend Projections

Simple linear projections are calculated based on the most recent two data points:

```
Projection = Latest Value + (Trend Slope × Years to Target)
```

This provides a "business-as-usual" projection showing what would happen without intervention.

### Evidence Grading

Evidence is graded based on confidence scores (1-3 scale):

- **Grade A**: Average confidence ≥2.5 (Strong evidence)
- **Grade B**: Average confidence 2.0-2.49 (Moderate evidence)
- **Grade C**: Average confidence 1.5-1.99 (Weak evidence)
- **Grade D**: Average confidence <1.5 (Limited evidence)

---

## Learnvia Initiative Metrics

### LEARNVIA-001: Reach Metrics

#### # of Math Courseware Available
**Rationale**: Track the development and deployment of TPP-aligned gateway math courseware. By Fall 2028, Learnvia aims to publish at least five new courseware products. This metric demonstrates platform maturity and content coverage essential for scaling impact.

**Target Rationale**: With strong technical and operational talent, CMU's expertise in STEM education and AI, and the foundation's track record, delivering five high-quality courseware by 2030 is ambitious but achievable. Early Calculus 1 launch demonstrates execution capability.

#### # of Student Users Served (Annual & Cumulative)
**Rationale**: Measures platform adoption and reach. By 2030, Learnvia aims to reach 180,000 students annually (about 6% of 2.7M U.S. gateway math enrollments). This establishes a credible foothold for large-scale growth toward majority market share by 2045.

**Target Rationale**: Incumbents like Pearson MyLab and McGraw Hill ALEKS already serve hundreds of thousands of students, proving market demand. Learnvia enters well-capitalized with differentiated advantages: AI-enabled, evidence-based, free to students, and designed by educators for educators.

**Disaggregation**: Data includes breakdown by:
- Post-secondary institutions (primary segment)
- High school dual enrollment/dual credit
- Race/ethnicity and Pell status (where available)

#### # of Faculty Adopters & Institutions
**Rationale**: Faculty adoption drives institutional change and ensures sustainable implementation. By 2030, targeting 2,265 faculty and 450 institutions creates a foundation for systemic transformation in gateway math instruction.

**Scaling Strategy**: Focus on institutions serving high populations of focus students to maximize equity impact.

---

### LEARNVIA-002: Outcome Metrics

#### Course Success Rates (Universal Goal)
**Rationale**: Gateway math courses are primary barriers to degree completion, especially for first-generation and underrepresented students. Improving course success rates directly impacts persistence and completion.

**Baseline Data**:
- Calculus I: 77%
- Calculus II: 74%
- Statistical Reasoning: 73%
- PreCalculus: 70%

**Target Strategy**: 
- 80% pass rate OR +10 percentage points (whichever requires smaller lift)
- Targets account for focus institutions typically starting 5-10pp below baseline rates
- Rolled up across adopting institutions by course

**Expected Impact**: By 2030, this translates to 144K students/year or 284K cumulative who pass because of Learnvia courseware.

#### Equity Gap Reduction (Target Goal)
**Rationale**: Closing equity gaps is central to the foundation's mission. Reducing gaps by 50% by 2030 demonstrates meaningful progress toward equitable outcomes.

**Baseline Gaps**:
- Calculus: 13.4%
- Statistical Reasoning: 19.1%
- PreCalculus: 13.5%

**Target (2030)**: 50% reduction
- Calculus: 6.7%
- Statistical Reasoning: 9.55%
- PreCalculus: 6.75%

**Target (2045)**: Further reduction to 3-4% range

#### Efficacy Research Studies
**Rationale**: Evidence base demonstrating causal impact strengthens platform credibility and guides continuous improvement. Tracking RCT and quasi-experimental studies provides validation of courseware effectiveness.

**Baseline**: 2 studies (Lumen Learning, UCR Real Chem)
**Target**: 4+ studies by 2030 demonstrating statistically significant improvements in learning outcomes

#### Satisfaction Rates
**Rationale**: High faculty and student satisfaction drives adoption and retention. CSAT rates >80% indicate platform meets user needs and supports successful implementation.

---

### LEARNVIA-003: Cost Metrics

#### Cost per Course Development
**Rationale**: Tracking development costs enables efficiency improvements and sustainability planning. Current estimates: $2-3M per course. AI advances may reduce costs by 2030.

**Baseline**: ~$2.5M per course
**Target**: Reduced to $2M by 2030, $1.5M by 2045 through AI-enabled development tools

#### Cost to Student
**Rationale**: Free-to-student model removes financial barriers and supports equity goals. Validating $0 cost sustainability ensures long-term accessibility.

**Target**: Maintain $0 cost to students through sustainable business model

---

## Data Sources & Quality

- **Learnvia Platform**: User counts, adoption data, platform metrics
- **Institution Records**: Course success rates, equity gap data (disaggregated by race/ethnicity, Pell status)
- **Research Database**: Efficacy studies, peer-reviewed publications
- **Survey Data**: Faculty and student satisfaction (CSAT)
- **Finance Records**: Development costs, operational expenditures

**Reporting Frequency**: 
- User/adoption metrics: Real-time or quarterly
- Course success: Per term (Fall/Spring semesters)
- Research: Annual or upon publication

---

## Evidence Framework

Evidence types tracked:
- **RCT (Randomized Controlled Trial)**: Highest confidence (3/3)
- **QED (Quasi-Experimental Design)**: Moderate confidence (2/3)
- **Descriptive**: Lower confidence (1/3), but valuable for context

Evidence grades reflect aggregate confidence across all studies for a given initiative/metric.

---

## Limitations & Future Enhancements

**Current Limitations**:
- Simple linear projections (no advanced forecasting)
- Manual evidence scoring
- Limited disaggregation capabilities

**Phase 2 Enhancements**:
- Add Pillar 1 (Sector Performance) and Pillar 3 (Resource Use)
- Automated evidence scoring from research databases
- Composite "Program Impact Index"
- Integration with enterprise BI tools (Power BI, Looker)

