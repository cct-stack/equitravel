import { useState } from "react";
import { useVenues, Venue } from "../hooks/api";

const VENUE_TYPES = [
  { value: "", label: "All" },
  { value: "track", label: "🏇 Tracks" },
  { value: "auction_house", label: "🔨 Auction Houses" },
  { value: "casino", label: "🎰 Casinos" },
  { value: "hotel", label: "🏨 Hotels" },
];

function VenueCard({ venue }: { venue: Venue }) {
  return (
    <div className="border border-zinc-800 rounded-xl p-5 hover:border-racing-gold/30 transition-all">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-display text-lg font-semibold text-zinc-100">
            {venue.name}
          </h3>
          <p className="text-xs text-zinc-500 mt-0.5 uppercase tracking-wider">
            {venue.venue_type.replace("_", " ")}
            {venue.region && ` · ${venue.region.name}, ${venue.region.country}`}
          </p>
          {venue.description && (
            <p className="text-sm text-zinc-400 mt-2 line-clamp-2">{venue.description}</p>
          )}
        </div>
        {venue.website && (
          <a
            href={venue.website}
            target="_blank"
            rel="noopener noreferrer"
            className="shrink-0 text-xs text-racing-gold hover:underline"
          >
            Visit →
          </a>
        )}
      </div>
    </div>
  );
}

export default function VenuesPage() {
  const [venueType, setVenueType] = useState("");
  const { data: venues, isLoading } = useVenues(venueType || undefined);

  return (
    <div>
      <div className="mb-8">
        <h2 className="font-display text-3xl font-bold text-racing-gold mb-2">
          Tracks & Venues
        </h2>
        <p className="text-zinc-500">
          Racetracks, auction houses, casinos, and hotels worldwide
        </p>
      </div>

      <div className="flex gap-1 bg-zinc-900 rounded-lg p-1 mb-6 w-fit">
        {VENUE_TYPES.map((t) => (
          <button
            key={t.value}
            onClick={() => setVenueType(t.value)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              venueType === t.value
                ? "bg-racing-green text-racing-gold"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="h-28 rounded-xl bg-zinc-900 animate-pulse" />
          ))}
        </div>
      )}
      {venues && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {venues.map((v) => (
            <VenueCard key={v.id} venue={v} />
          ))}
          {venues.length === 0 && (
            <p className="col-span-2 text-center py-12 text-zinc-600">No venues found</p>
          )}
        </div>
      )}
    </div>
  );
}
