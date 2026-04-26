interface TripEstimateData {
  nights: number;
  currency: string;
  hotel_low: number;
  hotel_high: number;
  tickets_low: number;
  tickets_high: number;
  dining_per_day: number;
  experiences_per_day: number;
  transport: number;
  total_low: number;
  total_high: number;
}

function sym(currency: string) {
  return currency === "GBP" ? "£" : currency === "AUD" ? "A$" : currency === "EUR" ? "€" : "$";
}

function fmt(n: number, currency: string) {
  return `${sym(currency)}${n.toLocaleString()}`;
}

function Row({ label, low, high, currency, note }: { label: string; low: number; high: number; currency: string; note?: string }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-zinc-800/50">
      <div>
        <span className="text-sm text-zinc-300">{label}</span>
        {note && <span className="text-xs text-zinc-600 ml-2">{note}</span>}
      </div>
      <span className="text-sm font-medium text-green-400">
        {fmt(low, currency)} – {fmt(high, currency)}
      </span>
    </div>
  );
}

export default function TripEstimateCard({ estimate }: { estimate: TripEstimateData }) {
  const { nights, currency } = estimate;
  return (
    <div>
      <h3 className="text-lg font-display font-semibold text-racing-gold mb-3 flex items-center gap-2">
        💰 Suggested {nights}-Night Trip Budget
      </h3>
      <div className="border border-zinc-800 rounded-xl p-5 bg-racing-slate/30">
        <Row label="🏨 Hotel" low={estimate.hotel_low * nights} high={estimate.hotel_high * nights} currency={currency} note={`${nights} nights`} />
        <Row label="🎟️ Tickets" low={estimate.tickets_low} high={estimate.tickets_high} currency={currency} />
        <Row label="🍽️ Dining" low={estimate.dining_per_day * nights} high={estimate.dining_per_day * nights} currency={currency} note={`${fmt(estimate.dining_per_day, currency)}/day`} />
        <Row label="⛳ Experiences" low={estimate.experiences_per_day * nights} high={estimate.experiences_per_day * nights} currency={currency} note={`${fmt(estimate.experiences_per_day, currency)}/day`} />
        <Row label="✈️ Transport" low={estimate.transport} high={estimate.transport} currency={currency} note="flights/car" />

        <div className="flex items-center justify-between pt-4 mt-2 border-t-2 border-racing-gold/30">
          <span className="text-base font-semibold text-zinc-100">Total Estimated</span>
          <span className="text-xl font-bold text-racing-gold">
            {fmt(estimate.total_low, currency)} – {fmt(estimate.total_high, currency)}
          </span>
        </div>
        <p className="text-[10px] text-zinc-600 mt-2">
          Estimates for a {nights}-night trip for 2 guests. Prices vary by tier, season, and availability.
        </p>
      </div>
    </div>
  );
}
