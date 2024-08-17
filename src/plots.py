import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_plot(df, start_times, end_times, plot_title="Time report"):
    assert "Tags" in df, "Error: 'Tags' column is missing from the dataframe"

    df['StartDateTime'] = pd.to_datetime(df['Time'].str.split(' -> ').str[0])
    df['EndDateTime'] = pd.to_datetime(df['Time'].str.split(' -> ').str[1])
    df['Duration'] = df['EndDateTime'] - df['StartDateTime']

    # y-levels based on unique days
    df['Day'] = df['StartDateTime'].dt.date
    unique_days = sorted(df['Day'].unique())
    y_levels = {day: i for i, day in enumerate(unique_days)}
    df['y'] = df['Day'].map(y_levels)

    # colors based on unique tags
    unique_tags = df['Tags'].unique()
    color_map = {tag: color for tag, color in zip(unique_tags, plt.cm.Set3(np.linspace(0, 1, len(unique_tags))))}

    plt.figure(figsize=(10, 6))

    for day in unique_days:
        day_data = df[df['Day'] == day]
        plt.barh(day_data['y'], day_data['Duration'].dt.total_seconds() / 3600,
                 left=day_data['StartDateTime'].dt.hour + day_data['StartDateTime'].dt.minute / 60,
                 color=day_data['Tags'].map(color_map), label=f'Day {day}')

    plt.title(plot_title)
    plt.yticks(list(y_levels.values()), labels=[str(day) for day in unique_days])
    plt.grid(axis='x', which='major', linestyle='--')

    handles = [plt.Rectangle((0,0),1,1, color=color_map[tag]) for tag in unique_tags]
    plt.legend(handles, unique_tags, title="Tags")
    plt.xticks(range(0, 24))
    
    return plt

