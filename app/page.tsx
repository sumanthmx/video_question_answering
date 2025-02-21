'use client';

import React, { useState } from 'react';
import axios from 'axios';
import { Container, Typography, TextField, Button, Grid, Card, CardContent, CircularProgress } from '@mui/material';

export default function Home() {
    const [videoUrl, setVideoUrl] = useState('');
    const [question, setQuestion] = useState('');
    const [extractedAnswers, setExtractedAnswers] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async () => {
        setIsLoading(true);
        setError('');
        try {
            const formData = new FormData();
            formData.append('video_url', videoUrl);
            formData.append('query', question);

            const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/search/`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setExtractedAnswers(response.data.fullJson.llmResponse);
        } catch (err) {
            setError(`An error occurred: ${err.message}`);
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Container maxWidth="md">
            <Typography variant="h4" align="center" gutterBottom>
                Video Question Answering
            </Typography>

            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <TextField
                        label="Video URL"
                        variant="outlined"
                        fullWidth
                        value={videoUrl}
                        onChange={(e) => setVideoUrl(e.target.value)}
                    />
                </Grid>

                <Grid item xs={12}>
                    <TextField
                        label="Question"
                        variant="outlined"
                        multiline
                        rows={4}
                        fullWidth
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                    />
                </Grid>

                <Grid item xs={12}>
                    <Button 
                        variant="contained" 
                        color="primary" 
                        onClick={handleSubmit}
                        disabled={isLoading}
                    >
                        {isLoading ? <CircularProgress size={24} /> : 'Submit'}
                    </Button>
                </Grid>

                {error && (
                    <Grid item xs={12}>
                        <Typography color="error">{error}</Typography>
                    </Grid>
                )}

                {extractedAnswers && (
                    <Grid item xs={12}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6">Response:</Typography>
                                <Typography>{extractedAnswers}</Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                )}
            </Grid>
        </Container>
    );
}
