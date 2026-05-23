import { useState, useMemo } from 'react';
import {
  Container, Paper, Typography, TextField, Button, Box, Alert,
  ToggleButton, ToggleButtonGroup, Link as MuiLink, LinearProgress, Stepper, Step, StepLabel,
  FormControl, InputLabel, Select, MenuItem
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../services/api';

// Password strength checker
function getPasswordStrength(pw: string): { score: number; label: string; color: string; errors: string[] } {
  const errors: string[] = [];
  if (pw.length < 8) errors.push('At least 8 characters');
  if (!/[A-Z]/.test(pw)) errors.push('One uppercase letter');
  if (!/[a-z]/.test(pw)) errors.push('One lowercase letter');
  if (!/[0-9]/.test(pw)) errors.push('One number');
  if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(pw)) errors.push('One special character (!@#$%...)');
  const score = Math.max(0, 5 - errors.length);
  const labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
  const colors = ['#DC2626', '#DC2626', '#F59E0B', '#F59E0B', '#16A34A', '#16A34A'];
  return { score, label: labels[score], color: colors[score], errors };
}

// Simple math captcha
function generateCaptcha(): { question: string; answer: number } {
  const a = Math.floor(Math.random() * 20) + 1;
  const b = Math.floor(Math.random() * 20) + 1;
  return { question: `What is ${a} + ${b}?`, answer: a + b };
}

export default function RegisterPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  // Steps: 0 = email+captcha, 1 = verify code, 2 = password+profile
  const [step, setStep] = useState(0);
  const [email, setEmail] = useState('');
  const [captcha] = useState(() => generateCaptcha());
  const [captchaAnswer, setCaptchaAnswer] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [demoCode, setDemoCode] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('tourist');
  const [country, setCountry] = useState('');
  const [currency, setCurrency] = useState('USD');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const pwStrength = useMemo(() => getPasswordStrength(password), [password]);

  // Step 1: Send verification code
  const handleSendCode = async () => {
    setError('');
    if (parseInt(captchaAnswer) !== captcha.answer) {
      setError('Wrong answer to the math question. Please try again.');
      return;
    }
    if (!email.includes('@')) { setError('Please enter a valid email.'); return; }
    setLoading(true);
    try {
      const res = await api.post('/auth/send-code', { email });
      setDemoCode(res.data.demo_code); // MVP: show code (production: sent via email)
      setStep(1);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to send code.');
    } finally { setLoading(false); }
  };

  // Step 2: Verify code
  const handleVerifyCode = async () => {
    setError('');
    setLoading(true);
    try {
      await api.post('/auth/verify-code', { email, code: verificationCode });
      setStep(2);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Invalid code.');
    } finally { setLoading(false); }
  };

  // Step 3: Complete registration
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (pwStrength.score < 4) { setError('Password is not strong enough. ' + pwStrength.errors.join(', ')); return; }
    if (!name.trim()) { setError('Please enter your name.'); return; }
    setLoading(true);
    try {
      const data = await api.post('/auth/register', { email, password, role, display_name: name, country, preferred_currency: currency });
      localStorage.setItem('glc_token', data.data.access_token);
      localStorage.setItem('glc_user', JSON.stringify({ id: data.data.user_id, role: data.data.role, display_name: name, email, country, currency }));
      window.location.href = '/dashboard';  // Force full navigation
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed.');
    } finally { setLoading(false); }
  };

  return (
    <Box sx={{ minHeight: '80vh', display: 'flex', alignItems: 'center', bgcolor: '#FEF2F2', py: 4 }}>
      <Container maxWidth="sm">
        <Paper sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h5" align="center" sx={{ fontWeight: 700, mb: 1 }}>
            {t('auth.register_title')}
          </Typography>

          <Stepper activeStep={step} sx={{ mb: 3 }}>
            <Step><StepLabel>Email</StepLabel></Step>
            <Step><StepLabel>Verify</StepLabel></Step>
            <Step><StepLabel>Profile</StepLabel></Step>
          </Stepper>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          {/* STEP 0: Email + Captcha */}
          {step === 0 && (
            <Box>
              <TextField fullWidth label={t('auth.email')} type="email" value={email}
                onChange={(e) => setEmail(e.target.value)} sx={{ mb: 2 }} required />

              {/* Anti-robot: math captcha */}
              <Paper variant="outlined" sx={{ p: 2, mb: 2, bgcolor: '#FFFBEB', borderColor: '#F59E0B' }}>
                <Typography variant="body2" sx={{ fontWeight: 600, mb: 1 }}>🤖 Prove you're human</Typography>
                <Typography variant="body1" sx={{ mb: 1 }}>{captcha.question}</Typography>
                <TextField size="small" value={captchaAnswer} onChange={(e) => setCaptchaAnswer(e.target.value)}
                  placeholder="Your answer" type="number" sx={{ width: 140 }} />
              </Paper>

              <Button fullWidth variant="contained" onClick={handleSendCode} disabled={loading}
                sx={{ bgcolor: '#DC2626', py: 1.5, '&:hover': { bgcolor: '#B91C1C' } }}>
                {loading ? 'Sending...' : 'Send Verification Code'}
              </Button>
            </Box>
          )}

          {/* STEP 1: Verify code */}
          {step === 1 && (
            <Box>
              <Alert severity="success" sx={{ mb: 2 }}>
                Code sent to <strong>{email}</strong>
              </Alert>
              {demoCode && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                  MVP Demo: Your code is <strong>{demoCode}</strong>
                  <br /><Typography variant="caption">(In production, this is sent via email)</Typography>
                </Alert>
              )}
              <TextField fullWidth label="Enter 6-digit code" value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)} sx={{ mb: 2 }}
                inputProps={{ maxLength: 6 }} placeholder="123456" />
              <Button fullWidth variant="contained" onClick={handleVerifyCode} disabled={loading}
                sx={{ bgcolor: '#DC2626', py: 1.5, '&:hover': { bgcolor: '#B91C1C' } }}>
                {loading ? 'Verifying...' : 'Verify Code'}
              </Button>
            </Box>
          )}

          {/* STEP 2: Password + Profile */}
          {step === 2 && (
            <Box component="form" onSubmit={handleRegister}>
              <Alert severity="success" sx={{ mb: 2 }}>Email verified ✓</Alert>

              <TextField fullWidth label={t('auth.name')} value={name}
                onChange={(e) => setName(e.target.value)} sx={{ mb: 2 }} required />

              <TextField fullWidth label={t('auth.password')} type="password" value={password}
                onChange={(e) => setPassword(e.target.value)} sx={{ mb: 1 }} required />

              {/* Password strength bar */}
              {password && (
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="caption" sx={{ color: pwStrength.color, fontWeight: 600 }}>
                      {pwStrength.label}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">{pwStrength.score}/5</Typography>
                  </Box>
                  <LinearProgress variant="determinate" value={pwStrength.score * 20}
                    sx={{ height: 6, borderRadius: 3, bgcolor: '#eee',
                      '& .MuiLinearProgress-bar': { bgcolor: pwStrength.color } }} />
                  {pwStrength.errors.length > 0 && (
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                      Missing: {pwStrength.errors.join(' · ')}
                    </Typography>
                  )}
                </Box>
              )}

              <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>{t('auth.role')}</Typography>
              <ToggleButtonGroup value={role} exclusive fullWidth
                onChange={(_, v) => v && setRole(v)} sx={{ mb: 3 }}>
                <ToggleButton value="tourist" sx={{ '&.Mui-selected': { bgcolor: '#FEF2F2', color: '#DC2626' } }}>
                  🌍 {t('auth.tourist')}
                </ToggleButton>
                <ToggleButton value="guide" sx={{ '&.Mui-selected': { bgcolor: '#FEF2F2', color: '#DC2626' } }}>
                  🧭 {t('auth.guide_role')}
                </ToggleButton>
              </ToggleButtonGroup>

              {role === 'tourist' && (
                <>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Country</InputLabel>
                    <Select value={country} label="Country" onChange={(e) => setCountry(e.target.value)}>
                      {[['US','🇺🇸 United States'],['GB','🇬🇧 United Kingdom'],['AU','🇦🇺 Australia'],['CA','🇨🇦 Canada'],['DE','🇩🇪 Germany'],['FR','🇫🇷 France'],['JP','🇯🇵 Japan'],['KR','🇰🇷 South Korea'],['SG','🇸🇬 Singapore'],['OTHER','🌍 Other']].map(([code, label]) => (
                        <MenuItem key={code} value={code}>{label}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Preferred Currency</InputLabel>
                    <Select value={currency} label="Preferred Currency" onChange={(e) => setCurrency(e.target.value)}>
                      {[['USD','$ US Dollar'],['EUR','€ Euro'],['GBP','£ British Pound'],['AUD','A$ Australian Dollar'],['JPY','¥ Japanese Yen'],['KRW','₩ Korean Won'],['CAD','C$ Canadian Dollar']].map(([code, label]) => (
                        <MenuItem key={code} value={code}>{label}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </>
              )}

              <Button fullWidth type="submit" variant="contained" disabled={loading || pwStrength.score < 4}
                sx={{ bgcolor: '#DC2626', py: 1.5, '&:hover': { bgcolor: '#B91C1C' } }}>
                {loading ? 'Creating...' : t('auth.register_btn')}
              </Button>
            </Box>
          )}

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
