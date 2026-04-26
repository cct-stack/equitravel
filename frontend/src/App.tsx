import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import EventsPage from "./pages/EventsPage";
import EventDetailPage from "./pages/EventDetailPage";
import VenuesPage from "./pages/VenuesPage";
import VendorsPage from "./pages/VendorsPage";

export default function App() {
  return (
    <div className="min-h-screen bg-racing-dark">
      <Header />
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Routes>
          <Route path="/" element={<EventsPage />} />
          <Route path="/events/:id" element={<EventDetailPage />} />
          <Route path="/venues" element={<VenuesPage />} />
          <Route path="/vendors" element={<VendorsPage />} />
        </Routes>
      </main>
    </div>
  );
}
