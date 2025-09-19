import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import plotly.graph_objects as go
from dash import Dash, dcc, html
from plotly.subplots import make_subplots
import logging

# --- Configuration & Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URLs for the data sources
URL_TOMSK = "http://sosrff.tsu.ru/new/shm.jpg"  # Tomsk data is embedded in an image, we'll simulate extracting it
URL_CUMIANA = "https://www.vlf.it/cumiana/schumann.php"

# --- Data Fetching ---

def fetch_tomsk_data_simulated():
    """
    Simulates fetching and parsing data for Tomsk.
    In a real-world scenario, this would involve OCR or finding a direct data source.
    For this example, we generate realistic placeholder data.
    """
    logging.info("Simulating data fetch for Tomsk.")
    try:
        # Simulate data points for a 24-hour period
        base_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        timestamps = [base_time + timedelta(minutes=15 * i) for i in range(96)] # 24 hours * 4 points/hour
        
        data = []
        # Mode 1: ~7.83 Hz
        # Mode 2: ~14.3 Hz
        # Mode 3: ~20.8 Hz
        # Mode 4: ~27.3 Hz
        modes = {
            1: (7.83, 0.1),
            2: (14.3, 0.08),
            3: (20.8, 0.05),
            4: (27.3, 0.03)
        }
        
        for ts in timestamps:
            for mode, (freq_base, amp_base) in modes.items():
                # Add some noise to make it look realistic
                freq = freq_base + pd.np.random.uniform(-0.1, 0.1)
                amp = amp_base + pd.np.random.uniform(-0.02, 0.02)
                data.append([ts, 'Tomsk', f'Mode {mode}', freq, amp])

        df = pd.DataFrame(data, columns=['timestamp', 'location', 'mode', 'frequency', 'amplitude'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        logging.info("Tomsk simulation successful.")
        return df
    except Exception as e:
        logging.error(f"Failed to simulate TomSK data: {e}")
        return pd.DataFrame()


def fetch_cumiana_data():
    """
    Fetches and parses the Schumann Resonance data from the VLF.it Cumiana page.
    """
    logging.info(f"Fetching data from Cumiana: {URL_CUMIANA}")
    try:
        response = requests.get(URL_CUMIANA, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the script tag containing the data arrays
        scripts = soup.find_all('script')
        data_script = None
        for script in scripts:
            if 'var F1' in script.text:
                data_script = script.text
                break
        
        if not data_script:
            logging.error("Data script not found on Cumiana page.")
            return pd.DataFrame()

        # Extract data using regex
        times_str = re.search(r"var labels = \[(.*?)\];", data_script)
        f1_str = re.search(r"var F1 = \[(.*?)\];", data_script)
        a1_str = re.search(r"var A1 = \[(.*?)\];", data_script)
        f2_str = re.search(r"var F2 = \[(.*?)\];", data_script)
        a2_str = re.search(r"var A2 = \[(.*?)\];", data_script)
        f3_str = re.search(r"var F3 = \[(.*?)\];", data_script)
        a3_str = re.search(r"var A3 = \[(.*?)\];", data_script)
        f4_str = re.search(r"var F4 = \[(.*?)\];", data_script)
        a4_str = re.search(r"var A4 = \[(.*?)\];", data_script)

        if not all([times_str, f1_str, a1_str, f2_str, a2_str, f3_str, a3_str, f4_str, a4_str]):
            logging.error("Could not extract all required data arrays from Cumiana script.")
            return pd.DataFrame()

        # Clean and convert to lists of floats/strings
        times = [t.strip('"') for t in times_str.group(1).split(',')]
        freq1 = [float(f) if f != 'null' else None for f in f1_str.group(1).split(',')]
        amp1 = [float(a) if a != 'null' else None for a in a1_str.group(1).split(',')]
        freq2 = [float(f) if f != 'null' else None for f in f2_str.group(1).split(',')]
        amp2 = [float(a) if a != 'null' else None for a in a2_str.group(1).split(',')]
        freq3 = [float(f) if f != 'null' else None for f in f3_str.group(1).split(',')]
        amp3 = [float(a) if a != 'null' else None for a in a3_str.group(1).split(',')]
        freq4 = [float(f) if f != 'null' else None for f in f4_str.group(1).split(',')]
        amp4 = [float(a) if a != 'null' else None for a in a4_str.group(1).split(',')]
        
        # Create timestamps
        base_date = datetime.utcnow().date()
        timestamps = [datetime.combine(base_date, datetime.strptime(t, '%H:%M').time()) for t in times]
        
        # Combine into a structured list
        data = []
        for i, ts in enumerate(timestamps):
            data.append([ts, 'Cumiana', 'Mode 1', freq1[i], amp1[i]])
            data.append([ts, 'Cumiana', 'Mode 2', freq2[i], amp2[i]])
            data.append([ts, 'Cumiana', 'Mode 3', freq3[i], amp3[i]])
            data.append([ts, 'Cumiana', 'Mode 4', freq4[i], amp4[i]])

        df = pd.DataFrame(data, columns=['timestamp', 'location', 'mode', 'frequency', 'amplitude'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.dropna(subset=['frequency', 'amplitude'], inplace=True)
        
        logging.info("Cumiana data fetched and parsed successfully.")
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request to Cumiana failed: {e}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"An error occurred during Cumiana data processing: {e}")
        return pd.DataFrame()

# --- Data Processing ---

def combine_data(df_tomsk, df_cumiana):
    """Combines data from two sources into a single DataFrame."""
    logging.info("Combining Tomsk and Cumiana dataframes.")
    if df_tomsk.empty and df_cumiana.empty:
        logging.warning("Both dataframes are empty. Returning an empty dataframe.")
        return pd.DataFrame(columns=['timestamp', 'location', 'mode', 'frequency', 'amplitude'])
    
    combined_df = pd.concat([df_tomsk, df_cumiana], ignore_index=True)
    combined_df.sort_values(by='timestamp', inplace=True)
    return combined_df

# --- Dashboard Creation ---

def create_dashboard(df):
    """Creates and runs the Plotly Dash dashboard."""
    if df.empty:
        logging.error("Cannot create dashboard, input dataframe is empty.")
        return

    app = Dash(__name__)
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=('Frequency (Hz)', 'Amplitude (Arbitrary Units)'),
        vertical_spacing=0.1
    )

    colors = {
        ('Tomsk', 'Mode 1'): '#1f77b4', ('Cumiana', 'Mode 1'): '#aec7e8',
        ('Tomsk', 'Mode 2'): '#ff7f0e', ('Cumiana', 'Mode 2'): '#ffbb78',
        ('Tomsk', 'Mode 3'): '#2ca02c', ('Cumiana', 'Mode 3'): '#98df8a',
        ('Tomsk', 'Mode 4'): '#d62728', ('Cumiana', 'Mode 4'): '#ff9896',
    }
    
    # Add traces
    for location in df['location'].unique():
        for mode in sorted(df['mode'].unique()):
            df_filtered = df[(df['location'] == location) & (df['mode'] == mode)]
            color_key = (location, mode)
            
            # Frequency Trace
            fig.add_trace(go.Scatter(
                x=df_filtered['timestamp'],
                y=df_filtered['frequency'],
                mode='lines',
                name=f'{location} {mode} Freq',
                legendgroup=f'{location}-{mode}',
                line=dict(color=colors[color_key], width=2 if location == 'Cumiana' else 1.5),
                opacity=1 if location == 'Cumiana' else 0.8
            ), row=1, col=1)

            # Amplitude Trace
            fig.add_trace(go.Scatter(
                x=df_filtered['timestamp'],
                y=df_filtered['amplitude'],
                mode='lines',
                name=f'{location} {mode} Amp',
                legendgroup=f'{location}-{mode}',
                showlegend=False, # Avoid duplicate legend entries
                line=dict(color=colors[color_key], width=2 if location == 'Cumiana' else 1.5),
                opacity=1 if location == 'Cumiana' else 0.8
            ), row=2, col=1)

    # Update layout
    fig.update_layout(
        title_text='Schumann Resonance Live Dashboard: Tomsk vs. Cumiana',
        height=800,
        legend_title_text='Data Series',
        template='plotly_dark'
    )
    fig.update_yaxes(title_text="Frequency (Hz)", row=1, col=1)
    fig.update_yaxes(title_text="Amplitude", row=2, col=1)
    fig.update_xaxes(title_text="Time (UTC)", row=2, col=1)

    app.layout = html.Div(children=[
        html.H1(children='Schumann Resonance Dashboard'),
        html.Div(children='''
            Comparing real-time data from Tomsk, Russia (simulated) and Cumiana, Italy.
        '''),
        dcc.Graph(
            id='schumann-graph',
            figure=fig
        )
    ])

    logging.info("Starting Dash server...")
    app.run_server(debug=True)

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Fetch data
    tomsk_df = fetch_tomsk_data_simulated()
    cumiana_df = fetch_cumiana_data()

    # 2. Combine data
    final_df = combine_data(tomsk_df, cumiana_df)

    # 3. Save combined data to CSV
    if not final_df.empty:
        output_filename = 'combined_schumann_data.csv'
        final_df.to_csv(output_filename, index=False, date_format='%Y-%m-%d %H:%M:%S')
        logging.info(f"Combined data successfully saved to {output_filename}")
    else:
        logging.warning("No data to save to CSV.")

    # 4. Create and launch the dashboard
    create_dashboard(final_df)