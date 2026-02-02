import React, { useState } from 'react';
import { 
  Container, Typography, Box, Button, Card, CardContent, 
  Grid, CircularProgress, Chip, Paper, Divider 
} from '@mui/material';
import { 
  CloudUpload as UploadIcon, 
  Speed as SpeedIcon, 
  RecordVoiceOver as VoiceIcon,
  Warning as WarningIcon,
  Lightbulb as IdeaIcon
} from '@mui/icons-material';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a video file first.");
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Assuming backend is on port 8000
      const response = await axios.post("http://localhost:8000/analyze", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze video. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: '#f5f5f5', py: 4 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#1976d2' }}>
            Rhetoric
          </Typography>
          <Typography variant="h5" color="text.secondary">
            Your AI Speech Coach
          </Typography>
        </Box>

        {/* Upload Section */}
        <Paper elevation={3} sx={{ p: 4, mb: 4, textAlign: 'center', borderRadius: 2 }}>
          <input
            accept="video/*"
            style={{ display: 'none' }}
            id="raised-button-file"
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="raised-button-file">
            <Button variant="outlined" component="span" startIcon={<UploadIcon />} size="large" sx={{ mb: 2 }}>
              Select Video
            </Button>
          </label>
          {file && (
            <Typography variant="body1" sx={{ mt: 1 }}>
              Selected: <strong>{file.name}</strong>
            </Typography>
          )}
          <Box sx={{ mt: 2 }}>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleUpload} 
              disabled={loading || !file}
              size="large"
              sx={{ px: 4 }}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : "Analyze Speech"}
            </Button>
          </Box>
          {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
        </Paper>

        {/* Results Section */}
        {result && (
          <Box sx={{ animation: 'fadeIn 1s ease-in' }}>
            
            {/* Quote */}
            <Card sx={{ mb: 4, bgcolor: '#e3f2fd', borderLeft: '6px solid #1976d2' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <IdeaIcon color="primary" fontSize="large" />
                  <Typography variant="h6" sx={{ fontStyle: 'italic' }}>
                    "{result.quote}"
                  </Typography>
                </Box>
              </CardContent>
            </Card>

            <Grid container spacing={4}>
              {/* Audio Analysis */}
              <Grid item xs={12} md={6}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <VoiceIcon color="primary" /> Audio Metrics
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle2" color="text.secondary">Words Per Minute</Typography>
                      <Typography variant="h4">{result.audio_analysis.wpm}</Typography>
                      <Chip 
                        label={result.audio_analysis.pacing} 
                        color={result.audio_analysis.pacing === 'Good' ? 'success' : 'warning'} 
                        size="small" 
                        sx={{ mt: 1 }}
                      />
                    </Box>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle2" color="text.secondary">Clarity Score (Est.)</Typography>
                      <Typography variant="h4">{result.audio_analysis.clarity_score}/100</Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle2" color="text.secondary">Transcript Snippet</Typography>
                      <Typography variant="body2" sx={{ bgcolor: '#eee', p: 1, borderRadius: 1, mt: 1, maxHeight: 100, overflowY: 'auto' }}>
                        {result.audio_analysis.transcript}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              {/* Gestures Analysis */}
              <Grid item xs={12} md={6}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <WarningIcon color="error" /> Gesture Analysis
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Typography variant="body2" color="text.secondary" paragraph>
                      We detected potential nervous or erratic movements at these frames. Review them to improve your poise.
                    </Typography>
                    
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', justifyContent: 'center' }}>
                      {result.flagged_frames.length > 0 ? (
                        result.flagged_frames.map((frame, index) => (
                          <Box key={index} sx={{ position: 'relative' }}>
                            <img 
                              src={`http://localhost:8000${frame}`} 
                              alt={`Flagged ${index}`} 
                              style={{ width: '100px', height: 'auto', borderRadius: '4px', border: '1px solid #ddd' }} 
                            />
                            <Chip label={`#${index+1}`} size="small" sx={{ position: 'absolute', top: 0, left: 0, bgcolor: 'rgba(255,255,255,0.8)' }} />
                          </Box>
                        ))
                      ) : (
                        <Typography color="success.main">No significant bad gestures detected!</Typography>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              {/* Suggestion Video */}
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      Recommended Study Material
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                        {/* Embedding Youtube Video */}
                        <iframe 
                            width="100%" 
                            height="400" 
                            src={`https://www.youtube.com/embed/${result.suggestion_video.split('v=')[1]}`} 
                            title="YouTube video player" 
                            frameBorder="0" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowFullScreen
                        ></iframe>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        )}
      </Container>
    </Box>
  );
}

export default App;