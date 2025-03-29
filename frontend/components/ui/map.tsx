"use client";

import { useEffect, useState, useRef, SetStateAction } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L, { LatLngExpression } from "leaflet";

interface ChildProps {
    openPostPage: (id: number) => void;
    addingPoints: boolean;
}

type Location = {
    latitude: number;
    longitude: number;
    name: string;
    scale?: number;
    id: number;
};

type LocationToDb = {
    latitude: number;
    longitude: number;
    name: string;
    scale?: number;
}

export default function FullScreenMap({ openPostPage, addingPoints }: ChildProps) {
    const [locations, setLocations] = useState<Location[]>([]);
    const [mapCenter, setMapCenter] = useState<LatLngExpression>([50.0499, 19.9610]);
    const [mounted, setMounted] = useState(false);
    const [newMarker, setNewMarker] = useState<LocationToDb | null>(null);
    const [newMarkerName, setNewMarkerName] = useState("");
    const newMarkerRef = useRef<L.Marker | null>(null);

    async function loadLocations() {
        try {
            const response = await fetch("http://localhost:8000/api/trash_places/");
            if (!response.ok) throw new Error("Błąd pobierania danych");

            const data = await response.json();
            setLocations(data);

            if (data.length > 0) setMapCenter([data[0].latitude, data[0].longitude]);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    useEffect(() => {
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
        });
    }

    function LocationMarker() {
        useMapEvents({
            click(e) {
                if (addingPoints) {
                    const markerData = {
                        latitude: e.latlng.lat,
                        longitude: e.latlng.lng,
                        name: "",
                    };
                    setNewMarker(markerData);
                    setNewMarkerName("");

                    setTimeout(() => {
                        if (newMarkerRef.current) {
                            newMarkerRef.current.openPopup();
                        }
                    }, 0);
                }
            },
        });
        return null;
    }

    const handleConfirm = async() => {
        if (newMarker && newMarkerName.trim()) {
            const newLocation = { ...newMarker, name: newMarkerName };
            setNewMarker(null);

            await fetch("http://localhost:8000/api/trash_places/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newLocation),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Błąd podczas dodawania lokalizacji");
                }
                return response.json();
            })
            .then(data => {
                console.log("Dodano nową lokalizację:", data);
            })
            .catch(error => {
                console.error("Błąd:", error);
            });

            loadLocations()
    
        }
    }

    if (!mounted) return <p>Loading map...</p>;

    return (
        <div style={{ width: "100vw", height: "100vh" }}>
            <MapContainer center={mapCenter} zoom={13} style={{ width: "100%", height: "100%" }}>
                <TileLayer
                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                    attribution='&copy; <a href="https://carto.com/">CARTO</a>'
                />
                <LocationMarker />
                {locations.map((loc, index) => (
                    <Marker key={index} position={[loc.latitude, loc.longitude]} icon={getIcon(loc.scale || 1)}>
                        <Popup>
                            <div className="bg-white text-black text-center">
                                <strong className="block text-lg mb-2">{loc.name}</strong>
                                <button
                                    className="px-6 py-2 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300 transition duration-300"
                                    onClick={() => {
                                        openPostPage(loc.id)}}
                                >
                                    Wykonane!
                                </button>
                            </div>
                        </Popup>
                    </Marker>
                ))}
                {newMarker && (
                    <Marker
                        position={[newMarker.latitude, newMarker.longitude]}
                        icon={getIcon(1)}
                        ref={(marker) => {
                            if (marker) {
                                newMarkerRef.current = marker;
                                setTimeout(() => marker.openPopup(), 0);
                            }
                        }}
                    >
                        <Popup>
                            <div className="text-black bg-white text-center">
                                <input
                                    type="text"
                                    className="border p-2 rounded w-full mb-2"
                                    placeholder="Wpisz nazwę"
                                    value={newMarkerName}
                                    onChange={(e) => setNewMarkerName(e.target.value)}
                                />
                                <button
                                    className="px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 transition duration-300"
                                    onClick={handleConfirm}
                                >
                                    Dodaj miejsce
                                </button>
                            </div>
                        </Popup>
                    </Marker>
                )}
            </MapContainer>
        </div>
    );
}
