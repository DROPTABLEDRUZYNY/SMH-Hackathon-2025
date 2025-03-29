"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import dynamic from "next/dynamic";
import L, { LatLngExpression } from "leaflet";
import { get } from "http";


export default function FullScreenMap() {

  const [locations, setLocations] = useState<Location[]>([]);
  const [mapCenter, setMapCenter] = useState<LatLngExpression>([50.0499, 19.9610]);
  const [mounted, setMounted] = useState(false);

  const scale = 3

  type Location = {
    latitude: number;
    longitude: number;
    name: string;
    scale?: number;
  };
  

  useEffect(() => {
    async function loadLocations() {
        try {
          const response = await fetch("https://your-backend.com/api/locations");
          if (!response.ok) {
            throw new Error("Błąd pobierania danych");
          }
          const data = await response.json();
          setLocations(data);
  
          if (data.length > 0) {
            setMapCenter([data[0].latitude, data[0].longitude]);
          }
        } catch (error) {
          console.error("Error fetching data:", error);
        }
    }
    loadLocations();
    setMounted(true);
  }, []);

  function getIcon(scale: number) {
    const size = scale === 3 ? 40 : scale === 2 ? 30 : 20;

    return new L.Icon({
      iconUrl: "/trashBin.webp",
      iconSize: [size, size],
      iconAnchor: [size / 2, size / 2],
      popupAnchor: [0, -size / 2],
      className: "custom-icon"
    });
  }

  if (!mounted) return <p>Loading map...</p>;



  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <MapContainer 
        center={[50.0499, 19.9610]} 
        zoom={13} 
        style={{ width: "100%", height: "100%" }} 
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        />
        <Marker 
            position={[50.0499, 19.9610]} 
            icon={getIcon(scale || 1)} 
            eventHandlers={{
              add: (e) => {
                const marker = e.target;
                marker.setOpacity(0.5);
              },
            }}>
          <Popup>Software Mansion, Cracow</Popup>
        </Marker>
        {locations.map((loc, index) => (
          <Marker 
          key={index} 
          position={[loc.latitude, loc.longitude]} 
          icon={getIcon(loc.scale || 1)}             
          eventHandlers={{
            add: (e) => {
              const marker = e.target;
              marker.setOpacity(0.5);
            },
          }}>
            <Popup>
              <strong>{loc.name}</strong> <br />
              {loc.scale ? `Scale: ${loc.scale}` : "No scale info"}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
