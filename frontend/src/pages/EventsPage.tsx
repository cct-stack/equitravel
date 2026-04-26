import { useState } from "react";
import { Link } from "react-router-dom";
import { useEvents, RaceEvent } from "../hooks/api";

const EVENT_TYPES = [
  { value: "", label: "All Events" },
  { value: "race", label: "🏇 Races" },
  { value: "auction", label: "🔨 Auctions" },
  { value: "festival", label: "🎪 Festivals" },
];

const COUNTRIES = [
  { value: "", label: "All Countries" },
  { value: "USA", label: "🇺🇸 USA" },
  { value: "UK", label: "🇬🇧 United Kingdom" },
  { value: "UAE", label: "🇦🇪 UAE" },
  { value: "Australia", label: "🇦🇺 Australia" },
  { value: "Japan", label: "🇯🇵 Japan" },
  { value: "France", label: "🇫🇷 France" },
  { value: "Hong Kong", label: "🇭🇰 Hong Kong" },
  { value: "Ireland", label: "🇮🇪 Ireland" },
  { value: "Saudi Arabia", label: "🇸🇦 Saudi Arabia" },
];

function formatDate(d: string, end?: string) {
  const start = new Date(d + "T00:00:00");
  const opts: Intl.DateTimeFormatOptions = { month: "short", day: "numeric", year: "numeric" };
  if (end) {
    const e = new Date(end + "T00:00:00");
    return `${start.toLocaleDateString("en-US", { month: "short", day: "numeric" })} – ${e.toLocaleDateString("en-US", opts)}`;
  }
  return start.toLocaleDateString("en-US", opts);
}

function daysUntil(d: string) {
  const diff = Math.ceil((new Date(d + "T00:00:00").getTime() - Date.now()) / 86400000);
  if (diff < 0) return "Past";
  if (diff === 0) return "Today";
  if (diff === 1) return "Tomorrow";
  return `${diff} days`;
}

function gradeColor(grade?: string) {
  if (!grade) return "bg-zinc-700 text-zinc-300";
  if (grade === "G1") return "bg-racing-gold/20 text-racing-gold";
  if (grade === "G2") return "bg-blue-900/40 text-blue-300";
  return "bg-zinc-800 text-zinc-400";
}

function typeIcon(type: string) {
  if (type === "race") return "🏇";
  if (type === "auction") return "🔨";
  return "📅";
}

function EventCard({ event }: { event: RaceEvent }) {
  const days = daysUntil(event.start_date);
  const isPast = days === "Past";

  return (
    <Link to={`/events/${event.id}`} className={`block border border-zinc-800 rounded-xl p-5 hover:border-racing-gold/30 transition-all cursor-pointer ${isPast ? "opacity-50" : ""}`}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg">{typeIcon(event.event_type)}</span>
            <h3 className="font-display text-lg font-semibold text-zinc-100 truncate">
              {event.name}
            </h3>
          </div>
          <div className="flex flex-wrap gap-2 mt-2">
            {event.grade && (
              <span className={`px-2 py-0.5 rounded text-xs font-semibold ${gradeColor(event.grade)}`}>
                {event.grade}
              </span>
            )}
            {event.purse && (
              <span className="px-2 py-0.5 rounded text-xs bg-green-900/30 text-green-400">
                {event.purse}
              </span>
            )}
            {event.surface && (
              <span className="px-2 py-0.5 rounded text-xs bg-zinc-800 text-zinc-400">
                {event.surface}
              </span>
            )}
            {event.distance && (
              <span className="px-2 py-0.5 rounded text-xs bg-zinc-800 text-zinc-400">
                {event.distance}
              </span>
            )}
          </div>
          <div className="mt-3 text-sm text-zinc-500">
            {event.venue?.name && <span className="text-zinc-400">{event.venue.name}</span>}
            {event.region && <span> · {event.region.name}, {event.region.country}</span>}
          </div>
        </div>
        <div className="text-right shrink-0">
          <p className="text-sm text-zinc-400">{formatDate(event.start_date, event.end_date)}</p>
          <p className={`text-xs font-medium mt-1 ${isPast ? "text-zinc-600" : "text-racing-gold"}`}>
            {days}
          </p>
          {event.ticket_url && (
            <a
              href={event.ticket_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2 px-3 py-1 rounded bg-racing-green text-racing-gold text-xs font-medium hover:bg-racing-green/80 transition-colors"
            >
              Tickets →
            </a>
          )}
        </div>
      </div>
    </Link>
  );
}

export default function EventsPage() {
  const [eventType, setEventType] = useState("");
  const [country, setCountry] = useState("");
  const { data, isLoading, error } = useEvents({
    event_type: eventType || undefined,
    country: country || undefined,
    from_date: "2026-01-01",
  });

  return (
    <div>
      <div className="mb-8">
        <h2 className="font-display text-3xl font-bold text-racing-gold mb-2">
          Racing Calendar
        </h2>
        <p className="text-zinc-500">
          Major races, auctions, and events worldwide — {data?.total ?? "…"} events
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <div className="flex gap-1 bg-zinc-900 rounded-lg p-1">
          {EVENT_TYPES.map((t) => (
            <button
              key={t.value}
              onClick={() => setEventType(t.value)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                eventType === t.value
                  ? "bg-racing-green text-racing-gold"
                  : "text-zinc-400 hover:text-zinc-200"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-1.5 text-xs text-zinc-300"
        >
          {COUNTRIES.map((c) => (
            <option key={c.value} value={c.value}>{c.label}</option>
          ))}
        </select>
      </div>

      {isLoading && (
        <div className="space-y-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-24 rounded-xl bg-zinc-900 animate-pulse" />
          ))}
        </div>
      )}
      {error && <p className="text-red-400">Failed to load events</p>}
      {data && (
        <div className="space-y-3">
          {data.events.map((e) => (
            <EventCard key={e.id} event={e} />
          ))}
          {data.events.length === 0 && (
            <p className="text-center py-12 text-zinc-600">No events found</p>
          )}
        </div>
      )}
    </div>
  );
}
