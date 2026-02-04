import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// Create an explicit default icon using imported asset URLs to avoid broken images
const defaultMarkerIcon = new L.Icon({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function MapView({ hospitals = [], userLocation = null }) {
  const [selectedIndex, setSelectedIndex] = useState(null);

  const center = userLocation
    ? [userLocation.lat, userLocation.lon]
    : hospitals && hospitals.length > 0
    ? [hospitals[0].lat, hospitals[0].lon]
    : [12.9716, 77.5946];

  const polyline =
    selectedIndex !== null && userLocation
      ? [
          [userLocation.lat, userLocation.lon],
          [hospitals[selectedIndex].lat, hospitals[selectedIndex].lon],
        ]
      : null;

  return (
    <div className="rounded-lg overflow-hidden">
      <MapContainer center={center} zoom={13} style={{ height: '300px', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {userLocation && (
          <CircleMarker
            center={[userLocation.lat, userLocation.lon]}
            radius={6}
            pathOptions={{ color: '#1f8ef1', fillColor: '#1f8ef1', fillOpacity: 1 }}
          >
            <Popup>Your location</Popup>
          </CircleMarker>
        )}

        {hospitals.map((h, i) => (
          <Marker key={i} icon={defaultMarkerIcon} position={[h.lat, h.lon]} eventHandlers={{ click: () => setSelectedIndex(i) }}>
            <Popup>
              <div style={{ minWidth: 160 }}>
                <div style={{ fontWeight: 700 }}>{h.name}</div>
                <div style={{ fontSize: 12, color: '#666' }}>{h.address}</div>
                <div style={{ marginTop: 8 }}>
                  <a href={h.maps_url} target="_blank" rel="noreferrer" style={{ color: '#1f8ef1' }}>
                    Open directions
                  </a>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}

        {polyline && <Polyline positions={polyline} pathOptions={{ color: 'red', weight: 3 }} />}
      </MapContainer>
    </div>
  );
}
