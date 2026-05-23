import { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Box, Alert, Link as MuiLink } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { authApi } from '../services/api';

export default function LoginPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await authApi.login({ email, password });
      localStorage.setItem('glc_token', data.access_token);
      localStorage.setItem('glc_user', JSON.stringify({ id: data.user_id, role: data.role }));
      navigate('/guides');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed. Check your email and password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '80vh', display: 'flex', alignItems: 'center', bgcolor: '#FEF2F2' }}>
      <Container maxWidth="xs">
        <Paper sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h5" align="center" sx={{ fontWeight: 700, mb: 3 }}>
            {t('auth.login_title')}
          </Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth label={t('auth.email')} type="email" value={email}
              onChange={(e) => setEmail(e.target.value)} sx={{ mb: 2 }} required
            />
            <TextField
              fullWidth label={t('auth.password')} type="password" value={password}
              onChange={(e) => setPassword(e.target.value)} sx={{ mb: 3 }} required
            />
            <Button
              fullWidth type="submit" variant="contained" disabled={loading}
              sx={{ bgcolor: '#DC2626', py: 1.5, '&:hover': { bgcolor: '#B91C1C' } }}
            >
              {loading ? '...' : t('auth.login_btn')}
            </Button>
          </Box>
          <Typography variant="body2" align="center" sx={{ mt: 2 }}>
            {t('auth.no_account')}{' '}
            <MuiLink component={Link} to="/register" sx={{ color: '#DC2626', fontWeight: 600 }}>
              {t('auth.or_register')}
            </MuiLink>
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
}
