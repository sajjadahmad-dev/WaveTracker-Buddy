# app.py (same code you shared earlier)
import os
import gradio as gr
import requests
import xml.etree.ElementTree as ET
from groq import Groq

# OpenCellID API Key
api_key = 'your-opencellid-api-key'
base_url = 'https://opencellid.org/cell/get'

# Groq API Key
groq_api_key = 'your-groq-api-key'

# Groq client
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
    signal_strength = int(cell_data['signal_strength'])

    if signal_strength == 0:
        signal_strength = -80

    range_value = int(cell_data['range'])

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
        messages=[
            {
                "role": "user",
                "content": f"Provide a helpful and concise response to this question: {query}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

# Function to clear WaveBuddy input
def clear_wavebuddy_input():
    return "", ""  # Clear input and output

# Gradio Interface function for main app (fetching tower data)
def gradio_interface(mcc, mnc, cellid, lac):
    tower_data = fetch_tower_data(mcc, mnc, cellid, lac)

    if isinstance(tower_data, dict):
        output = "\nFetched Tower Data:\n"
        for key, value in tower_data.items():
            output += f"{key}: {value}\n"

        predicted_speed = estimate_internet_speed(tower_data)
        output += f"\nPredicted Internet Speed for tower {tower_data['cellid']}: {predicted_speed} Mbps"

        return output
    else:
        return tower_data

# Gradio UI with tabs and styling
def create_gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("""
        # WaveTracker - Network Troubleshooting
        Welcome to **WaveTracker**. Ask questions related to your network and receive helpful suggestions.
        """)
        
        with gr.Tabs():
            with gr.TabItem("Network Info"):
                with gr.Row():
                    mcc_input = gr.Number(label="Enter Mobile Country Code (MCC)", elem_id="mcc_input")
                    mnc_input = gr.Number(label="Enter Mobile Network Code (MNC)", elem_id="mnc_input")
                    lac_input = gr.Number(label="Enter Location Area Code (LAC)", elem_id="lac_input")
                    cellid_input = gr.Number(label="Enter Cell ID", elem_id="cellid_input")

                with gr.Row():
                    fetch_button = gr.Button("Fetch Tower Data and Predict Speed", elem_id="fetch_button", elem_classes="primary-btn")
                    result_output = gr.Textbox(label="Output", interactive=False, lines=10, elem_id="result_output", elem_classes="output-box")
                
                fetch_button.click(gradio_interface,
                                   inputs=[mcc_input, mnc_input, cellid_input, lac_input],
                                   outputs=result_output)

            with gr.TabItem("WaveBuddy"):
                gr.Markdown("### Ask your WaveBuddy a question")
                user_query = gr.Textbox(label="Your Query", placeholder="Enter your query here", elem_id="user_query", elem_classes="input-box")
                
                with gr.Row():
                    submit_button = gr.Button("Submit", elem_id="submit_button", elem_classes="submit-btn")
                    clear_button = gr.Button("Clear", elem_id="clear_button", elem_classes="clear-btn")
                
                wavebuddy_response = gr.Textbox(label="WaveBuddy Response", interactive=False, elem_id="wavebuddy_response", elem_classes="output-box")
                
                submit_button.click(wavebuddy_chat, inputs=user_query, outputs=wavebuddy_response)
                clear_button.click(clear_wavebuddy_input, inputs=None, outputs=[user_query, wavebuddy_response])

        demo.launch(share=True)

# Run Gradio interface
create_gradio_ui()
