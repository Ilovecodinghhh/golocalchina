import { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Box, Alert, ToggleButton, ToggleButtonGroup, Link as MuiLink } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { authApi } from '../services/api';

export default function RegisterPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('tourist');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await authApi.register({ email, password, role, display_name: name });
      localStorage.setItem('glc_token', data.access_token);
      localStorage.setItem('glc_user', JSON.stringify({ id: data.user_id, role: data.role }));
      navigate('/guides');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed. Try a different email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '80vh', display: 'flex', alignItems: 'center', bgcolor: '#FEF2F2' }}>
      <Container maxWidth="xs">
        <Paper sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h5" align="center" sx={{ fontWeight: 700, mb: 3 }}>
            {t('auth.register_title')}
          </Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth label={t('auth.name')} value={name}
              onChange={(e) => setName(e.target.value)} sx={{ mb: 2 }} required
            />
            <TextField
              fullWidth label={t('auth.email')} type="email" value={email}
              onChange={(e) => setEmail(e.target.value)} sx={{ mb: 2 }} required
            />
            <TextField
              fullWidth label={t('auth.password')} type="password" value={password}
              onChange={(e) => setPassword(e.target.value)} sx={{ mb: 2 }} required
              inputProps={{ minLength: 8 }} helperText="Minimum 8 characters"
            />
            <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>{t('auth.role')}</Typography>
            <ToggleButtonGroup
              value={role} exclusive fullWidth
              onChange={(_, v) => v && setRole(v)} sx={{ mb: 3 }}
            >
              <ToggleButton value="tourist" sx={{ '&.Mui-selected': { bgcolor: '#FEF2F2', color: '#DC2626' } }}>
                🌍 {t('auth.tourist')}
              </ToggleButton>
              <ToggleButton value="guide" sx={{ '&.Mui-selected': { bgcolor: '#FEF2F2', color: '#DC2626' } }}>
                🧭 {t('auth.guide_role')}
              </ToggleButton>
            </ToggleButtonGroup>
            <Button
              fullWidth type="submit" variant="contained" disabled={loading}
              sx={{ bgcolor: '#DC2626', py: 1.5, '&:hover': { bgcolor: '#B91C1C' } }}
            >
              {loading ? '...' : t('auth.register_btn')}
            </Button>
          </Box>
          <Typography variant="body2" align="center" sx={{ mt: 2 }}>
            {t('auth.has_account')}{' '}
            <MuiLink component={Link} to="/login" sx={{ color: '#DC2626', fontWeight: 600 }}>
              {t('auth.or_login')}
            </MuiLink>
          </Typography>
        </Paper>
      </Container>
    </Box>
  );
}
