import { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container, Typography, Box, Grid, Chip, Rating, Paper, Button,
  TextField, Dialog, DialogTitle, DialogContent, DialogActions, Alert
} from '@mui/material';
import VerifiedIcon from '@mui/icons-material/Verified';
import { useTranslation } from 'react-i18next';

// Mock detail (replace with guideApi.getDetail())
const MOCK_DETAIL = {
  user_id: '1', display_name: 'Li Wei', languages: ['en', 'zh'],
  service_cities: ['Beijing'], specialties: ['history', 'food'],
  rating_avg: 4.8, rating_count: 127, default_rate_cny: 800,
  avatar_url: null, bio: 'Born and raised in Beijing. 15 years guiding foreign visitors through hutongs, temples, and hidden restaurants. I studied Chinese history at Peking University and love sharing the stories behind every alley and courtyard. Whether you want to explore the Great Wall at sunrise or find the best jianbing in the city, I know the way.',
  guide_license_no: 'D-1101-0****', guide_license_issuer: '北京市文化和旅游局',
  kyc_status: 'approved',
  listings: [
    { id: 'l1', title: 'Beijing Hutong Deep Dive — Half Day', summary: 'Explore hidden alleys, local markets, and centuries-old courtyard homes with a born-and-raised Beijinger.', city: 'Beijing', price_amount: 800, price_currency: 'CNY', price_unit: 'per_half_day' },
    { id: 'l2', title: 'Great Wall at Sunrise — Full Day', summary: 'Skip the crowds. We leave at 5 AM for the Jinshanling section — the most photogenic stretch, with almost no tourists.', city: 'Beijing', price_amount: 1500, price_currency: 'CNY', price_unit: 'per_day' },
    { id: 'l3', title: 'Beijing Street Food Night Walk', summary: 'From Wangfujing to Guijie — taste your way through lamb skewers, stinky tofu, fried scorpions, and the best hand-pulled noodles in the city.', city: 'Beijing', price_amount: 600, price_currency: 'CNY', price_unit: 'per_half_day' },
  ],
};

export default function GuideDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { t } = useTranslation();
  const [connectOpen, setConnectOpen] = useState(false);
  const [selectedListing, setSelectedListing] = useState<string | null>(null);
  const guide = MOCK_DETAIL; // Replace with API call

  const handleConnect = (listingId: string) => {
    setSelectedListing(listingId);
    setConnectOpen(true);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={4}>
        {/* Left: Guide info */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Box sx={{
              width: 150, height: 150, borderRadius: '50%', bgcolor: '#1a472a', color: 'white',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 48, mx: 'auto', mb: 2
            }}>
              {guide.display_name.charAt(0)}
            </Box>

            <Typography variant="h5" sx={{ fontWeight: 700 }}>{guide.display_name}</Typography>

            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
              <VerifiedIcon color="success" sx={{ mr: 0.5 }} />
              <Typography variant="body2" color="success.main">{t('guide.verified')}</Typography>
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
              <Rating value={guide.rating_avg} precision={0.1} readOnly />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {guide.rating_avg} ({guide.rating_count})
              </Typography>
            </Box>

            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
              License: {guide.guide_license_no}
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block">
              Issued by: {guide.guide_license_issuer}
            </Typography>

            <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 0.5, justifyContent: 'center' }}>
              {guide.languages.map((l) => (
                <Chip key={l} label={l.toUpperCase()} size="small" />
              ))}
              {guide.specialties.map((s) => (
                <Chip key={s} label={s} size="small" color="primary" variant="outlined" />
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Right: Bio + Listings */}
        <Grid item xs={12} md={8}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>{t('guide.about')}</Typography>
          <Typography variant="body1" sx={{ mb: 4, lineHeight: 1.8 }}>{guide.bio}</Typography>

          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>{t('guide.listings')}</Typography>

          {guide.listings.map((listing) => (
            <Paper key={listing.id} sx={{ p: 3, mb: 2, '&:hover': { boxShadow: 4 } }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>{listing.title}</Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {listing.summary}
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'right', ml: 2, minWidth: 120 }}>
                  <Typography variant="h5" color="primary" sx={{ fontWeight: 700 }}>
                    ¥{listing.price_amount}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {t('search.price_set_by_guide')}
                    <br />
                    {t(`search.${listing.price_unit}`)}
                  </Typography>
                </Box>
              </Box>
              <Button
                variant="contained"
                sx={{ mt: 2, bgcolor: '#1a472a', '&:hover': { bgcolor: '#2d5a3f' } }}
                onClick={() => handleConnect(listing.id)}
              >
                {t('guide.connect')}
              </Button>
            </Paper>
          ))}
        </Grid>
      </Grid>

      {/* Connection Request Dialog */}
      <Dialog open={connectOpen} onClose={() => setConnectOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{t('guide.connect')}</DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            {t('guide.connect_note')}
          </Alert>
          <TextField fullWidth label="Date" type="date" InputLabelProps={{ shrink: true }} sx={{ mb: 2, mt: 1 }} />
          <TextField fullWidth label="Group size" type="number" defaultValue={1} inputProps={{ min: 1, max: 30 }} sx={{ mb: 2 }} />
          <TextField fullWidth label="Notes for the guide (optional)" multiline rows={3} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConnectOpen(false)}>Cancel</Button>
          <Button variant="contained" sx={{ bgcolor: '#1a472a' }} onClick={() => setConnectOpen(false)}>
            Send Request
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
