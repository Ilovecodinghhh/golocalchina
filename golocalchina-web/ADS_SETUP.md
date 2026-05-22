# GoLocalChina — Ad Revenue Setup Guide

## Phase 1: Google AdSense (Day 1)

1. Apply at https://adsense.google.com
2. Once approved, get your `ca-pub-XXXXX` ID
3. Add to `index.html`:
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXX" crossorigin="anonymous"></script>
```
4. Update `AdBanner.tsx` — replace placeholder with:
```tsx
<ins className="adsbygoogle"
     style={{ display: 'block' }}
     data-ad-client="ca-pub-XXXXX"
     data-ad-slot="YOUR_SLOT_ID"
     data-ad-format="auto"
     data-full-width-responsive="true" />
```

### Ad Slot Placements
| Slot | Location | Format | Expected RPM |
|------|----------|--------|-------------|
| `top` | Above search results on /guides | Leaderboard (728×90) | $1-3 |
| `sidebar` | Guide detail sidebar | Medium rectangle (300×250) | $2-5 |
| `in-feed` | Between guide listings | In-feed native | $1-4 |
| `bottom` | Bottom of search results | Leaderboard (728×90) | $0.5-2 |

## Phase 2: Travel Affiliate Links (Week 2)

| Partner | Program | Commission |
|---------|---------|-----------|
| Trip.com | trip.com/affiliates | 3-5% per hotel/flight booking |
| Booking.com | booking.com/affiliate | 25-40% of Booking.com commission |
| Klook | klook.com/affiliateprogram | 3-5% per activity booking |
| GetYourGuide | partner.getyourguide.com | 8% per booking |

Add affiliate banners to AdBanner component with your referral links.

## Phase 3: Sponsored Guide Listings (Month 2+)

- Charge guides $20-50/month for "Featured" badge and priority placement
- Add `is_sponsored` field to guide_listings table
- Boost sponsored listings to top of search results
- Clearly label "Sponsored" per advertising regulations

## Revenue Projections

| Monthly visitors | AdSense est. | Affiliate est. | Sponsored est. | Total |
|-----------------|-------------|----------------|----------------|-------|
| 1,000 | $5-15 | $10-50 | $0 | $15-65 |
| 10,000 | $50-150 | $100-500 | $200 | $350-850 |
| 50,000 | $250-750 | $500-2,500 | $1,000 | $1,750-4,250 |
| 100,000 | $500-1,500 | $1,000-5,000 | $2,500 | $4,000-9,000 |
