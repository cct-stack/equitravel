import { useQuery } from "@tanstack/react-query";

const BASE = "/api";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

// ── Types ────────────────────────────────────────────────────────

export interface Region {
  id: number;
  name: string;
  country: string;
  timezone: string;
  latitude?: number;
  longitude?: number;
}

export interface Venue {
  id: number;
  name: string;
  venue_type: string;
  description?: string;
  address?: string;
  city?: string;
  website?: string;
  price_tier?: string;
  image_url?: string;
  latitude?: number;
  longitude?: number;
  rating?: number;
  region?: Region;
}

export interface RaceEvent {
  id: number;
  name: string;
  event_type: string;
  description?: string;
  start_date: string;
  end_date?: string;
  start_time?: string;
  purse?: string;
  grade?: string;
  surface?: string;
  distance?: string;
  ticket_url?: string;
  image_url?: string;
  source_url?: string;
  venue?: Venue;
  region?: Region;
}

export interface EventListResponse {
  events: RaceEvent[];
  total: number;
  page: number;
  page_size: number;
}

export interface Vendor {
  id: number;
  vendor_name: string;
  vendor_type: string;
  description?: string;
  website?: string;
  price_range?: string;
  featured: boolean;
  image_url?: string;
  latitude?: number;
  longitude?: number;
  venue?: Venue;
}

export interface TripEstimateData {
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

export interface TicketPrice {
  id: number;
  source: string;
  tier: string;
  price_low: number;
  price_high?: number;
  currency: string;
  url?: string;
  in_stock: boolean;
}

export interface HotelRate {
  id: number;
  vendor_name: string;
  check_in: string;
  check_out: string;
  room_type: string;
  rate_per_night: number;
  currency: string;
  source: string;
  url?: string;
  available: boolean;
}

export interface EventDetail {
  event: RaceEvent;
  ticket_prices: TicketPrice[];
  nearby_hotels: Vendor[];
  nearby_casinos: Vendor[];
  nearby_restaurants: Vendor[];
  nearby_experiences: Vendor[];
  hotel_rates: HotelRate[];
  trip_estimate?: TripEstimateData;
}

// ── Hooks ────────────────────────────────────────────────────────

export function useEvents(params?: {
  event_type?: string;
  country?: string;
  from_date?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params?.event_type) searchParams.set("event_type", params.event_type);
  if (params?.country) searchParams.set("country", params.country);
  if (params?.from_date) searchParams.set("from_date", params.from_date);
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["events", params],
    queryFn: () => fetchJson<EventListResponse>(`/events${qs ? `?${qs}` : ""}`),
    staleTime: 5 * 60_000,
  });
}

export function useVenues(venueType?: string) {
  const qs = venueType ? `?venue_type=${venueType}` : "";
  return useQuery({
    queryKey: ["venues", venueType],
    queryFn: () => fetchJson<Venue[]>(`/venues${qs}`),
    staleTime: 5 * 60_000,
  });
}

export function useVendors(vendorType?: string) {
  const qs = vendorType ? `?vendor_type=${vendorType}` : "";
  return useQuery({
    queryKey: ["vendors", vendorType],
    queryFn: () => fetchJson<Vendor[]>(`/vendors${qs}`),
    staleTime: 5 * 60_000,
  });
}

export function useEventDetail(eventId: number | undefined) {
  return useQuery({
    queryKey: ["event-detail", eventId],
    queryFn: () => fetchJson<EventDetail>(`/events/${eventId}`),
    enabled: !!eventId,
    staleTime: 5 * 60_000,
  });
}
