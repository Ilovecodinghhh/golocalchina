import { useState, useEffect } from 'react';
import { Container, Typography, Grid, Box, Pagination, Alert } from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchFilters from '../components/SearchFilters';
import GuideCard from '../components/GuideCard';
import AdBanner from '../components/AdBanner';
import type { Guide, SearchParams } from '../services/api';

const MOCK_GUIDES = [
  {
    user_id: '1', display_name: 'Li Wei', is_certified: true,
    languages: ['en', 'zh'], service_cities: ['Beijing'],
    specialties: ['history', 'food'], rating_avg: 4.8, rating_count: 127,
    default_rate_cny: 800, avatar_url: null,
    bio: 'Born and raised in Beijing. 15 years guiding foreign visitors.',
    featured_trip: {
      title: 'Hidden Hutongs & Imperial Secrets — Half Day',
      highlight: 'I\'ll take you through alleys that haven\'t changed in 600 years. We\'ll drink tea in a courtyard home, eat jianbing from the best street vendor in Dongcheng, and I\'ll tell you the stories that guidebooks don\'t have.',
      cover_url: 'https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80',
    },
  },
  {
    user_id: '2', display_name: 'Zhang Mei', is_certified: true,
    languages: ['en', 'zh', 'ja'], service_cities: ['Shanghai'],
    specialties: ['art', 'photography'], rating_avg: 4.9, rating_count: 89,
    default_rate_cny: 1000, avatar_url: null,
    bio: 'Shanghai native and photographer.',
    featured_trip: {
      title: 'Shanghai Through the Lens — Full Day Photo Walk',
      highlight: 'From the neon of Nanjing Road to the quiet lanes of the French Concession. I know the light, the angles, and the moments. You\'ll leave with photos that make your friends jealous.',
      cover_url: 'https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600&q=80',
    },
  },
  {
    user_id: '3', display_name: 'Wang Jun', is_certified: true,
    languages: ['en', 'zh', 'ko'], service_cities: ['Xian'],
    specialties: ['history', 'nature'], rating_avg: 4.7, rating_count: 203,
    default_rate_cny: 600, avatar_url: null,
    bio: 'History professor turned guide.',
    featured_trip: {
      title: 'Terracotta Warriors — The Story They Won\'t Tell You',
      highlight: 'I spent 20 years researching the warriors. I\'ll show you the 3 pits, but more importantly, I\'ll tell you who these soldiers were, why they were built, and the murder mystery behind the emperor\'s tomb.',
      cover_url: 'https://images.unsplash.com/photo-1591017403286-fd8493524e1e?w=600&q=80',
    },
  },
  {
    user_id: '4', display_name: 'Chen Xiao', is_certified: false,
    languages: ['en', 'zh', 'fr'], service_cities: ['Chengdu'],
    specialties: ['food', 'nature', 'family'], rating_avg: 4.6, rating_count: 156,
    default_rate_cny: 700, avatar_url: null,
    bio: 'Sichuan food expert and panda lover.',
    featured_trip: {
      title: 'Pandas, Hot Pot & Sichuan Spice — Full Day',
      highlight: 'Morning with the giant pandas (I know the quiet paths), afternoon learning to cook mapo tofu with my grandmother, evening at the most authentic hot pot spot in Chengdu. Your taste buds will never be the same.',
      cover_url: 'https://images.unsplash.com/photo-1528164344705-47542687000d?w=600&q=80',
    },
  },
  {
    user_id: '5', display_name: 'Liu Fang', is_certified: false,
    languages: ['en', 'zh', 'de'], service_cities: ['Beijing'],
    specialties: ['nightlife', 'shopping', 'food'], rating_avg: 4.5, rating_count: 94,
    default_rate_cny: 900, avatar_url: null,
    bio: 'Beijing after dark specialist.',
    featured_trip: {
      title: 'Beijing After Midnight — Night Food & Bar Crawl',
      highlight: 'Forget the tourist restaurants. I\'ll take you to the lamb skewer alley at 11pm, the hidden speakeasy behind a bookshelf, and the 3am hand-pulled noodle shop where taxi drivers eat. This is my Beijing.',
      cover_url: 'https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=600&q=80',
    },
  },
  {
    user_id: '6', display_name: 'Zhao Min', is_certified: true,
    languages: ['en', 'zh', 'es'], service_cities: ['Shanghai'],
    specialties: ['history', 'art'], rating_avg: 4.8, rating_count: 68,
    default_rate_cny: 850, avatar_url: null,
    bio: '150 years of Shanghai history.',
    featured_trip: {
      title: 'From Opium Wars to Skyscrapers — Shanghai\'s Wild History',
      highlight: 'I\'ll walk you through 150 years in one day. The old Jewish quarter, the underground jazz scene of the 1930s, the revolutionary sites, and the architect who designed half of the Bund. History is never boring when I tell it.',
      cover_url: 'https://images.unsplash.com/photo-1567789884554-0b844b597180?w=600&q=80',
    },
  },
];

export default function GuidesPage() {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [guides, setGuides] = useState<typeof MOCK_GUIDES>([]);
  const [total, setTotal] = useState(0);

  const [filters, setFilters] = useState<SearchParams>({
    city: searchParams.get('city') || undefined,
    language: searchParams.get('language') || undefined,
    page: 1, per_page: 20,
  });

  const doSearch = () => {
    let results = [...MOCK_GUIDES];
    if (filters.city) results = results.filter(g => g.service_cities.includes(filters.city!));
    if (filters.language) results = results.filter(g => g.languages.includes(filters.language!));
    setGuides(results);
    setTotal(results.length);
    const params: Record<string, string> = {};
    if (filters.city) params.city = filters.city;
    if (filters.language) params.language = filters.language;
    setSearchParams(params);
  };

  useEffect(() => { doSearch(); }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 800, mb: 1 }}>{t('search.title')}</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Every guide writes their own story. Browse their trips and find the one that speaks to you.
      </Typography>

      <SearchFilters filters={filters} onChange={setFilters} onSearch={doSearch} />

      {total > 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {t('search.results', { count: total })}
        </Typography>
      )}

      {guides.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>{t('search.no_results')}</Alert>
      )}

      <Grid container spacing={3}>
        {guides.map((guide) => (
          <Grid item xs={12} sm={6} md={4} key={guide.user_id}>
            <GuideCard guide={guide as any} />
          </Grid>
        ))}
      </Grid>

      <AdBanner slot="bottom" />
    </Container>
  );
}
