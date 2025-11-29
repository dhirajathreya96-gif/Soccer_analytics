import pandas as pd
import numpy as np

# Set a seed for reproducibility
np.random.seed(42)

# --- 1. Data Generation (1000 Rows) ---

N_ROWS = 1000
N_PLAYERS = 50
N_TEAMS = 10

# Helper lists for realistic data
player_ids = [f'P{i:03d}' for i in range(1, N_PLAYERS + 1)]
team_names = [f'Team {chr(65 + i)}' for i in range(N_TEAMS)]
positions = ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']
opponent_strength = ['Strong', 'Average', 'Weak']

# Create the base DataFrame
data = pd.DataFrame({
    'Match_ID': np.random.randint(100, 300, N_ROWS),
    'Player_ID': np.random.choice(player_ids, N_ROWS),
    'Team_Name': np.random.choice(team_names, N_ROWS),
    'Opponent_Strength': np.random.choice(opponent_strength, N_ROWS),
    'Position': np.random.choice(positions, N_ROWS, p=[0.25, 0.35, 0.30, 0.10]),
    'Minutes_Played': np.random.randint(1, 91, N_ROWS),
    'Goals': np.random.poisson(0.4, N_ROWS), # Most are 0, some are 1, very few are 2+
    'Assists': np.random.poisson(0.2, N_ROWS),
    'Shots_On_Target': np.random.randint(0, 6, N_ROWS),
    'Pass_Completion_Rate': np.random.uniform(0.65, 0.95, N_ROWS).round(2),
    'Tackles_Succeeded': np.random.randint(0, 7, N_ROWS),
    'Interceptions': np.random.randint(0, 5, N_ROWS)
})

# Filter out Goalkeeper rows for certain metrics for realism (setting them to 0)
goalkeeper_mask = data['Position'] == 'Goalkeeper'
data.loc[goalkeeper_mask, ['Goals', 'Assists', 'Shots_On_Target', 'Tackles_Succeeded', 'Interceptions']] = 0

# --- 2. Complex Python Manipulation ---

# **Manipulation A: Conditional Feature Creation (Performance_Score)**
# The score is a weighted combination of offensive and defensive metrics.
# Weights: Goals (40%), Assists (20%), Shots_On_Target (10%), Pass_Completion_Rate (10%), Tackles_Succeeded (10%), Interceptions (10%)

offensive_weight = (data['Goals'] * 4.0) + (data['Assists'] * 2.0) + (data['Shots_On_Target'] * 0.5)
defensive_weight = (data['Tackles_Succeeded'] * 1.0) + (data['Interceptions'] * 0.5)

# Calculate a raw score
data['Raw_Score'] = offensive_weight + defensive_weight + (data['Pass_Completion_Rate'] * 5)

# Normalize and scale the score for a final Performance_Score between 0 and 10
min_score = data['Raw_Score'].min()
max_score = data['Raw_Score'].max()

data['Performance_Score'] = 1 + 9 * (data['Raw_Score'] - min_score) / (max_score - min_score)
data['Performance_Score'] = data['Performance_Score'].round(2)

# Drop the temporary raw score column
data = data.drop(columns=['Raw_Score'])


# **Manipulation B: Categorical Binning (Efficiency_Tier)**
# Categorize performance into tiers based on the score distribution.
bins = [0, 3, 5, 7.5, 10]
labels = ['Poor', 'Average', 'Good', 'Excellent']
data['Efficiency_Tier'] = pd.cut(data['Performance_Score'], bins=bins, labels=labels, right=True, include_lowest=True)


# **Manipulation C: Aggregation and Pivoting (Player Summary Table)**
# Create a second, aggregated table that summarizes each player's average performance
# against different opponent strengths. This structure is often valuable for Power BI visuals.

player_summary = data.groupby(['Player_ID', 'Opponent_Strength'])['Performance_Score'].mean().reset_index()

# Pivot the table so Opponent_Strength becomes columns, showing the average performance score
# as a pivot table, which is a key preparation step for Power BI's reporting efficiency.
player_summary_pivoted = player_summary.pivot(
    index='Player_ID',
    columns='Opponent_Strength',
    values='Performance_Score'
).reset_index()

# Rename the new columns for clarity
player_summary_pivoted.columns.name = None
player_summary_pivoted = player_summary_pivoted.rename(columns={
    'Strong': 'Avg_Score_vs_Strong',
    'Average': 'Avg_Score_vs_Average',
    'Weak': 'Avg_Score_vs_Weak'
})

# Fill NaN values (in case a player never played against a specific strength)
player_summary_pivoted = player_summary_pivoted.fillna(0).round(2)

# Merge the player summary back into the main dataset to enrich the rows
# (e.g., adding a player's average performance metrics across different contexts)
# We will use this summary table as a separate sheet for a star schema approach.

# Finalize the main dataset for the report (data)
final_report_data = data[['Match_ID', 'Player_ID', 'Team_Name', 'Position', 'Opponent_Strength',
                          'Goals', 'Assists', 'Minutes_Played', 'Shots_On_Target',
                          'Pass_Completion_Rate', 'Tackles_Succeeded', 'Interceptions',
                          'Performance_Score', 'Efficiency_Tier']]

# --- 3. Export to Excel ---
excel_file_path = 'Soccer_Analytics_Report_Data.xlsx'

with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
    final_report_data.to_excel(writer, sheet_name='Match_Performance_Facts', index=False)
    player_summary_pivoted.to_excel(writer, sheet_name='Player_Summary_Dim', index=False)

print(f"✅ Success! Two sheets of prepared data saved to '{excel_file_path}'")
print("\nSheets created:")
print(f"1. Match_Performance_Facts: {len(final_report_data)} rows (Raw Match-Level Data)")
print(f"2. Player_Summary_Dim: {len(player_summary_pivoted)} rows (Aggregated Player Data)")