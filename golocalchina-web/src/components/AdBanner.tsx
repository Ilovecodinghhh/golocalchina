interface Props {
  slot: 'top' | 'sidebar' | 'in-feed' | 'bottom';
}

/**
 * Ad placement component — currently disabled.
 * 
 * Phase 1: Placeholder slots (disabled)
 * Phase 2: Google AdSense (drop in script + data-ad-slot)
 * Phase 3: Travel affiliate links (Trip.com, Booking.com, Klook)
 * Phase 4: Sponsored guide listings (premium placement)
 * 
 * To re-enable, restore the Paper component below.
 * To switch to AdSense, replace with:
 * <ins className="adsbygoogle" data-ad-client="ca-pub-XXXXX" data-ad-slot="XXXXX" />
 */
export default function AdBanner({ slot }: Props) {
  // Temporarily disabled — return null to hide all ad placeholders
  return null;
}
