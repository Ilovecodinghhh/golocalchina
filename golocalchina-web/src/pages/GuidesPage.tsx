import { useState, useEffect } from 'react';
import { Container, Typography, Grid, Box, Alert } from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchFilters from '../components/SearchFilters';
import GuideCard from '../components/GuideCard';
import AdBanner from '../components/AdBanner';
import api from '../services/api';
import type { SearchParams } from '../services/api';

// Mock data as fallback — shown alongside real listings
const MOCK_GUIDES = [
  {
    user_id: 'mock-1', display_name: 'Li Wei', is_certified: true,
    languages: ['en', 'zh'], service_cities: ['Beijing'],
    specialties: ['history', 'food'], rating_avg: 4.8, rating_count: 127,
    default_rate_cny: 800, avatar_url: null,
    bio: 'Born and raised in Beijing. 15 years guiding foreign visitors.',
    featured_trip: {
      title: 'Hidden Hutongs & Imperial Secrets — Half Day',
      highlight: "I'll take you through alleys that haven't changed in 600 years. We'll drink tea in a courtyard home and eat the best jianbing in Dongcheng.",
      cover_url: 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600&q=80',
    },
  },
  {
    user_id: 'mock-2', display_name: 'Zhang Mei', is_certified: true,
    languages: ['en', 'zh', 'ja'], service_cities: ['Shanghai'],
    specialties: ['art', 'photography'], rating_avg: 4.9, rating_count: 89,
    default_rate_cny: 1000, avatar_url: null,
    bio: 'Shanghai native and photographer.',
    featured_trip: {
      title: 'Shanghai Through the Lens — Full Day Photo Walk',
      highlight: "From the neon of Nanjing Road to the quiet lanes of the French Concession. You'll leave with photos that make your friends jealous.",
      cover_url: 'https://images.unsplash.com/photo-1573455494060-c5595004fb6c?w=600&q=80',
    },
  },
  {
    user_id: 'mock-3', display_name: 'Wang Jun', is_certified: true,
    languages: ['en', 'zh', 'ko'], service_cities: ['Xian'],
    specialties: ['history', 'nature'], rating_avg: 4.7, rating_count: 203,
    default_rate_cny: 600, avatar_url: null,
    bio: 'History professor turned guide.',
    featured_trip: {
      title: "Terracotta Warriors — The Story They Won't Tell You",
      highlight: "I spent 20 years researching the warriors. I'll tell you who these soldiers were, why they were built, and the murder mystery behind the emperor's tomb.",
      cover_url: 'https://images.unsplash.com/photo-1591017403286-fd8493524e1e?w=600&q=80',
    },
  },
  {
    user_id: 'mock-4', display_name: 'Chen Xiao', is_certified: false,
    languages: ['en', 'zh', 'fr'], service_cities: ['Chengdu'],
    specialties: ['food', 'nature'], rating_avg: 4.6, rating_count: 156,
    default_rate_cny: 700, avatar_url: null,
    bio: 'Sichuan food expert and panda lover.',
    featured_trip: {
      title: 'Pandas, Hot Pot & Sichuan Spice — Full Day',
      highlight: "Morning with the giant pandas, afternoon cooking mapo tofu with my grandmother, evening at the most authentic hot pot in Chengdu.",
      cover_url: 'https://images.unsplash.com/photo-1598887142487-3c854d51eabb?w=600&q=80',
    },
  },
];

export default function GuidesPage() {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [allGuides, setAllGuides] = useState<any[]>([]);
  const [filtered, setFiltered] = useState<any[]>([]);

  const [filters, setFilters] = useState<SearchParams>({
    city: searchParams.get('city') || undefined,
    language: searchParams.get('language') || undefined,
    page: 1, per_page: 20,
  });

  // Load real listings from API + merge with mock data
  useEffect(() => {
    const load = async () => {
      let realGuides: any[] = [];
      try {
        const res = await api.get('/explore/listings');
        const listings = res.data.listings || [];
        // Convert API listings to guide card format
        realGuides = listings.map((l: any) => ({
          user_id: l.guide.user_id,
          display_name: l.guide.display_name,
          is_certified: l.guide.is_certified,
          languages: l.guide.languages || l.languages || [],
          service_cities: l.city ? [l.city] : l.guide.service_cities || [],
          specialties: l.guide.specialties || [],
          rating_avg: l.guide.rating_avg || 0,
          rating_count: l.guide.rating_count || 0,
          default_rate_cny: l.price_amount || l.guide.default_rate_cny || 0,
          avatar_url: l.guide.avatar_url,
          bio: l.guide.bio,
          featured_trip: {
            title: l.title,
            highlight: l.summary,
            cover_url: l.cover_image_url || 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600&q=80',
          },
        }));
      } catch (err) {
        console.log('API not available, using mock data only');
      }

      // Merge: real guides first, then mock guides (deduplicate by display_name)
      const realNames = new Set(realGuides.map((g: any) => g.display_name));
      const mockFiltered = MOCK_GUIDES.filter(g => !realNames.has(g.display_name));
      setAllGuides([...realGuides, ...mockFiltered]);
    };
    load();
  }, []);

  // Filter whenever allGuides or filters change
  useEffect(() => {
    let results = [...allGuides];
    if (filters.city) results = results.filter(g => g.service_cities.some((c: string) => c.toLowerCase().includes(filters.city!.toLowerCase())));
    if (filters.language) results = results.filter(g => g.languages.includes(filters.language!));
    setFiltered(results);
  }, [allGuides, filters]);

  const doSearch = () => {
    const params: Record<string, string> = {};
    if (filters.city) params.city = filters.city;
    if (filters.language) params.language = filters.language;
    setSearchParams(params);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 800, mb: 1 }}>{t('search.title')}</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Every guide writes their own story. Browse their trips and find the one that speaks to you.
      </Typography>

      <SearchFilters filters={filters} onChange={setFilters} onSearch={doSearch} />

      {filtered.length > 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {t('search.results', { count: filtered.length })}
        </Typography>
      )}

      {filtered.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>{t('search.no_results')}</Alert>
      )}

      <Grid container spacing={3}>
        {filtered.map((guide, idx) => (
          <Grid item xs={12} sm={6} md={4} key={guide.user_id + '-' + idx}>
            <GuideCard guide={guide} />
          </Grid>
        ))}
      </Grid>

      <AdBanner slot="bottom" />
    </Container>
  );
}
