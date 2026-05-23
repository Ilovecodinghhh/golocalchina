import { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container, Typography, Box, Grid, Chip, Rating, Paper, Button,
  TextField, Dialog, DialogTitle, DialogContent, DialogActions, Alert, Divider
} from '@mui/material';
import VerifiedIcon from '@mui/icons-material/Verified';
import QrCodeIcon from '@mui/icons-material/QrCode2';
import PaymentsIcon from '@mui/icons-material/Payments';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import { useTranslation } from 'react-i18next';
import AdBanner from '../components/AdBanner';

// Mock detail
const MOCK_DETAIL = {
  user_id: '1', display_name: 'Li Wei', languages: ['en', 'zh'],
  service_cities: ['Beijing'], specialties: ['history', 'food'],
  rating_avg: 4.8, rating_count: 127, default_rate_cny: 800,
  avatar_url: null,
  bio: 'Born and raised in Beijing. 15 years guiding foreign visitors through hutongs, temples, and hidden restaurants. I studied Chinese history at Peking University and love sharing the stories behind every alley and courtyard. Whether you want to explore the Great Wall at sunrise or find the best jianbing in the city, I know the way.',
  guide_license_no: 'D-1101-0****', guide_license_issuer: '北京市文化和旅游局',
  kyc_status: 'approved',
  accepts_cash: true,
  alipay_qr_url: null,  // Guide uploads their QR code
  wechat_pay_qr_url: null,
  payment_note: 'I accept Alipay, WeChat Pay, or USD/CNY cash. Scan my QR code when we meet!',
  listings: [
    { id: 'l1', title: 'Beijing Hutong Deep Dive — Half Day', summary: 'Explore hidden alleys, local markets, and centuries-old courtyard homes with a born-and-raised Beijinger.', city: 'Beijing', price_amount: 800, price_currency: 'CNY', price_unit: 'per_half_day' },
    { id: 'l2', title: 'Great Wall at Sunrise — Full Day', summary: 'Skip the crowds. We leave at 5 AM for the Jinshanling section — the most photogenic stretch, with almost no tourists.', city: 'Beijing', price_amount: 1500, price_currency: 'CNY', price_unit: 'per_day' },
    { id: 'l3', title: 'Beijing Street Food Night Walk', summary: 'From Wangfujing to Guijie — taste your way through lamb skewers, stinky tofu, fried scorpions, and the best hand-pulled noodles.', city: 'Beijing', price_amount: 600, price_currency: 'CNY', price_unit: 'per_half_day' },
  ],
};

export default function GuideDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { t } = useTranslation();
  const [connectOpen, setConnectOpen] = useState(false);
  const [selectedListing, setSelectedListing] = useState<string | null>(null);
  const guide = MOCK_DETAIL;

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

          {/* Payment Methods Card */}
          <Paper sx={{ p: 3, mt: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1.5, display: 'flex', alignItems: 'center' }}>
              <PaymentsIcon sx={{ mr: 1 }} /> {t('guide.payment_methods')}
            </Typography>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {guide.alipay_qr_url && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <QrCodeIcon color="primary" />
                  <Typography variant="body2">{t('payment.alipay')}</Typography>
                </Box>
              )}
              {guide.wechat_pay_qr_url && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <QrCodeIcon color="success" />
                  <Typography variant="body2">{t('payment.wechat')}</Typography>
                </Box>
              )}
              {guide.accepts_cash && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AccountBalanceWalletIcon color="action" />
                  <Typography variant="body2">{t('payment.cash')}</Typography>
                </Box>
              )}
            </Box>

            {guide.payment_note && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1.5, fontStyle: 'italic' }}>
                "{guide.payment_note}"
              </Typography>
            )}

            <Alert severity="info" sx={{ mt: 2, fontSize: '0.75rem' }}>
              {t('payment.note')}
            </Alert>
          </Paper>

          {/* Sidebar Ad */}
          <AdBanner slot="sidebar" />
        </Grid>

        {/* Right: Bio + Listings */}
        <Grid item xs={12} md={8}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>{t('guide.about')}</Typography>
          <Typography variant="body1" sx={{ mb: 4, lineHeight: 1.8 }}>{guide.bio}</Typography>

          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>{t('guide.listings')}</Typography>

          {guide.listings.map((listing, idx) => (
            <Box key={listing.id}>
              <Paper sx={{ p: 3, mb: 2, '&:hover': { boxShadow: 4 } }}>
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

              {/* In-feed ad after every 2 listings */}
              {idx === 1 && <AdBanner slot="in-feed" />}
            </Box>
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
          <Alert severity="success" sx={{ mb: 2 }} icon={<PaymentsIcon />}>
            {t('payment.direct_desc')}
          </Alert>
          <TextField fullWidth label="Date" type="date" InputLabelProps={{ shrink: true }} sx={{ mb: 2, mt: 1 }} />
          <TextField fullWidth label="Group size" type="number" defaultValue={1} inputProps={{ min: 1, max: 30 }} sx={{ mb: 2 }} />
          <TextField fullWidth label="Notes for the guide (optional)" multiline rows={3} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConnectOpen(false)}>Cancel</Button>
          <Button variant="contained" sx={{ bgcolor: '#1a472a' }} onClick={async () => {
              const stored = localStorage.getItem('glc_user');
              if (!stored) { window.location.href = '/login'; return; }
              const user = JSON.parse(stored);
              const dateEl = document.querySelector('input[type="date"]') as HTMLInputElement;
              const sizeEl = document.querySelector('input[type="number"]') as HTMLInputElement;
              const notesEl = document.querySelector('textarea') as HTMLTextAreaElement;
              try {
                const { default: api } = await import('../services/api');
                await api.post(`/service-requests?tourist_user_id=${user.id}`, {
                  guide_user_id: guide.user_id,
                  service_date: dateEl?.value || new Date().toISOString().split('T')[0],
                  party_size: parseInt(sizeEl?.value || '1'),
                  language: 'en',
                  tourist_notes: notesEl?.value || '',
                  quoted_amount: guide.listings?.find((l: any) => l.id === selectedListing)?.price_amount || guide.default_rate_cny || 0,
                  quoted_currency: 'CNY',
                });
                setConnectOpen(false);
                alert('Request sent! Check your dashboard for updates.');
              } catch (err: any) {
                alert(err?.response?.data?.detail || 'Failed to send request. Make sure you are logged in.');
              }
            }}>
            Send Request
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
