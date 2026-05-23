import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Typography, Box, Paper, Button, Grid, Avatar, Chip,
  TextField, Alert, Tabs, Tab, Dialog, DialogTitle, DialogContent,
  DialogActions, Select, MenuItem, FormControl, InputLabel, IconButton
} from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import api from '../services/api';

const CITIES = ['Beijing', 'Shanghai', 'Xian', 'Chengdu', 'Guilin', 'Hangzhou'];

export default function DashboardPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [tab, setTab] = useState(0);
  const [profile, setProfile] = useState<any>({});
  const [listings, setListings] = useState<any[]>([]);
  const [requests, setRequests] = useState<any[]>([]);
  const [saveMsg, setSaveMsg] = useState('');
  const [newListingOpen, setNewListingOpen] = useState(false);
  const [newListing, setNewListing] = useState({ title: '', summary: '', description_md: '', city: 'Beijing', price_amount: 500, price_unit: 'per_half_day', cover_image_url: '', languages: 'en,zh' });

  useEffect(() => {
    const stored = localStorage.getItem('glc_user');
    if (!stored) { navigate('/login'); return; }
    const u = JSON.parse(stored);
    setUser(u);
    loadProfile(u.id);
    loadRequests(u.id, u.role);
    if (u.role === 'guide') loadListings(u.id);
  }, [navigate]);

  const loadRequests = async (userId: string, role: string) => {
    try {
      const res = await api.get(\`/service-requests/mine?user_id=\${userId}&role=\${role}\`);
      setRequests(res.data);
    } catch {}
  };

  const loadProfile = async (userId: string) => {
    try {
      const res = await api.get(`/profile/me?user_id=${userId}`);
      setProfile(res.data);
    } catch {}
  };

  const loadListings = async (userId: string) => {
    try {
      const res = await api.get(`/listings/mine?guide_user_id=${userId}`);
      setListings(res.data);
    } catch {}
  };

  const saveProfile = async () => {
    setSaveMsg('');
    try {
      if (user.role === 'tourist') {
        await api.put(`/profile/me/tourist?user_id=${user.id}`, {
          display_name: profile.display_name,
          nationality: profile.nationality,
          preferred_currency: profile.preferred_currency,
        });
      } else {
        await api.put(`/profile/me/guide?user_id=${user.id}`, {
          display_name: profile.display_name,
          bio: profile.bio,
          languages: typeof profile.languages === 'string' ? profile.languages.split(',').map((s: string) => s.trim()) : profile.languages,
          service_cities: typeof profile.service_cities === 'string' ? profile.service_cities.split(',').map((s: string) => s.trim()) : profile.service_cities,
          default_rate_cny: profile.default_rate_cny,
          alipay_qr_url: profile.alipay_qr_url,
          wechat_pay_qr_url: profile.wechat_pay_qr_url,
          payment_note: profile.payment_note,
        });
      }
      // Update local storage
      localStorage.setItem('glc_user', JSON.stringify({ ...user, display_name: profile.display_name, email: profile.email }));
      setSaveMsg('✅ Profile saved!');
    } catch (err: any) {
      setSaveMsg('❌ ' + (err?.response?.data?.detail || 'Failed to save'));
    }
  };

  const createListing = async () => {
    try {
      await api.post(`/listings?guide_user_id=${user.id}`, {
        ...newListing,
        languages: newListing.languages.split(',').map(s => s.trim()),
        price_amount: Number(newListing.price_amount),
      });
      setNewListingOpen(false);
      setNewListing({ title: '', summary: '', description_md: '', city: 'Beijing', price_amount: 500, price_unit: 'per_half_day', cover_image_url: '', languages: 'en,zh' });
      loadListings(user.id);
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to create listing');
    }
  };

  const deleteListing = async (id: string) => {
    if (!confirm('Delete this listing?')) return;
    try {
      await api.delete(`/listings/${id}?guide_user_id=${user.id}`);
      loadListings(user.id);
    } catch {}
  };

  const handleLogout = () => {
    localStorage.removeItem('glc_token');
    localStorage.removeItem('glc_user');
    navigate('/');
  };

  if (!user) return null;
  const up = (field: string, value: any) => setProfile((p: any) => ({ ...p, [field]: value }));

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Paper sx={{ p: 4, mb: 4, borderRadius: 3, background: 'linear-gradient(135deg, #DC2626 0%, #991B1B 100%)', color: 'white' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <Avatar sx={{ width: 80, height: 80, bgcolor: 'rgba(255,255,255,0.2)', fontSize: 32, fontWeight: 700 }}>
            {(profile.display_name || user.email || 'U').charAt(0).toUpperCase()}
          </Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>{profile.display_name || user.email}</Typography>
            <Chip label={user.role === 'guide' ? '🧭 Local Guide' : '🌍 Tourist'}
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', mt: 1, fontWeight: 600 }} />
          </Box>
          <Button startIcon={<LogoutIcon />} onClick={handleLogout}
            sx={{ color: 'white', border: '1px solid rgba(255,255,255,0.3)' }}>Log Out</Button>
        </Box>
      </Paper>

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3, '& .Mui-selected': { color: '#DC2626' }, '& .MuiTabs-indicator': { bgcolor: '#DC2626' } }}>
        {user.role === 'guide'
          ? [<Tab key={0} label="My Listings" />, <Tab key={1} label="Requests" />, <Tab key={2} label="Profile" />]
          : [<Tab key={0} label="My Requests" />, <Tab key={1} label="Profile" />]}
      </Tabs>

      {/* GUIDE: Listings tab */}
      {user.role === 'guide' && tab === 0 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>Your Service Listings</Typography>
            <Button variant="contained" startIcon={<AddIcon />} onClick={() => setNewListingOpen(true)}
              sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>Create New Listing</Button>
          </Box>
          {listings.length === 0 ? (
            <Alert severity="info">No listings yet. Create your first one to start connecting with travelers!</Alert>
          ) : (
            listings.map((l) => (
              <Paper key={l.id} sx={{ p: 3, mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{l.title}</Typography>
                  <Typography variant="body2" color="text.secondary">{l.city} · ¥{l.price_amount} {l.price_unit}</Typography>
                  <Chip label={l.status} size="small" color={l.status === 'published' ? 'success' : 'default'} sx={{ mt: 0.5 }} />
                </Box>
                <IconButton color="error" onClick={() => deleteListing(l.id)}><DeleteIcon /></IconButton>
              </Paper>
            ))
          )}
        </Box>
      )}

      {/* TOURIST: Requests tab */}
      {user.role === 'tourist' && tab === 0 && (
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>Your Connection Requests</Typography>
          {requests.length === 0 ? (
            <Alert severity="info" action={<Button color="inherit" size="small" onClick={() => navigate('/guides')}>Browse Guides</Button>}>
              No requests yet. Find a guide and start planning!
            </Alert>
          ) : (
            requests.map((r: any) => (
              <Paper key={r.id} sx={{ p: 3, mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {r.service_date} · {r.party_size} {r.party_size > 1 ? 'people' : 'person'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      ¥{r.quoted_amount} {r.quoted_currency} · Language: {r.language}
                    </Typography>
                    {r.tourist_notes && <Typography variant="body2" sx={{ mt: 0.5, fontStyle: 'italic' }}>"{r.tourist_notes}"</Typography>}
                  </Box>
                  <Chip label={r.status} color={r.status === 'accepted' ? 'success' : r.status === 'pending' ? 'warning' : 'default'} />
                </Box>
              </Paper>
            ))
          )}
        </Box>
      )}

      {/* GUIDE: Requests tab */}
      {user.role === 'guide' && tab === 1 && (
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>Connection Requests from Tourists</Typography>
          {requests.length === 0 ? (
            <Alert severity="info">No requests yet. Once tourists find your listings, their requests appear here.</Alert>
          ) : (
            requests.map((r: any) => (
              <Paper key={r.id} sx={{ p: 3, mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>{r.service_date} · {r.party_size} {r.party_size > 1 ? 'people' : 'person'}</Typography>
                    <Typography variant="body2" color="text.secondary">¥{r.quoted_amount} · {r.language}</Typography>
                    {r.tourist_notes && <Typography variant="body2" sx={{ mt: 0.5, fontStyle: 'italic' }}>"{r.tourist_notes}"</Typography>}
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                    <Chip label={r.status} color={r.status === 'accepted' ? 'success' : r.status === 'pending' ? 'warning' : 'default'} />
                    {r.status === 'pending' && (
                      <>
                        <Button size="small" variant="contained" color="success"
                          onClick={async () => { await api.put(\`/service-requests/\${r.id}/accept?guide_user_id=\${user.id}\`); loadRequests(user.id, user.role); }}>
                          Accept
                        </Button>
                        <Button size="small" variant="outlined" color="error"
                          onClick={async () => { await api.put(\`/service-requests/\${r.id}/decline?guide_user_id=\${user.id}\`); loadRequests(user.id, user.role); }}>
                          Decline
                        </Button>
                      </>
                    )}
                  </Box>
                </Box>
              </Paper>
            ))
          )}
        </Box>
      )}

      {/* PROFILE tab (both roles) */}
      {((user.role === 'guide' && tab === 2) || (user.role === 'tourist' && tab === 1)) && (
        <Paper sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>Edit Profile</Typography>
          {saveMsg && <Alert severity={saveMsg.startsWith('✅') ? 'success' : 'error'} sx={{ mb: 2 }}>{saveMsg}</Alert>}
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Display Name" value={profile.display_name || ''} onChange={(e) => up('display_name', e.target.value)} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Email" value={profile.email || ''} disabled />
            </Grid>

            {user.role === 'tourist' && (
              <>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Country Code (e.g. US, GB, AU)" value={profile.nationality || ''}
                    onChange={(e) => up('nationality', e.target.value.toUpperCase())} inputProps={{ maxLength: 2 }} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Preferred Currency</InputLabel>
                    <Select value={profile.preferred_currency || 'USD'} label="Preferred Currency"
                      onChange={(e) => up('preferred_currency', e.target.value)}>
                      {[['USD','$ US Dollar'],['EUR','€ Euro'],['GBP','£ British Pound'],['AUD','A$ Australian Dollar'],['JPY','¥ Japanese Yen'],['KRW','₩ Korean Won'],['CAD','C$ Canadian Dollar'],['CNY','¥ Chinese Yuan']].map(([code, label]) => (
                        <MenuItem key={code} value={code}>{label}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              </>
            )}

            {user.role === 'guide' && (
              <>
                <Grid item xs={12}>
                  <TextField fullWidth multiline rows={4} label="Bio — Tell travelers your story"
                    value={profile.bio || ''} onChange={(e) => up('bio', e.target.value)}
                    placeholder="What makes you unique? What will travelers experience with you?" />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Languages (comma separated)" placeholder="en, zh, fr"
                    value={Array.isArray(profile.languages) ? profile.languages.join(', ') : profile.languages || ''}
                    onChange={(e) => up('languages', e.target.value)} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Cities (comma separated)" placeholder="Beijing, Shanghai"
                    value={Array.isArray(profile.service_cities) ? profile.service_cities.join(', ') : profile.service_cities || ''}
                    onChange={(e) => up('service_cities', e.target.value)} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Default Rate (CNY)" type="number" value={profile.default_rate_cny || ''}
                    onChange={(e) => up('default_rate_cny', Number(e.target.value))} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Payment Note" placeholder="I accept Alipay, WeChat Pay, or cash"
                    value={profile.payment_note || ''} onChange={(e) => up('payment_note', e.target.value)} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Alipay QR URL" value={profile.alipay_qr_url || ''} onChange={(e) => up('alipay_qr_url', e.target.value)} />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="WeChat Pay QR URL" value={profile.wechat_pay_qr_url || ''} onChange={(e) => up('wechat_pay_qr_url', e.target.value)} />
                </Grid>
              </>
            )}

            <Grid item xs={12}>
              <Button variant="contained" onClick={saveProfile}
                sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>Save Changes</Button>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* New Listing Dialog */}
      <Dialog open={newListingOpen} onClose={() => setNewListingOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Listing</DialogTitle>
        <DialogContent>
          <TextField fullWidth label="Title" placeholder="e.g. Beijing Hutong Deep Dive — Half Day" sx={{ mt: 1, mb: 2 }}
            value={newListing.title} onChange={(e) => setNewListing(p => ({ ...p, title: e.target.value }))} />
          <TextField fullWidth label="Summary (short pitch)" placeholder="What will the traveler experience?" sx={{ mb: 2 }}
            value={newListing.summary} onChange={(e) => setNewListing(p => ({ ...p, summary: e.target.value }))} multiline rows={2} />
          <TextField fullWidth label="Full Description" placeholder="Tell the full story. Paint a picture. Make them feel it." sx={{ mb: 2 }}
            value={newListing.description_md} onChange={(e) => setNewListing(p => ({ ...p, description_md: e.target.value }))} multiline rows={4} />
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>City</InputLabel>
                <Select value={newListing.city} label="City" onChange={(e) => setNewListing(p => ({ ...p, city: e.target.value }))}>
                  {CITIES.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Price (CNY)" type="number" value={newListing.price_amount}
                onChange={(e) => setNewListing(p => ({ ...p, price_amount: Number(e.target.value) }))} />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Duration</InputLabel>
                <Select value={newListing.price_unit} label="Duration" onChange={(e) => setNewListing(p => ({ ...p, price_unit: e.target.value }))}>
                  <MenuItem value="per_hour">Per Hour</MenuItem>
                  <MenuItem value="per_half_day">Per Half Day</MenuItem>
                  <MenuItem value="per_day">Per Full Day</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <TextField fullWidth label="Languages" placeholder="en, zh" value={newListing.languages}
                onChange={(e) => setNewListing(p => ({ ...p, languages: e.target.value }))} />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Cover Image URL (optional)" placeholder="https://..." value={newListing.cover_image_url}
                onChange={(e) => setNewListing(p => ({ ...p, cover_image_url: e.target.value }))} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewListingOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={createListing}
            sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>Publish Listing</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
