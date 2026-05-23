import { Card, CardContent, CardMedia, Typography, Box, Chip, Rating, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import VerifiedIcon from '@mui/icons-material/Verified';
import PersonIcon from '@mui/icons-material/Person';
import type { Guide } from '../services/api';

interface Props {
  guide: Guide & { is_certified?: boolean };
}

export default function GuideCard({ guide }: Props) {
  const { t } = useTranslation();
  const isCertified = (guide as any).is_certified !== false; // default true for mock

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', borderRadius: 3, '&:hover': { boxShadow: 8, transform: 'translateY(-4px)' }, transition: 'all 0.2s' }}>
      <CardMedia
        component="img" height="180"
        image={guide.avatar_url || `https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&q=80`}
        alt={guide.display_name}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>{guide.display_name}</Typography>
          <Typography variant="h6" sx={{ fontWeight: 700, color: '#DC2626' }}>¥{guide.default_rate_cny}</Typography>
        </Box>

        {/* Certified vs Community badge */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {isCertified ? (
            <Chip icon={<VerifiedIcon />} label={t('guide.certified')} size="small"
                  sx={{ bgcolor: '#FEF2F2', color: '#DC2626', fontWeight: 600 }} />
          ) : (
            <Chip icon={<PersonIcon />} label={t('guide.community')} size="small" variant="outlined" />
          )}
        </Box>

        <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
          {t('search.price_set_by_guide')}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Rating value={guide.rating_avg} precision={0.1} size="small" readOnly />
          <Typography variant="body2" sx={{ ml: 1 }}>
            {guide.rating_avg.toFixed(1)} ({guide.rating_count})
          </Typography>
        </Box>

        <Box sx={{ mb: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {guide.languages.map((l) => <Chip key={l} label={l.toUpperCase()} size="small" variant="outlined" />)}
          {guide.specialties.slice(0, 2).map((s) => <Chip key={s} label={s} size="small" sx={{ bgcolor: '#FEF2F2', color: '#DC2626' }} />)}
        </Box>

        {guide.bio && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            {guide.bio.slice(0, 80)}{guide.bio.length > 80 ? '…' : ''}
          </Typography>
        )}
      </CardContent>

      <Box sx={{ p: 2, pt: 0 }}>
        <Button fullWidth variant="contained" component={Link} to={`/guides/${guide.user_id}`}
          sx={{ bgcolor: '#DC2626', borderRadius: 2, '&:hover': { bgcolor: '#B91C1C' } }}>
          {t('guide.connect')}
        </Button>
      </Box>
    </Card>
  );
}
