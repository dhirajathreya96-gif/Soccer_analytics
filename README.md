# Soccer_analytics
The primary objective of this project is to analyze player performance based on various in-game metrics and opponent strength. The report provides a clear, categorized view of player efficiency to aid in tactical assessment and recruitment.

⚽ Soccer Analytics Performance Report

A Data Analytics project demonstrating a complete ETL (Extract, Transform, Load) workflow: from generating simulated data with Python, to preparing and modeling the data with Pandas, and finally visualizing performance metrics in an interactive Power BI dashboard.

📁 Repository Structure
The project is divided into the following key files and folders:

File/Folder |	Description
soccer_data.py |	Python script used to generate 1000 rows of synthetic performance data and perform data manipulation/preparation.
Soccer_Analytics_Report_Data.xlsx |	The prepared dataset, containing two sheets (Match_Performance_Facts and Player_Summary_Dim), ready for Power BI import.
Soccer_Analytics_PBI.pbix |	The final Power BI report file, containing the data model, DAX measures, and dashboard visuals.
README.md	This document (formatted in Markdown).

💻 Data Pipeline (ETL Workflow)
The data transformation process includes complex steps to create valuable features for the report.

1. Data Generation

Technology: Python, Pandas, NumPy

Method: Generated 1000 rows of simulated match-level data for 50 players across 10 teams.

2. Transformation & Feature Engineering

The soccer_data_prep.py script performs the following critical data preparation steps:

Calculated KPI (Performance_Score): A weighted average score (0-10) is calculated based on both offensive (Goals, Assists) and defensive (Tackles, Interceptions) metrics.

Categorical Binning (Efficiency_Tier): The continuous Performance_Score is converted into a categorical tier (e.g., 'Poor', 'Average', 'Good', 'Excellent') using pd.cut().

Aggregation and Pivoting: A separate dimensional table (Player_Summary_Dim) is created by aggregating the average performance scores against different Opponent_Strength categories and pivoting the result for efficient lookup.

3. Data Modeling

Tool: Power BI

Model: A Star Schema is implemented by creating a One-to-Many relationship between the Player_Summary_Dim (Dimension Table) and the Match_Performance_Facts (Fact Table) using the Player_ID key.

✨ Key Dashboard Features
The Power BI report focuses on interactivity and comparative analysis:

KPI Overview: Cards tracking Total Matches, Overall Avg. Score, and Total Goals.

Performance Comparison: A table showing each player's average score when facing Strong vs. Weak opponents.

Efficiency Distribution: A visual breakdown of how player performances fall across the four Efficiency_Tier categories.

Slicers: Interactive filters allow users to slice data by Team, Position, and Opponent Strength to conduct granular analysis.
