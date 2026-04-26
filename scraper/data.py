"""Centralized venue, vendor, and coordinate data for all regions."""

from __future__ import annotations

# ── Track coordinates ─────────────────────────────────────────────

TRACK_COORDS = {
    "Churchill Downs":          (38.2026, -85.7706),
    "Pimlico Race Course":      (39.3495, -76.6515),
    "Saratoga Race Course":     (43.0788, -73.7802),
    "Del Mar":                  (32.9376, -117.2470),
    "Gulfstream Park":          (25.9714, -80.1396),
    "Ascot Racecourse":         (51.4085, -0.6745),
    "Cheltenham Racecourse":    (51.9065, -2.0670),
    "Epsom Downs":              (51.3158, -0.2613),
    "Goodwood Racecourse":      (50.8961, -0.7544),
    "Meydan Racecourse":        (25.1630, 55.3040),
    "King Abdulaziz Racecourse":(24.7500, 46.7500),
    "Flemington Racecourse":    (-37.7880, 144.9120),
    "Moonee Valley Racecourse": (-37.7663, 144.9268),
    "Royal Randwick":           (-33.9044, 151.2353),
    "Tokyo Racecourse":         (35.6614, 139.4953),
    "Sha Tin Racecourse":       (22.3990, 114.2053),
    "ParisLongchamp":           (48.8570, 2.2340),
    # Auction houses
    "Keeneland":                (38.0415, -84.5974),
    "Fasig-Tipton":             (38.0490, -84.4970),
    "Fasig-Tipton Saratoga":    (43.0790, -73.7810),
    "Tattersalls":              (52.2422, 0.3742),
    "Goffs":                    (53.2690, -6.6780),
    "Magic Millions Sales Complex": (-28.0015, 153.4300),
    "Arqana":                   (49.3550, 0.0740),
}

# ── Region coordinates (center point) ────────────────────────────

REGION_COORDS = {
    "Kentucky":       (38.20, -84.87),
    "Maryland":       (39.35, -76.65),
    "New York":       (43.08, -73.78),
    "California":     (32.94, -117.25),
    "Florida":        (25.97, -80.14),
    "Berkshire":      (51.41, -0.67),
    "Gloucestershire":(51.91, -2.07),
    "Surrey":         (51.32, -0.26),
    "West Sussex":    (50.90, -0.75),
    "Dubai":          (25.16, 55.30),
    "Riyadh":         (24.75, 46.75),
    "Victoria":       (-37.79, 144.91),
    "New South Wales":(-33.90, 151.24),
    "Tokyo":          (35.66, 139.50),
    "Hong Kong":      (22.40, 114.21),
    "Paris":          (48.86, 2.23),
    "Newmarket":      (52.24, 0.37),
    "County Kildare": (53.27, -6.68),
    "Queensland":     (-28.00, 153.43),
    "Deauville":      (49.36, 0.07),
}


# ── Hotels with coordinates ──────────────────────────────────────

HOTELS = [
    # Kentucky
    {"vendor_name": "The Brown Hotel", "vendor_type": "hotel", "price_range": "$350-800/night", "website": "https://www.brownhotel.com", "description": "Historic luxury hotel in downtown Louisville. Home of the Hot Brown. 15 min to Churchill Downs.", "region_name": "Kentucky", "country": "USA", "lat": 38.2478, "lng": -85.7559},
    {"vendor_name": "21c Museum Hotel Louisville", "vendor_type": "hotel", "price_range": "$300-600/night", "website": "https://www.21cmuseumhotels.com/louisville", "description": "Boutique art museum hotel in downtown Louisville.", "region_name": "Kentucky", "country": "USA", "lat": 38.2560, "lng": -85.7595},
    {"vendor_name": "The Grady Hotel", "vendor_type": "hotel", "price_range": "$275-500/night", "website": "https://www.thegradyhotel.com", "description": "Boutique hotel in the heart of Louisville's Whiskey Row.", "region_name": "Kentucky", "country": "USA", "lat": 38.2565, "lng": -85.7575},
    {"vendor_name": "Keeneland Hotel", "vendor_type": "hotel", "price_range": "$400-1200/night", "description": "Luxury resort adjacent to Keeneland racecourse in Lexington.", "region_name": "Kentucky", "country": "USA", "lat": 38.0430, "lng": -84.5980},
    # Maryland
    {"vendor_name": "Sagamore Pendry Baltimore", "vendor_type": "hotel", "price_range": "$350-700/night", "website": "https://www.pendry.com/baltimore", "description": "Waterfront luxury hotel in Fell's Point. 20 min to Pimlico.", "region_name": "Maryland", "country": "USA", "lat": 39.2832, "lng": -76.5923},
    {"vendor_name": "Hotel Ivy Baltimore", "vendor_type": "hotel", "price_range": "$250-500/night", "description": "Boutique hotel in Mt. Vernon, Baltimore.", "region_name": "Maryland", "country": "USA", "lat": 39.2971, "lng": -76.6160},
    # New York / Saratoga
    {"vendor_name": "The Adelphi Hotel", "vendor_type": "hotel", "price_range": "$400-900/night", "website": "https://www.theadelphihotel.com", "description": "Grand Victorian-era hotel in downtown Saratoga Springs.", "region_name": "New York", "country": "USA", "lat": 43.0838, "lng": -73.7855},
    {"vendor_name": "The Inn at Saratoga", "vendor_type": "hotel", "price_range": "$250-600/night", "description": "Boutique inn on Broadway, walking distance to the track.", "region_name": "New York", "country": "USA", "lat": 43.0826, "lng": -73.7867},
    # California / Del Mar
    {"vendor_name": "L'Auberge Del Mar", "vendor_type": "hotel", "price_range": "$500-1500/night", "website": "https://www.laubergedelmar.com", "description": "Luxury oceanfront resort steps from Del Mar racetrack.", "region_name": "California", "country": "USA", "lat": 32.9596, "lng": -117.2653},
    {"vendor_name": "Fairmont Grand Del Mar", "vendor_type": "hotel", "price_range": "$600-2000/night", "website": "https://www.fairmont.com/san-diego", "description": "5-star resort with Tom Fazio golf, spa, and fine dining.", "region_name": "California", "country": "USA", "lat": 32.9386, "lng": -117.2087},
    {"vendor_name": "The Lodge at Torrey Pines", "vendor_type": "hotel", "price_range": "$500-1200/night", "website": "https://www.lodgetorreypines.com", "description": "Craftsman-style AAA 5-Diamond lodge at Torrey Pines.", "region_name": "California", "country": "USA", "lat": 32.8993, "lng": -117.2470},
    # Florida
    {"vendor_name": "The Diplomat Beach Resort", "vendor_type": "hotel", "price_range": "$350-800/night", "website": "https://www.diplomatresort.com", "description": "Beachfront resort near Gulfstream Park in Hollywood, FL.", "region_name": "Florida", "country": "USA", "lat": 26.0146, "lng": -80.1184},
    {"vendor_name": "The Ritz-Carlton Fort Lauderdale", "vendor_type": "hotel", "price_range": "$500-1500/night", "description": "Beachfront luxury. 10 min from Gulfstream Park.", "region_name": "Florida", "country": "USA", "lat": 26.1107, "lng": -80.1039},
    # UK
    {"vendor_name": "Coworth Park", "vendor_type": "hotel", "price_range": "£600-2500/night", "website": "https://www.dorchestercollection.com/coworth-park", "description": "Dorchester Collection estate. Polo, equestrian, spa. 10 min to Ascot.", "region_name": "Berkshire", "country": "UK", "lat": 51.4085, "lng": -0.6495},
    {"vendor_name": "The Langley", "vendor_type": "hotel", "price_range": "£400-1200/night", "website": "https://www.thelangley.com", "description": "Luxury hotel in a Grade II listed mansion near Ascot.", "region_name": "Berkshire", "country": "UK", "lat": 51.5015, "lng": -0.5480},
    {"vendor_name": "Queens Hotel Cheltenham", "vendor_type": "hotel", "price_range": "£200-600/night", "website": "https://www.queenshotelcheltenham.co.uk", "description": "Grand Regency hotel overlooking Imperial Gardens. 5 min to racecourse.", "region_name": "Gloucestershire", "country": "UK", "lat": 51.8975, "lng": -2.0800},
    {"vendor_name": "Ellenborough Park", "vendor_type": "hotel", "price_range": "£300-900/night", "website": "https://www.ellenboroughpark.com", "description": "15th-century manor hotel. Adjacent to Cheltenham racecourse.", "region_name": "Gloucestershire", "country": "UK", "lat": 51.9170, "lng": -2.0540},
    # Dubai
    {"vendor_name": "One&Only Royal Mirage", "vendor_type": "hotel", "price_range": "$500-3000/night", "website": "https://www.oneandonlyresorts.com", "description": "Palatial beachfront resort on The Palm. 15 min to Meydan.", "region_name": "Dubai", "country": "UAE", "lat": 25.0920, "lng": 55.1485},
    {"vendor_name": "Meydan Hotel", "vendor_type": "hotel", "price_range": "$300-1200/night", "website": "https://www.meydanhotels.com", "description": "Luxury hotel integrated with Meydan Racecourse.", "region_name": "Dubai", "country": "UAE", "lat": 25.1640, "lng": 55.3060},
    {"vendor_name": "Burj Al Arab", "vendor_type": "hotel", "price_range": "$1500-25000/night", "website": "https://www.jumeirah.com/burj-al-arab", "description": "Iconic sail-shaped tower. The world's most luxurious hotel.", "region_name": "Dubai", "country": "UAE", "lat": 25.1412, "lng": 55.1854},
    # Australia
    {"vendor_name": "Crown Towers Melbourne", "vendor_type": "hotel", "price_range": "A$500-2000/night", "website": "https://www.crownmelbourne.com.au", "description": "6-star luxury hotel in Crown Melbourne complex. 10 min to Flemington.", "region_name": "Victoria", "country": "Australia", "lat": -37.8238, "lng": 144.9575},
    {"vendor_name": "The Langham Melbourne", "vendor_type": "hotel", "price_range": "A$350-1000/night", "website": "https://www.langhamhotels.com/melbourne", "description": "5-star Southbank hotel overlooking the Yarra. Easy to Flemington.", "region_name": "Victoria", "country": "Australia", "lat": -37.8197, "lng": 144.9620},
    # Japan
    {"vendor_name": "Palace Hotel Tokyo", "vendor_type": "hotel", "price_range": "¥50,000-200,000/night", "website": "https://www.palacehoteltokyo.com", "description": "5-star hotel facing Imperial Palace gardens.", "region_name": "Tokyo", "country": "Japan", "lat": 35.6841, "lng": 139.7628},
    # Hong Kong
    {"vendor_name": "The Peninsula Hong Kong", "vendor_type": "hotel", "price_range": "HK$4,000-50,000/night", "website": "https://www.peninsula.com/hong-kong", "description": "The Grande Dame of the Far East, since 1928.", "region_name": "Hong Kong", "country": "Hong Kong", "lat": 22.2951, "lng": 114.1722},
    # France
    {"vendor_name": "Le Bristol Paris", "vendor_type": "hotel", "price_range": "€800-5000/night", "website": "https://www.oetkercollection.com/hotels/le-bristol-paris", "description": "Palace hotel on rue du Faubourg Saint-Honoré.", "region_name": "Paris", "country": "France", "lat": 48.8704, "lng": 2.3155},
]

# ── Casinos ───────────────────────────────────────────────────────

CASINOS = [
    {"vendor_name": "Churchill Downs Casino", "vendor_type": "casino", "website": "https://www.churchilldowns.com", "description": "On-track gaming and entertainment at Churchill Downs.", "region_name": "Kentucky", "country": "USA", "lat": 38.2046, "lng": -85.7716},
    {"vendor_name": "Horseshoe Casino Baltimore", "vendor_type": "casino", "website": "https://www.caesars.com/horseshoe-baltimore", "description": "Major casino resort 15 min from Pimlico.", "region_name": "Maryland", "country": "USA", "lat": 39.2848, "lng": -76.6205},
    {"vendor_name": "Saratoga Casino Hotel", "vendor_type": "casino", "website": "https://www.saratogacasino.com", "description": "Full casino with 1,700+ machines. Minutes from the track.", "region_name": "New York", "country": "USA", "lat": 43.0530, "lng": -73.7630},
    {"vendor_name": "Crown Casino Melbourne", "vendor_type": "casino", "website": "https://www.crownmelbourne.com.au", "description": "Australia's largest casino complex. Fine dining, gaming, entertainment.", "region_name": "Victoria", "country": "Australia", "lat": -37.8240, "lng": 144.9580},
    {"vendor_name": "The Star Sydney", "vendor_type": "casino", "website": "https://www.star.com.au", "description": "Sydney's premier casino near Royal Randwick.", "region_name": "New South Wales", "country": "Australia", "lat": -33.8679, "lng": 151.1945},
]

# ── High-end restaurants & steakhouses ────────────────────────────

RESTAURANTS = [
    # Kentucky / Louisville / Lexington
    {"vendor_name": "Jeff Ruby's Steaks Louisville", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.jeffruby.com", "description": "Premier steakhouse. Prime beef, seafood, cigar bar. THE Derby Week destination.", "region_name": "Kentucky", "country": "USA", "lat": 38.2536, "lng": -85.7548},
    {"vendor_name": "Jack Fry's", "vendor_type": "restaurant", "price_range": "$$$", "website": "https://www.jackfrys.com", "description": "Upscale Southern bistro in the Highlands. Louisville institution since 1933.", "region_name": "Kentucky", "country": "USA", "lat": 38.2364, "lng": -85.7221},
    {"vendor_name": "Le Relais", "vendor_type": "restaurant", "price_range": "$$$", "website": "https://www.lerelaisrestaurant.com", "description": "French country restaurant at Bowman Field. Horse country favorite.", "region_name": "Kentucky", "country": "USA", "lat": 38.2284, "lng": -85.6663},
    {"vendor_name": "Tony's of Lexington", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.tonysoflex.com", "description": "Premier steakhouse in Lexington. Keeneland crowd favorite.", "region_name": "Kentucky", "country": "USA", "lat": 38.0475, "lng": -84.5018},
    {"vendor_name": "Dudley's on Short", "vendor_type": "restaurant", "price_range": "$$$", "description": "Fine dining in downtown Lexington. Southern-meets-French cuisine.", "region_name": "Kentucky", "country": "USA", "lat": 38.0496, "lng": -84.4978},
    # Maryland / Baltimore
    {"vendor_name": "The Prime Rib", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.theprimerib.com", "description": "Baltimore's legendary steakhouse since 1965. Live piano, tuxedo-clad staff.", "region_name": "Maryland", "country": "USA", "lat": 39.2876, "lng": -76.6166},
    {"vendor_name": "Charleston Restaurant", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.charlestonrestaurant.com", "description": "Refined American cuisine in Harbor East. James Beard nominated.", "region_name": "Maryland", "country": "USA", "lat": 39.2856, "lng": -76.5975},
    # New York / Saratoga
    {"vendor_name": "Hattie's Restaurant", "vendor_type": "restaurant", "price_range": "$$$", "website": "https://www.hattiesrestaurant.com", "description": "Legendary Southern cuisine in downtown Saratoga. A racing tradition since 1938.", "region_name": "New York", "country": "USA", "lat": 43.0826, "lng": -73.7844},
    {"vendor_name": "Prime at Saratoga National", "vendor_type": "restaurant", "price_range": "$$$$", "description": "Upscale steakhouse at Saratoga National Golf Club.", "region_name": "New York", "country": "USA", "lat": 43.0427, "lng": -73.7538},
    {"vendor_name": "Salt & Char", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.saltandchar.com", "description": "Modern steakhouse on Broadway. Dry-aged beef, craft cocktails.", "region_name": "New York", "country": "USA", "lat": 43.0840, "lng": -73.7860},
    # California / Del Mar / San Diego
    {"vendor_name": "Addison at the Grand Del Mar", "vendor_type": "restaurant", "price_range": "$$$$$", "description": "San Diego's only Forbes 5-Star restaurant. Michelin-starred French-American.", "region_name": "California", "country": "USA", "lat": 32.9390, "lng": -117.2090},
    {"vendor_name": "Born & Raised", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.bornandraisedsteak.com", "description": "Lavish steakhouse in Little Italy, San Diego. Best steak in SoCal.", "region_name": "California", "country": "USA", "lat": 32.7229, "lng": -117.1682},
    {"vendor_name": "Pamplemousse Grille", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.pfrsd.com", "description": "Del Mar fine dining institution. Seafood and steaks near the track.", "region_name": "California", "country": "USA", "lat": 32.9580, "lng": -117.2565},
    # Florida
    {"vendor_name": "Council Oak Steaks & Seafood", "vendor_type": "restaurant", "price_range": "$$$$", "website": "https://www.seminolehardrockhollywood.com", "description": "Award-winning steakhouse at Seminole Hard Rock. Near Gulfstream.", "region_name": "Florida", "country": "USA", "lat": 26.0512, "lng": -80.2116},
    {"vendor_name": "Bourbon Steak Fort Lauderdale", "vendor_type": "restaurant", "price_range": "$$$$", "description": "Michael Mina's upscale steakhouse. USDA Prime dry-aged beef.", "region_name": "Florida", "country": "USA", "lat": 26.1195, "lng": -80.1070},
    # UK — Royal Ascot area
    {"vendor_name": "The Fat Duck", "vendor_type": "restaurant", "price_range": "£350/person", "website": "https://www.thefatduck.co.uk", "description": "Heston Blumenthal's 3-Michelin-star in Bray. 15 min from Ascot.", "region_name": "Berkshire", "country": "UK", "lat": 51.5081, "lng": -0.6988},
    {"vendor_name": "The Waterside Inn", "vendor_type": "restaurant", "price_range": "£250/person", "website": "https://www.waterside-inn.co.uk", "description": "3-Michelin-star French by the Roux family. Riverside in Bray.", "region_name": "Berkshire", "country": "UK", "lat": 51.5091, "lng": -0.6950},
    {"vendor_name": "The Hinds Head", "vendor_type": "restaurant", "price_range": "£80/person", "website": "https://www.hindsheadbray.com", "description": "Heston Blumenthal's gastropub. 1-Michelin-star British classics.", "region_name": "Berkshire", "country": "UK", "lat": 51.5076, "lng": -0.6985},
    # UK — Cheltenham
    {"vendor_name": "Le Champignon Sauvage", "vendor_type": "restaurant", "price_range": "£120/person", "description": "2-Michelin-star fine dining. Cheltenham's finest restaurant.", "region_name": "Gloucestershire", "country": "UK", "lat": 51.8995, "lng": -2.0750},
    # Dubai
    {"vendor_name": "Nobu Dubai", "vendor_type": "restaurant", "price_range": "$$$$", "description": "World-famous Japanese fusion in Atlantis, The Palm.", "region_name": "Dubai", "country": "UAE", "lat": 25.1310, "lng": 55.1170},
    {"vendor_name": "CUT by Wolfgang Puck", "vendor_type": "restaurant", "price_range": "$$$$", "description": "Beverly Hills steakhouse concept at Four Seasons DIFC.", "region_name": "Dubai", "country": "UAE", "lat": 25.2135, "lng": 55.2804},
    {"vendor_name": "NUSR-ET Steakhouse", "vendor_type": "restaurant", "price_range": "$$$$$", "website": "https://www.nusr-et.com.tr", "description": "Salt Bae's famous steakhouse. Gold-leaf tomahawk experience.", "region_name": "Dubai", "country": "UAE", "lat": 25.0770, "lng": 55.1390},
    # Australia
    {"vendor_name": "Rockpool Bar & Grill Melbourne", "vendor_type": "restaurant", "price_range": "$$$$", "description": "Neil Perry's legendary steakhouse on Crown promenade.", "region_name": "Victoria", "country": "Australia", "lat": -37.8235, "lng": 144.9590},
    {"vendor_name": "Attica", "vendor_type": "restaurant", "price_range": "$$$$$", "website": "https://www.attica.com.au", "description": "Australia's #1 restaurant. Ben Shewry's tasting menu. World's 50 Best.", "region_name": "Victoria", "country": "Australia", "lat": -37.8775, "lng": 145.0020},
    # Japan
    {"vendor_name": "Aragawa", "vendor_type": "restaurant", "price_range": "¥40,000+/person", "description": "Legendary Kobe beef steakhouse in Shinbashi. One of Tokyo's finest.", "region_name": "Tokyo", "country": "Japan", "lat": 35.6650, "lng": 139.7560},
    {"vendor_name": "Sukiyabashi Jiro", "vendor_type": "restaurant", "price_range": "¥30,000+/person", "description": "World-famous 3-Michelin-star sushi. Reservation essential.", "region_name": "Tokyo", "country": "Japan", "lat": 35.6735, "lng": 139.7638},
    # Hong Kong
    {"vendor_name": "Lung King Heen", "vendor_type": "restaurant", "price_range": "HK$1,500+/person", "description": "World's first Chinese restaurant to earn 3 Michelin stars. At Four Seasons.", "region_name": "Hong Kong", "country": "Hong Kong", "lat": 22.2862, "lng": 114.1589},
    {"vendor_name": "Caprice", "vendor_type": "restaurant", "price_range": "HK$2,000+/person", "description": "3-Michelin-star French at Four Seasons. Harbour views.", "region_name": "Hong Kong", "country": "Hong Kong", "lat": 22.2864, "lng": 114.1590},
    # France
    {"vendor_name": "Le Cinq at Four Seasons George V", "vendor_type": "restaurant", "price_range": "€300+/person", "description": "3-Michelin-star French haute cuisine. Near ParisLongchamp.", "region_name": "Paris", "country": "France", "lat": 48.8686, "lng": 2.3012},
    {"vendor_name": "Le Jules Verne", "vendor_type": "restaurant", "price_range": "€200+/person", "description": "Alain Ducasse restaurant on the Eiffel Tower. Iconic Paris dining.", "region_name": "Paris", "country": "France", "lat": 48.8584, "lng": 2.2945},
]

# ── Trip cost estimates (3/4/5 night stays) ───────────────────────
# Format: {event_keyword: {nights: {category: (low, high, currency)}}}

TRIP_ESTIMATES = {
    "Kentucky Derby": {"nights": 4, "currency": "USD", "hotel_low": 350, "hotel_high": 800, "tickets_low": 250, "tickets_high": 5000, "dining_per_day": 200, "experiences_per_day": 100, "transport": 500},
    "Preakness": {"nights": 3, "currency": "USD", "hotel_low": 300, "hotel_high": 700, "tickets_low": 150, "tickets_high": 1200, "dining_per_day": 175, "experiences_per_day": 75, "transport": 400},
    "Belmont": {"nights": 3, "currency": "USD", "hotel_low": 350, "hotel_high": 900, "tickets_low": 100, "tickets_high": 1500, "dining_per_day": 200, "experiences_per_day": 100, "transport": 400},
    "Breeders' Cup": {"nights": 4, "currency": "USD", "hotel_low": 500, "hotel_high": 1500, "tickets_low": 150, "tickets_high": 3500, "dining_per_day": 250, "experiences_per_day": 150, "transport": 500},
    "Pegasus World Cup": {"nights": 3, "currency": "USD", "hotel_low": 350, "hotel_high": 1500, "tickets_low": 50, "tickets_high": 2000, "dining_per_day": 200, "experiences_per_day": 100, "transport": 400},
    "Travers": {"nights": 4, "currency": "USD", "hotel_low": 400, "hotel_high": 900, "tickets_low": 50, "tickets_high": 500, "dining_per_day": 175, "experiences_per_day": 100, "transport": 400},
    "Royal Ascot": {"nights": 5, "currency": "GBP", "hotel_low": 400, "hotel_high": 2500, "tickets_low": 90, "tickets_high": 5000, "dining_per_day": 200, "experiences_per_day": 150, "transport": 300},
    "Cheltenham": {"nights": 4, "currency": "GBP", "hotel_low": 200, "hotel_high": 900, "tickets_low": 40, "tickets_high": 1500, "dining_per_day": 120, "experiences_per_day": 75, "transport": 250},
    "Epsom Derby": {"nights": 3, "currency": "GBP", "hotel_low": 250, "hotel_high": 800, "tickets_low": 50, "tickets_high": 2000, "dining_per_day": 150, "experiences_per_day": 100, "transport": 200},
    "Goodwood": {"nights": 5, "currency": "GBP", "hotel_low": 250, "hotel_high": 800, "tickets_low": 50, "tickets_high": 1500, "dining_per_day": 150, "experiences_per_day": 100, "transport": 250},
    "Dubai World Cup": {"nights": 5, "currency": "USD", "hotel_low": 500, "hotel_high": 3000, "tickets_low": 100, "tickets_high": 5000, "dining_per_day": 300, "experiences_per_day": 200, "transport": 800},
    "Saudi Cup": {"nights": 4, "currency": "USD", "hotel_low": 400, "hotel_high": 2000, "tickets_low": 0, "tickets_high": 5000, "dining_per_day": 250, "experiences_per_day": 150, "transport": 800},
    "Melbourne Cup": {"nights": 5, "currency": "AUD", "hotel_low": 350, "hotel_high": 2000, "tickets_low": 70, "tickets_high": 5000, "dining_per_day": 200, "experiences_per_day": 150, "transport": 600},
    "Cox Plate": {"nights": 3, "currency": "AUD", "hotel_low": 300, "hotel_high": 1500, "tickets_low": 50, "tickets_high": 1000, "dining_per_day": 175, "experiences_per_day": 100, "transport": 500},
    "Everest": {"nights": 3, "currency": "AUD", "hotel_low": 350, "hotel_high": 1500, "tickets_low": 100, "tickets_high": 2000, "dining_per_day": 200, "experiences_per_day": 150, "transport": 500},
    "Japan Cup": {"nights": 4, "currency": "USD", "hotel_low": 350, "hotel_high": 1500, "tickets_low": 50, "tickets_high": 500, "dining_per_day": 250, "experiences_per_day": 150, "transport": 700},
    "Hong Kong International": {"nights": 4, "currency": "USD", "hotel_low": 400, "hotel_high": 2000, "tickets_low": 50, "tickets_high": 1000, "dining_per_day": 250, "experiences_per_day": 150, "transport": 700},
    "Arc de Triomphe": {"nights": 4, "currency": "EUR", "hotel_low": 400, "hotel_high": 2000, "tickets_low": 50, "tickets_high": 1500, "dining_per_day": 250, "experiences_per_day": 150, "transport": 500},
}