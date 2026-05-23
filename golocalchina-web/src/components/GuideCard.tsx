import { Card, CardContent, Typography, Box, Chip, Rating, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import VerifiedIcon from '@mui/icons-material/Verified';
import PersonIcon from '@mui/icons-material/Person';
import PlaceIcon from '@mui/icons-material/Place';
import type { Guide } from '../services/api';

interface GuideWithExtras extends Guide {
  is_certified?: boolean;
  featured_trip?: {
    title: string;
    highlight: string;
    cover_url: string;
  };
}

interface Props {
  guide: GuideWithExtras;
}

export default function GuideCard({ guide }: Props) {
  const { t } = useTranslation();
  const isCertified = guide.is_certified !== false;
  const trip = guide.featured_trip;

  return (
    <Card sx={{
      height: '100%', display: 'flex', flexDirection: 'column', borderRadius: 3,
      '&:hover': { boxShadow: 8, transform: 'translateY(-4px)' }, transition: 'all 0.2s', overflow: 'hidden',
    }}>
      {/* Trip thumbnail — shows the experience, not just the guide's face */}
      <Box sx={{ position: 'relative', height: 200, overflow: 'hidden' }}>
        <Box component="img"
          src={trip?.cover_url || `https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600&q=80`}
          alt={trip?.title || guide.display_name}
          sx={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        {/* Dark gradient overlay with trip title */}
        <Box sx={{
          position: 'absolute', inset: 0,
          background: 'linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 50%)',
          display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', p: 2,
        }}>
          {trip && (
            <Typography variant="subtitle1" sx={{ color: 'white', fontWeight: 700, lineHeight: 1.3 }}>
              {trip.title}
            </Typography>
          )}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
            <PlaceIcon sx={{ color: 'rgba(255,255,255,0.8)', fontSize: 16 }} />
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              {guide.service_cities.join(' · ')}
            </Typography>
          </Box>
        </Box>
        {/* Price badge */}
        <Box sx={{
          position: 'absolute', top: 12, right: 12,
          bgcolor: '#DC2626', color: 'white', px: 1.5, py: 0.5, borderRadius: 2,
          fontWeight: 700, fontSize: '0.9rem',
        }}>
          ¥{guide.default_rate_cny}
        </Box>
        {/* Certified badge */}
        {isCertified && (
          <Chip icon={<VerifiedIcon sx={{ fontSize: 14 }} />} label="Certified" size="small"
            sx={{ position: 'absolute', top: 12, left: 12, bgcolor: 'rgba(255,255,255,0.95)', fontWeight: 600, fontSize: '0.7rem' }} />
        )}
      </Box>

      <CardContent sx={{ flexGrow: 1, pt: 2 }}>
        {/* Guide info row */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
          <Box sx={{
            width: 40, height: 40, borderRadius: '50%', bgcolor: '#DC2626', color: 'white',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 16, flexShrink: 0,
          }}>
            {guide.display_name.charAt(0)}
          </Box>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>{guide.display_name}</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <Rating value={guide.rating_avg} precision={0.1} size="small" readOnly sx={{ fontSize: 14 }} />
              <Typography variant="caption" color="text.secondary">
                {guide.rating_avg.toFixed(1)} ({guide.rating_count})
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Trip highlight text — the guide's pitch */}
        {trip?.highlight && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, lineHeight: 1.6, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
            "{trip.highlight}"
          </Typography>
        )}

        {/* Languages */}
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {guide.languages.map((l) => <Chip key={l} label={l.toUpperCase()} size="small" variant="outlined" sx={{ fontSize: '0.65rem', height: 22 }} />)}
        </Box>

        <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
          {t('search.price_set_by_guide')}
        </Typography>
      </CardContent>

      <Box sx={{ p: 2, pt: 0 }}>
        <Button fullWidth variant="contained" component={Link} to={`/guides/${guide.user_id}`}
          sx={{ bgcolor: '#DC2626', borderRadius: 2, '&:hover': { bgcolor: '#B91C1C' } }}>
          View Details →
        </Button>
      </Box>
    </Card>
  );
}
