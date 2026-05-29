import { useState, useEffect } from 'react';
import { AppBar, Toolbar, Button, Box, Select, MenuItem, Avatar, IconButton } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

export default function Navbar() {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const check = () => {
      const stored = localStorage.getItem('glc_user');
      setUser(stored ? JSON.parse(stored) : null);
    };
    check();
    window.addEventListener('storage', check);
    // Re-check on route changes
    const interval = setInterval(check, 1000);
    return () => { window.removeEventListener('storage', check); clearInterval(interval); };
  }, []);

  return (
    <AppBar position="sticky" sx={{ bgcolor: 'white', color: '#1a1a1a', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
      <Toolbar>
        <Box component={Link} to="/" sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none', mr: 4 }}>
          <img src="/logo.svg" alt="GoLocalChina" style={{ height: 36 }} />
        </Box>

        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          <Button component={Link} to="/guides" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.guides')}</Button>
          <Button component={Link} to="/how-it-works" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.how_it_works')}</Button>
          <Button component={Link} to="/posts" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.posts', 'Posts')}</Button>
        </Box>

        <Select value={i18n.language} onChange={(e) => i18n.changeLanguage(e.target.value)}
          size="small" variant="standard" sx={{ mr: 2 }}>
          <MenuItem value="en">EN</MenuItem>
          <MenuItem value="zh">中文</MenuItem>
        </Select>

        {user ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <IconButton onClick={() => navigate('/dashboard')}>
              <Avatar sx={{ width: 36, height: 36, bgcolor: '#DC2626', fontSize: 16 }}>
                {(user.display_name || user.email || 'U').charAt(0).toUpperCase()}
              </Avatar>
            </IconButton>
          </Box>
        ) : (
          <>
            <Button component={Link} to="/login" sx={{ color: '#333', fontWeight: 600 }}>{t('nav.login')}</Button>
            <Button variant="contained" component={Link} to="/register"
              sx={{ ml: 1, bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}>
              {t('nav.register')}
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}
