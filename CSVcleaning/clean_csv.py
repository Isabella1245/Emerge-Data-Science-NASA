import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors


def clean_precipitation_data(df):
    df = df.copy()
    df[' precipitation'] = df[' precipitation'].replace(-99.99, np.nan) /100
    df.drop(columns=['COOPID'], inplace=True)

    df[[' YEAR', ' MONTH', ' DAY']] = df[[' YEAR', ' MONTH', ' DAY']].apply(pd.to_numeric, errors='coerce')
    df.loc[df[' DAY'] == 0, ' DAY'] = 1

    df['date'] = pd.to_datetime(dict(year=df[' YEAR'], month=df[' MONTH'], day=df[' DAY']), errors='coerce')
    df = df.dropna(subset=['date'])

    df.set_index('date', inplace=True)
    df.drop(columns=[' YEAR', ' MONTH', ' DAY'], inplace=True)

    df = df.resample('M').mean()

    return df


def output_precipitation_data(df, output_path):
    df.to_csv(output_path, index=True)
    print(f"Saved cleaned data to {output_path}")


def plot_precipitation(df, title='Precipitation Over Time', save_path=None):
    fig, ax = plt.subplots(figsize=(12, 6))
    line, = ax.plot(df.index, df[' precipitation'], marker='o', linestyle='-', markersize=4)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Precipitation (inches)')
    ax.grid(True)


    cursor = mplcursors.cursor(line, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        date = df.index[sel.index].strftime('%Y-%m-%d')
        value = df[' precipitation'].iloc[sel.index]
        sel.annotation.set_text(f"{date}\n{value:.3f} in")

    if save_path:
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
        plt.close(fig)  
    else:
        plt.show()


def process_folder(input_folder, output_folder, plot_folder=None):
    os.makedirs(output_folder, exist_ok=True)
    if plot_folder:
        os.makedirs(plot_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            df = pd.read_csv(input_path)
            df_clean = clean_precipitation_data(df)

            output_path = os.path.join(output_folder, f"cleaned_{filename}")
            output_precipitation_data(df_clean, output_path)

            if plot_folder:
                plot_path = os.path.join(plot_folder, f"{os.path.splitext(filename)[0]}.png")
                plot_precipitation(df_clean, title=filename, save_path=plot_path)


input_folder = 'C:/TEMPinput'
output_folder = 'C:/TEMPoutput'
plot_folder = 'C:/TEMPplots'

process_folder(input_folder, output_folder, plot_folder)
