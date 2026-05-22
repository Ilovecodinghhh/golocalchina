import { Box, Typography, Paper } from '@mui/material';

interface Props {
  slot: 'top' | 'sidebar' | 'in-feed' | 'bottom';
}

/**
 * Ad placement component.
 * 
 * Phase 1: Placeholder slots (current)
 * Phase 2: Google AdSense (drop in script + data-ad-slot)
 * Phase 3: Travel affiliate links (Trip.com, Booking.com, Klook)
 * Phase 4: Sponsored guide listings (premium placement)
 * 
 * To switch to AdSense, replace the placeholder with:
 * <ins className="adsbygoogle" data-ad-client="ca-pub-XXXXX" data-ad-slot="XXXXX" />
 */
export default function AdBanner({ slot }: Props) {
  const sizes: Record<string, { width: string; height: number }> = {
    'top': { width: '100%', height: 90 },
    'sidebar': { width: '100%', height: 250 },
    'in-feed': { width: '100%', height: 120 },
    'bottom': { width: '100%', height: 90 },
  };

  const { width, height } = sizes[slot] || sizes['in-feed'];

  // Placeholder for development — replace with real ads in production
  return (
    <Paper
      elevation={0}
      sx={{
        width, height, display: 'flex', alignItems: 'center', justifyContent: 'center',
        bgcolor: '#f9f9f6', border: '1px dashed #ccc', borderRadius: 2, my: 2,
        overflow: 'hidden',
      }}
    >
      {/* 
        PRODUCTION: Replace this Box with Google AdSense:
        <ins className="adsbygoogle"
             style={{ display: 'block' }}
             data-ad-client="ca-pub-YOUR_ID"
             data-ad-slot="YOUR_SLOT_ID"
             data-ad-format="auto"
             data-full-width-responsive="true" />
        
        Or travel affiliate:
        <a href="https://www.trip.com/?ref=golocalchina">
          <img src="/ads/trip-com-banner.png" />
        </a>
      */}
      <Box sx={{ textAlign: 'center', opacity: 0.4 }}>
        <Typography variant="caption">Ad Space — {slot}</Typography>
        <Typography variant="caption" display="block">Travel deals, hotels, flights</Typography>
      </Box>
    </Paper>
  );
}
