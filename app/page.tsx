import React from 'react';
import VideoUpload from './components/VideoUpload';
import LLMSearchBar from './components/VideoSearch';

export default function Home() {
  return (
    <div>
      <h1>Video Upload and LLM Search</h1>
      <VideoUpload />
      <LLMSearchBar />
    </div>
  );
}
