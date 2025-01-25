# WaveTracker and WaveBuddy: Comprehensive Documentation

## Project Overview

### **Problem Statement**
In today’s interconnected world, users often face challenges related to:
- Mobile network connectivity.
- Internet speed.
- Understanding cellular network performance.

These challenges result in frustration, productivity losses, and difficulty in troubleshooting network issues. Users need a user-friendly, interactive solution to provide relevant suggestions and insights based on cellular data.

### **Solution**
An integrated platform consisting of two main components:
- **WaveTracker**: A network troubleshooting tool to fetch cellular tower data, predict internet speed, and provide optimization suggestions.
- **WaveBuddy**: An AI-driven chatbot to assist users with queries about network connectivity, troubleshooting, and optimization in a conversational format.

This application leverages APIs and advanced AI models for an efficient and user-friendly experience.

---

## Technologies Used

### **1. OpenCellID API**
Used to fetch detailed information about cellular towers based on:
- **MCC**: Mobile Country Code (identifies the country).
- **MNC**: Mobile Network Code (identifies the network operator).
- **Cell ID**: Identifies the specific tower.
- **LAC**: Location Area Code (identifies the location area within the network).

The API provides details like:
- Latitude, longitude.
- Signal strength and radio type (e.g., LTE, GSM).
- Tower range and samples.

---

### **2. Groq API**
Used for AI-driven suggestions and chatbot responses. Key features:
- **Chat Completions**: Processes cellular data to provide concise optimization suggestions.
- **Large Language Model**: Utilizes `llama-3.3-70b-versatile` for intelligent and context-aware responses.

---

### **3. Gradio**
Used to build a user-friendly web interface:
- **Interactive Inputs**: For cellular data entry.
- **Navigation Tabs**: Separate WaveTracker and WaveBuddy functionalities.
- **Visual Design**: Intuitive and accessible layout.

---

## Application Features

### **WaveTracker**
- **Fetch Cellular Tower Data**:
  - Users enter MCC, MNC, Cell ID, and LAC.
  - The app retrieves detailed tower data using the OpenCellID API.
- **Predict Internet Speed**:
  - Estimates internet speed based on signal strength, tower range, and radio type.
- **Generate Suggestions**:
  - Provides actionable insights for improving connectivity.

### **WaveBuddy**
- **Conversational Support**:
  - Users ask network-related queries in natural language.
- **Interactive Responses**:
  - AI-driven answers generated via the Groq API.
- **Enhanced Usability**:
  - Clear input and submit buttons for better interaction.

---

## Implementation Details

### **1. Input Data Processing**
Users provide:
- **MCC** (e.g., 260 for Poland).
- **MNC** (e.g., 2 for T-Mobile Poland).
- **Cell ID** (e.g., 22613).
- **LAC** (e.g., 45080).

Input validation ensures proper formats.

### **2. Fetching Data from OpenCellID**
- API parameters are sent via HTTP GET requests.
- XML responses are parsed for key details.
- Error handling provides user-friendly messages.

### **3. Internet Speed Estimation**
- Signal strength and tower range are used to calculate approximate speeds.
- Adjustments are made based on the radio type (e.g., LTE is faster than GSM).

### **4. AI-Driven Suggestions**
- Tower data is formatted and sent to the Groq API.
- Suggestions are generated to optimize connectivity.

### **5. WaveBuddy Chat**
- User queries are processed via the Groq API.
- Contextually accurate and conversational responses are provided.

---

## Example Usage

### **WaveTracker**
**Input**:
- MCC: 260
- MNC: 2
- Cell ID: 22613
- LAC: 45080

**Output**:
- Fetched Tower Data:
  - Latitude: 52.2296756
  - Longitude: 21.0122287
  - Signal Strength: -65 dBm
  - Radio Type: LTE
- Predicted Internet Speed: 75 Mbps
- Suggestion: *"The signal strength and radio type indicate good performance. Consider using this tower for optimal connectivity."*

---

### **WaveBuddy**
**Input**:
- *"How can I improve my internet speed?"*

**Output**:
- *"Ensure you are within the tower’s range and prioritize LTE towers for better speeds. Reduce interference by minimizing obstacles."*

---

## Future Enhancements

1. **Localization**:
   - Add multi-language support for global accessibility.

2. **Additional Metrics**:
   - Include latency, jitter, and packet loss.

3. **Real-Time Monitoring**:
   - Integrate live data feeds for dynamic updates.

4. **Mobile App**:
   - Extend functionality to Android and iOS platforms.

---

## Conclusion

**WaveTracker** and **WaveBuddy** provide a comprehensive solution for network troubleshooting and optimization. By leveraging APIs like OpenCellID and Groq, this application delivers accurate insights and user-friendly features, making it an invaluable tool for enhancing connectivity experiences.
