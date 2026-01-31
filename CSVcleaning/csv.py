import datetime
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import os
import mplcursors

def read_precipitation_data(file_path):

    """Input format:
    COOPID, YEAR, MONTH, DAY, precipitation
    80211,1931,1,1,-99.99000
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    print(df.columns)


    return df

def clean_precipitation_data(df):
    df = df.copy()

    # clean precipitation
    df['precipitation'] = df['precipitation'].replace(-99.99, np.nan) 

    # drop unused column
    df.drop(columns=['COOPID'], inplace=True)

    # force date columns to numeric
    df[['YEAR', 'MONTH', 'DAY']] = df[['YEAR', 'MONTH', 'DAY']].apply(
        pd.to_numeric, errors='coerce'
    )

    # monthly datasets often use DAY = 0
    df.loc[df['DAY'] == 0, 'DAY'] = 1

    # build datetime safely
    df['date'] = pd.to_datetime(
        dict(year=df['YEAR'], month=df['MONTH'], day=df['DAY']),
        errors='coerce'
    )

    # drop invalid dates
    df = df.dropna(subset=['date'])

    # set index
    df.set_index('date', inplace=True)

    # drop date parts
    df.drop(columns=['YEAR', 'MONTH', 'DAY'], inplace=True)

    # resample to monthly mean
    df = df.resample('M').mean()

    return df

def output_precipitation_data(df, output_path):
    
    """Output the cleaned precipitation data to a CSV file."""
    df.to_csv(output_path, index=True)
    print(f"Cleaned data saved to {output_path}")


import mplcursors

def plot_precipitation(df, start_date=None, end_date=None):
    if start_date:
        df = df[df.index >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df.index <= pd.to_datetime(end_date)]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot line and keep the Line2D object
    line, = ax.plot(
        df.index,
        df['precipitation'],
        marker='o',
        linestyle='-',
        markersize=3
    )

    ax.set_title('Precipitation Over Time (Gainesville)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Precipitation (inches)')
    ax.grid(True)

    # Only hover over the plotted line
    cursor = mplcursors.cursor(line, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        date = df.index[sel.index].strftime('%Y-%m-%d')
        value = df['precipitation'].iloc[sel.index]
        sel.annotation.set_text(f"{date}\n{value:.3f} in")

    plt.show()



def main():
    input_file = 'C:/Users/genui/Desktop/NASA/input.csv'
    output_file = 'cleaned_precipitation_data.csv'
    
    # Read the data
    df = read_precipitation_data(input_file)
    
    # Clean the data
    df = clean_precipitation_data(df)
    
    # Output the cleaned data
    output_precipitation_data(df, output_file)
    
    # Plot the data
    plot_precipitation(df, start_date='2020-01-01', end_date='2024-12-31')
    
if __name__ == "__main__":
    main()