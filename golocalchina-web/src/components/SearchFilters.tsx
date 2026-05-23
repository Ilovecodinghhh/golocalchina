import { Box, Select, MenuItem, FormControl, InputLabel, Button, Paper } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useTranslation } from 'react-i18next';
import type { SearchParams } from '../services/api';

interface Props {
  filters: SearchParams;
  onChange: (filters: SearchParams) => void;
  onSearch: () => void;
}

const CITIES = ['Beijing', 'Shanghai', 'Xian', 'Chengdu', 'Guilin', 'Hangzhou'];
const LANGUAGES = [
  { value: 'en', label: 'English' }, { value: 'zh', label: '中文' },
  { value: 'ja', label: '日本語' }, { value: 'ko', label: '한국어' },
  { value: 'fr', label: 'Français' }, { value: 'de', label: 'Deutsch' },
  { value: 'es', label: 'Español' },
];

export default function SearchFilters({ filters, onChange, onSearch }: Props) {
  const { t } = useTranslation();
  const update = (key: keyof SearchParams, value: string) => onChange({ ...filters, [key]: value || undefined });

  return (
    <Paper elevation={2} sx={{ p: 3, mb: 4, borderRadius: 3 }}>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
        <FormControl sx={{ minWidth: 180 }}>
          <InputLabel>{t('search.city')}</InputLabel>
          <Select value={filters.city || ''} label={t('search.city')} onChange={(e) => update('city', e.target.value)}>
            <MenuItem value="">All Cities</MenuItem>
            {CITIES.map((c) => <MenuItem key={c} value={c}>{t(`cities.${c}`)}</MenuItem>)}
          </Select>
        </FormControl>
        <FormControl sx={{ minWidth: 180 }}>
          <InputLabel>{t('search.language')}</InputLabel>
          <Select value={filters.language || ''} label={t('search.language')} onChange={(e) => update('language', e.target.value)}>
            <MenuItem value="">All Languages</MenuItem>
            {LANGUAGES.map((l) => <MenuItem key={l.value} value={l.value}>{l.label}</MenuItem>)}
          </Select>
        </FormControl>
        <Button variant="contained" startIcon={<SearchIcon />} onClick={onSearch}
          sx={{ height: 56, px: 4, bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>
          {t('search.search_btn')}
        </Button>
      </Box>
    </Paper>
  );
}
