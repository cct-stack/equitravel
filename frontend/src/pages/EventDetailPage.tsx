import { useParams, Link } from "react-router-dom";
import { useEventDetail, TicketPrice, Vendor } from "../hooks/api";
import EventMap from "../components/EventMap";
import TripEstimateCard from "../components/TripEstimate";

function formatDate(d: string, end?: string) {
  const start = new Date(d + "T00:00:00");
  const opts: Intl.DateTimeFormatOptions = { weekday: "long", month: "long", day: "numeric", year: "numeric" };
  if (end) {
    const e = new Date(end + "T00:00:00");
    return `${start.toLocaleDateString("en-US", { month: "long", day: "numeric" })} – ${e.toLocaleDateString("en-US", opts)}`;
  }
  return start.toLocaleDateString("en-US", opts);
}

function daysUntil(d: string) {
  const diff = Math.ceil((new Date(d + "T00:00:00").getTime() - Date.now()) / 86400000);
  if (diff <= 0) return "Past";
  if (diff === 1) return "Tomorrow";
  return `${diff} days away`;
}

function formatPrice(low: number, high?: number, currency = "USD") {
  const sym = currency === "GBP" ? "£" : currency === "AUD" ? "A$" : currency === "EUR" ? "€" : "$";
  if (low === 0 && (!high || high === 0)) return "Free";
  if (!high || high === low) return `${sym}${low.toLocaleString()}`;
  return `${sym}${low.toLocaleString()} – ${sym}${high.toLocaleString()}`;
}

function TicketSection({ prices }: { prices: TicketPrice[] }) {
  if (!prices.length) return null;
  return (
    <div>
      <h3 className="text-lg font-display font-semibold text-racing-gold mb-3 flex items-center gap-2">
        🎟️ Ticket Pricing
      </h3>
      <div className="space-y-2">
        {prices.map((t) => (
          <div key={t.id} className="flex items-center justify-between border border-zinc-800 rounded-lg p-3 hover:border-racing-gold/30 transition-colors">
            <div>
              <p className="text-sm font-medium text-zinc-200">{t.tier}</p>
              <p className="text-xs text-zinc-500">{t.source} · {t.in_stock ? "Available" : "Sold Out"}</p>
            </div>
            <div className="text-right flex items-center gap-3">
              <span className="text-lg font-semibold text-green-400">
                {formatPrice(t.price_low, t.price_high ?? undefined, t.currency)}
              </span>
              {t.url && (
                <a href={t.url} target="_blank" rel="noopener noreferrer"
                  className="px-3 py-1.5 rounded bg-racing-green text-racing-gold text-xs font-medium hover:bg-racing-green/80 transition-colors">
                  Buy →
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function VendorSection({ title, icon, vendors }: { title: string; icon: string; vendors: Vendor[] }) {
  if (!vendors.length) return null;
  return (
    <div>
      <h3 className="text-lg font-display font-semibold text-racing-gold mb-3 flex items-center gap-2">
        {icon} {title}
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {vendors.map((v) => (
          <div key={v.id} className="border border-zinc-800 rounded-lg p-4 hover:border-racing-gold/30 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-zinc-200 text-sm truncate">{v.vendor_name}</h4>
                {v.description && <p className="text-xs text-zinc-500 mt-1 line-clamp-2">{v.description}</p>}
                {v.price_range && <p className="text-xs text-green-400 mt-1">{v.price_range}</p>}
              </div>
              {v.website && (
                <a href={v.website} target="_blank" rel="noopener noreferrer"
                  className="shrink-0 ml-3 text-xs text-racing-gold hover:underline">
                  Visit →
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function EventDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading, error } = useEventDetail(id ? parseInt(id) : undefined);

  if (isLoading) return (
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => <div key={i} className="h-20 rounded-xl bg-zinc-900 animate-pulse" />)}
    </div>
  );
  if (error || !data) return <p className="text-red-400">Failed to load event</p>;

  const { event: e } = data;

  return (
    <div className="max-w-5xl">
      <Link to="/" className="text-xs text-zinc-500 hover:text-racing-gold transition-colors mb-4 inline-block">
        ← Back to Calendar
      </Link>

      {/* Hero */}
      <div className="border border-zinc-800 rounded-xl p-6 mb-6 bg-racing-slate/40">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="font-display text-3xl font-bold text-zinc-100">{e.name}</h1>
            <p className="text-zinc-400 mt-1">
              {e.venue?.name && <span className="text-zinc-300">{e.venue.name}</span>}
              {e.region && <span> · {e.region.name}, {e.region.country}</span>}
            </p>
            <div className="flex flex-wrap gap-2 mt-3">
              {e.grade && <span className="px-2 py-0.5 rounded text-xs font-semibold bg-racing-gold/20 text-racing-gold">{e.grade}</span>}
              {e.purse && <span className="px-2 py-0.5 rounded text-xs bg-green-900/30 text-green-400">{e.purse}</span>}
              {e.surface && <span className="px-2 py-0.5 rounded text-xs bg-zinc-800 text-zinc-400">{e.surface}</span>}
              {e.distance && <span className="px-2 py-0.5 rounded text-xs bg-zinc-800 text-zinc-400">{e.distance}</span>}
            </div>
          </div>
          <div className="text-right shrink-0">
            <p className="text-lg font-semibold text-zinc-200">{formatDate(e.start_date, e.end_date ?? undefined)}</p>
            <p className="text-racing-gold font-medium mt-1">{daysUntil(e.start_date)}</p>
          </div>
        </div>
      </div>

      {/* Map */}
      <EventMap
        event={e}
        hotels={data.nearby_hotels}
        casinos={data.nearby_casinos}
        restaurants={data.nearby_restaurants}
        experiences={data.nearby_experiences}
      />

      {/* Trip estimate */}
      {data.trip_estimate && (
        <div className="mt-8">
          <TripEstimateCard estimate={data.trip_estimate} />
        </div>
      )}

      {/* Services grid */}
      <div className="space-y-8 mt-8">
        <TicketSection prices={data.ticket_prices} />
        <VendorSection title="Hotels" icon="🏨" vendors={data.nearby_hotels} />
        <VendorSection title="Casinos" icon="🎰" vendors={data.nearby_casinos} />
        <VendorSection title="Restaurants & Steakhouses" icon="🍽️" vendors={data.nearby_restaurants} />
        <VendorSection title="Experiences" icon="⛳" vendors={data.nearby_experiences} />
      </div>

      {data.ticket_prices.length === 0 && data.nearby_hotels.length === 0 && (
        <div className="text-center py-12 border border-zinc-800 rounded-xl mt-6">
          <p className="text-zinc-500">No pricing or services data available yet for this event.</p>
          <p className="text-xs text-zinc-600 mt-1">Data is scraped periodically — check back soon.</p>
        </div>
      )}
    </div>
  );
}
