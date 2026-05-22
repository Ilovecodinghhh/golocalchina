import { AppBar, Toolbar, Typography, Button, Box, Select, MenuItem } from '@mui/material';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export default function Navbar() {
  const { t, i18n } = useTranslation();

  return (
    <AppBar position="sticky" sx={{ bgcolor: '#1a472a' }}>
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to="/"
          sx={{ textDecoration: 'none', color: 'white', fontWeight: 700, flexGrow: 0, mr: 4 }}
        >
          🌏 {t('app.name')}
        </Typography>

        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          <Button color="inherit" component={Link} to="/guides">{t('nav.guides')}</Button>
          <Button color="inherit" component={Link} to="/how-it-works">{t('nav.how_it_works')}</Button>
        </Box>

        <Select
          value={i18n.language}
          onChange={(e) => i18n.changeLanguage(e.target.value)}
          size="small"
          sx={{ color: 'white', mr: 2, '& .MuiSelect-icon': { color: 'white' } }}
        >
          <MenuItem value="en">EN</MenuItem>
          <MenuItem value="zh">中文</MenuItem>
        </Select>

        <Button color="inherit" component={Link} to="/login">{t('nav.login')}</Button>
        <Button variant="outlined" color="inherit" component={Link} to="/register" sx={{ ml: 1 }}>
          {t('nav.register')}
        </Button>
      </Toolbar>
    </AppBar>
  );
}
