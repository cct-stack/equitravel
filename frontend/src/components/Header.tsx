import { Link, useLocation } from "react-router-dom";

const NAV = [
  { to: "/", label: "Events" },
  { to: "/venues", label: "Tracks & Venues" },
  { to: "/vendors", label: "Travel & Experiences" },
];

export default function Header() {
  const { pathname } = useLocation();

  return (
    <header className="border-b border-zinc-800 bg-racing-slate/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <span className="text-2xl">🏇</span>
          <div>
            <h1 className="font-display text-xl font-bold text-racing-gold tracking-wide">
              EquiTravel
            </h1>
            <p className="text-[10px] text-zinc-500 uppercase tracking-[0.2em]">
              Horse Racing Travel Intelligence
            </p>
          </div>
        </Link>
        <nav className="flex gap-1">
          {NAV.map((n) => (
            <Link
              key={n.to}
              to={n.to}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                pathname === n.to
                  ? "bg-racing-green text-racing-gold"
                  : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60"
              }`}
            >
              {n.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
