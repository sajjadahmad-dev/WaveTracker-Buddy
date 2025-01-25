import os
import gradio as gr
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Fetch API keys from environment variables
api_key = os.getenv("OPENCELLID_API_KEY")
base_url = os.getenv("BASE_URL", "https://opencellid.org/cell/get")
groq_api_key = os.getenv("GROQ_API_KEY")

if not api_key or not groq_api_key:
    raise ValueError("API keys are missing! Please set them in the .env file.")

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)

# Function to fetch tower data from OpenCellID
def fetch_tower_data(mcc, mnc, cellid, lac):
    params = {
        'key': api_key,
        'mcc': mcc,
        'mnc': mnc,
        'cellid': cellid,
        'lac': lac
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            error = root.find(".//err")
            if error is not None:
                return f"Error: {error.attrib.get('info')}"
            else:
                cell_data = {
                    "latitude": root.find(".//cell").attrib.get("lat"),
                    "longitude": root.find(".//cell").attrib.get("lon"),
                    "mcc": root.find(".//cell").attrib.get("mcc"),
                    "mnc": root.find(".//cell").attrib.get("mnc"),
                    "lac": root.find(".//cell").attrib.get("lac"),
                    "cellid": root.find(".//cell").attrib.get("cellid"),
                    "range": root.find(".//cell").attrib.get("range"),
                    "samples": root.find(".//cell").attrib.get("samples"),
                    "signal_strength": root.find(".//cell").attrib.get("averageSignalStrength"),
                    "radio": root.find(".//cell").attrib.get("radio")
                }
                return cell_data
        except ET.ParseError as e:
            return f"XML Parse Error: {str(e)}"
    else:
        return f"Error: Status code {response.status_code}"

# Function to estimate internet speed based on tower data
def estimate_internet_speed(cell_data):
    signal_strength = int(cell_data.get('signal_strength', -80))
    range_value = int(cell_data.get('range', 1000))

    if signal_strength > -70:
        speed = 50
    elif signal_strength > -80:
        speed = 25
    else:
        speed = 6.5

    if range_value > 1000:
        speed *= 0.8
    elif range_value > 500:
        speed *= 0.9

    if cell_data.get('radio') == 'LTE':
        speed *= 1.5
    elif cell_data.get('radio') == 'GSM':
        speed *= 0.8

    return speed

# Function for Groq chat completion (WaveBuddy chat)
def wavebuddy_chat(query):
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# Function to clear WaveBuddy input
def clear_wavebuddy_input():
    return "", ""

# Gradio Interface function for main app (fetching tower data)
def gradio_interface(mcc, mnc, cellid, lac):
    tower_data = fetch_tower_data(mcc, mnc, cellid, lac)

    if isinstance(tower_data, dict):
        output = "\nFetched Tower Data:\n"
        for key, value in tower_data.items():
            output += f"{key}: {value}\n"

        predicted_speed = estimate_internet_speed(tower_data)
        output += f"\nPredicted Internet Speed: {predicted_speed:.2f} Mbps"

        return output
    else:
        return tower_data

# Gradio UI with tabs and styling
def create_gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("""
        # WaveTracker
        A tool for network troubleshooting and assistance.
        """)
        
        with gr.Tabs():
            with gr.TabItem("Network Info"):
                mcc_input = gr.Number(label="Mobile Country Code (MCC)")
                mnc_input = gr.Number(label="Mobile Network Code (MNC)")
                lac_input = gr.Number(label="Location Area Code (LAC)")
                cellid_input = gr.Number(label="Cell ID")
                
                fetch_button = gr.Button("Fetch Data")
                result_output = gr.Textbox(label="Output", lines=10)

                fetch_button.click(gradio_interface, 
                                   inputs=[mcc_input, mnc_input, cellid_input, lac_input],
                                   outputs=result_output)

            with gr.TabItem("WaveBuddy"):
                query_input = gr.Textbox(label="Ask WaveBuddy")
                submit_button = gr.Button("Submit")
                clear_button = gr.Button("Clear")
                response_output = gr.Textbox(label="WaveBuddy Response", lines=5)

                submit_button.click(wavebuddy_chat, inputs=query_input, outputs=response_output)
                clear_button.click(clear_wavebuddy_input, inputs=None, outputs=[query_input, response_output])

        demo.launch()

# Run Gradio interface
create_gradio_ui()
