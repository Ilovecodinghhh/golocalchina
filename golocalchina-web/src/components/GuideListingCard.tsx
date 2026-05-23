import { Card, CardContent, Typography, Box, Chip, Rating } from '@mui/material';
import { Link } from 'react-router-dom';
import VerifiedIcon from '@mui/icons-material/Verified';
import PlaceIcon from '@mui/icons-material/Place';
import { useTranslation } from 'react-i18next';

const DEFAULT_COVER = 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600&q=80';

// Currency conversion
const FX: Record<string, [string, number]> = {
  USD: ['$', 0.14], EUR: ['€', 0.13], GBP: ['£', 0.11], AUD: ['A$', 0.22],
  JPY: ['¥', 21.5], KRW: ['₩', 192], CAD: ['C$', 0.19], CNY: ['¥', 1],
};
function convertPrice(cny: number): string {
  try {
    const stored = localStorage.getItem('glc_user');
    if (!stored) return '¥' + cny;
    const { currency } = JSON.parse(stored);
    if (!currency || currency === 'CNY') return '¥' + cny;
    const [sym, rate] = FX[currency] || ['¥', 1];
    return sym + Math.round(cny * rate);
  } catch { return '¥' + cny; }
}

interface Props {
  listing: any;
}

export default function GuideListingCard({ listing }: Props) {
  const { t } = useTranslation();
  const guide = listing.guide || {};

  return (
    <Card
      component={Link}
      to={'/listing/' + listing.id}
      sx={{
        height: '100%', display: 'flex', flexDirection: 'column', borderRadius: 3,
        textDecoration: 'none', color: 'inherit', overflow: 'hidden',
        '&:hover': { boxShadow: 8, transform: 'translateY(-4px)' }, transition: 'all 0.2s',
      }}
    >
      {/* Cover image with overlay */}
      <Box sx={{ position: 'relative', height: 200, overflow: 'hidden' }}>
        <Box
          component="img"
          src={listing.cover_image_url || DEFAULT_COVER}
          alt={listing.title}
          sx={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <Box sx={{
          position: 'absolute', inset: 0,
          background: 'linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 50%)',
          display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', p: 2,
        }}>
          <Typography variant="subtitle1" sx={{ color: 'white', fontWeight: 700, lineHeight: 1.3 }}>
            {listing.title}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
            <PlaceIcon sx={{ color: 'rgba(255,255,255,0.8)', fontSize: 16 }} />
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              {listing.city}
            </Typography>
          </Box>
        </Box>
        {/* Price badge */}
        <Box sx={{
          position: 'absolute', top: 12, right: 12,
          bgcolor: '#DC2626', color: 'white', px: 1.5, py: 0.5, borderRadius: 2,
          fontWeight: 700, fontSize: '0.9rem',
        }}>
          {convertPrice(listing.price_amount)}
        </Box>
        {/* Certified badge */}
        {guide.is_certified && (
          <Chip icon={<VerifiedIcon sx={{ fontSize: 14 }} />} label="Certified" size="small"
            sx={{ position: 'absolute', top: 12, left: 12, bgcolor: 'rgba(255,255,255,0.95)', fontWeight: 600, fontSize: '0.7rem' }} />
        )}
      </Box>

      <CardContent sx={{ flexGrow: 1, pt: 2 }}>
        {/* Guide info */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
          <Box sx={{
            width: 40, height: 40, borderRadius: '50%', bgcolor: '#DC2626', color: 'white',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 16, flexShrink: 0,
          }}>
            {(guide.display_name || '?').charAt(0)}
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>{guide.display_name}</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <Rating value={guide.rating_avg || 0} precision={0.1} size="small" readOnly sx={{ fontSize: 14 }} />
              <Typography variant="caption" color="text.secondary">
                ({guide.rating_count || 0})
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Summary */}
        <Typography variant="body2" color="text.secondary" sx={{
          mb: 1.5, lineHeight: 1.6, display: '-webkit-box',
          WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden',
        }}>
          {listing.summary}
        </Typography>

        {/* Languages */}
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {(listing.languages || []).map((l: string) => (
            <Chip key={l} label={l.toUpperCase()} size="small" variant="outlined" sx={{ fontSize: '0.65rem', height: 22 }} />
          ))}
        </Box>

        <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
          {t('search.price_set_by_guide')} · {listing.price_unit === 'per_day' ? t('search.per_day') : listing.price_unit === 'per_hour' ? t('search.per_hour') : t('search.per_half_day')}
        </Typography>
      </CardContent>
    </Card>
  );
}
