import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { RaceEvent, Vendor } from "../hooks/api";

// Marker icons by type
const ICONS: Record<string, { emoji: string; color: string }> = {
  track: { emoji: "🏇", color: "#c9a84c" },
  hotel: { emoji: "🏨", color: "#3b82f6" },
  casino: { emoji: "🎰", color: "#a855f7" },
  restaurant: { emoji: "🍽️", color: "#ef4444" },
  tour: { emoji: "🥃", color: "#f59e0b" },
  charter: { emoji: "✈️", color: "#06b6d4" },
  golf: { emoji: "⛳", color: "#22c55e" },
  fishing: { emoji: "🎣", color: "#0ea5e9" },
  experience: { emoji: "🌟", color: "#eab308" },
};

function makeIcon(type: string) {
  const cfg = ICONS[type] || ICONS.experience;
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="
      background: ${cfg.color}22;
      border: 2px solid ${cfg.color};
      border-radius: 50%;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    ">${cfg.emoji}</div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -20],
  });
}

interface Props {
  event: RaceEvent;
  hotels: Vendor[];
  casinos: Vendor[];
  restaurants: Vendor[];
  experiences: Vendor[];
}

export default function EventMap({ event, hotels, casinos, restaurants, experiences }: Props) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return;

    // Center on venue or region
    const center: [number, number] = event.venue?.latitude && event.venue?.longitude
      ? [event.venue.latitude, event.venue.longitude]
      : event.region?.latitude && event.region?.longitude
        ? [event.region.latitude, event.region.longitude]
        : [38.2, -85.8]; // default Kentucky

    const map = L.map(mapRef.current, {
      center,
      zoom: 11,
      scrollWheelZoom: true,
    });

    L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
      maxZoom: 19,
    }).addTo(map);

    // Track marker
    if (event.venue?.latitude && event.venue?.longitude) {
      L.marker([event.venue.latitude, event.venue.longitude], { icon: makeIcon("track") })
        .addTo(map)
        .bindPopup(`<b>${event.venue.name}</b><br/>${event.name}`);
    }

    // Vendor markers
    const allVendors = [
      ...hotels.map((v) => ({ ...v, _type: "hotel" })),
      ...casinos.map((v) => ({ ...v, _type: "casino" })),
      ...restaurants.map((v) => ({ ...v, _type: "restaurant" })),
      ...experiences.map((v) => ({ ...v, _type: v.vendor_type })),
    ];

    const bounds = L.latLngBounds([]);
    if (event.venue?.latitude && event.venue?.longitude) {
      bounds.extend([event.venue.latitude, event.venue.longitude]);
    }

    for (const v of allVendors) {
      if (!v.latitude || !v.longitude) continue;
      const icon = makeIcon(v._type);
      const popup = `<b>${v.vendor_name}</b><br/><span style="color:#888">${v._type}</span>${v.price_range ? `<br/><span style="color:#4ade80">${v.price_range}</span>` : ""}${v.website ? `<br/><a href="${v.website}" target="_blank" style="color:#c9a84c">Visit →</a>` : ""}`;
      L.marker([v.latitude, v.longitude], { icon }).addTo(map).bindPopup(popup);
      bounds.extend([v.latitude, v.longitude]);
    }

    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 13 });
    }

    mapInstance.current = map;

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, [event, hotels, casinos, restaurants, experiences]);

  return (
    <div>
      <h3 className="text-lg font-display font-semibold text-racing-gold mb-3 flex items-center gap-2">
        🗺️ Area Map
      </h3>
      <div className="flex flex-wrap gap-3 mb-2 text-xs text-zinc-500">
        {Object.entries(ICONS).map(([type, cfg]) => (
          <span key={type} className="flex items-center gap-1">
            <span style={{ color: cfg.color }}>●</span> {cfg.emoji} {type}
          </span>
        ))}
      </div>
      <div ref={mapRef} className="h-[400px] rounded-xl border border-zinc-800 overflow-hidden" />
    </div>
  );
}
