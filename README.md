# 🌐 VEXA ATLAS — Tactical Cyber & OSINT Global Command

**VEXA ATLAS** is an interactive, military-grade geospatial intelligence dashboard and global atlas designed for cybersecurity analysts, OSINT researchers, and strategic monitoring.

---

## ⚡ Core Features

### 1. Dual-Engine Geospatial Modes
- **2D Tactical Map View (Leaflet.js)**:
  - Deep Dark Matter & Satellite Hybrid Basemaps
  - Real-time coordinate HUD (Latitude, Longitude, WGS84 Mercator projection)
  - Animated cyber warfare trajectories with dynamic pulse packets
  - Aircraft headings with live transponder telemetry
  - Interactive subsea fiber optic cable routes and landing stations
  - Pulsing radar rings on geopolitical hotspots
  - Strategic naval and allied air bases

- **3D Holographic Earth Globe (Three.js WebGL)**:
  - 60 FPS interactive WebGL globe with atmospheric outer glow rim
  - Rotatable, zoomable tactical mesh with procedural landmass point-cloud
  - 3D parabolic curved cyber attack arcs with traveling light packets
  - Orbital satellites with inclination rings
  - 3D laser beacon columns pointing to global conflict flashpoints

### 2. Multi-Domain Intelligence Layers
- 🛡️ **Cyber Warfare Vectors**: APT attacks (Volt Typhoon, Cozy Bear, Lazarus, KillNet), attack types (SCADA infiltration, Zero-Day RCE, L7 DDoS, BGP Hijacks), severity ratings, and target locations.
- ✈️ **Airspace & Aviation ISR**: High-altitude reconnaissance UAVs (RQ-4B Global Hawk FORTE12), electronic warfare planes (RC-135 Rivet Joint), AWACS, and tactical airlifters.
- 🛰️ **Space & Orbital Reconnaissance**: Recon satellites (USA-326), orbital inspector platforms (COSMOS-2558), and space stations (Tiangong).
- 🌐 **Subsea Fiber Infrastructure**: Critical transoceanic cables (Dunant, SEA-ME-WE 5, Pacific Light, FASTER).
- ⚠️ **Geopolitical Flashpoints**: Taiwan Strait, Red Sea Maritime Corridor, Suwałki Gap, Strait of Hormuz, Zaporizhzhia Nuclear Complex.
- ⚓ **Strategic Bases**: Key naval ports, carrier strike hubs, and ISR stations.

### 3. Vexa AI Companion & Intelligence Analyst
- Integrated companion terminal powered by the Vexa persona: *hyper-intelligent, cybersecurity-oriented, precise, concise, and direct*.
- Connects to local Ollama (`deepseek-r1:1.5b` or `llama3`) or autonomous heuristic knowledge engine when offline.
- Synthesized Voice Audio (TTS) with Web Audio tactical procedural audio effects (radar pings, alert alarms, chirp telemetry).
- Quick command chips: Pacific Cyber Threat, Airspace ISR Corridors, Subsea Cable Vulnerability, Orbital Surveillance.

### 4. Interactive Target Dossier Inspector
- Click on any flight, cyber attack, cable, base, or satellite to inspect detailed telemetry, risk metrics, and trigger immediate Vexa AI intelligence briefings.

---

## 🚀 Quick Start

### Option 1: Standalone Python Server (Zero pip dependencies)
```bash
cd /home/holmes/vexa_atlas
./start.sh
```
Then open: **`http://localhost:8080`** in your browser.

### Option 2: Live Development Server (Hot-reloading)
```bash
cd /home/holmes/vexa_atlas
npm run dev
```
Then open: **`http://localhost:5173`** in your browser.

---

## 🛠️ Tech Stack
- **Frontend**: React 18, Vite, Three.js, Leaflet, Tailwind CSS, Lucide Icons
- **Audio Engine**: Procedural Web Audio API sound synthesizer
- **Backend / Proxy**: Python 3 standard library `http.server` with OpenSky & Ollama APIs
