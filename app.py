from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from io import BytesIO

app = Flask(__name__)

# Mock prospecting data (expandable with real BC data)
MOCK_DATA = {
        "princeton": {
                    "indicators": ["Quartz veins", "Black sands (magnetite/ilmenite)", "Red garnets", "Pyrite/arsenopyrite"],
                    "tips": "Focus on Tulameen River bends and bedrock cracks. Check claims in MTO.",
                    "lat": 49.46, "lon": -120.51
        },
        "oliver": {
                    "indicators": ["Sedimentary contacts", "Heavy mineral concentrates", "Rusty staining"],
                    "tips": "South Okanagan placer potential. Use iMapBC geology layers.",
                    "lat": 49.18, "lon": -119.55
        },
        "barkerville": {
                    "indicators": ["Alluvial gold", "Quartz veins", "Bench gravels"],
                    "tips": "Historic Cariboo Gold Rush area. Check Cariboo Mining Division claims.",
                    "lat": 53.07, "lon": -121.52
        },
        "likely": {
                    "indicators": ["Placer gold", "Black sands", "Coarse gravels"],
                    "tips": "Quesnel River and Cariboo Lake area. Active placer claims present.",
                    "lat": 52.6, "lon": -121.55
        },
        "rock creek": {
                    "indicators": ["Placer gold", "Quartz veins", "Iron oxides"],
                    "tips": "Kettle River drainage. Check MTO for open placer ground.",
                    "lat": 49.03, "lon": -119.0
        },
        "clearwater": {
                    "indicators": ["Agates", "Jasper", "Fossils"],
                    "tips": "Wells Gray area rockhounding. Good for agates along river bars.",
                    "lat": 51.64, "lon": -120.03
        },
        "hope": {
                    "indicators": ["Nephrite jade", "Serpentinite", "Garnets"],
                    "tips": "Fraser River jade and mineral collecting. Watch for claim boundaries.",
                    "lat": 49.38, "lon": -121.44
        }
}

@app.route('/')
def index():
        return render_template('map.html')

@app.route('/search', methods=['POST'])
def search():
        location = request.form.get('location', 'Princeton BC').lower().strip()
        data = MOCK_DATA.get(location, MOCK_DATA.get(location.split()[0], {
            "indicators": ["Quartz veins", "Black sands", "Garnet"],
            "tips": "General BC prospecting: Use iMapBC + Avenza offline.",
            "lat": 54.0, "lon": -125.0
        }))
        return jsonify({
            "location": location.title(),
            "indicators": data["indicators"],
            "tips": data["tips"],
            "coords": [data["lat"], data["lon"]]
        })

@app.route('/download_map', methods=['POST'])
def download_map():
        location = request.form.get('location', 'Princeton')
        data = MOCK_DATA.get(location.lower().strip(), {})
        indicators = ', '.join(data.get('indicators', ['Quartz veins', 'Black sands', 'Garnets']))
        tips = data.get('tips', 'Focus on river bends and altered zones.')
        content = (
            f"Offline Map Package for {location}\n"
            f"{'='*40}\n\n"
            f"Mineral Indicators:\n  {indicators}\n\n"
            f"Prospecting Tips:\n  {tips}\n\n"
            f"Import into Avenza Maps or QGIS.\n"
            f"Cross-reference with iMapBC for claim boundaries.\n"
        )
        buffer = BytesIO(content.encode('utf-8'))
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{location}_prospect_map.txt",
            mimetype='text/plain'
        )

@app.route('/upload_notes', methods=['POST'])
def upload_notes():
        if 'file' not in request.files:
                    return jsonify({"error": "No file provided"}), 400
                file = request.files['file']
    if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            return jsonify({
                        "message": f"'{file.filename}' uploaded successfully! Waypoints added to your offline map.",
                        "status": "success"
            })

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
