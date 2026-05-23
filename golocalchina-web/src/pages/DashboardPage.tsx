import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Typography, Box, Paper, Button, Grid, Avatar, Chip,
  TextField, Alert, Tabs, Tab, Divider
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import LogoutIcon from '@mui/icons-material/Logout';
import HistoryIcon from '@mui/icons-material/History';
import AddIcon from '@mui/icons-material/Add';
import { useTranslation } from 'react-i18next';

interface UserInfo {
  id: string;
  role: string;
  email?: string;
  display_name?: string;
}

export default function DashboardPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [user, setUser] = useState<UserInfo | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    const stored = localStorage.getItem('glc_user');
    if (!stored) { navigate('/login'); return; }
    setUser(JSON.parse(stored));
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('glc_token');
    localStorage.removeItem('glc_user');
    navigate('/');
  };

  if (!user) return null;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Paper sx={{ p: 4, mb: 4, borderRadius: 3, background: 'linear-gradient(135deg, #DC2626 0%, #991B1B 100%)', color: 'white' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <Avatar sx={{ width: 80, height: 80, bgcolor: 'rgba(255,255,255,0.2)', fontSize: 32, fontWeight: 700 }}>
            {(user.display_name || user.email || 'U').charAt(0).toUpperCase()}
          </Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              {user.display_name || user.email || 'User'}
            </Typography>
            <Chip
              label={user.role === 'guide' ? '🧭 Local Guide' : '🌍 Tourist'}
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', mt: 1, fontWeight: 600 }}
            />
          </Box>
          <Button startIcon={<LogoutIcon />} onClick={handleLogout}
            sx={{ color: 'white', border: '1px solid rgba(255,255,255,0.3)', '&:hover': { bgcolor: 'rgba(255,255,255,0.1)' } }}>
            Log Out
          </Button>
        </Box>
      </Paper>

      {/* Tabs */}
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3, '& .Mui-selected': { color: '#DC2626' }, '& .MuiTabs-indicator': { bgcolor: '#DC2626' } }}>
        {user.role === 'guide' ? (
          [<Tab key={0} label="My Listings" />, <Tab key={1} label="Requests" />, <Tab key={2} label="Profile" />]
        ) : (
          [<Tab key={0} label="My Requests" />, <Tab key={1} label="Saved Guides" />, <Tab key={2} label="Profile" />]
        )}
      </Tabs>

      {/* Guide Dashboard */}
      {user.role === 'guide' && tab === 0 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>Your Service Listings</Typography>
            <Button variant="contained" startIcon={<AddIcon />}
              sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>
              Create New Listing
            </Button>
          </Box>
          <Alert severity="info">
            You haven't created any listings yet. Click "Create New Listing" to start offering your guide services to travelers from around the world.
          </Alert>
        </Box>
      )}
      {user.role === 'guide' && tab === 1 && (
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>Connection Requests</Typography>
          <Alert severity="info">No requests yet. Once tourists find your listings, their requests will appear here.</Alert>
        </Box>
      )}

      {/* Tourist Dashboard */}
      {user.role === 'tourist' && tab === 0 && (
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>Your Connection Requests</Typography>
          <Alert severity="info" action={
            <Button color="inherit" size="small" onClick={() => navigate('/guides')}>Browse Guides</Button>
          }>
            You haven't sent any requests yet. Find a guide and start planning your trip!
          </Alert>
        </Box>
      )}
      {user.role === 'tourist' && tab === 1 && (
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>Saved Guides</Typography>
          <Alert severity="info">You haven't saved any guides yet. Browse guides and click the heart icon to save them.</Alert>
        </Box>
      )}

      {/* Profile tab — shared */}
      {((user.role === 'guide' && tab === 2) || (user.role === 'tourist' && tab === 2)) && (
        <Paper sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>Edit Profile</Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Display Name" defaultValue={user.display_name || ''} />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField fullWidth label="Email" defaultValue={user.email || ''} disabled />
            </Grid>
            {user.role === 'guide' && (
              <>
                <Grid item xs={12}>
                  <TextField fullWidth label="Bio — Tell travelers about yourself" multiline rows={4}
                    placeholder="Share your story, your passion for your city, and what makes your tours special..." />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Languages (comma separated)" placeholder="English, Chinese, French" />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="City" placeholder="Beijing" />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="Alipay QR Code URL" placeholder="Upload link to your Alipay QR" />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField fullWidth label="WeChat Pay QR Code URL" placeholder="Upload link to your WeChat QR" />
                </Grid>
              </>
            )}
            <Grid item xs={12}>
              <Button variant="contained" sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>
                Save Changes
              </Button>
            </Grid>
          </Grid>
        </Paper>
      )}
    </Container>
  );
}
