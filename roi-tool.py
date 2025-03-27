import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os
import json
import traceback

# Set page config
st.set_page_config(
    page_title="Endpoint Central ROI Calculator for MAXAR Technologies ",
    page_icon="📊",
    layout="wide"
)

# Sidebar for theme toggle
with st.sidebar:
    st.title("Settings")
    theme = st.radio("Choose Theme", ["Light", "Dark"], index=0)

    st.markdown("---")
    st.markdown("### About")
    st.info("""
    Endpoint Central ROI Calculator for MAXAR Technologies

    Calculate the potential savings and ROI from implementing
    ManageEngine Endpoint Central for your IT infrastructure.

    Version 1.0 | March 2025
    """)

# Apply theme-specific CSS
if theme == "Light":
    theme_color = "#0066B3"
    background_color = "#FFFFFF"
    text_color = "#333333"
    card_bg = "#f7f7f7"
    plot_bg = "#FFFFFF"
    plot_color = "#333333"
else:  # Dark theme
    theme_color = "#4098E5"
    background_color = "#1E1E1E"
    text_color = "#F0F0F0"
    card_bg = "#2D2D2D"
    plot_bg = "#1E1E1E"
    plot_color = "#F0F0F0"

# Custom CSS based on selected theme
st.markdown(f"""
<style>
    .title {{
        font-size: 42px;
        font-weight: bold;
        color: {theme_color};
        margin-bottom: 0px;
    }}
    .subtitle {{
        font-size: 20px;
        color: {text_color};
        margin-top: 0px;
        margin-bottom: 30px;
    }}
    .section-header {{
        font-size: 24px;
        font-weight: bold;
        color: {theme_color};
        margin-top: 30px;
        margin-bottom: 20px;
    }}
    .metric-container {{
        background-color: {card_bg};
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .metric-value {{
        font-size: 36px;
        font-weight: bold;
        color: {theme_color};
    }}
    .metric-label {{
        font-size: 16px;
        color: {text_color};
    }}
    .stApp {{
        background-color: {background_color};
        color: {text_color};
    }}
    .stTextInput>div>div>input {{
        color: {text_color};
    }}
    .stSelectbox>div>div>div {{
        color: {text_color};
    }}
    .stNumberInput>div>div>input {{
        color: {text_color};
    }}
    .st-bx {{
        color: {text_color};
    }}
    .st-bs {{
        color: {text_color};
    }}

    /* Block scrollbar on all elements */
    ::-webkit-scrollbar {{
        width: 10px;
        background: {background_color};
    }}
    ::-webkit-scrollbar-track {{
        background: {background_color};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {theme_color};
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown("<div class='title'>Endpoint Central ROI Calculator for MAXAR Technologies</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Quantify the cost and time savings by automating routine IT management tasks with Endpoint Central</div>",
    unsafe_allow_html=True)

st.markdown("""
This calculator helps you estimate the Return on Investment (ROI) from implementing Endpoint Central for your 
IT infrastructure management. By comparing manual processes with automated solutions, you can visualize potential 
cost savings, efficiency gains, and strategic benefits.
""")

# Create two columns for the main layout
col1, col2 = st.columns([1, 2])

# ----------- COL1: Input parameters and calculations -------------
with col1:
    st.markdown("<div class='section-header'>Input Parameters</div>", unsafe_allow_html=True)

    # User inputs with default values from the blueprint
    devices = st.number_input("Number of Devices", min_value=1, value=3000,
                                help="Total number of endpoints to be managed")
    applications = st.number_input("Number of Applications", min_value=1, value=1500,
                                   help="Total number of applications to be updated")
    updates_per_app = st.number_input("Updates per Application per Year", min_value=1, value=4,
                                      help="Average number of updates required per application per year")
    hours_per_update = st.number_input("Hours per Update (Manual Process)", min_value=0.1, value=4.0,
                                       help="Average time required to manually update one application")
    hourly_rate = st.number_input("Technician Hourly Rate ($)", min_value=1.0, value=50.0,
                                  help="Average cost per hour for IT personnel")

    st.markdown("### Automation Efficiency")
    automation_efficiency = st.slider("Automation Efficiency (%)", min_value=50, max_value=99, value=90,
                                      help="Percentage reduction in manual effort achieved through automation")

    st.markdown("### Endpoint Central Edition")

    # Create a dictionary of edition information
    edition_info = {
        "Free": {
            "description": "Basic management for up to 25-50 endpoints at no cost",
            "features": "Basic endpoint management, patch management",
            "best_for": "Small businesses with limited IT needs"
        },
        "Professional": {
            "description": "Complete endpoint management for LAN environments",
            "features": "Patch management, application distribution, asset management, remote troubleshooting, BYOD management, kiosk mode",
            "best_for": "Small to medium businesses in single-location environments",
            "base_price": 795
        },
        "Enterprise": {
            "description": "Enhanced management for WAN environments",
            "features": "Everything in Professional + self-service portal, USB device management, audit remote sessions, license management",
            "best_for": "Organizations with multiple locations requiring centralized management",
            "base_price": 945
        },
        "UEM": {
            "description": "Unified endpoint management across all devices",
            "features": "Everything in Enterprise + remote data wipe, OS deployment, FileVault encryption, mobile device management",
            "best_for": "Organizations with diverse device types and operating systems",
            "base_price": 1095
        },
        "Security": {
            "description": "Comprehensive security-focused endpoint management",
            "features": "Everything in UEM + vulnerability remediation, data loss prevention, endpoint privilege management, browser security, ransomware protection",
            "best_for": "Organizations with high security requirements or in regulated industries",
            "base_price": 1695
        }
    }
    # Create columns for edition selection and information display
    edition_col1, edition_col2 = st.columns([1, 2])

    with edition_col1:
        edition = st.selectbox(
            "Select Edition",
            ["Free", "Professional", "Enterprise", "UEM", "Security"],
            index=3,
            help="Different editions offer varying features and pricing"
        )

    with edition_col2:
        st.markdown(f"**{edition} Edition**: {edition_info[edition]['description']}")
        st.markdown(f"**Key Features**: {edition_info[edition]['features']}")
        st.markdown(f"**Best For**: {edition_info[edition]['best_for']}")

    # Calculate license cost based on edition and number of devices
    try:
        if edition == "Free":
            if devices <= 50:
                license_cost = 0
            else:
                st.warning("Free Edition is limited to 50 endpoints. Please select a paid edition for larger deployments.")
                license_cost = 0
        else:
            base_prices = {
                "Professional": 795,
                "Enterprise": 945,
                "UEM": 1095,
                "Security": 1695
            }
            if devices <= 50:
                license_cost = base_prices[edition]
            else:
                tiers = [
                    (100, 0.9),
                    (500, 0.8),
                    (1000, 0.7),
                    (float('inf'), 0.6)
                ]
                remaining_devices = devices - 50
                additional_cost = 0
                base_cost_per_device = base_prices[edition] / 50
                current_devices = 50
                for tier_limit, discount_factor in tiers:
                    if current_devices >= devices:
                        break
                    devices_in_tier = min(tier_limit, devices) - current_devices
                    if devices_in_tier > 0:
                        additional_cost += devices_in_tier * base_cost_per_device * discount_factor
                        current_devices += devices_in_tier
                license_cost = base_prices[edition] + additional_cost
    except Exception as e:
        st.error(f"Error calculating license cost: {str(e)}")
        license_cost = 0

    st.markdown(f"### Calculated Annual License Cost: ${license_cost:,.2f}")
    st.caption("Based on selected edition and number of devices")

    override_license = st.checkbox("Override calculated license cost", value=False)
    if override_license:
        license_cost = st.number_input("Custom Annual License Cost ($)", min_value=0, value=int(license_cost),
                                       help="Enter your specific license cost if you have a custom quote")

    implementation_cost = st.number_input("One-time Implementation Cost ($)", min_value=0, value=20000,
                                          help="One-time cost for implementation, training, etc.")

    st.markdown("### Additional Benefits")
    edition_benefits = {
        "Free": {
            "security_benefit_max": 30,
            "downtime_reduction_max": 20,
            "default_compliance_hours": 100
        },
        "Professional": {
            "security_benefit_max": 50,
            "downtime_reduction_max": 35,
            "default_compliance_hours": 150
        },
        "Enterprise": {
            "security_benefit_max": 65,
            "downtime_reduction_max": 50,
            "default_compliance_hours": 200
        },
        "UEM": {
            "security_benefit_max": 75,
            "downtime_reduction_max": 60,
            "default_compliance_hours": 250
        },
        "Security": {
            "security_benefit_max": 90,
            "downtime_reduction_max": 70,
            "default_compliance_hours": 300
        }
    }
    with st.expander("Security & Compliance Benefits"):
        security_benefit = st.slider(
            "Security Incident Reduction (%)",
            min_value=0,
            max_value=100,
            value=min(edition_benefits[edition]["security_benefit_max"], 60),
            help="Estimated reduction in security incidents"
        )
        if edition == "Security":
            st.info("The Security Edition includes advanced vulnerability remediation and ransomware protection, significantly enhancing your security posture.")
        compliance_time_saved = st.number_input(
            "Hours Saved on Compliance Reporting (Annual)",
            min_value=0,
            value=edition_benefits[edition]["default_compliance_hours"],
            help="Estimated hours saved on compliance reporting"
        )
        if edition in ["Enterprise", "UEM", "Security"]:
            st.info("Enterprise+ editions include advanced compliance reporting features.")
    with st.expander("Operational Benefits"):
        downtime_reduction = st.slider(
            "Downtime Reduction (%)",
            min_value=0,
            max_value=100,
            value=min(edition_benefits[edition]["downtime_reduction_max"], 40),
            help="Estimated reduction in system downtime"
        )
        bandwidth_savings = st.number_input(
            "Bandwidth Cost Savings ($)",
            min_value=0,
            value=5000,
            help="Estimated bandwidth cost savings from optimized patch downloads"
        )
        if edition in ["UEM", "Security"]:
            st.info("UEM and Security editions include advanced remote troubleshooting and deployment optimization features that can significantly reduce downtime and bandwidth usage.")
        try:
            total_updates = applications * updates_per_app
            total_manual_hours = total_updates * hours_per_update
            total_manual_cost = total_manual_hours * hourly_rate

            automation_factor = 1 - (automation_efficiency / 100)
            total_automated_hours = total_manual_hours * automation_factor
            total_automated_cost = total_automated_hours * hourly_rate

            annual_labor_savings = total_manual_cost - total_automated_cost

            if edition == "Security":
                avg_incident_cost = 7500
            elif edition in ["UEM", "Enterprise"]:
                avg_incident_cost = 6000
            else:
                avg_incident_cost = 5000

            security_incidents_reduction_value = (security_benefit / 100) * (devices * 0.05) * avg_incident_cost

            if edition in ["UEM", "Security"]:
                downtime_hours_per_device = 2.5
                efficiency_factor = 1.8
            elif edition == "Enterprise":
                downtime_hours_per_device = 2.2
                efficiency_factor = 1.5
            else:
                downtime_hours_per_device = 2.0
                efficiency_factor = 1.5

            downtime_hours_saved = (downtime_reduction / 100) * (devices * downtime_hours_per_device)
            downtime_cost_saved = downtime_hours_saved * hourly_rate * efficiency_factor

            if edition in ["UEM", "Security"]:
                bandwidth_factor = 1.2
            else:
                bandwidth_factor = 1.0

            bandwidth_savings_adjusted = bandwidth_savings * bandwidth_factor

            annual_compliance_savings = compliance_time_saved * hourly_rate

            total_annual_savings = (annual_labor_savings + annual_compliance_savings +
                                    bandwidth_savings_adjusted + security_incidents_reduction_value +
                                    downtime_cost_saved)

            edition_specific_features = {
                "Free": {},
                "Professional": {
                    "Application Deployment Automation": annual_labor_savings * 0.1,
                    "Remote Troubleshooting": downtime_cost_saved * 0.2
                },
                "Enterprise": {
                    "Application Deployment Automation": annual_labor_savings * 0.1,
                    "Remote Troubleshooting": downtime_cost_saved * 0.2,
                    "Self-Service Portal": devices * 5,
                    "USB Device Management": devices * 2
                },
                "UEM": {
                    "Application Deployment Automation": annual_labor_savings * 0.1,
                    "Remote Troubleshooting": downtime_cost_saved * 0.2,
                    "Self-Service Portal": devices * 5,
                    "USB Device Management": devices * 2,
                    "OS Deployment": devices * 10,
                    "Mobile Device Management": devices * 8
                },
                "Security": {
                    "Application Deployment Automation": annual_labor_savings * 0.1,
                    "Remote Troubleshooting": downtime_cost_saved * 0.2,
                    "Self-Service Portal": devices * 5,
                    "USB Device Management": devices * 2,
                    "OS Deployment": devices * 10,
                    "Mobile Device Management": devices * 8,
                    "Vulnerability Remediation": security_incidents_reduction_value * 0.3,
                    "Endpoint Privilege Management": devices * 15,
                    "Ransomware Protection": devices * 25
                }
            }

            total_benefits = {
                "Direct Labor Savings": annual_labor_savings,
                "Compliance Reporting Savings": annual_compliance_savings,
                "Bandwidth Cost Savings": bandwidth_savings_adjusted,
                "Security Incident Reduction Value": security_incidents_reduction_value,
                "Downtime Cost Savings": downtime_cost_saved
            }

            for feature, value in edition_specific_features.get(edition, {}).items():
                if value > 0:
                    total_benefits[f"{feature} ({edition} Edition)"] = value

            edition_value_factors = {
                "Free": 1.0,
                "Professional": 1.05,
                "Enterprise": 1.1,
                "UEM": 1.15,
                "Security": 1.25
            }

            adjusted_annual_savings = total_annual_savings * edition_value_factors[edition]

            total_first_year_cost = license_cost + implementation_cost
            subsequent_years_cost = license_cost

            if total_first_year_cost > 0:
                first_year_roi = ((adjusted_annual_savings - total_first_year_cost) / total_first_year_cost) * 100
            else:
                first_year_roi = float('inf')

            if subsequent_years_cost > 0:
                subsequent_roi = ((adjusted_annual_savings - subsequent_years_cost) / subsequent_years_cost) * 100
            else:
                subsequent_roi = float('inf')

            if adjusted_annual_savings > total_first_year_cost and total_first_year_cost > 0:
                payback_months = (total_first_year_cost / adjusted_annual_savings) * 12
            else:
                payback_months = float('inf')

            years = list(range(1, 6))
            costs_manual = [total_manual_cost] * 5
            costs_automated = [
                total_automated_cost + (license_cost if i > 0 else (license_cost + implementation_cost))
                for i in range(5)
            ]
            cumulative_savings = [0]
            for i in range(5):
                if i == 0:
                    cumulative_savings.append(adjusted_annual_savings - total_first_year_cost)
                else:
                    cumulative_savings.append(
                        cumulative_savings[-1] + adjusted_annual_savings - subsequent_years_cost)
            cumulative_savings = cumulative_savings[1:]
        except Exception as e:
            st.error(f"An error occurred in calculations: {str(e)}")
            st.error(traceback.format_exc())
            total_manual_hours = 0
            total_automated_hours = 0
            total_manual_cost = 0
            total_automated_cost = 0
            adjusted_annual_savings = 0
            first_year_roi = 0
            subsequent_roi = 0
            payback_months = 0
            total_benefits = {}
            costs_manual = [0] * 5
            costs_automated = [0] * 5
            cumulative_savings = [0] * 5
            edition_specific_features = {edition: {}}

# ------------------ End of COL1 ------------------

# ----------- COL2: Display charts, export options, and summary -------------
with col2:
    st.markdown("<div class='section-header'>ROI Analysis Results</div>", unsafe_allow_html=True)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>${adjusted_annual_savings:,.2f}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Annual Savings</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with metric_col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        if first_year_roi != float('inf'):
            st.markdown(f"<div class='metric-value'>{first_year_roi:.1f}%</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='metric-value'>∞</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>First Year ROI</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with metric_col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        if payback_months != float('inf'):
            st.markdown(f"<div class='metric-value'>{payback_months:.1f} months</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='metric-value'>N/A</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Payback Period</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    if edition != "Free":
        st.markdown(f"### {edition} Edition Benefits")
        edition_features = list(edition_specific_features.get(edition, {}).keys())
        if len(edition_features) > 0:
            feature_values = [f"**{feature}**: ${edition_specific_features[edition][feature]:,.2f}" for feature in edition_features]
            st.markdown("Additional value from edition-specific features:")
            for value in feature_values:
                st.markdown(f"- {value}")
    st.markdown("### Time Savings Analysis")
    hours_df = pd.DataFrame({
        'Process': ['Manual Process', 'Endpoint Central'],
        'Hours': [total_manual_hours, total_automated_hours]
    })
    fig_hours = px.bar(
        hours_df,
        x='Process',
        y='Hours',
        title='Annual Hours Comparison: Manual vs. Automated',
        labels={'Hours': 'Hours per Year'},
        color='Process',
        color_discrete_map={'Manual Process': '#FF6B6B', 'Endpoint Central': '#4ECDC4'},
        template='plotly_white' if theme == 'Light' else 'plotly_dark'
    )
    fig_hours.update_layout(
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_color,
        height=500
    )
    fig_hours.update_traces(
        texttemplate='%{y:,.0f}',
        textposition='outside'
    )
    st.plotly_chart(fig_hours, use_container_width=True)
    st.markdown("### Cost Analysis")
    cost_df = pd.DataFrame({
        'Process': ['Manual Process', 'Endpoint Central'],
        'Cost': [total_manual_cost, total_automated_cost + license_cost]
    })
    fig_cost = px.bar(
        cost_df,
        x='Process',
        y='Cost',
        title='Annual Cost Comparison: Manual vs. Automated',
        labels={'Cost': 'Annual Cost ($)'},
        color='Process',
        color_discrete_map={'Manual Process': '#FF6B6B', 'Endpoint Central': '#4ECDC4'},
        template='plotly_white' if theme == 'Light' else 'plotly_dark'
    )
    fig_cost.update_layout(
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_color,
        height=500
    )
    fig_cost.update_traces(
        texttemplate='$%{y:,.0f}',
        textposition='outside'
    )
    st.plotly_chart(fig_cost, use_container_width=True)
    st.markdown("### 5-Year Projection")
    projection_df = pd.DataFrame({
        'Year': years,
        'Manual Process': costs_manual,
        'Endpoint Central': costs_automated,
        'Cumulative Savings': cumulative_savings
    })
    fig_projection = go.Figure()
    fig_projection.add_trace(go.Scatter(
        x=projection_df['Year'],
        y=projection_df['Manual Process'],
        mode='lines+markers',
        name='Manual Process',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    fig_projection.add_trace(go.Scatter(
        x=projection_df['Year'],
        y=projection_df['Endpoint Central'],
        mode='lines+markers',
        name='Endpoint Central',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8)
    ))
    fig_projection.add_trace(go.Scatter(
        x=projection_df['Year'],
        y=projection_df['Cumulative Savings'],
        mode='lines+markers',
        name='Cumulative Savings',
        line=dict(color='#5D9CEC', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    fig_projection.update_layout(
        title='5-Year Cost and Savings Projection',
        xaxis_title='Year',
        yaxis_title='Cost/Savings ($)',
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_color,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template='plotly_white' if theme == 'Light' else 'plotly_dark',
        height=500,
        hovermode="x unified"
    )
    fig_projection.update_yaxes(tickprefix='$', tickformat=',')
    st.plotly_chart(fig_projection, use_container_width=True)
    st.markdown("### Total Benefits Breakdown")
    benefits_df = pd.DataFrame({
        'Benefit': list(total_benefits.keys()),
        'Value': list(total_benefits.values())
    }).sort_values('Value', ascending=False)
    fig_benefits = px.bar(
        benefits_df,
        x='Benefit',
        y='Value',
        title='Breakdown of Annual Benefits',
        labels={'Value': 'Annual Value ($)', 'Benefit': ''},
        template='plotly_white' if theme == 'Light' else 'plotly_dark',
        color='Value',
        color_continuous_scale='Viridis'
    )
    fig_benefits.update_layout(
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_color,
        height=500,
        xaxis_tickangle=-45
    )
    fig_benefits.update_traces(
        texttemplate='$%{y:,.0f}',
        textposition='outside'
    )
    st.plotly_chart(fig_benefits, use_container_width=True)
    st.markdown("### Proportion of Benefits")
    fig_pie = px.pie(
        benefits_df,
        values='Value',
        names='Benefit',
        title='Distribution of Total Benefits',
        template='plotly_white' if theme == 'Light' else 'plotly_dark',
        color_discrete_sequence=px.colors.sequential.Viridis,
        hole=0.3
    )
    fig_pie.update_layout(
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font_color=plot_color,
        height=600
    )
    fig_pie.update_traces(
        textinfo='percent+label',
        textposition='inside',
        insidetextorientation='radial'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # The following expanders are now siblings, not nested:
    with st.expander("Detailed Comparison: Manual Process vs. Endpoint Central"):
        edition_specific_comparisons = {
            "Free": {
                "Response Time to Critical Updates": "Days to weeks",
                "Consistency in Deployment": "Limited consistency",
                "Ability to Track Compliance": "Basic reporting",
                "Remote Troubleshooting Capabilities": "Basic",
                "Bandwidth Usage Optimization": "Minimal",
                "Security Risk Exposure": "Somewhat reduced",
                "Staff Focus on Strategic Projects": "Limited improvement"
            },
            "Professional": {
                "Response Time to Critical Updates": "1-2 days",
                "Consistency in Deployment": "Good consistency",
                "Ability to Track Compliance": "Improved reporting",
                "Remote Troubleshooting Capabilities": "Good",
                "Bandwidth Usage Optimization": "Optimized",
                "Security Risk Exposure": "Moderately reduced",
                "Staff Focus on Strategic Projects": "Moderate improvement"
            },
            "Enterprise": {
                "Response Time to Critical Updates": "Hours to a day",
                "Consistency in Deployment": "Very consistent",
                "Ability to Track Compliance": "Comprehensive reporting",
                "Remote Troubleshooting Capabilities": "Advanced",
                "Bandwidth Usage Optimization": "Highly optimized",
                "Security Risk Exposure": "Significantly reduced",
                "Staff Focus on Strategic Projects": "Significant improvement"
            },
            "UEM": {
                "Response Time to Critical Updates": "Hours",
                "Consistency in Deployment": "Highly consistent",
                "Ability to Track Compliance": "Comprehensive cross-platform reporting",
                "Remote Troubleshooting Capabilities": "Advanced cross-platform",
                "Bandwidth Usage Optimization": "Highly optimized",
                "Security Risk Exposure": "Greatly reduced",
                "Staff Focus on Strategic Projects": "Major improvement"
            },
            "Security": {
                "Response Time to Critical Updates": "Near real-time",
                "Consistency in Deployment": "Maximum consistency",
                "Ability to Track Compliance": "Enterprise-grade security reporting",
                "Remote Troubleshooting Capabilities": "Advanced with security focus",
                "Bandwidth Usage Optimization": "Maximum optimization",
                "Security Risk Exposure": "Minimized",
                "Staff Focus on Strategic Projects": "Maximum improvement"
            }
        }
        comparison_data = {
            "Metric": [
                "Total Annual Hours Required",
                "Annual Labor Cost",
                "Response Time to Critical Updates",
                "Consistency in Deployment",
                "Ability to Track Compliance",
                "Remote Troubleshooting Capabilities",
                "Bandwidth Usage Optimization",
                "Security Risk Exposure",
                "Staff Focus on Strategic Projects"
            ],
            "Manual Process": [
                f"{total_manual_hours:,.0f} hours",
                f"${total_manual_cost:,.2f}",
                "Days to weeks",
                "Variable (human-dependent)",
                "Limited (manual reporting)",
                "Limited",
                "Suboptimal",
                "Higher",
                "Limited (focus on maintenance)"
            ],
            "Endpoint Central": [
                f"{total_automated_hours:,.0f} hours",
                f"${total_automated_cost:,.2f}",
                edition_specific_comparisons[edition]["Response Time to Critical Updates"],
                edition_specific_comparisons[edition]["Consistency in Deployment"],
                edition_specific_comparisons[edition]["Ability to Track Compliance"],
                edition_specific_comparisons[edition]["Remote Troubleshooting Capabilities"],
                edition_specific_comparisons[edition]["Bandwidth Usage Optimization"],
                edition_specific_comparisons[edition]["Security Risk Exposure"],
                edition_specific_comparisons[edition]["Staff Focus on Strategic Projects"]
            ],
            "Impact": [
                f"{total_manual_hours - total_automated_hours:,.0f} hours saved",
                f"${annual_labor_savings:,.2f} saved",
                "Faster vulnerability mitigation",
                "Improved reliability",
                "Better audit readiness",
                "Faster issue resolution",
                "Reduced network congestion",
                "Improved security posture",
                "More innovation"
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        fig_comparison = go.Figure(data=[
            go.Table(
                header=dict(
                    values=list(comparison_df.columns),
                    fill_color=theme_color,
                    font=dict(color='white', size=14),
                    align='center'
                ),
                cells=dict(
                    values=[comparison_df[col] for col in comparison_df.columns],
                    fill_color=[[plot_bg, card_bg] * len(comparison_df)],
                    font=dict(color=plot_color, size=12),
                    align=['left', 'center', 'center', 'center'],
                    height=30
                )
            )
        ])
        fig_comparison.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=500
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

    with st.expander("Strategic Recommendations"):
        if edition == "Free":
            st.markdown("""
            Based on the analysis, implementing the Free Edition of Endpoint Central for your IT infrastructure represents:

            1. **Entry-Level Automation**: A good starting point for basic automation of patch management.
            2. **Limited Value for Larger Environments**: Consider upgrading to a paid edition if managing more than 50 endpoints.
            3. **Foundation for Growth**: Establishes processes that can be expanded with paid editions as your needs grow.
            """)
        elif edition == "Professional":
            st.markdown("""
            Based on the analysis, implementing the Professional Edition of Endpoint Central for your IT infrastructure represents:

            1. **Significant Operational Efficiency**: The automation of routine tasks translates to substantial time and cost savings.
            2. **Rapid Return on Investment**: The payback period demonstrates quick value realization for LAN environments.
            3. **Improved Security Posture**: Better patch management and configuration control help reduce common security risks.
            4. **Resource Optimization**: IT staff can focus more on strategic initiatives rather than routine maintenance.
            """)
        elif edition == "Enterprise":
            st.markdown("""
            Based on the analysis, implementing the Enterprise Edition of Endpoint Central for your IT infrastructure represents:

            1. **Multi-Location Management**: Centralized control across distributed environments reduces complexity and overhead.
            2. **Enhanced Security Controls**: Additional features like USB device management provide stronger protection.
            3. **Improved Visibility**: Comprehensive audit capabilities and self-service portal improve both security and user experience.
            4. **Scalable Solution**: As your organization grows across locations, the centralized management becomes increasingly valuable.
            """)
        elif edition == "UEM":
            st.markdown("""
            Based on the analysis, implementing the UEM Edition of Endpoint Central for your IT infrastructure represents:

            1. **Cross-Platform Unification**: Single console management for diverse device types increases operational efficiency.
            2. **Advanced Deployment Capabilities**: OS deployment features significantly reduce provisioning time and effort.
            3. **Mobile-Inclusive Strategy**: Extending management to mobile devices provides comprehensive device lifecycle control.
            4. **Holistic Approach**: Managing all endpoints through a unified system reduces security gaps and management overhead.
            """)
        elif edition == "Security":
            st.markdown("""
            Based on the analysis, implementing the Security Edition of Endpoint Central for your IT infrastructure represents:

            1. **Comprehensive Security Focus**: Advanced protection against modern threats including ransomware and data loss.
            2. **Privilege Management**: Control of user rights helps prevent unauthorized changes and reduce attack surface.
            3. **Proactive Vulnerability Management**: Early identification and remediation of security issues.
            4. **Regulatory Compliance**: Enhanced security controls and reporting help meet stringent compliance requirements.
            5. **Maximum Protection**: A complete solution that addresses both management efficiency and security requirements.
            """)
    with st.expander("Export Your Results"):
        def generate_csv_report():
            try:
                buffer = io.BytesIO()
                data = {
                    'Metric': [
                        'Number of Devices', 'Number of Applications', 'Updates per Application',
                        'Hours per Update (Manual)', 'Technician Hourly Rate', 'Selected Edition',
                        'Automation Efficiency', 'Annual License Cost', 'Implementation Cost',
                        'Total Manual Hours', 'Total Automated Hours', 'Hours Saved',
                        'Total Manual Cost', 'Total Automated Cost', 'Direct Labor Savings',
                        'Compliance Reporting Savings', 'Bandwidth Cost Savings',
                        'Security Incident Reduction Value', 'Downtime Cost Savings',
                        'Total Annual Savings', 'First Year ROI', 'Subsequent Years ROI',
                        'Payback Period (Months)'
                    ],
                    'Value': [
                        devices, applications, updates_per_app,
                        hours_per_update, hourly_rate, edition,
                        f"{automation_efficiency}%", f"${license_cost:,.2f}",
                        f"${implementation_cost:,.2f}",
                        f"{total_manual_hours:,.2f}", f"{total_automated_hours:,.2f}",
                        f"{total_manual_hours - total_automated_hours:,.2f}",
                        f"${total_manual_cost:,.2f}", f"${total_automated_cost:,.2f}",
                        f"${annual_labor_savings:,.2f}",
                        f"${annual_compliance_savings:,.2f}", f"${bandwidth_savings_adjusted:,.2f}",
                        f"${security_incidents_reduction_value:,.2f}",
                        f"${downtime_cost_saved:,.2f}",
                        f"${adjusted_annual_savings:,.2f}",
                        f"{first_year_roi:.2f}%" if first_year_roi != float('inf') else "∞",
                        f"{subsequent_roi:.2f}%" if subsequent_roi != float('inf') else "∞",
                        f"{payback_months:.2f}" if payback_months != float('inf') else "N/A"
                    ]
                }
                if edition != "Free" and len(edition_specific_features[edition]) > 0:
                    for feature, value in edition_specific_features[edition].items():
                        data['Metric'].append(f"{feature} Value")
                        data['Value'].append(f"${value:,.2f}")
                df = pd.DataFrame(data)
                df.to_csv(buffer, index=False)
                return buffer
            except Exception as e:
                st.error(f"Error generating CSV: {str(e)}")
                return None
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            csv_buffer = generate_csv_report()
            if csv_buffer:
                csv_data = csv_buffer.getvalue()
                b64_csv = base64.b64encode(csv_data).decode()
                href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="maxar_endpoint_central_roi_{edition.lower()}_edition.csv" class="btn" style="text-decoration:none; background-color:{theme_color}; color:white; padding:10px 15px; border-radius:5px; display:inline-block; text-align:center;">Download Results as CSV</a>'
                st.markdown(href_csv, unsafe_allow_html=True)
        with export_col2:
            if st.button("Generate PDF Report", key="pdf_button"):
                with st.spinner("Generating PDF report..."):
                    def generate_pdf_report():
                        try:
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", "B", 16)
                            pdf.cell(0, 10, "Endpoint Central ROI Calculator for MAXAR Technologies", ln=True, align="C")
                            pdf.set_font("Arial", "", 12)
                            pdf.cell(0, 10, f"Report for {edition} Edition", ln=True, align="C")
                            pdf.line(10, 30, 200, 30)
                            pdf.ln(10)
                            pdf.set_font("Arial", "B", 14)
                            pdf.cell(0, 10, "Input Parameters", ln=True)
                            pdf.set_font("Arial", "", 10)
                            params = [
                                ["Number of Devices", f"{devices}"],
                                ["Number of Applications", f"{applications}"],
                                ["Updates per Application", f"{updates_per_app}"],
                                ["Hours per Update (Manual)", f"{hours_per_update}"],
                                ["Technician Hourly Rate", f"${hourly_rate}"],
                                ["Automation Efficiency", f"{automation_efficiency}%"],
                                ["Annual License Cost", f"${license_cost:,.2f}"],
                                ["Implementation Cost", f"${implementation_cost:,.2f}"]
                            ]
                            for param in params:
                                pdf.cell(90, 7, param[0], border=1)
                                pdf.cell(90, 7, param[1], border=1, ln=True)
                            pdf.ln(10)
                            pdf.set_font("Arial", "B", 14)
                            pdf.cell(0, 10, "Key Results", ln=True)
                            pdf.set_font("Arial", "", 10)
                            results = [
                                ["Annual Savings", f"${adjusted_annual_savings:,.2f}"],
                                ["First Year ROI", f"{first_year_roi:.1f}%" if first_year_roi != float('inf') else "∞"],
                                ["Subsequent Years ROI", f"{subsequent_roi:.1f}%" if subsequent_roi != float('inf') else "∞"],
                                ["Payback Period", f"{payback_months:.1f} months" if payback_months != float('inf') else "N/A"]
                            ]
                            for result in results:
                                pdf.cell(90, 7, result[0], border=1)
                                pdf.cell(90, 7, result[1], border=1, ln=True)
                            pdf.ln(10)
                            pdf.set_font("Arial", "B", 14)
                            pdf.cell(0, 10, "Time and Cost Comparison", ln=True)
                            pdf.set_font("Arial", "", 10)
                            comparisons = [
                                ["Total Manual Hours", f"{total_manual_hours:,.0f} hours"],
                                ["Total Automated Hours", f"{total_automated_hours:,.0f} hours"],
                                ["Hours Saved", f"{total_manual_hours - total_automated_hours:,.0f} hours"],
                                ["Manual Process Cost", f"${total_manual_cost:,.2f}"],
                                ["Automated Process Cost", f"${total_automated_cost:,.2f}"],
                                ["Direct Labor Savings", f"${annual_labor_savings:,.2f}"]
                            ]
                            for comp in comparisons:
                                pdf.cell(90, 7, comp[0], border=1)
                                pdf.cell(90, 7, comp[1], border=1, ln=True)
                            pdf.ln(10)
                            pdf.set_font("Arial", "B", 14)
                            pdf.cell(0, 10, "Benefits Breakdown", ln=True)
                            pdf.set_font("Arial", "", 10)
                            for benefit, value in total_benefits.items():
                                pdf.cell(120, 7, benefit, border=1)
                                pdf.cell(60, 7, f"${value:,.2f}", border=1, ln=True)
                            pdf.ln(10)
                            if edition != "Free" and len(edition_specific_features[edition]) > 0:
                                pdf.set_font("Arial", "B", 14)
                                pdf.cell(0, 10, f"{edition} Edition Specific Features", ln=True)
                                pdf.set_font("Arial", "", 10)
                                for feature, value in edition_specific_features[edition].items():
                                    pdf.cell(120, 7, feature, border=1)
                                    pdf.cell(60, 7, f"${value:,.2f}", border=1, ln=True)
                            pdf.ln(10)
                            pdf.set_font("Arial", "B", 14)
                            pdf.cell(0, 10, "5-Year Projection Summary", ln=True)
                            pdf.set_font("Arial", "", 10)
                            pdf.cell(40, 7, "Year", border=1)
                            pdf.cell(50, 7, "Manual Cost", border=1)
                            pdf.cell(50, 7, "Automated Cost", border=1)
                            pdf.cell(50, 7, "Cumulative Savings", border=1, ln=True)
                            for i in range(5):
                                pdf.cell(40, 7, f"Year {i + 1}", border=1)
                                pdf.cell(50, 7, f"${costs_manual[i]:,.2f}", border=1)
                                pdf.cell(50, 7, f"${costs_automated[i]:,.2f}", border=1)
                                pdf.cell(50, 7, f"${cumulative_savings[i]:,.2f}", border=1, ln=True)
                            pdf.ln(10)
                            pdf.set_font("Arial", "B", 14)
                            pdf.cell(0, 10, "Conclusion", ln=True)
                            pdf.set_font("Arial", "", 10)
                            if edition == "Free":
                                conclusion = "The Free Edition provides basic endpoint management capabilities suitable for small environments up to 50 devices."
                            elif edition == "Professional":
                                conclusion = "The Professional Edition offers strong ROI for LAN environments with significant automation benefits."
                            elif edition == "Enterprise":
                                conclusion = "The Enterprise Edition provides enhanced value for multi-location environments with centralized management needs."
                            elif edition == "UEM":
                                conclusion = "The UEM Edition delivers comprehensive device management across all platforms with advanced deployment capabilities."
                            else:
                                conclusion = "The Security Edition offers maximum protection and management capabilities, ideal for security-conscious organizations."
                            pdf.multi_cell(0, 7, conclusion)
                            pdf.ln(10)
                            pdf.set_font("Arial", "I", 8)
                            pdf.cell(0, 10, "© 2025 MAXAR Technologies | This report is for informational purposes only.",
                                     ln=True, align="C")
                            pdf.cell(0, 10,
                                     "Contact MAXAR Technologies for a detailed assessment tailored to your specific environment.",
                                     ln=True, align="C")
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                                pdf_path = tmp.name
                                pdf.output(pdf_path)
                            return pdf_path
                        except Exception as e:
                            st.error(f"Failed to generate PDF: {str(e)}")
                            return None
                    pdf_path = generate_pdf_report()
                    if pdf_path:
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        b64_pdf = base64.b64encode(pdf_bytes).decode()
                        href_pdf = f'<a href="data:application/pdf;base64,{b64_pdf}" download="maxar_endpoint_central_roi_{edition.lower()}_edition.pdf" class="btn" style="text-decoration:none; background-color:{theme_color}; color:white; padding:10px 15px; border-radius:5px; display:inline-block; text-align:center;">Download PDF Report</a>'
                        st.markdown(href_pdf, unsafe_allow_html=True)
                        try:
                            os.unlink(pdf_path)
                        except:
                            pass
                    else:
                        st.error("Failed to generate PDF report. Please try again.")
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {text_color};">
        © 2025 MAXAR Technologies | Endpoint Central ROI Calculator<br>
        <span style="font-size: 0.8em;">Calculator Version 1.0 | Based on ManageEngine Endpoint Central Pricing as of March 2025<br>
        Disclaimer: This calculator provides estimates. Actual results may vary. Please consult with our technicians for a detailed assessment.</span>
    </div>
    """, unsafe_allow_html=True)

    def handle_calculation_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                st.error(f"Calculation error: {str(e)}")
                st.error(traceback.format_exc())
                return None
        return wrapper

    @handle_calculation_error
    def save_calculator_state():
        state = {
            "devices": devices,
            "applications": applications,
            "updates_per_app": updates_per_app,
            "hours_per_update": hours_per_update,
            "hourly_rate": hourly_rate,
            "automation_efficiency": automation_efficiency,
            "edition": edition,
            "implementation_cost": implementation_cost,
            "security_benefit": security_benefit,
            "compliance_time_saved": compliance_time_saved,
            "downtime_reduction": downtime_reduction,
            "bandwidth_savings": bandwidth_savings,
            "theme": theme
        }
        return json.dumps(state)

    @handle_calculation_error
    def load_calculator_state(state_json):
        try:
            state = json.loads(state_json)
            return state
        except:
            return None
