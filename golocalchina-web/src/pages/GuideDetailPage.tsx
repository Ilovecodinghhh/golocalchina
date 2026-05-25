import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container, Typography, Box, Grid, Chip, Rating, Paper, Button,
  TextField, Dialog, DialogTitle, DialogContent, DialogActions, Alert, CircularProgress
} from '@mui/material';
import VerifiedIcon from '@mui/icons-material/Verified';
import QrCodeIcon from '@mui/icons-material/QrCode2';
import PaymentsIcon from '@mui/icons-material/Payments';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import AdBanner from '../components/AdBanner';

export default function GuideDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [guide, setGuide] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [connectOpen, setConnectOpen] = useState(false);
  const [selectedListing, setSelectedListing] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get('/guides/' + id);
        setGuide(res.data);
      } catch {
        setGuide(null);
      }
      setLoading(false);
    };
    load();
  }, [id]);

  const handleConnect = (listingId: string) => {
    setSelectedListing(listingId);
    setSent(false);
    setConnectOpen(true);
  };

  const handleSendRequest = async () => {
    const stored = localStorage.getItem('glc_token');
    if (!stored) { navigate('/login'); return; }
    const dateEl = document.querySelector('input[type="date"]') as HTMLInputElement;
    const sizeEl = document.querySelector('input[type="number"]') as HTMLInputElement;
    const notesEl = document.querySelector('textarea') as HTMLTextAreaElement;
    setSending(true);
    try {
      await api.post('/service-requests', {
        guide_user_id: guide.user_id,
        service_date: dateEl?.value || new Date().toISOString().split('T')[0],
        party_size: parseInt(sizeEl?.value || '1'),
        language: 'en',
        tourist_notes: notesEl?.value || '',
        quoted_amount: guide.listings?.find((l: any) => l.id === selectedListing)?.price_amount || guide.default_rate_cny || 0,
        quoted_currency: 'CNY',
      });
      setSent(true);
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to send request. Make sure you are logged in.');
    } finally {
      setSending(false);
    }
  };

  if (loading) return (
    <Container sx={{ py: 8, textAlign: 'center' }}>
      <CircularProgress sx={{ color: '#DC2626' }} />
    </Container>
  );

  if (!guide) return (
    <Container sx={{ py: 8, textAlign: 'center' }}>
      <Typography variant="h5" sx={{ mb: 2 }}>Guide not found</Typography>
      <Button variant="contained" onClick={() => navigate('/guides')} sx={{ bgcolor: '#DC2626' }}>Browse All Guides</Button>
    </Container>
  );

  const listings = guide.listings || [];

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
              {(guide.display_name || '?').charAt(0)}
            </Box>

            <Typography variant="h5" sx={{ fontWeight: 700 }}>{guide.display_name}</Typography>

            {guide.kyc_status === 'approved' && (
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
                <VerifiedIcon color="success" sx={{ mr: 0.5 }} />
                <Typography variant="body2" color="success.main">{t('guide.verified')}</Typography>
              </Box>
            )}

            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
              <Rating value={guide.rating_avg || 0} precision={0.1} readOnly />
              <Typography variant="body2" sx={{ ml: 1 }}>
                {guide.rating_avg || 0} ({guide.rating_count || 0})
              </Typography>
            </Box>

            {guide.guide_license_no && (
              <>
                <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
                  License: {guide.guide_license_no}
                </Typography>
                <Typography variant="caption" color="text.secondary" display="block">
                  Issued by: {guide.guide_license_issuer}
                </Typography>
              </>
            )}

            <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 0.5, justifyContent: 'center' }}>
              {(guide.languages || []).map((l: string) => (
                <Chip key={l} label={l.toUpperCase()} size="small" />
              ))}
              {(guide.specialties || []).map((s: string) => (
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
          <Typography variant="body1" sx={{ mb: 4, lineHeight: 1.8 }}>{guide.bio || 'No bio provided yet.'}</Typography>

          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>{t('guide.listings')}</Typography>

          {listings.length === 0 && (
            <Alert severity="info">This guide hasn't published any listings yet.</Alert>
          )}

          {listings.map((listing: any, idx: number) => (
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
                      {listing.price_unit === 'per_day' ? t('search.per_day') : listing.price_unit === 'per_hour' ? t('search.per_hour') : t('search.per_half_day')}
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
          {sent ? (
            <Alert severity="success" sx={{ my: 2 }}>
              Request sent! Check your dashboard for updates.
            </Alert>
          ) : (
            <>
              <Alert severity="info" sx={{ mb: 2 }}>
                {t('guide.connect_note')}
              </Alert>
              <Alert severity="success" sx={{ mb: 2 }} icon={<PaymentsIcon />}>
                {t('payment.direct_desc')}
              </Alert>
              <TextField fullWidth label="Date" type="date" InputLabelProps={{ shrink: true }} sx={{ mb: 2, mt: 1 }} />
              <TextField fullWidth label="Group size" type="number" defaultValue={1} inputProps={{ min: 1, max: 30 }} sx={{ mb: 2 }} />
              <TextField fullWidth label="Notes for the guide (optional)" multiline rows={3} />
            </>
          )}
        </DialogContent>
        <DialogActions>
          {sent ? (
            <>
              <Button onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
              <Button onClick={() => { setConnectOpen(false); setSent(false); }}>Close</Button>
            </>
          ) : (
            <>
              <Button onClick={() => setConnectOpen(false)}>Cancel</Button>
              <Button variant="contained" sx={{ bgcolor: '#1a472a' }} disabled={sending}
                onClick={handleSendRequest}>
                {sending ? 'Sending...' : 'Send Request'}
              </Button>
            </>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
}
