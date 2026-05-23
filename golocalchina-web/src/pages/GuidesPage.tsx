import { useState, useEffect } from 'react';
import { Container, Typography, Grid, Box, Alert, CircularProgress } from '@mui/material';
import { useSearchParams, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import SearchFilters from '../components/SearchFilters';
import AdBanner from '../components/AdBanner';
import api from '../services/api';
import type { SearchParams } from '../services/api';
import GuideListingCard from '../components/GuideListingCard';

export default function GuidesPage() {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [listings, setListings] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const [filters, setFilters] = useState<SearchParams>({
    city: searchParams.get('city') || undefined,
    language: searchParams.get('language') || undefined,
  });

  const fetchListings = async () => {
    setLoading(true);
    try {
      let url = '/explore/listings?per_page=30';
      if (filters.city) url += '&city=' + filters.city;
      if (filters.language) url += '&language=' + filters.language;
      const res = await api.get(url);
      setListings(res.data.listings || []);
      setTotal(res.data.total || 0);
    } catch {
      setListings([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchListings(); }, []);

  const doSearch = () => {
    const params: Record<string, string> = {};
    if (filters.city) params.city = filters.city;
    if (filters.language) params.language = filters.language;
    setSearchParams(params);
    fetchListings();
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 800, mb: 1 }}>{t('search.title')}</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Every guide writes their own story. Browse their trips and find the one that speaks to you.
      </Typography>

      <SearchFilters filters={filters} onChange={setFilters} onSearch={doSearch} />

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress sx={{ color: '#DC2626' }} />
        </Box>
      )}

      {!loading && total > 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {t('search.results', { count: total })}
        </Typography>
      )}

      {!loading && listings.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>{t('search.no_results')}</Alert>
      )}

      <Grid container spacing={3}>
        {listings.map((listing: any) => (
          <Grid item xs={12} sm={6} md={4} key={listing.id}>
            <GuideListingCard listing={listing} />
          </Grid>
        ))}
      </Grid>

      <AdBanner slot="bottom" />
    </Container>
  );
}
