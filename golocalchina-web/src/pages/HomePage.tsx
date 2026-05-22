import { Box, Container, Typography, Button, Grid, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchIcon from '@mui/icons-material/Search';
import VerifiedIcon from '@mui/icons-material/Verified';
import TranslateIcon from '@mui/icons-material/Translate';
import PaymentIcon from '@mui/icons-material/Payment';

export default function HomePage() {
  const { t } = useTranslation();

  const features = [
    { icon: <VerifiedIcon sx={{ fontSize: 48 }} />, title: 'Verified Guides', desc: 'Every guide holds a valid 导游证 (Tour Guide License) verified by us.' },
    { icon: <TranslateIcon sx={{ fontSize: 48 }} />, title: 'Auto-Translation', desc: 'Chat with your guide in your language — messages are translated in real time.' },
    { icon: <PaymentIcon sx={{ fontSize: 48 }} />, title: 'Free to Connect', desc: 'No platform fees. Pay your guide directly — cash, Alipay, or WeChat Pay.' },
  ];

  const cities = [
    { name: 'Beijing', emoji: '🏛️', desc: 'Great Wall, Forbidden City, Hutongs' },
    { name: 'Shanghai', emoji: '🌃', desc: 'The Bund, French Concession, Street Food' },
    { name: "Xi'an", emoji: '⚔️', desc: 'Terracotta Warriors, City Wall, Muslim Quarter' },
    { name: 'Chengdu', emoji: '🐼', desc: 'Giant Pandas, Sichuan Cuisine, Tea Houses' },
  ];

  return (
    <Box>
      {/* Hero */}
      <Box sx={{
        bgcolor: '#1a472a', color: 'white', py: 12, textAlign: 'center',
        background: 'linear-gradient(135deg, #1a472a 0%, #2d6a4f 100%)'
      }}>
        <Container maxWidth="md">
          <Typography variant="h2" sx={{ fontWeight: 800, mb: 2 }}>
            🌏 {t('app.name')}
          </Typography>
          <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
            {t('app.tagline')}
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<SearchIcon />}
            component={Link}
            to="/guides"
            sx={{ bgcolor: '#d4a843', color: '#1a472a', fontWeight: 700, px: 5, py: 1.5, fontSize: '1.1rem',
                  '&:hover': { bgcolor: '#c49a38' } }}
          >
            {t('nav.guides')}
          </Button>
        </Container>
      </Box>

      {/* Cities */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h4" align="center" sx={{ fontWeight: 700, mb: 4 }}>
          Explore China with a Local
        </Typography>
        <Grid container spacing={3}>
          {cities.map((city) => (
            <Grid item xs={12} sm={6} md={3} key={city.name}>
              <Paper
                component={Link}
                to={`/guides?city=${city.name}`}
                sx={{
                  p: 3, textAlign: 'center', textDecoration: 'none', color: 'inherit',
                  '&:hover': { boxShadow: 6, transform: 'translateY(-4px)' },
                  transition: 'all 0.2s',
                }}
              >
                <Typography variant="h2" sx={{ mb: 1 }}>{city.emoji}</Typography>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>{city.name}</Typography>
                <Typography variant="body2" color="text.secondary">{city.desc}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features */}
      <Box sx={{ bgcolor: '#f5f5f0', py: 8 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {features.map((f, i) => (
              <Grid item xs={12} md={4} key={i}>
                <Box sx={{ textAlign: 'center' }}>
                  <Box sx={{ color: '#1a472a', mb: 2 }}>{f.icon}</Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>{f.title}</Typography>
                  <Typography variant="body2" color="text.secondary">{f.desc}</Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Platform Notice (Path B compliance) */}
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Typography variant="caption" color="text.secondary" align="center" display="block">
          {t('app.platform_notice')}
        </Typography>
      </Container>
    </Box>
  );
}
