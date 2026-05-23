import { Container, Typography, Box, Grid, Paper, Button, Divider } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchIcon from '@mui/icons-material/Search';
import ChatIcon from '@mui/icons-material/Chat';
import ExploreIcon from '@mui/icons-material/Explore';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import MoneyOffIcon from '@mui/icons-material/MoneyOff';
import SecurityIcon from '@mui/icons-material/Security';

export default function HowItWorksPage() {
  const { t } = useTranslation();

  return (
    <Box>
      {/* Header */}
      <Box sx={{ bgcolor: '#DC2626', color: 'white', py: 8, textAlign: 'center' }}>
        <Container maxWidth="md">
          <Typography variant="h3" sx={{ fontWeight: 800, mb: 2 }}>
            {t('how.title')}
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.9 }}>
            {t('how.subtitle')}
          </Typography>
        </Container>
      </Box>

      {/* 3 Steps — detailed */}
      <Container maxWidth="md" sx={{ py: 8 }}>
        {[
          {
            icon: <SearchIcon sx={{ fontSize: 48 }} />, num: '1',
            title: t('how.step1_title'), desc: t('how.step1_desc'),
            details: [
              'Filter by city: Beijing, Shanghai, Xi\'an, Chengdu, Guilin, Hangzhou',
              'Filter by language: English, Chinese, Japanese, Korean, French, and more',
              'Filter by specialty: History, Food, Nature, Photography, Nightlife',
              'Read reviews from real travelers who have used the guide',
              'Certified guides display a verified badge — their tour guide license (导游证) has been checked',
            ],
          },
          {
            icon: <ChatIcon sx={{ fontSize: 48 }} />, num: '2',
            title: t('how.step2_title'), desc: t('how.step2_desc'),
            details: [
              'Send a free connection request to any guide',
              'The guide accepts or declines — it\'s their choice',
              'Chat to discuss what you want to see and do',
              'The guide suggests a plan based on your interests',
              'Agree on meeting time, place, and price',
            ],
          },
          {
            icon: <ExploreIcon sx={{ fontSize: 48 }} />, num: '3',
            title: t('how.step3_title'), desc: t('how.step3_desc'),
            details: [
              'Meet your guide at the agreed location',
              'Enjoy an authentic local experience',
              'Pay your guide directly — no platform fees whatsoever',
              'Accepted: Cash (CNY or USD), Alipay, WeChat Pay',
              'Leave a review to help future travelers',
            ],
          },
        ].map((step, i) => (
          <Box key={i} sx={{ mb: 6 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 2 }}>
              <Box sx={{
                width: 72, height: 72, borderRadius: '50%', bgcolor: '#FEF2F2',
                display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#DC2626',
                flexShrink: 0,
              }}>
                {step.icon}
              </Box>
              <Box>
                <Typography variant="overline" sx={{ color: '#DC2626', fontWeight: 700 }}>Step {step.num}</Typography>
                <Typography variant="h5" sx={{ fontWeight: 700 }}>{step.title}</Typography>
              </Box>
            </Box>
            <Typography variant="body1" sx={{ mb: 2, ml: { md: '104px' } }}>{step.desc}</Typography>
            <Box sx={{ ml: { md: '104px' } }}>
              {step.details.map((d, j) => (
                <Typography key={j} variant="body2" color="text.secondary" sx={{ mb: 0.5, pl: 2, borderLeft: '2px solid #DC2626' }}>
                  {d}
                </Typography>
              ))}
            </Box>
            {i < 2 && <Divider sx={{ mt: 4 }} />}
          </Box>
        ))}
      </Container>

      {/* Why GoLocalChina */}
      <Box sx={{ bgcolor: '#FEF2F2', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" align="center" sx={{ fontWeight: 800, mb: 5 }}>Why GoLocalChina?</Typography>
          <Grid container spacing={4}>
            {[
              { icon: <MoneyOffIcon sx={{ fontSize: 40 }} />, title: 'Zero Fees', desc: 'We don\'t charge tourists or guides. No commissions, no hidden costs, no subscription.' },
              { icon: <VerifiedUserIcon sx={{ fontSize: 40 }} />, title: 'Verified Guides', desc: 'Certified guides have their official 导游证 (Tour Guide License) verified. Community guides are clearly labeled.' },
              { icon: <SecurityIcon sx={{ fontSize: 40 }} />, title: 'Direct & Transparent', desc: 'You deal directly with your guide. We just make the introduction. Prices are set by guides, visible upfront.' },
            ].map((item, i) => (
              <Grid item xs={12} md={4} key={i}>
                <Paper sx={{ p: 4, textAlign: 'center', height: '100%', borderRadius: 3 }}>
                  <Box sx={{ color: '#DC2626', mb: 2 }}>{item.icon}</Box>
                  <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>{item.title}</Typography>
                  <Typography variant="body2" color="text.secondary">{item.desc}</Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA */}
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 3 }}>
          Ready to Go Local?
        </Typography>
        <Button
          variant="contained" size="large" component={Link} to="/guides"
          sx={{ bgcolor: '#DC2626', px: 5, py: 1.5, fontSize: '1.1rem', borderRadius: 3,
                '&:hover': { bgcolor: '#B91C1C' } }}
        >
          {t('how.cta')}
        </Button>
      </Box>
    </Box>
  );
}
