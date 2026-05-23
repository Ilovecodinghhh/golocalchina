import { useState, useEffect } from 'react';
import { Container, Typography, Grid, Box, Pagination, Alert } from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchFilters from '../components/SearchFilters';
import GuideCard from '../components/GuideCard';
import AdBanner from '../components/AdBanner';
import type { Guide, SearchParams } from '../services/api';

// Mock data for development (replace with guideApi.search() when backend is running)
const MOCK_GUIDES: (Guide & { is_certified: boolean })[] = [
  {
    user_id: '1', display_name: 'Li Wei', is_certified: true, languages: ['en', 'zh'], service_cities: ['Beijing'],
    specialties: ['history', 'food'], rating_avg: 4.8, rating_count: 127,
    default_rate_cny: 800, avatar_url: null, bio: 'Born and raised in Beijing. 15 years guiding foreign visitors through hutongs, temples, and hidden restaurants.',
  },
  {
    user_id: '2', display_name: 'Zhang Mei', is_certified: true, languages: ['en', 'zh', 'ja'], service_cities: ['Shanghai'],
    specialties: ['art', 'photography'], rating_avg: 4.9, rating_count: 89,
    default_rate_cny: 1000, avatar_url: null, bio: 'Shanghai native and professional photographer. I show you the city through a camera lens.',
  },
  {
    user_id: '3', display_name: 'Wang Jun', is_certified: true, languages: ['en', 'zh', 'ko'], service_cities: ['Xian'],
    specialties: ['history', 'nature'], rating_avg: 4.7, rating_count: 203,
    default_rate_cny: 600, avatar_url: null, bio: 'History professor turned guide. Terracotta Warriors specialist with 20 years of research experience.',
  },
  {
    user_id: '4', display_name: 'Chen Xiao', is_certified: false, languages: ['en', 'zh', 'fr'], service_cities: ['Chengdu'],
    specialties: ['food', 'nature', 'family'], rating_avg: 4.6, rating_count: 156,
    default_rate_cny: 700, avatar_url: null, bio: 'Sichuan food expert and panda enthusiast. Family-friendly tours with lots of spicy snacks!',
  },
  {
    user_id: '5', display_name: 'Liu Fang', is_certified: false, languages: ['en', 'zh', 'de'], service_cities: ['Beijing'],
    specialties: ['nightlife', 'shopping', 'food'], rating_avg: 4.5, rating_count: 94,
    default_rate_cny: 900, avatar_url: null, bio: 'Discover Beijing after dark. Best bars, night markets, and late-night eats.',
  },
  {
    user_id: '6', display_name: 'Zhao Min', is_certified: true, languages: ['en', 'zh', 'es'], service_cities: ['Shanghai'],
    specialties: ['history', 'art'], rating_avg: 4.8, rating_count: 68,
    default_rate_cny: 850, avatar_url: null, bio: 'From the French Concession to Pudong — I cover 150 years of Shanghai history.',
  },
];

export default function GuidesPage() {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [guides, setGuides] = useState<Guide[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const [filters, setFilters] = useState<SearchParams>({
    city: searchParams.get('city') || undefined,
    language: searchParams.get('language') || undefined,
    specialty: searchParams.get('specialty') || undefined,
    page: 1,
    per_page: 20,
  });

  const doSearch = () => {
    setLoading(true);
    // Filter mock data locally (replace with API call in production)
    let results = [...MOCK_GUIDES];
    if (filters.city) results = results.filter(g => g.service_cities.includes(filters.city!));
    if (filters.language) results = results.filter(g => g.languages.includes(filters.language!));
    if (filters.specialty) results = results.filter(g => g.specialties.includes(filters.specialty!));

    setGuides(results);
    setTotal(results.length);
    setLoading(false);

    // Update URL params
    const params: Record<string, string> = {};
    if (filters.city) params.city = filters.city;
    if (filters.language) params.language = filters.language;
    if (filters.specialty) params.specialty = filters.specialty;
    setSearchParams(params);
  };

  useEffect(() => { doSearch(); }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 3 }}>
        {t('search.title')}
      </Typography>

      <SearchFilters filters={filters} onChange={setFilters} onSearch={doSearch} />

      <AdBanner slot="top" />

      {total > 0 && (
        <Typography variant="body1" sx={{ mb: 2 }}>
          {t('search.results', { count: total })}
        </Typography>
      )}

      {!loading && guides.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>{t('search.no_results')}</Alert>
      )}

      <Grid container spacing={3}>
        {guides.map((guide) => (
          <Grid item xs={12} sm={6} md={4} key={guide.user_id}>
            <GuideCard guide={guide} />
          </Grid>
        ))}
      </Grid>

      {total > 20 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination count={Math.ceil(total / 20)} color="primary" />
        </Box>
      )}
      <AdBanner slot="bottom" />
    </Container>
  );
}
