# Hardware-in-the-Loop Software
Software for hardware-in-the-loop testing of CubeSat satellites
## Real-Time Satellite Visualization and Ground Station Interface
### Overview
This project provides a real-time 3D visualization of satellites using TLE data, incorporating Earth rotation, Sun position, and user location based on IP geolocation. It supports dynamic simulation speed control and outputs satellite and ground station data through a UART interface for hardware-in-the-loop testing.
### Features
- Real-time satellite position and velocity visualization in 3D using React.js and Three.js  
- Accurate orbital propagation via SGP4 and coordinate transformations (ECI and ECEF) on backend (Python FastAPI)  
- IP-based user location displayed as a red sphere on the Earth  
- Earth rotation modeled by Greenwich Mean Sidereal Time (GMST) for proper alignment  
- Interactive controls for simulation speed and camera movement  
- Visualization of velocity, Earth, and Sun vectors with arrows on satellite  
- Sun modeled as a glowing emissive sphere with directional light  
- UART data output from backend for embedded system integration  
### Technologies Used
- **Backend:** Python, FastAPI, SGP4, pymap3d, PySerial  
- **Frontend:** React.js, Three.js, @react-three/fiber, @react-three/drei  
- **Visualization:** Three.js 3D graphics, real-time orbital mechanics  
- **Communication:** UART interface for hardware connection  
### Installation
#### Backend
1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
2. Install dependencies:
```bash
pip install fastapi uvicorn sgp4 pymap3d pyserial
```
3. Run the backend server:
```bash
uvicorn main:app --reload
```
#### Frontend
1. Navigate to the frontend directory and install dependencies:
```bash
npm install
```
2. Run the React development server:
```bash
npm run dev
```
3. Here is an option for deploying the application:
```bash
npm run build
serve -s dist -l tcp://IP_ADDRESS:PORT
```
### Usage
- Access the frontend in your browser at http://localhost:3000
- The satellite visualization will load with real-time data from the backend
- Use controls in the sidebar to adjust simulation speed or reset the simulation clock
- The IP-based location marker shows your current ground position on the Earth
- UART data is sent from backend to the configured serial port for external hardware
### Project Structure
```bash
/backend
├── modules/            # Core logic modules for orbital calculations, coordinate conversions, and simulation
├── uart/               # UART output utilities and communication handlers
├── main.py             # Main Python app with FastAPI backend, routes and API endpoints
├── state.py            # Simulation state management, including clock and satellite state handling
├── system_converter.py # Coordinate system conversion functions (ECI ⇄ ECEF, geodetic, etc.)
├── time_controller.py  # Simulation clock control, time acceleration and synchronization logic
/frontend
├── src/
    ├── assets/         # Static assets such as textures, images, and shaders
    ├── services/       # API clients, data fetching hooks, and utility functions for frontend
    ├── App.jsx         # Main React app with state management and controls
    ├── SidebarData.jsx # Sidebar UI component containing simulation controls and settings
    ├── Viewer3D.jsx    # 3D visualization component for Earth, satellites, sun, and other elements
```
### Known Issues and Limitations
- Complex objects synchronization process due to using ECI over ECEF
- UART interface currently supports output only, no command reception
- Visualization performance depends on browser and hardware capabilities
- No automatic download of TLE inputs
- Only one satellite can be observed at a time
### Future Work
- Implement bidirectional UART command handling
- Add ground pass prediction and notification system
- Introduce multi-satellite and constellation visualization
- Integrate 3D terrain and weather overlays
- Replace polling with WebSocket or MQTT real-time backend communication
### License
This project is licensed under the MIT License.
### Acknowledgments
- Uses SGP4 for orbital propagation
- Utilizes pymap3d for coordinate transforms
- Based on React Three Fiber and Drei for 3D visualization