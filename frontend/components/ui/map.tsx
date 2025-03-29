"use client"; // Jeśli używasz Next.js (App Router)

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import dynamic from "next/dynamic";


export default function FullScreenMap() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <p>Ładowanie mapy...</p>;

  return (
    <div style={{ width: "100vw", height: "100vh" }}> {/* Pełny ekran */}
      <MapContainer 
        center={[50.0499, 19.9610]} 
        zoom={13} 
        style={{ width: "100%", height: "100%" }} 
      >
        {/* Dark Mode Tile Layer */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        />

        {/* Przykładowy marker */}
        {/* 1-3 scale =*/}
        <Marker position={[50.0499, 19.9610]}>
          <Popup>Software Mansion, Cracow</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
