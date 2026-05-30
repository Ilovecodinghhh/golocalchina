import { Container, Typography, Box, Grid, Paper, Button, Divider } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchIcon from '@mui/icons-material/Search';
import ChatIcon from '@mui/icons-material/Chat';
import ExploreIcon from '@mui/icons-material/Explore';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import MoneyOffIcon from '@mui/icons-material/MoneyOff';
import SecurityIcon from '@mui/icons-material/Security';
import EditNoteIcon from '@mui/icons-material/EditNote';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import HandshakeIcon from '@mui/icons-material/Handshake';

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

      {/* For Travelers */}
      <Container maxWidth="md" sx={{ py: 8 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 1, color: '#DC2626' }}>For Travelers</Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 5 }}>
          Find a local guide, connect with fellow travelers, and explore China your way.
        </Typography>
        {[
          {
            icon: <SearchIcon sx={{ fontSize: 48 }} />, num: '1',
            title: 'Find Your Guide at /guides',
            desc: 'Browse verified local guides by city, language, and specialty. Every guide sets their own price and designs their own trip.',
            details: [
              'Filter by city: Beijing, Shanghai, Xi\'an, Chengdu, Guilin, Hangzhou',
              'Filter by language: English, Chinese, Japanese, Korean, French, and more',
              'Filter by specialty: History, Food, Nature, Photography, Nightlife',
              'Read guide profiles — see their bio, specialties, and pricing upfront',
              'Certified guides display a verified badge — their 导游证 has been checked',
            ],
          },
          {
            icon: <EditNoteIcon sx={{ fontSize: 48 }} />, num: '2',
            title: 'Share & Connect at /posts',
            desc: 'The community board is where travelers meet travelers. Post your stories, ask questions, and plan together.',
            details: [
              'Share your travel experiences and photos with the community',
              'Ask questions before your trip — get answers from people who\'ve been there',
              'Exchange tips on routes, restaurants, and hidden gems',
              'Like and engage with posts from fellow travelers',
              'Build your itinerary with real local insights from the community',
            ],
          },
          {
            icon: <ExploreIcon sx={{ fontSize: 48 }} />, num: '3',
            title: 'Explore & Pay Direct',
            desc: 'Meet your guide in person and enjoy an authentic local experience. No middleman, no platform fees.',
            details: [
              'Send a free connection request to any guide',
              'Discuss your interests, schedule, and meeting point directly',
              'Meet your guide at the agreed location',
              'Pay your guide directly — Cash (CNY/USD), Alipay, or WeChat Pay',
              'Leave a review to help future travelers find great guides',
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

      {/* For Guides */}
      <Box sx={{ bgcolor: '#FEF2F2', py: 8 }}>
        <Container maxWidth="md">
          <Typography variant="h4" sx={{ fontWeight: 800, mb: 1, color: '#DC2626' }}>For Guides</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 5 }}>
            Design trips your way. Set your own price, schedule, and style. Keep 100% of what you earn.
          </Typography>
          {[
            {
              icon: <LightbulbIcon sx={{ fontSize: 48 }} />, num: '1',
              title: 'Design Your Trip',
              desc: 'Create listings that showcase your unique perspective as a local. The best trips are the ones no guidebook can offer.',
              details: [
                'Focus on hidden gems only locals know — a family recipe, a quiet temple at dawn',
                'Tell a story: what makes YOUR version of this city different from anyone else\'s?',
                'Write a compelling summary — this is what travelers see first on the card',
                'Include specific details: meeting points, duration, what\'s included, group size',
                'Use high-quality photos that show the real experience, not stock images',
              ],
            },
            {
              icon: <AttachMoneyIcon sx={{ fontSize: 48 }} />, num: '2',
              title: 'Set Your Price',
              desc: 'You decide your rate, schedule, and group size. No commission is taken — travelers pay you directly.',
              details: [
                'Choose your pricing: per hour, per half day, or per full day',
                'Set a fair price that reflects your expertise and the value you provide',
                'Specify your accepted payment methods: Cash, Alipay, WeChat Pay',
                'You can update your listings and pricing anytime',
                'Travelers see your price upfront — no surprises, no haggling',
              ],
            },
            {
              icon: <HandshakeIcon sx={{ fontSize: 48 }} />, num: '3',
              title: 'Connect & Deliver',
              desc: 'Respond to requests, plan the details with your guest, and deliver an unforgettable experience.',
              details: [
                'Respond to connection requests promptly — travelers appreciate quick replies',
                'Discuss interests and preferences before the trip to personalize the experience',
                'Be flexible: adapt the itinerary to weather, energy levels, and spontaneous discoveries',
                'Great experiences lead to great reviews — and more travelers finding you',
                'Build your reputation: certified guides with good reviews get more bookings',
              ],
            },
          ].map((step, i) => (
            <Box key={i} sx={{ mb: 6 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 2 }}>
                <Box sx={{
                  width: 72, height: 72, borderRadius: '50%', bgcolor: 'white',
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
      </Box>

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
