import { Box, Container, Typography, Button, Grid, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import HandshakeIcon from '@mui/icons-material/Handshake';
import ExploreIcon from '@mui/icons-material/Explore';

// User-uploaded China scenic photos
const HERO_IMAGES = [
  '/images/hanson-lu-Q36BvLGdOAg-unsplash.jpg',
  '/images/sergio-kian-JLJ3H21VDXU-unsplash.jpg',
  '/images/texco-kwok-aPV-DzCvgX4-unsplash.jpg',
  '/images/wang-xiaoqi-4UficfJjTcc-unsplash.jpg',
  '/images/yiran-ding-g-Z4_2nnXcc-unsplash.jpg',
  '/images/pascal-muller-4EajIuUxgAQ-unsplash.jpg',  // Panda
];

const CITY_IMAGES: Record<string, { img: string; emoji: string; desc: string }> = {
  Beijing: {
    img: '/images/Beijing.jpg',  // Forbidden City / Temple of Heaven
    emoji: '🏛️', desc: 'Great Wall · Forbidden City · Hutongs',
  },
  Shanghai: {
    img: '/images/Shanghai.jpg',  // Shanghai skyline
    emoji: '🌃', desc: 'The Bund · French Concession · Street Food',
  },
  "Xi'an": {
    img: '/images/Xian.jpg',  // Xi'an ancient wall
    emoji: '⚔️', desc: 'Terracotta Warriors · City Wall · Muslim Quarter',
  },
  Chengdu: {
    img: '/images/Chengdu.jpg',  // Chinese traditional architecture
    emoji: '🐼', desc: 'Giant Pandas · Sichuan Cuisine · Tea Houses',
  },
  Guilin: {
    img: '/images/Guilin.jpg',     // Karst mountains
    emoji: '🏔️', desc: 'Li River · Karst Mountains · Rice Terraces',
  },
  Hangzhou: {
    img: '/images/Hangzhou.jpg',     // Traditional Chinese architecture
    emoji: '🍵', desc: 'West Lake · Dragon Well Tea · Silk Market',
  },
};

export default function HomePage() {
  const { t } = useTranslation();
  const [heroIdx, setHeroIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setHeroIdx((i) => (i + 1) % HERO_IMAGES.length), 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <Box>
      {/* Hero */}
      <Box sx={{ position: 'relative', height: { xs: '80vh', md: '90vh' }, overflow: 'hidden' }}>
        {HERO_IMAGES.map((img, idx) => (
          <Box key={img} sx={{
            position: 'absolute', inset: 0,
            backgroundImage: `url(${img})`, backgroundSize: 'cover', backgroundPosition: 'center',
            opacity: idx === heroIdx ? 1 : 0, transition: 'opacity 1.5s ease-in-out',
          }} />
        ))}
        <Box sx={{ position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 100%)' }} />
        <Container maxWidth="md" sx={{ position: 'relative', zIndex: 1, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', textAlign: 'center' }}>
          <Typography variant="h2" sx={{ color: 'white', fontWeight: 800, mb: 2, fontSize: { xs: '2rem', md: '3.5rem' }, textShadow: '2px 2px 8px rgba(0,0,0,0.5)' }}>
            {t('app.tagline')}
          </Typography>
          <Typography variant="h6" sx={{ color: 'rgba(255,255,255,0.9)', mb: 4, maxWidth: 600, mx: 'auto', lineHeight: 1.6 }}>
            {t('app.subtitle')}
          </Typography>
          <Box>
            <Button variant="contained" size="large" startIcon={<SearchIcon />} component={Link} to="/guides"
              sx={{ bgcolor: '#DC2626', color: 'white', fontWeight: 700, px: 5, py: 1.5, fontSize: '1.1rem', borderRadius: 3,
                    '&:hover': { bgcolor: '#B91C1C', transform: 'scale(1.05)' }, transition: 'all 0.2s', boxShadow: '0 4px 20px rgba(220,38,38,0.4)' }}>
              {t('nav.guides')}
            </Button>
          </Box>
          <Box sx={{ position: 'absolute', bottom: 30, left: '50%', transform: 'translateX(-50%)' }}>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.6)', letterSpacing: 2 }}>SCROLL TO EXPLORE ↓</Typography>
          </Box>
        </Container>
        <Box sx={{ position: 'absolute', bottom: 60, left: '50%', transform: 'translateX(-50%)', display: 'flex', gap: 1 }}>
          {HERO_IMAGES.map((_, idx) => (
            <Box key={idx} onClick={() => setHeroIdx(idx)} sx={{
              width: idx === heroIdx ? 24 : 8, height: 8, borderRadius: 4,
              bgcolor: idx === heroIdx ? '#DC2626' : 'rgba(255,255,255,0.5)', cursor: 'pointer', transition: 'all 0.3s',
            }} />
          ))}
        </Box>
      </Box>

      {/* Cities */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h4" align="center" sx={{ fontWeight: 800, mb: 1 }}>Explore China with a Local</Typography>
        <Typography variant="body1" align="center" color="text.secondary" sx={{ mb: 5, maxWidth: 500, mx: 'auto' }}>
          From ancient capitals to modern megacities — find a guide who calls it home.
        </Typography>
        <Grid container spacing={3}>
          {Object.entries(CITY_IMAGES).map(([city, data]) => (
            <Grid item xs={6} md={4} key={city}>
              <Paper component={Link} to={`/guides?city=${city}`} sx={{
                position: 'relative', height: { xs: 200, md: 260 }, borderRadius: 3, overflow: 'hidden', textDecoration: 'none', display: 'block',
                '&:hover img': { transform: 'scale(1.1)' },
                '&:hover .overlay': { background: 'linear-gradient(to top, rgba(220,38,38,0.8) 0%, rgba(0,0,0,0.2) 100%)' },
              }}>
                <Box component="img" src={data.img} alt={city} sx={{ width: '100%', height: '100%', objectFit: 'cover', transition: 'transform 0.5s' }} />
                <Box className="overlay" sx={{
                  position: 'absolute', inset: 0,
                  background: 'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.1) 100%)',
                  transition: 'background 0.3s', display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', p: 2,
                }}>
                  <Typography variant="h5" sx={{ color: 'white', fontWeight: 700 }}>{data.emoji} {city}</Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>{data.desc}</Typography>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* How it works */}
      <Box sx={{ bgcolor: '#FEF2F2', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" align="center" sx={{ fontWeight: 800, mb: 5 }}>How It Works</Typography>
          <Grid container spacing={4}>
            {[
              { icon: <SearchIcon sx={{ fontSize: 40 }} />, num: '01', title: 'Browse & Choose', desc: 'Search guides by city and language. Read real reviews. Certified guides have verified licenses.' },
              { icon: <HandshakeIcon sx={{ fontSize: 40 }} />, num: '02', title: 'Connect & Plan', desc: 'Send a connection request. Chat with your guide to plan the perfect day — hidden gems, best food, local stories.' },
              { icon: <ExploreIcon sx={{ fontSize: 40 }} />, num: '03', title: 'Meet & Explore', desc: 'Meet in person. Pay directly — cash, Alipay, or WeChat Pay. No middleman, no fees. Just you and a local.' },
            ].map((step, i) => (
              <Grid item xs={12} md={4} key={i}>
                <Box sx={{ textAlign: 'center', px: 2 }}>
                  <Typography variant="h1" sx={{ fontWeight: 900, color: '#DC2626', opacity: 0.15, fontSize: 80, lineHeight: 1 }}>{step.num}</Typography>
                  <Box sx={{ color: '#DC2626', mt: -3, mb: 2 }}>{step.icon}</Box>
                  <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>{step.title}</Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>{step.desc}</Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Stats bar */}
      <Box sx={{ bgcolor: '#DC2626', color: 'white', py: 6 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} justifyContent="center">
            {[{ num: '6', label: 'Cities' }, { num: 'Free', label: 'No Platform Fees' }, { num: '100%', label: 'Direct to Guide' }, { num: '✓', label: 'License Verified' }].map((stat, i) => (
              <Grid item xs={6} md={3} key={i} sx={{ textAlign: 'center' }}>
                <Typography variant="h3" sx={{ fontWeight: 800 }}>{stat.num}</Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>{stat.label}</Typography>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA */}
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <Container maxWidth="sm">
          <Typography variant="h4" sx={{ fontWeight: 800, mb: 2 }}>Ready to Discover the Real China?</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>No sign-up required to browse. Find your guide in minutes.</Typography>
          <Button variant="contained" size="large" component={Link} to="/guides"
            sx={{ bgcolor: '#DC2626', px: 5, py: 1.5, fontSize: '1.1rem', borderRadius: 3, '&:hover': { bgcolor: '#B91C1C' } }}>
            Find a Guide →
          </Button>
        </Container>
      </Box>

      <Box sx={{ bgcolor: '#f5f5f0', py: 3 }}>
        <Container maxWidth="md">
          <Typography variant="caption" color="text.secondary" align="center" display="block">{t('app.platform_notice')}</Typography>
        </Container>
      </Box>
    </Box>
  );
}
