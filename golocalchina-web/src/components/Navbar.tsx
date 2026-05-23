import { AppBar, Toolbar, Typography, Button, Box, Select, MenuItem } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export default function Navbar() {
  const { t, i18n } = useTranslation();

  return (
    <AppBar position="sticky" sx={{ bgcolor: 'white', color: '#1a1a1a', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
      <Toolbar>
        <Box component={Link} to="/" sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none', mr: 4 }}>
          <img src="/logo.svg" alt="GoLocalChina" style={{ height: 36 }} />
        </Box>

        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          <Button component={Link} to="/guides" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.guides')}</Button>
          <Button component={Link} to="/how-it-works" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.how_it_works')}</Button>
        </Box>

        <Select
          value={i18n.language}
          onChange={(e) => i18n.changeLanguage(e.target.value)}
          size="small" variant="standard"
          sx={{ mr: 2 }}
        >
          <MenuItem value="en">EN</MenuItem>
          <MenuItem value="zh">中文</MenuItem>
        </Select>

        <Button component={Link} to="/login" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.login')}</Button>
        <Button
          variant="contained" component={Link} to="/register"
          sx={{ ml: 1, bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}
        >
          {t('nav.register')}
        </Button>
      </Toolbar>
    </AppBar>
  );
}
