import { useState } from "react";
import { useVendors, Vendor } from "../hooks/api";

const VENDOR_TYPES = [
  { value: "", label: "All" },
  { value: "hotel", label: "🏨 Hotels" },
  { value: "casino", label: "🎰 Casinos" },
  { value: "restaurant", label: "🍽️ Restaurants" },
  { value: "charter", label: "✈️ Private Aviation" },
  { value: "golf", label: "⛳ Golf" },
  { value: "tour", label: "🥃 Tours" },
  { value: "fishing", label: "🎣 Fishing" },
];

function VendorCard({ vendor }: { vendor: Vendor }) {
  return (
    <div className={`border rounded-xl p-5 transition-all ${
      vendor.featured
        ? "border-racing-gold/40 bg-racing-gold/5"
        : "border-zinc-800 hover:border-racing-gold/30"
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-display text-lg font-semibold text-zinc-100 truncate">
              {vendor.vendor_name}
            </h3>
            {vendor.featured && (
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-racing-gold/20 text-racing-gold">
                FEATURED
              </span>
            )}
          </div>
          <p className="text-xs text-zinc-500 mt-0.5 uppercase tracking-wider">
            {vendor.vendor_type}
          </p>
          {vendor.description && (
            <p className="text-sm text-zinc-400 mt-2 line-clamp-2">{vendor.description}</p>
          )}
          {vendor.price_range && (
            <p className="text-xs text-green-400 mt-2">{vendor.price_range}</p>
          )}
        </div>
        {vendor.website && (
          <a
            href={vendor.website}
            target="_blank"
            rel="noopener noreferrer"
            className="shrink-0 ml-4 px-3 py-1.5 rounded bg-racing-green text-racing-gold text-xs font-medium hover:bg-racing-green/80 transition-colors"
          >
            Visit →
          </a>
        )}
      </div>
    </div>
  );
}

export default function VendorsPage() {
  const [vendorType, setVendorType] = useState("");
  const { data: vendors, isLoading } = useVendors(vendorType || undefined);

  return (
    <div>
      <div className="mb-8">
        <h2 className="font-display text-3xl font-bold text-racing-gold mb-2">
          Travel & Experiences
        </h2>
        <p className="text-zinc-500">
          Hotels, dining, private aviation, bourbon tours, golf, and more
        </p>
      </div>

      <div className="flex flex-wrap gap-1 bg-zinc-900 rounded-lg p-1 mb-6 w-fit">
        {VENDOR_TYPES.map((t) => (
          <button
            key={t.value}
            onClick={() => setVendorType(t.value)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              vendorType === t.value
                ? "bg-racing-green text-racing-gold"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {isLoading && (
        <div className="space-y-3">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-24 rounded-xl bg-zinc-900 animate-pulse" />
          ))}
        </div>
      )}
      {vendors && (
        <div className="space-y-3">
          {vendors.map((v) => (
            <VendorCard key={v.id} vendor={v} />
          ))}
          {vendors.length === 0 && (
            <p className="text-center py-12 text-zinc-600">No vendors found</p>
          )}
        </div>
      )}
    </div>
  );
}
