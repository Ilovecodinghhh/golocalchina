import { useState, useEffect } from 'react';
import {
  Container, Typography, Box, Paper, Button, Grid, TextField,
  Dialog, DialogTitle, DialogContent, DialogActions, Alert, Chip,
  Card, CardContent, CardMedia, CardActions, IconButton
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DeleteIcon from '@mui/icons-material/Delete';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function PostsPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [posts, setPosts] = useState<any[]>([]);
  const [newPostOpen, setNewPostOpen] = useState(false);
  const [newPost, setNewPost] = useState({ title: '', content: '', images: '' });
  const [postError, setPostError] = useState('');
  const [msg, setMsg] = useState('');

  useEffect(() => {
    const stored = localStorage.getItem('glc_user');
    if (!stored) {
      navigate('/login');
      return;
    }
    setUser(JSON.parse(stored));
    loadPosts();
  }, [navigate]);

  const loadPosts = async () => {
    try {
      const res = await api.get('/posts?per_page=50');
      setPosts(res.data.posts || []);
    } catch (err) {
      console.error('Failed to load posts:', err);
    }
  };

  const createPost = async () => {
    setPostError('');
    if (newPost.title.length < 5) {
      setPostError('Title must be at least 5 characters.');
      return;
    }
    if (newPost.content.length < 10) {
      setPostError('Content must be at least 10 characters.');
      return;
    }
    try {
      await api.post('/posts?author_user_id=' + user.id, {
        title: newPost.title,
        content: newPost.content,
        images: newPost.images.split(',').map(s => s.trim()).filter(s => s),
      });
      setNewPostOpen(false);
      setNewPost({ title: '', content: '', images: '' });
      loadPosts();
      setMsg('Post created!');
      setTimeout(() => setMsg(''), 3000);
    } catch (err: any) {
      setPostError(err?.response?.data?.detail || 'Failed to create post.');
    }
  };

  const markAsDone = async (postId: string) => {
    try {
      await api.put(`/posts/${postId}/done?author_user_id=${user.id}`);
      loadPosts();
      setMsg('Post marked as done!');
      setTimeout(() => setMsg(''), 3000);
    } catch (err: any) {
      alert('Failed: ' + (err?.response?.data?.detail || 'Unknown error'));
    }
  };

  const deletePost = async (postId: string) => {
    if (!confirm('Delete this post?')) return;
    try {
      await api.delete(`/posts/${postId}?author_user_id=${user.id}`);
      loadPosts();
      setMsg('Post deleted!');
      setTimeout(() => setMsg(''), 3000);
    } catch (err: any) {
      alert('Failed: ' + (err?.response?.data?.detail || 'Unknown error'));
    }
  };

  if (!user) return null;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 800 }}>Community Posts</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Share your travel experiences, questions, and tips with other travelers.
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setNewPostOpen(true)}
          sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}
        >
          Create Post
        </Button>
      </Box>

      {msg && <Alert severity="success" sx={{ mb: 2 }}>{msg}</Alert>}

      {posts.length === 0 ? (
        <Alert severity="info">No posts yet. Be the first to share your story!</Alert>
      ) : (
        <Grid container spacing={3}>
          {posts.map((post) => (
            <Grid item xs={12} key={post.id}>
              <Card sx={{ '&:hover': { boxShadow: 4 } }}>
                {post.images && post.images.length > 0 && (
                  <CardMedia
                    component="img"
                    height="300"
                    image={post.images[0]}
                    alt={post.title}
                    sx={{ objectFit: 'cover' }}
                  />
                )}
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      {post.title}
                    </Typography>
                    {post.is_done && (
                      <Chip
                        icon={<CheckCircleIcon />}
                        label="Done"
                        size="small"
                        color="success"
                      />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    By {post.author.display_name} · {new Date(post.created_at).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>
                    {post.content}
                  </Typography>
                  {post.images && post.images.length > 1 && (
                    <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
                      {post.images.slice(1).map((img: string, idx: number) => (
                        <Box
                          key={idx}
                          component="img"
                          src={img}
                          alt={`Image ${idx + 2}`}
                          sx={{ width: 100, height: 100, objectFit: 'cover', borderRadius: 1 }}
                        />
                      ))}
                    </Box>
                  )}
                </CardContent>
                {post.author.user_id === user.id && (
                  <CardActions>
                    {!post.is_done && (
                      <Button
                        size="small"
                        startIcon={<CheckCircleIcon />}
                        onClick={() => markAsDone(post.id)}
                        color="success"
                      >
                        Mark as Done
                      </Button>
                    )}
                    <Button
                      size="small"
                      startIcon={<DeleteIcon />}
                      onClick={() => deletePost(post.id)}
                      color="error"
                    >
                      Delete
                    </Button>
                  </CardActions>
                )}
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Create Post Dialog */}
      <Dialog open={newPostOpen} onClose={() => setNewPostOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Post</DialogTitle>
        <DialogContent>
          {postError && <Alert severity="error" sx={{ mb: 2 }}>{postError}</Alert>}
          <TextField
            fullWidth
            label="Title (min 5 chars)"
            placeholder="e.g. Amazing experience in Beijing!"
            sx={{ mt: 1, mb: 2 }}
            value={newPost.title}
            onChange={(e) => setNewPost(p => ({ ...p, title: e.target.value }))}
          />
          <TextField
            fullWidth
            label="Content (min 10 chars)"
            placeholder="Share your story, tips, or questions..."
            multiline
            rows={6}
            sx={{ mb: 2 }}
            value={newPost.content}
            onChange={(e) => setNewPost(p => ({ ...p, content: e.target.value }))}
          />
          <TextField
            fullWidth
            label="Image URLs (comma separated, optional)"
            placeholder="https://example.com/image1.jpg, https://example.com/image2.jpg"
            helperText="Add image URLs separated by commas"
            value={newPost.images}
            onChange={(e) => setNewPost(p => ({ ...p, images: e.target.value }))}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewPostOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={createPost}
            sx={{ bgcolor: '#DC2626', '&:hover': { bgcolor: '#B91C1C' } }}
          >
            Publish Post
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
