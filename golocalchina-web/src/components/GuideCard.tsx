import { Card, CardContent, CardMedia, Typography, Box, Chip, Rating, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import type { Guide } from '../services/api';

const AVATAR_PLACEHOLDER = 'https://via.placeholder.com/300x200/1a472a/ffffff?text=Guide';

interface Props {
  guide: Guide;
}

export default function GuideCard({ guide }: Props) {
  const { t } = useTranslation();

  const priceLabel = `¥${guide.default_rate_cny}`;

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', '&:hover': { boxShadow: 6 } }}>
      <CardMedia
        component="img"
        height="180"
        image={guide.avatar_url || AVATAR_PLACEHOLDER}
        alt={guide.display_name}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            {guide.display_name}
          </Typography>
          <Typography variant="h6" color="primary" sx={{ fontWeight: 700 }}>
            {priceLabel}
          </Typography>
        </Box>

        <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 1 }}>
          {t('search.price_set_by_guide')}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Rating value={guide.rating_avg} precision={0.1} size="small" readOnly />
          <Typography variant="body2" sx={{ ml: 1 }}>
            {guide.rating_avg.toFixed(1)} ({guide.rating_count} {t('guide.reviews')})
          </Typography>
        </Box>

        <Box sx={{ mb: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {guide.languages.map((lang) => (
            <Chip key={lang} label={lang.toUpperCase()} size="small" variant="outlined" />
          ))}
        </Box>

        <Box sx={{ mb: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {guide.specialties.slice(0, 3).map((s) => (
            <Chip key={s} label={s} size="small" color="primary" variant="outlined" />
          ))}
        </Box>

        {guide.bio && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            {guide.bio.slice(0, 100)}{guide.bio.length > 100 ? '…' : ''}
          </Typography>
        )}
      </CardContent>

      <Box sx={{ p: 2, pt: 0 }}>
        <Button
          fullWidth
          variant="contained"
          component={Link}
          to={`/guides/${guide.user_id}`}
          sx={{ bgcolor: '#1a472a', '&:hover': { bgcolor: '#2d5a3f' } }}
        >
          {t('guide.connect')}
        </Button>
      </Box>
    </Card>
  );
}
