'use client';

import React from 'react';
import LLMSearchBar from './components/VideoSearch';
import { Container, Typography, TextField, Button, CircularProgress } from '@mui/material';

export default function Home() {
  // Your component logic here
  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Video Frame Analyzer
      </Typography>
      {<LLMSearchBar />}
    </Container>
  );
}

