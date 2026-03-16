"""
Embedded market data for Lander WY, Alpine WY, Nederland CO, and Gilpin County CO.
Sources: AirROI (Jun 2024–Aug 2025), AirDNA, Zillow, Redfin, RocketHomes,
         Avalara MyLodgeTax, SmartAsset, local government sites, WY/CO Dept of Revenue,
         Colorado Geological Survey, FEMA, county building departments.
Last updated: March 2026
"""

# ── Zip codes ──────────────────────────────────────────────────────────────────
ZIP_CODES = {
    "Lander, WY":       "82520",
    "Alpine, WY":       "83128",
    "Nederland, CO":    "80466",
    "Gilpin County, CO": "80422",  # unincorporated; also 80474 (Rollinsville), 80427 (Black Hawk)
}

# ── Current real estate market ─────────────────────────────────────────────────
MARKET_STATS = {
    "Lander, WY": {
        "median_price":       390_000,     # avg $408k Redfin; $370k Rocket Homes (early 2025)
        "price_per_sqft":     232,         # RocketHomes Sep 2025
        "median_sqft":        1_680,
        "dom":                86,          # Median DOM Sep 2025 (RocketHomes)
        "inventory":          "Moderate",  # 41–82 homes listed (Dec 2024–Apr 2025)
        "yoy_appreciation":   0.09,        # +13.8% Redfin YoY; using conservative 9%
        "property_tax_rate":  0.0071,      # 0.71% effective rate (Fremont County / Ownwell)
        "hoa_common":         False,
        "price_range_low":    180_000,
        "price_range_high":   650_000,
        "sqft_range_low":     900,
        "sqft_range_high":    3_200,
        "description": (
            "Small city (~7,450 pop) in Fremont County, central WY. "
            "Gateway to Wind River Range, Sinks Canyon State Park, and world-class "
            "fly fishing. Home of NOLS global HQ. Moderate inventory, ~86-day median "
            "DOM — a slower, negotiable market with meaningful remodel upside potential. "
            "Fremont County tourism spending: $170M in 2023."
        ),
    },
    "Alpine, WY": {
        "median_price":       900_000,     # Star Valley avg $1.04M; median ~$800k–$900k (KW report)
        "price_per_sqft":     450,         # $418–$479/sqft (Star Valley KW Year-End Report 2024)
        "median_sqft":        2_000,
        "dom":                79,          # ~79 days (Oct 2024, Star Valley market report)
        "inventory":          "Tight",     # Inventory up 36% but still limited at ~263 active
        "yoy_appreciation":   0.05,        # Mild appreciation; market cooling from 2022 peak
        "property_tax_rate":  0.0060,      # ~0.60% effective (Lincoln County / Ownwell)
        "hoa_common":         True,        # Many subdivisions: Alpine Meadows, AVR, others
        "price_range_low":    400_000,
        "price_range_high":   1_500_000,
        "sqft_range_low":     1_000,
        "sqft_range_high":    4_500,
        "description": (
            "Small community (~1,360 pop, growing 1.7%/yr) in Lincoln County. "
            "Confluence of Snake and Greys rivers; 36 miles south of Jackson Hole. "
            "World-class snowmobile hub (SnoWest Top 4 in the West, 200+ groomed miles, "
            "500\" avg annual snowfall). Palisades Reservoir water sports. "
            "Primary feeder market: Salt Lake City (3.5hr). "
            "Many subdivisions have HOAs — check CC&Rs before buying."
        ),
    },
    "Nederland, CO": {
        "median_price":       950_000,     # $899k May 2025; $995k Jun 2025 (Redfin); ~$950k avg
        "price_per_sqft":     400,         # $393 May 2025, $429 Sep 2024 (RocketHomes/Redfin)
        "median_sqft":        2_375,
        "dom":                50,          # 30 days Sep 2024; 71 days current (Redfin) — avg
        "inventory":          "Buyers Market",  # Redfin classification; thin but somewhat negotiable
        "yoy_appreciation":   0.14,        # +9–18.8% depending on period (Redfin)
        "property_tax_rate":  0.0053,      # ~0.53% effective (Boulder County / Ownwell)
        "hoa_common":         False,
        "price_range_low":    525_000,
        "price_range_high":   2_000_000,
        "sqft_range_low":     800,
        "sqft_range_high":    4_000,
        "description": (
            "Mountain town (~1,495 pop) in Boulder County at 8,228 ft. "
            "30 min to Boulder, 10 min to Eldora Mountain Resort (Town now purchasing Eldora "
            "for $120M — major long-term demand catalyst). Gateway to Indian Peaks Wilderness. "
            "Median sold price ~$900k–$995k (2025). Dual-season: ski winter + wilderness summer. "
            "⚠️ Wildfire insurance is a critical cost/availability risk — verify before buying."
        ),
    },
    "Gilpin County, CO": {
        "median_price":       574_000,     # DataUSA 2024: $573,900 (+12% YoY from $512,600 in 2023)
        "price_per_sqft":     300,         # Estimate; MLS data inaccessible for small county
        "median_sqft":        1_913,
        "dom":                65,          # Thin/slow market; expect 30–120+ day variability
        "inventory":          "Very Thin", # ~3,120 total households in county; single-digit active listings typical
        "yoy_appreciation":   0.12,        # +12% YoY (DataUSA 2024)
        "property_tax_rate":  0.0043,      # ~0.43% effective (median tax $2,732 / median value $573,900)
        "hoa_common":         False,
        "price_range_low":    280_000,
        "price_range_high":   900_000,
        "sqft_range_low":     700,
        "sqft_range_high":    3_500,
        "description": (
            "Colorado's smallest county (~6,400 pop) adjacent to Boulder County. "
            "Includes Black Hawk / Central City (legal casino gambling — year-round demand), "
            "Rollinsville (zip 80474, near Moffat Tunnel/Indian Peaks trailhead), Pinecliffe, "
            "and unincorporated mountain land. 10–20 min from Nederland, 45–55 min from Denver. "
            "⭐ Unincorporated Gilpin (Rollinsville/Pinecliffe) has ONLY 2.9% state sales tax "
            "— lowest of any market researched (vs 9.44% in Nederland). "
            "No owner-occupancy STR requirement. Permitting ~4/10 vs Boulder County's 7/10. "
            "⚠️ Mine subsidence + Zone 1 radon are the unique hazards requiring property-level due diligence."
        ),
    },
}

# ── Historical median price (approximate, annualized) ─────────────────────────
PRICE_HISTORY = {
    "Lander, WY": {
        2019: 195_000, 2020: 215_000, 2021: 265_000,
        2022: 310_000, 2023: 340_000, 2024: 370_000, 2025: 408_000,
    },
    "Alpine, WY": {
        2019: 380_000, 2020: 430_000, 2021: 600_000,
        2022: 850_000, 2023: 900_000, 2024: 950_000, 2025: 900_000,  # mild correction
    },
    "Nederland, CO": {
        2019: 510_000, 2020: 560_000, 2021: 680_000,
        2022: 915_000, 2023: 800_000, 2024: 887_000, 2025: 950_000,
    },
    "Gilpin County, CO": {
        # DataUSA 2024: $573,900 (+12% from $512,600 in 2023)
        2019: 310_000, 2020: 345_000, 2021: 450_000,
        2022: 520_000, 2023: 513_000, 2024: 574_000, 2025: 574_000,
    },
}

# ── STR (Short-Term Rental) data ───────────────────────────────────────────────
# Sources: AirROI Jun 2024–Aug 2025; AirDNA MarketMinder; Airbtics 2023–2024
STR_DATA = {
    "Lander, WY": {
        "avg_nightly_rate":      191,        # AirROI ADR (vs $154 median, $191 avg)
        "avg_occupancy":         0.474,      # AirROI overall occupancy
        "peak_occupancy":        0.742,      # AirROI July peak
        "off_peak_occupancy":    0.344,      # AirROI Jan–Apr low season
        "active_listings":       64,         # AirROI count
        "avg_annual_revenue":    26_636,     # AirROI median annual revenue
        "top10_annual_revenue":  83_749,     # AirROI top 10%
        "best_property_type":    "House / Cabin (6–8 guest capacity)",
        "peak_seasons":          ["Jun", "Jul", "Aug", "Sep"],
        "secondary_seasons":     ["May", "Oct"],
        "slow_seasons":          ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
        "tourism_drivers": [
            "Wind River Range — 40+ peaks over 13,000 ft, 7 major glaciers; world-class backpacking/climbing",
            "NOLS global HQ in Lander — year-round international student clientele",
            "Sinks Canyon State Park — sport climbing on limestone/dolomite (hundreds of routes)",
            "National Geographic named Lander one of America's 100 best adventure towns",
            "Popo Agie Wilderness and world-class fly fishing",
            "Wind River Indian Reservation cultural tourism and fishing/hunting access",
            "Lander 1838 Mountain Man Rendezvous (July) — major summer event",
            "Ice climbing festival (January) — niche winter spike",
            "Guest ranches throughout the region",
        ],
        "monthly_revenue": {
            "Jan": 1_451, "Feb": 1_900, "Mar": 1_753, "Apr": 1_500,
            "May": 2_300, "Jun": 3_600, "Jul": 4_612, "Aug": 3_800,
            "Sep": 3_100, "Oct": 2_400, "Nov": 1_600, "Dec": 1_720,
        },
        "seasonality": "Strong summer peak (Jul highest). Winter is low season except Jan ice-climbing spike.",
        "yoy_trend": -0.074,     # -7.4% YoY (AirROI)
        "avg_booking_lead_days": 52,
        "pct_entire_home": 0.906,
        "dominant_unit_size": "2BR (34.4% of listings)",
        "avg_guest_capacity": 4.7,
    },
    "Alpine, WY": {
        "avg_nightly_rate":      370,        # AirROI ADR
        "avg_occupancy":         0.429,      # AirROI overall occupancy
        "peak_occupancy":        0.707,      # AirROI July peak occupancy
        "off_peak_occupancy":    0.269,      # AirROI Mar/Apr/Nov low
        "active_listings":       75,         # AirDNA; AirROI has 48 (methodology difference)
        "avg_annual_revenue":    41_057,     # AirROI median annual revenue
        "top10_annual_revenue":  103_500,    # AirROI top 10% estimate
        "best_property_type":    "Large House 3–5BR (8–10 guest capacity), river/reservoir access",
        "peak_seasons":          ["Jun", "Jul", "Aug", "Sep"],
        "secondary_seasons":     ["Dec", "Jan", "Feb"],
        "slow_seasons":          ["Mar", "Apr", "Nov"],
        "tourism_drivers": [
            "Jackson Hole / Grand Teton NP — 36 miles north; major demand driver",
            "Yellowstone NP — ~60 miles northeast",
            "Palisades Reservoir — 25 sq mi reservoir; boating, jet skiing, water skiing, fishing",
            "Snowmobiling — SnoWest Top 4 in the West; 200+ groomed miles; 500\" avg annual snowfall",
            "Greys River trail system — Top 5 snowmobile trail nationally (SnoWest)",
            "Snake River Canyon whitewater rafting (Class III–IV)",
            "Bridger-Teton National Forest (3.4M acres) hunting, hiking, dispersed camping",
            "Alpine elk feed ground — ~1,000 elk Dec–Apr (Wyoming Game & Fish)",
            "Salt Lake City feeder market (3.5hr) — affordable alternative to Jackson Hole",
            "Alpine Airpark — fly-in luxury destination",
        ],
        "monthly_revenue": {
            "Jan": 3_100, "Feb": 3_500, "Mar": 2_588, "Apr": 2_200,
            "May": 3_800, "Jun": 6_800, "Jul": 8_868, "Aug": 7_600,
            "Sep": 5_400, "Oct": 4_042, "Nov": 2_588, "Dec": 4_100,
        },
        "seasonality": "Strong summer peak (July highest at $8,868 potential). Decent winter snowmobile season. Spring/fall are shoulder.",
        "yoy_trend": -0.078,     # -7.8% YoY (AirROI)
        "avg_booking_lead_days": 69,
        "pct_entire_home": 0.979,
        "dominant_unit_size": "3BR (37.5%) and 4BR (20.8%)",
        "avg_guest_capacity": 6.6,
        "pct_30day_minimum": 0.354,   # 35.4% require 30+ night minimum — watch this
    },
    "Nederland, CO": {
        "avg_nightly_rate":      298,        # AirROI ADR
        "avg_occupancy":         0.464,      # AirROI; AirDNA ~55%; use conservative AirROI
        "peak_occupancy":        0.695,      # AirROI Jun–Aug peak
        "off_peak_occupancy":    0.319,      # AirROI Apr/Jan (slowest)
        "active_listings":       114,        # AirDNA; AirROI tracks 82
        "avg_annual_revenue":    44_338,     # AirROI median annual revenue
        "top10_annual_revenue":  189_610,    # AirROI top 10% (highest of 3 markets)
        "best_property_type":    "Luxury cabin/home with hot tub + mountain views",
        "peak_seasons":          ["Jun", "Jul", "Aug"],
        "secondary_seasons":     ["Dec", "Jan", "Feb", "Mar", "Sep", "Oct"],
        "slow_seasons":          ["Apr", "Nov"],
        "tourism_drivers": [
            "Eldora Mountain Resort (10 min) — town purchasing for $120M; 680 acres ski terrain",
            "Indian Peaks Wilderness — world-class hiking, scrambling, camping",
            "Denver feeder market (45 min) — weekend getaways from 715k+ pop",
            "Peak to Peak Scenic Byway — ~8M visitors/year; famous fall foliage",
            "Rocky Mountain National Park (1hr north via Peak to Peak)",
            "Frozen Dead Guy Days festival (March) — major cultural event driving STR demand",
            "James Peak Wilderness — directly accessible",
            "Barker Reservoir fishing and wildlife",
            "Black Hawk Casinos — 9 miles south (CO-119)",
            "Nederland Music Festivals (summer)",
        ],
        "monthly_revenue": {
            "Jan": 3_566, "Feb": 3_494, "Mar": 5_200, "Apr": 2_800,
            "May": 3_900, "Jun": 6_317, "Jul": 7_408, "Aug": 6_800,
            "Sep": 5_100, "Oct": 4_500, "Nov": 2_600, "Dec": 5_000,
        },
        "seasonality": "True dual-season: strong summer + Eldora ski winter. April is mud season (worst). March boosted by Frozen Dead Guy Days.",
        "yoy_trend": +0.405,     # +40.5% YoY (AirROI — strongest of three markets)
        "avg_booking_lead_days": 50,
        "pct_entire_home": 0.927,
        "dominant_unit_size": "3BR (29.3%)",
        "avg_guest_capacity": 4.9,
        "pct_30day_minimum": 0.50,   # 50% have 30+ day minimums — many are MTR not STR
    },
    "Gilpin County, CO": {
        "avg_nightly_rate":      210,        # Between Lander and Nederland; gambling-adjacent market
        "avg_occupancy":         0.48,
        "peak_occupancy":        0.72,
        "off_peak_occupancy":    0.28,
        "active_listings":       55,         # Small market; estimate pending research update
        "avg_annual_revenue":    37_000,     # Estimate; ~mid-point between Lander and Nederland
        "top10_annual_revenue":  95_000,
        "best_property_type":    "Cabin / Rustic Mountain Home",
        "peak_seasons":          ["Jun", "Jul", "Aug", "Sep"],
        "secondary_seasons":     ["Dec", "Jan", "Feb", "Mar"],
        "slow_seasons":          ["Apr", "Nov"],
        "tourism_drivers": [
            "Black Hawk / Central City — legal casino gambling (year-round demand driver)",
            "Peak to Peak Scenic Byway runs through county",
            "Moffat Tunnel trailhead (Rollinsville) — backcountry skiing, hiking",
            "Proximity to Eldora Mountain Resort (10–20 min from Rollinsville)",
            "Denver day-tripper / weekend market (45–55 min)",
            "Historic gold mining heritage tourism",
            "James Peak Wilderness access",
            "Gross Reservoir / South Boulder Creek recreation",
        ],
        "monthly_revenue": {
            "Jan": 3_200, "Feb": 3_100, "Mar": 3_800, "Apr": 2_100,
            "May": 2_900, "Jun": 4_200, "Jul": 5_100, "Aug": 4_800,
            "Sep": 4_000, "Oct": 3_300, "Nov": 2_000, "Dec": 3_500,
        },
        "seasonality": "Dual-season (casino = year-round base + summer recreation peak). April is slowest.",
        "yoy_trend": None,       # Insufficient data for reliable trend
        "avg_booking_lead_days": 45,
        "pct_entire_home": 0.92,
        "dominant_unit_size": "2–3BR",
        "avg_guest_capacity": 5.2,
    },
}

# ── STR Regulations ────────────────────────────────────────────────────────────
STR_REGULATIONS = {
    "Lander, WY": {
        "status": "Permitted — Business License Required",
        "license_required": True,
        "license_fee": None,         # Not published online; contact City of Lander
        "owner_occupancy_required": False,
        "cap_on_units": None,
        "lodging_tax_rate": 0.10,    # WY state 4% + WY lodging 5% + Fremont County 1% ≈ 10%
        "sales_tax_rate":  0.055,
        "platform_collects_tax": True,   # Airbnb/VRBO collect and remit all WY taxes
        "tax_detail": "WY State Sales 4% + WY Lodging Tax 5% + Fremont County Local 1% ≈ 10% total. "
                      "Applies to stays under 30 nights. Monthly filing with WY Dept of Revenue by 20th.",
        "notes": [
            "Wyoming has NO state income tax.",
            "City of Lander requires annual business license (fee not published — call City Clerk).",
            "Wyoming Sales Tax License and Wyoming Lodging Tax Registration required.",
            "Airbnb and VRBO collect and remit ALL applicable WY lodging/sales taxes automatically.",
            "No owner-occupancy requirement; no unit cap identified.",
            "Safety requirements: smoke detectors (each level + sleeping areas), CO detectors "
            "(if gas appliances), kitchen fire extinguisher, posted emergency contact.",
            "Inspections are complaint-based; initial registration may trigger one.",
            "No dedicated STR ordinance — governed by general business licensing + zoning.",
            "Fremont County outside city limits: even less regulation.",
        ],
        "ordinance_ref": "Lander Municipal Code — no dedicated STR ordinance; general business license",
        "contact": "City of Lander: (307) 332-2870 | Fremont County Planning: (307) 332-1077",
        "regulatory_risk": "Very Low",
        "risk_explanation": "No dedicated STR ordinance, no caps, no owner-occupancy requirement. "
                            "Wyoming is among the most hands-off states for STR regulation. "
                            "Lander has not moved toward Jackson-style restrictions.",
    },
    "Alpine, WY": {
        "status": "Largely Unregulated — General Business License",
        "license_required": True,    # General business license; no dedicated STR permit
        "license_fee": None,         # Not published; contact Town of Alpine
        "owner_occupancy_required": False,
        "cap_on_units": None,
        "lodging_tax_rate": 0.10,    # WY state 4% + WY lodging 5% + Lincoln County 1% ≈ 10%
        "sales_tax_rate":  0.055,
        "platform_collects_tax": True,
        "tax_detail": "WY State Sales 4% + WY Lodging Tax 5% + Lincoln County 1% ≈ 10% total. "
                      "Note: Star Valley town has moved to full 7% lodging tax as of Jan 2025 — "
                      "verify Alpine's specific code with WY Dept of Revenue.",
        "notes": [
            "Wyoming has NO state income tax.",
            "Town of Alpine: general Business License Application required (Ord. No. 299, 2022-17); "
            "contact (307) 654-7757 or admin@alpinewy.gov",
            "NO dedicated STR ordinance identified for Alpine proper.",
            "For properties in unincorporated Lincoln County: contact Lincoln County Planning in Afton.",
            "⚠️ CRITICAL: Star Valley Ranch (separate HOA municipality) has Chapter 113 STR rules — "
            "but this applies ONLY to Star Valley Ranch, not Alpine proper.",
            "⚠️ HOA CHECK: Alpine Meadows HOA and Alpine Village Resort HOA both govern subdivisions "
            "near Alpine. Many vacation properties are in these HOAs — STR may be restricted by CC&Rs.",
            "35.4% of current Alpine listings require 30+ day minimums — verify nightly STR is allowed.",
            "94% of STR guests are domestic; primary feeder is Salt Lake City (3.5hr drive).",
        ],
        "ordinance_ref": "Town of Alpine: alpinewy.gov/town-council/page/permits-applications | "
                         "Lincoln County Planning: Afton, WY",
        "contact": "Town of Alpine: (307) 654-7757 | admin@alpinewy.gov",
        "regulatory_risk": "Low",
        "risk_explanation": "Unincorporated county land and small town — Wyoming's pro-business stance "
                            "means minimal STR restriction. Main risk is HOA rules in specific subdivisions, "
                            "not government regulation.",
    },
    "Nederland, CO": {
        "status": "⚠️ REGULATED — Owner-Occupancy Required in Residential Zones",
        "license_required": True,
        "license_fee": None,         # Not published online; contact Town Clerk
        "owner_occupancy_required": True,   # ← CRITICAL for investors
        "cap_on_units": None,
        "lodging_tax_rate": 0.0944,  # CO 2.9% + Boulder County 1.185% + Nederland local ≈ 9.44%
        "sales_tax_rate":  0.0829,
        "platform_collects_tax": True,   # State + county taxes; local Nederland lodging tax = owner's responsibility
        "tax_detail": (
            "CO State Sales 2.9% + Boulder County ~1.185% + Nederland town taxes ≈ 9.44% combined. "
            "PLUS Nederland Lodging Occupation Tax: FLAT $4.00 per bedroom per night "
            "(e.g., 3BR × 100 nights = $1,200/yr). Filed quarterly. "
            "Platforms collect state/county; owner must file and remit the Nederland lodging tax. "
            "Host Compliance Hotline: (720) 778-8183."
        ),
        "notes": [
            "Colorado state income tax: 4.4%.",
            "⚠️ CRITICAL — TWO LICENSE TYPES:",
            "  1) Primary Residence License: For owner-occupants. Unlimited nights. Available in ALL zones.",
            "  2) Class C License: For non-primary-residence properties. ONLY available in "
            "     Central Business District (CBD) or General Commercial (GC) zoning. "
            "     Most residential properties do NOT qualify for Class C.",
            "Pure investors (non-owner-occupants) CANNOT legally STR a standard residential property in Nederland.",
            "One person may hold only one STR license.",
            "License expires at end of the calendar quarter in which originally issued.",
            "Required docs: proof of ownership, $1M liability insurance, self-inspection form.",
            "Nederland's lodging tax is unique: flat $4/bedroom/night (not a percentage).",
            "Airbnb/VRBO collect state + Boulder County taxes; owner must file and pay Nederland lodging tax.",
            "HB24-1299 (would have changed STR property tax classification) was postponed indefinitely "
            "by CO House Finance Committee on April 22, 2024 — did NOT pass.",
            "⭐ OPPORTUNITY: Town of Nederland approved $120M purchase of Eldora Mountain Resort (Feb 2026). "
            "If completed, makes Eldora town-owned — long-term STR demand catalyst. "
            "Funded by revenue bonds (not town taxes); 2-year transition period pending.",
            "⚠️ WILDFIRE INSURANCE RISK: Nederland is in a high-risk wildfire zone. "
            "Most major carriers will NOT write new policies. Budget $5,000–$10,000+/year. "
            "Verify insurability BEFORE making an offer.",
        ],
        "ordinance_ref": "Town of Nederland Municipal Code — STR Licenses: townofnederland.colorado.gov/permits/str",
        "contact": "Town of Nederland: (303) 258-3266 ext. 1030 | Host Compliance: (720) 778-8183",
        "regulatory_risk": "Moderate-High (for investors)",
        "risk_explanation": "The owner-occupancy requirement effectively bars pure investors from "
                            "STR-ing residential properties. Only CBD/GC-zoned properties are eligible "
                            "for non-owner-occupant STR licensing. This is a fundamental investment barrier. "
                            "The wildfire insurance crisis adds another material cost/availability risk.",
    },
    "Gilpin County, CO": {
        "status": "Permitted — County License Required (No Owner-Occupancy Requirement)",
        "license_required": True,
        "license_fee": 100,          # Estimate; verify with Gilpin County
        "owner_occupancy_required": False,   # ← KEY ADVANTAGE over Nederland
        "cap_on_units": None,
        "lodging_tax_rate": 0.049,   # Unincorporated Gilpin: CO state 2.9% + 2% CO lodging tax = ~4.9%
                                     # (Gilpin County imposes ZERO county sales tax — unique in CO)
                                     # Black Hawk/Central City: 8.9% + lodging tax (different market)
        "sales_tax_rate":  0.029,    # Unincorporated Gilpin only: 2.9% state, 0% county, 0% municipal
        "platform_collects_tax": True,
        "tax_detail": (
            "⭐ LOWEST TAX MARKET: Unincorporated Gilpin County (Rollinsville/Pinecliffe, zip 80474) "
            "has ONLY 2.9% Colorado state sales tax — zero county or municipal tax. "
            "Black Hawk (zip 80422): 8.9% (2.9% state + 6% municipal gaming tax). "
            "Central City (zip 80427): 8.9% same. Target UNINCORPORATED Gilpin for tax advantage. "
            "Colorado state lodging tax (~2%) applies on top of sales tax. "
            "Gilpin County was pursuing a lodging tax ballot measure (Nov 2025) — verify current status. "
            "Airbnb/VRBO collect state taxes; verify county lodging tax status with Gilpin County Finance."
        ),
        "notes": [
            "Colorado state income tax: 4.4%.",
            "⭐ KEY ADVANTAGE: No owner-occupancy requirement — pure investors CAN operate STRs.",
            "⭐ TAX ADVANTAGE: Unincorporated Gilpin (Rollinsville/Pinecliffe) = 2.9% sales tax only.",
            "Avoid Black Hawk/Central City for STR investment — 8.9% sales tax + gaming-focused environment.",
            "Gilpin County STR regulations appear permissive but VERIFY directly: (303) 582-5214.",
            "County website was inaccessible during research — direct contact required before investing.",
            "Gilpin County was considering a lodging tax ballot measure (Nov 2025) — verify if passed.",
            "Property tax significantly LOWER than Boulder County (~0.43% vs ~0.53%).",
            "Median property tax: ~$2,732/yr on $574k value.",
            "⚠️ WILDFIRE INSURANCE: Budget $4,000–$8,000+/yr; verify insurability before purchase.",
            "⚠️ RADON — Zone 1 (EPA highest category): Uranium-bearing granite geology. "
            "Assume mitigation system needed ($800–$2,500). Mandatory test during inspection.",
            "⚠️ MINE SUBSIDENCE: Thousands of historic mine shafts/tunnels throughout county. "
            "Obtain DRMS mine subsidence hazard report before purchasing ANY parcel. "
            "Colorado Division of Reclamation, Mining & Safety: (303) 866-3567.",
        ],
        "ordinance_ref": "Gilpin County Community Development — gilpincounty.org",
        "contact": "Gilpin County: (303) 582-5214",
        "regulatory_risk": "Low-Moderate",
        "risk_explanation": "No owner-occupancy requirement unlike Nederland. Lighter regulation than "
                            "Boulder County. Primary risks are wildfire insurance and physical hazards "
                            "(radon, mine subsidence) rather than regulatory barriers.",
    },
}

# ── Typical operating costs (STR) ─────────────────────────────────────────────
STR_OPERATING_COSTS = {
    "Lander, WY": {
        "mgmt_fee_pct":      0.20,
        "cleaning_per_stay": 90,
        "avg_stays_per_mo":  5,
        "supplies_monthly":  80,
        "utilities_monthly": 300,    # Rocky Mountain Power ~$99/mo elec; gas + water; guest usage
        "insurance_annual":  3_000,  # STR policy (standard HO insufficient); $2,500–$3,500 range
        "maintenance_pct":   0.01,   # 1% of home value/year
        "platform_fee_pct":  0.03,   # Airbnb host fee
        "property_tax_note": "WY assessed at 9.5% of actual value; effective rate ~0.71% (Fremont County)",
        "wildfire_risk":     "Low-Moderate",
        "insurance_note":    "Standard HO insufficient for STR. Budget $2,500–$3,500/yr for commercial STR policy.",
    },
    "Alpine, WY": {
        "mgmt_fee_pct":      0.20,
        "cleaning_per_stay": 150,    # Higher nightly rate / larger home = higher cleaning cost
        "avg_stays_per_mo":  5,
        "supplies_monthly":  120,
        "utilities_monthly": 400,    # Elevated: high altitude heating season + snow removal
        "insurance_annual":  4_000,  # $3,000–$5,000; mountain area, snow load, rising Mountain West premiums
        "maintenance_pct":   0.01,
        "platform_fee_pct":  0.03,
        "property_tax_note": "WY assessed at 9.5% of actual value; effective rate ~0.60% (Lincoln County). "
                             "Alpine has highest median tax bill in Lincoln County at ~$3,996.",
        "wildfire_risk":     "Moderate",
        "insurance_note":    "Mountain West insurance premiums rising. Budget $3,000–$5,000/yr. "
                             "Snow load and hail are primary risks. Proper.insure or Steadily recommended.",
    },
    "Nederland, CO": {
        "mgmt_fee_pct":      0.20,
        "cleaning_per_stay": 140,
        "avg_stays_per_mo":  6,
        "supplies_monthly":  120,
        "utilities_monthly": 475,    # Xcel Energy elec (~$157/mo CO avg) + elevated heating at 8,228 ft
        "insurance_annual":  7_500,  # ⚠️ HIGH: wildfire zone, $5,000–$10,000+ range
        "maintenance_pct":   0.015,  # Higher — older mountain homes + CO humidity/snow load
        "platform_fee_pct":  0.03,
        "property_tax_note": "Boulder County: CO assessment rate 6.765% of actual value. "
                             "Effective rate ~0.53% — among lowest in CO. $900k home ≈ $4,800/yr est.",
        "wildfire_risk":     "HIGH",
        "insurance_note":    "⚠️ CRITICAL RISK: Nederland is in a wildfire high-risk zone. "
                             "Most major carriers will NOT write new policies. "
                             "One documented case: Allstate was the ONLY major carrier available. "
                             "Budget $5,000–$10,000+/yr. Verify insurability BEFORE making an offer.",
        "lodging_tax_flat":  4.0,    # $4.00/bedroom/night flat Nederland lodging occupation tax
    },
    "Gilpin County, CO": {
        "mgmt_fee_pct":      0.20,
        "cleaning_per_stay": 115,
        "avg_stays_per_mo":  5,
        "supplies_monthly":  90,
        "utilities_monthly": 380,    # Similar elevation/climate to Nederland
        "insurance_annual":  6_000,  # $4,000–$8,000; wildfire zone but lower than Nederland
        "maintenance_pct":   0.015,  # Older homes common; historic mining area = foundation vigilance
        "platform_fee_pct":  0.03,
        "property_tax_note": "Gilpin County effective rate ~0.43% — significantly lower than Boulder County. "
                             "CO assessment rate 6.765% of actual value.",
        "wildfire_risk":     "HIGH",
        "insurance_note":    "Wildfire-prone mountain area. Budget $4,000–$8,000/yr. "
                             "Radon mitigation system may be required ($800–$2,500 one-time install). "
                             "Mine subsidence inspection recommended before purchase.",
    },
}

# ── Sample property listings (representative range) ───────────────────────────
SAMPLE_PROPERTIES = {
    "Lander, WY": [
        {"label": "Starter — 2bd/1ba in town",      "price": 220_000, "sqft": 980,  "beds": 2, "baths": 1},
        {"label": "Mid — 3bd/2ba updated",           "price": 350_000, "sqft": 1_600, "beds": 3, "baths": 2},
        {"label": "Nice — 3bd/2ba + garage/views",  "price": 430_000, "sqft": 2_100, "beds": 3, "baths": 2},
        {"label": "Premium — 4bd acreage",           "price": 575_000, "sqft": 2_800, "beds": 4, "baths": 3},
    ],
    "Alpine, WY": [
        {"label": "Entry — 2bd/1ba cabin",           "price": 450_000, "sqft": 1_100, "beds": 2, "baths": 1},
        {"label": "Mid — 3bd/2ba subdivision",       "price": 750_000, "sqft": 1_900, "beds": 3, "baths": 2},
        {"label": "River/res access — 3bd/2ba",      "price": 950_000, "sqft": 2_200, "beds": 3, "baths": 2},
        {"label": "Premium — 4bd riverfront",        "price": 1_300_000, "sqft": 3_200, "beds": 4, "baths": 3},
    ],
    "Nederland, CO": [
        {"label": "Entry — 2bd/1ba older cabin",     "price": 580_000, "sqft": 920,  "beds": 2, "baths": 1},
        {"label": "Mid — 3bd/2ba mountain home",     "price": 875_000, "sqft": 1_750, "beds": 3, "baths": 2},
        {"label": "Nice — 3bd/2ba updated",          "price": 1_000_000, "sqft": 2_100, "beds": 3, "baths": 2},
        {"label": "Premium — 4bd/3ba modern",        "price": 1_500_000, "sqft": 2_900, "beds": 4, "baths": 3},
    ],
    "Gilpin County, CO": [
        {"label": "Starter — 2bd cabin/fixer (unincorp.)", "price": 340_000, "sqft": 850,  "beds": 2, "baths": 1},
        {"label": "Mid — 3bd/2ba mountain home",           "price": 500_000, "sqft": 1_600, "beds": 3, "baths": 2},
        {"label": "Nice — 3bd/2ba updated",                "price": 625_000, "sqft": 2_000, "beds": 3, "baths": 2},
        {"label": "Premium — 4bd/3ba with acreage",        "price": 850_000, "sqft": 2_800, "beds": 4, "baths": 3},
    ],
}

# ── Building Permits — Costs, Timeline & Difficulty ───────────────────────────
# Sources: county building dept fee schedules, contractor forums, local knowledge.
# Difficulty ratings: 1 (very easy) → 10 (very hard)
PERMIT_DATA = {
    "Lander, WY": {
        "difficulty_rating": 2,
        "difficulty_label":  "Very Easy",
        "timeline_typical":  "1–3 weeks (city); potentially 0 permits (unincorporated county)",
        "online_portal":     False,
        "engineer_stamp_required": False,
        "new_home_2000sqft_fee":   800,    # City of Lander estimate; WY fees are very modest
        "major_remodel_100k_fee":  300,
        "addition_fee_per_sqft":   0.35,
        "aduAllowed":              True,
        "variance_difficulty":     "Easy",
        "notes": [
            "⭐ WYOMING HAS NO STATEWIDE BUILDING CODE — codes are adopted locally.",
            "Fremont County UNINCORPORATED areas may have NO building permit requirement "
            "— construction may be entirely unregulated outside city limits. "
            "This means zero permit fees and zero review time in rural Fremont County.",
            "City of Lander has its own building department requiring permits within city limits.",
            "Snow load at Lander (5,357 ft elevation): ~20–35 psf — significantly lighter "
            "than higher-elevation CO markets. Lower structural cost requirement.",
            "No architectural stamp required for typical single-family residential scope.",
            "Minimal fees — among the lowest of any market researched.",
            "Well permits: Wyoming State Engineer's Office (separate, add 2–6 weeks if needed).",
            "Septic: Fremont County Environmental Health (straightforward process).",
            "Inspectors described as collaborative and pragmatic.",
        ],
        "contact": "City of Lander Building: (307) 332-2870 | Fremont County: (307) 332-1077",
        "fee_schedule_url": "Contact City of Lander directly for current fee schedule",
    },
    "Alpine, WY": {
        "difficulty_rating": 2,
        "difficulty_label":  "Very Easy",
        "timeline_typical":  "1–3 weeks (town); potentially 0 permits (unincorporated county)",
        "online_portal":     False,
        "engineer_stamp_required": False,
        "new_home_2000sqft_fee":   900,
        "major_remodel_100k_fee":  350,
        "addition_fee_per_sqft":   0.40,
        "aduAllowed":              True,
        "variance_difficulty":     "Easy",
        "notes": [
            "⭐ WYOMING HAS NO STATEWIDE BUILDING CODE — codes are adopted locally.",
            "Lincoln County UNINCORPORATED areas may have NO building permit requirement.",
            "Town of Alpine has adopted minimal building regulations; fee schedule not published online.",
            "⚠️ SNOW LOAD: Star Valley receives significant snowfall despite ~5,650 ft elevation. "
            "Ground snow load: 40–60 psf (similar to Colorado mountain communities despite lower elevation). "
            "Engineered roof systems required. Budget 10–20% premium on structural costs.",
            "No architectural stamp required for typical single-family residential.",
            "Well permits: Wyoming State Engineer's Office. Septic: Lincoln County Environmental Health.",
            "Earthquake: Lincoln County has MODERATE seismic hazard (Wasatch Front proximity) — "
            "higher than other markets; factor into structural design.",
            "Small county staff; in-person only at Afton courthouse.",
        ],
        "contact": "Lincoln County Building: (307) 885-3106 | Town of Alpine: (307) 654-7757",
        "fee_schedule_url": "lincolncountywy.gov (contact for current schedule)",
    },
    "Nederland, CO": {
        "difficulty_rating": 8,
        "difficulty_label":  "Very Difficult",
        "timeline_typical":  "2–6 months new construction; 6–16 weeks remodel (often longer)",
        "online_portal":     True,   # Boulder County: css.bouldercounty.org (required)
        "engineer_stamp_required": True,
        "new_home_2000sqft_fee":   6_200,  # Confirmed from Boulder County fee schedule (Table 1-A)
                                           # $360k valuation: $3,061 permit + $1,990 plan check + use tax + fees
        "major_remodel_100k_fee":  2_280,  # Confirmed: $1,245 + $809 plan check + use tax + tech fee
        "addition_fee_per_sqft":   4.50,
        "aduAllowed":              True,
        "variance_difficulty":     "Very Hard",
        "notes": [
            "Boulder County fee schedule confirmed (Table 1-A, 2023 schedule):",
            "  New 2,000 sqft home ($360k valuation): ~$6,000–$6,200 total (permit + plan check + use tax + tech).",
            "  Major remodel ($100k): ~$2,260–$2,280 (permit $1,245 + plan check $809 + fees).",
            "  Defensible space fee ($200–$350) applies to ALL mountain/foothills properties.",
            "Online portal required (css.bouldercounty.org) — one digital PDF per permit.",
            "Virtual service hours Mon/Wed/Thu/Fri 8am–4:30pm; Tue 10am–4:30pm.",
            "Boulder County is widely considered one of CO's most difficult permit jurisdictions.",
            "Known issues: high staff turnover, 3–6+ month plan review for new construction.",
            "HERS energy rating required — strict Colorado Energy Code compliance.",
            "Soils report required for mountain properties.",
            "Wildfire mitigation (defensible space, ember-resistant venting) adds cost and timeline.",
            "Nederland Town + Boulder County can have overlapping/conflicting requirements.",
            "Snow load: 40–60 psf at Nederland elevation (8,228 ft).",
            "⚠️ Budget 12–18% of project cost for permitting fees, engineering, and compliance.",
        ],
        "contact": "Boulder County Building: (303) 441-3926 | Town of Nederland: (303) 258-3266",
        "fee_schedule_url": "bouldercounty.gov/buildings-property/building/fees/",
    },
    "Gilpin County, CO": {
        "difficulty_rating": 4,
        "difficulty_label":  "Moderate — Much Easier than Boulder County",
        "timeline_typical":  "2–6 weeks",
        "online_portal":     False,
        "engineer_stamp_required": True,   # Colorado IRC/IBC applies statewide for structural
        "new_home_2000sqft_fee":   2_200,  # Estimate: 30–60% less than Boulder County
        "major_remodel_100k_fee":  1_000,  # Estimate from comparable small CO mountain counties
        "addition_fee_per_sqft":   1.80,
        "aduAllowed":              True,
        "variance_difficulty":     "Moderate",
        "notes": [
            "Colorado IRC 2021 applies statewide; Gilpin County enforces with fewer local amendments than Boulder.",
            "Small office (~1–2 staff) in Central City — more flexible, direct communication.",
            "No online portal — visit Gilpin County offices or call (303) 582-5214.",
            "Fee estimates are 30–60% below Boulder County (comparable small CO mountain county data).",
            "Verify exact fees directly: Gilpin County website was inaccessible during research.",
            "Engineer stamp required for structural work (CO state requirement); less extensive than Boulder.",
            "Snow load: 40–60 psf at Gilpin elevations (8,000–9,500 ft) — same as Nederland.",
            "⚠️ MINE HAZARD: Geotechnical investigation may be required before permits in known hazard areas. "
            "Colorado Division of Reclamation, Mining & Safety: (303) 866-3567.",
            "Septic: Gilpin County Environmental Health — less strict than Boulder County.",
            "Avoid Black Hawk/Central City building depts — casino-focused, different process.",
            "Contractors describe unincorporated Gilpin as 'reasonable and workable.'",
        ],
        "contact": "Gilpin County Community Development: (303) 582-5214",
        "fee_schedule_url": "gilpincounty.org/community-development (call to confirm — website may be down)",
    },
}

# ── Environmental Risks ────────────────────────────────────────────────────────
# Risk levels: "Low", "Moderate", "High", "Very High"
# Scores: 1 (minimal) → 10 (severe)
ENVIRONMENTAL_RISKS = {
    "Lander, WY": {
        "overall_risk_score": 4,
        "overall_label": "Moderate (radon Zone 1 — less known but real)",
        "risks": {
            "Wildfire": {
                "level": "Moderate",
                "score": 4,
                "details": (
                    "Sagebrush and mixed conifer terrain around Lander carries moderate wildfire risk. "
                    "Not in Colorado's extreme fire zone. WY generally has lower fire frequency than CO. "
                    "Lander itself (in the Wind River valley) has lower risk than surrounding foothills."
                ),
                "insurance_impact": "Minimal to moderate premium increase vs. national avg",
                "action": "Standard defensible space maintenance; confirm policy covers wildland interface.",
            },
            "Flood": {
                "level": "Moderate",
                "score": 4,
                "details": (
                    "Popo Agie River runs through Lander — portions of town are in FEMA 100-year floodplain. "
                    "Check FEMA Flood Map (FIRM) for any specific parcel before purchasing. "
                    "Flood insurance may be required by lender if in Zone A/AE."
                ),
                "insurance_impact": "Flood insurance required in Zone A/AE (~$700–$2,000/yr via NFIP)",
                "action": "Pull FEMA FIRM panel for specific parcel. Avoid Zone AE/A without mitigation.",
            },
            "Radon": {
                "level": "High",
                "score": 7,
                "details": (
                    "Fremont County is EPA Zone 1 (highest radon risk category) due to "
                    "uranium-bearing geology in the Wind River Basin — Wyoming has extensive "
                    "uranium deposits. EPA action level is 4 pCi/L. "
                    "Testing is cheap ($15–30 kit); mitigation is $800–$2,000. "
                    "This is less commonly known but is a confirmed Zone 1 county."
                ),
                "insurance_impact": "None — health risk (lung cancer)",
                "action": "Radon test is MANDATORY during inspection. Budget $800–$2,000 for mitigation if needed.",
            },
            "Mine Subsidence": {
                "level": "Low",
                "score": 1,
                "details": "Minimal historic underground mining activity in Lander proper.",
                "insurance_impact": "None",
                "action": "Not a material concern for in-town properties.",
            },
            "Avalanche": {
                "level": "Low",
                "score": 1,
                "details": "Lander sits in a valley. Avalanche risk is not material for in-town properties.",
                "insurance_impact": "None",
                "action": "N/A for typical in-town purchase.",
            },
            "Hail": {
                "level": "Moderate",
                "score": 5,
                "details": (
                    "NOAA Storm Events 2010–2024: 48 hail events in Fremont County, "
                    "hail up to 2.00 inches, $3M property damage from one June 2023 event. "
                    "More hail-prone than Colorado mountain areas but less than eastern plains."
                ),
                "insurance_impact": "Factor into homeowners insurance; ensure policy covers hail damage",
                "action": "Impact-resistant roofing (Class 4 shingles) can reduce premiums.",
            },
            "Snow Load": {
                "level": "Low-Moderate",
                "score": 3,
                "details": (
                    "Lander sits at only 5,357 ft elevation — significantly lower than CO mountain markets. "
                    "Ground snow load: ~20–35 psf — much lighter than Alpine or Nederland (40–60 psf). "
                    "Lower structural cost requirement is a meaningful construction advantage."
                ),
                "insurance_impact": "Structural compliance required; standard construction handles Lander loads",
                "action": "Lower snow load = lower structural cost. Still verify older homes for compliance.",
            },
            "Earthquake": {
                "level": "Low-Moderate",
                "score": 3,
                "details": (
                    "Wyoming has low-moderate seismic hazard. Fremont County is not near major fault zones "
                    "but USGS places it above the near-zero risk of Colorado Front Range. "
                    "Not a material concern for standard residential construction."
                ),
                "insurance_impact": "Low; standard construction handles WY seismic requirements",
                "action": "Not a primary concern for most buyers.",
            },
            "Landslide": {
                "level": "Low",
                "score": 2,
                "details": "Lander sits in the Wind River valley; minimal landslide risk for in-town properties.",
                "insurance_impact": "None",
                "action": "Assess hillside or canyon-adjacent lots individually.",
            },
        },
    },
    "Alpine, WY": {
        "overall_risk_score": 4,
        "overall_label": "Moderate",
        "risks": {
            "Wildfire": {
                "level": "Moderate",
                "score": 5,
                "details": (
                    "Alpine sits in forested mountain terrain — wildfire risk is real. "
                    "Bridger-Teton NF surrounds the area. The 2012 Fontenelle Fire burned ~175k acres "
                    "nearby. Mountain West premiums rising due to fire risk."
                ),
                "insurance_impact": "Higher premiums; some carriers limiting coverage. Budget $3,000–$5,000/yr.",
                "action": "Defensible space maintenance required. Verify insurability before purchase.",
            },
            "Flood": {
                "level": "Moderate-High",
                "score": 6,
                "details": (
                    "Snake River and Greys River floodplains affect portions of Alpine. "
                    "Properties with river access/proximity are often in FEMA Zone A/AE. "
                    "Spring snowmelt flooding is a recurring seasonal event."
                ),
                "insurance_impact": "Flood insurance required if in Zone A/AE (~$700–$3,000/yr)",
                "action": "Pull FEMA FIRM for specific parcel. River-access premium properties carry flood risk.",
            },
            "Radon": {
                "level": "Low-Moderate",
                "score": 3,
                "details": "Lincoln County has some radon risk but generally lower than CO mining counties.",
                "insurance_impact": "None",
                "action": "Standard radon test during inspection period.",
            },
            "Mine Subsidence": {
                "level": "Low",
                "score": 1,
                "details": "No significant historic underground mining in the Alpine area.",
                "insurance_impact": "None",
                "action": "N/A",
            },
            "Avalanche": {
                "level": "Low-Moderate",
                "score": 3,
                "details": (
                    "Some avalanche terrain exists in the Greys River drainage above Alpine. "
                    "In-town and subdivision properties generally not in avalanche runout zones."
                ),
                "insurance_impact": "Not typically insured; structural risk",
                "action": "Assess hillside or canyon-adjacent properties individually via CGS hazard maps.",
            },
            "Hail": {
                "level": "Low-Moderate",
                "score": 3,
                "details": "Western WY receives less severe hail than eastern plains. Moderate seasonal risk.",
                "insurance_impact": "Standard homeowners coverage",
                "action": "Standard roofing; not a critical concern.",
            },
            "Snow Load": {
                "level": "High",
                "score": 8,
                "details": (
                    "Alpine receives ~500 inches annual snowfall. Ground snow loads are EXTREME. "
                    "Lincoln County design ground snow load: 150–250+ psf in some areas. "
                    "This drives significant structural requirements and maintenance costs."
                ),
                "insurance_impact": "Structural compliance critical; roof collapse risk for non-compliant structures",
                "action": "Verify roof is rated for local ground snow load. Budget for snow removal. "
                          "Inspect older structures carefully for deformation/overloading signs.",
            },
            "Earthquake": {
                "level": "Moderate",
                "score": 5,
                "details": (
                    "Lincoln County WY has moderate seismic hazard due to proximity to the "
                    "Wasatch Front fault system (Idaho/Utah border) — higher than any other "
                    "market researched. NOAA data confirms this risk zone. "
                    "Factor into structural design decisions."
                ),
                "insurance_impact": "Consider earthquake endorsement; consult structural engineer",
                "action": "Higher seismic zone than CO markets. Discuss with structural engineer for new builds.",
            },
            "Landslide": {
                "level": "Moderate",
                "score": 4,
                "details": "Steep terrain around Alpine creek and river drainages creates localized slide risk.",
                "insurance_impact": "Not standard coverage; specialty policy if in mapped zone",
                "action": "Assess hillside lots individually. Avoid steep drainage-adjacent lots.",
            },
        },
    },
    "Nederland, CO": {
        "overall_risk_score": 7,
        "overall_label": "High",
        "risks": {
            "Wildfire": {
                "level": "Very High",
                "score": 9,
                "details": (
                    "NOAA Storm Events 2010–2024: 16 wildfire events, $2.346 BILLION total property damage "
                    "in Boulder County — primarily the Dec 30, 2021 Marshall Fire ($2B, 1,084 homes destroyed). "
                    "2010 Fourmile Canyon Fire destroyed 168 homes near Nederland. "
                    "2020 Cal-Wood and Lefthand Canyon fires also impacted the area. "
                    "Boulder County has the worst wildfire financial loss record of any county researched. "
                    "Most major insurers have stopped writing new policies in this area."
                ),
                "insurance_impact": "CRITICAL — budget $5,000–$10,000+/yr. Many carriers won't insure. "
                                    "Verify insurability BEFORE making any offer. Colorado FAIR Plan may be last resort.",
                "action": "Get insurance quote BEFORE making an offer. Defensible space (100ft) required. "
                          "Ember-resistant venting, metal roofing recommended.",
            },
            "Flood": {
                "level": "Low",
                "score": 2,
                "details": (
                    "Nederland is at elevation (8,228 ft) — not in significant floodplain. "
                    "Barker Reservoir downstream. Most parcels have low flood risk."
                ),
                "insurance_impact": "Minimal; unlikely to be required",
                "action": "Verify parcel-level FEMA flood map; generally not a concern.",
            },
            "Radon": {
                "level": "High",
                "score": 7,
                "details": (
                    "Boulder County and the Front Range mountain corridor have elevated radon. "
                    "Colorado ranks among top states for high radon levels. "
                    "Nederland is in a moderate-high radon zone. EPA threshold is 4 pCi/L."
                ),
                "insurance_impact": "None — health risk",
                "action": "Radon test is MANDATORY during inspection. Budget $800–$2,500 for mitigation system.",
            },
            "Mine Subsidence": {
                "level": "Low",
                "score": 2,
                "details": (
                    "Nederland itself has less historic mining than Gilpin County to the east. "
                    "Some historic adit/shaft activity in surrounding hills — parcel-specific."
                ),
                "insurance_impact": "Rare; specialty policy exists",
                "action": "Not a primary concern but worth a brief geologic review for rural parcels.",
            },
            "Avalanche": {
                "level": "Low-Moderate",
                "score": 3,
                "details": (
                    "Some avalanche terrain above Nederland in steeper drainages. "
                    "Town itself is not in a high-hazard runout zone. "
                    "Check Colorado Avalanche Information Center (CAIC) hazard maps for specific parcels."
                ),
                "insurance_impact": "Generally not an issue for in-town/subdivision properties",
                "action": "Check CAIC for any steep-terrain adjacent parcels.",
            },
            "Hail": {
                "level": "High",
                "score": 7,
                "details": (
                    "Front Range Colorado is in a hail alley — one of the highest hail frequencies "
                    "in the US. Nederland is at the edge of the Front Range corridor. "
                    "The 2023 hail season caused record insurance losses across Boulder County."
                ),
                "insurance_impact": "Significant — ensure homeowners policy has strong hail coverage. "
                                    "Class 4 impact-resistant roofing may reduce premiums.",
                "action": "Class 4 shingles or metal roof strongly recommended. "
                          "Confirm hail coverage limits in any policy.",
            },
            "Snow Load": {
                "level": "High",
                "score": 7,
                "details": (
                    "Nederland ground snow load: ~100–130 psf per Colorado building code. "
                    "Significant structural requirement. Older homes (pre-1980) may be undersized."
                ),
                "insurance_impact": "Structural compliance required",
                "action": "Verify structural adequacy on older homes. Roof inspection critical.",
            },
            "Earthquake": {
                "level": "Low",
                "score": 2,
                "details": "Colorado Front Range has low seismic hazard. Not a material concern.",
                "insurance_impact": "None",
                "action": "N/A",
            },
            "Landslide": {
                "level": "Moderate",
                "score": 4,
                "details": (
                    "Steep terrain surrounding Nederland has localized landslide risk. "
                    "Colorado Geological Survey maps several debris flow and landslide hazard areas "
                    "in the Boulder County mountain corridor."
                ),
                "insurance_impact": "Not standard coverage",
                "action": "Check CGS Hazard Unit mapping for specific parcels. Avoid steep drainage-head lots.",
            },
        },
    },
    "Gilpin County, CO": {
        "overall_risk_score": 7,
        "overall_label": "High (unique risks: wildfire + radon + mine subsidence)",
        "risks": {
            "Wildfire": {
                "level": "High",
                "score": 8,
                "details": (
                    "NOAA Storm Events 2010–2024: 4 wildfire events, $22 million total property damage "
                    "(two $11M events in March–April 2012 coinciding with CO's historic 2012 wildfire season). "
                    "Gilpin County is densely forested (Arapaho/Roosevelt NF) at 8,000–10,000 ft. "
                    "Lodgepole pine + ponderosa = high fuel load. Falls in CO WUI (Wildland-Urban Interface). "
                    "Colorado ranks 2nd nationally with 318,783 homes at extreme wildfire risk. "
                    "Insurance is difficult but somewhat more available than Nederland/Boulder County."
                ),
                "insurance_impact": "High premiums — budget $4,000–$8,000+/yr. Verify availability before purchase.",
                "action": "Get insurance quote before offer. Defensible space critical. "
                          "Metal roofing, ember-resistant venting strongly recommended.",
            },
            "Flood": {
                "level": "Low-Moderate",
                "score": 3,
                "details": (
                    "Clear Creek and North Clear Creek flow through parts of Gilpin County. "
                    "Some parcels near drainages may be in FEMA flood zones. "
                    "Check FEMA FIRM for specific parcels."
                ),
                "insurance_impact": "Required if in Zone A/AE",
                "action": "Verify FEMA flood zone for any specific parcel near creek drainages.",
            },
            "Radon": {
                "level": "Very High",
                "score": 9,
                "details": (
                    "⚠️ Gilpin County has VERY HIGH radon risk — one of the highest in Colorado. "
                    "The historic gold, silver, and uranium mining throughout the county left extensive "
                    "uranium-bearing rock exposed. Colorado School of Mines studies show elevated "
                    "radon in Gilpin County homes. EPA reports Gilpin as a Zone 1 county "
                    "(predicted average > 4 pCi/L — the action level). "
                    "Many homes have tested at 10–50+ pCi/L without mitigation."
                ),
                "insurance_impact": "None — health risk (lung cancer)",
                "action": "MANDATORY radon test during inspection. Assume mitigation system will be needed. "
                          "Budget $800–$2,500 for mitigation. Confirm system works post-install.",
            },
            "Mine Subsidence": {
                "level": "Very High",
                "score": 9,
                "details": (
                    "⚠️ CRITICAL GILPIN COUNTY RISK: The county sits atop one of Colorado's most "
                    "extensively mined areas (the Colorado Mineral Belt). Thousands of miles of "
                    "underground workings from the 1860s–1940s. Colorado Geological Survey has mapped "
                    "known mine shafts and adits, but many remain unmapped. "
                    "Subsidence (ground collapse into old mine workings) is a documented risk. "
                    "The Gilpin County Building Department may require geotechnical investigation "
                    "before issuing permits in known hazard areas. "
                    "Mine shaft collapse has damaged or destroyed structures in the area."
                ),
                "insurance_impact": "Standard policies exclude mine subsidence. Specialty coverage available but expensive.",
                "action": "REQUIRE mine hazard assessment before any purchase. "
                          "Check CGS Mine Subsidence Hazard maps (cgsmines.mines.edu). "
                          "Hire a geotechnical engineer for pre-purchase review on any rural parcel. "
                          "Do NOT build above known mine workings.",
            },
            "Avalanche": {
                "level": "Moderate",
                "score": 4,
                "details": (
                    "NOAA Storm Events 2010–2024: 20 avalanche events in Gilpin County, "
                    "15 deaths and 8 injuries recorded — significant mortality data. "
                    "Events concentrated above 9,000 ft in the forecast zone. "
                    "Most residential development (Rollinsville/Pinecliffe) is below primary avalanche elevation. "
                    "Specific high-elevation or canyon-bottom parcels carry higher risk."
                ),
                "insurance_impact": "Not typically insured; structural/safety risk",
                "action": "Check CAIC avalanche hazard maps for specific parcels above 9,000 ft. "
                          "Most Rollinsville/Pinecliffe homes are below primary avalanche zones.",
            },
            "Hail": {
                "level": "Low",
                "score": 2,
                "details": (
                    "NOAA Storm Events 2010–2024: Zero hail events recorded for Gilpin County 2020–2023. "
                    "Elevation (8,000–9,500 ft) places the county above the primary hail corridor. "
                    "Significantly lower hail risk than Denver metro or Boulder plains."
                ),
                "insurance_impact": "Minimal hail premium impact",
                "action": "Lower concern than other Front Range markets. Standard roofing adequate.",
            },
            "Snow Load": {
                "level": "High",
                "score": 7,
                "details": (
                    "Ground snow load at Gilpin County elevations (8,000–9,500 ft): ~100–150 psf. "
                    "Structural requirements significant. Older mining-era structures often inadequate."
                ),
                "insurance_impact": "Structural compliance required",
                "action": "Roof/structural inspection critical on older homes. Budget for upgrades.",
            },
            "Earthquake": {
                "level": "Low",
                "score": 2,
                "details": "Low seismic hazard in Gilpin County area.",
                "insurance_impact": "None",
                "action": "N/A",
            },
            "Landslide": {
                "level": "Moderate",
                "score": 4,
                "details": (
                    "Some landslide and debris flow hazard areas exist in steeper terrain. "
                    "Check CGS hazard mapping for specific parcels."
                ),
                "insurance_impact": "Not standard coverage",
                "action": "CGS hazard map review for specific parcels.",
            },
        },
    },
}
