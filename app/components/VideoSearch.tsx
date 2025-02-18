'use client';
import React, { useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

const LLMSearchBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [answer, setAnswer] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('video_url', videoUrl);
      formData.append('query', query);

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/search/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data', // Crucial for sending files
          },
        }
      );
      setAnswer(response.data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const sortJsonRecursive = (obj: any): any => {
    if (Array.isArray(obj)) {
      return obj.map(sortJsonRecursive);
    } else if (obj !== null && typeof obj === 'object') {
      return Object.keys(obj)
        .sort()
        .reduce((result: any, key) => {
          result[key] = sortJsonRecursive(obj[key]);
          return result;
        }, {});
    }
    return obj;
  };

  return (
    <div className="flex flex-col items-center">

      <input
        type="text"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
        placeholder="Enter Video URL"
        className="w-[600px] p-2 border border-gray-300 rounded mb-2"
      />

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question about the video"
        className="w-[600px] p-2 border border-gray-300 rounded"
      />
      <button
        onClick={handleSearch}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        disabled={isLoading}
      >
        {isLoading ? 'Searching...' : 'Search'}
      </button>

      {answer && (
        <div className="mt-4 w-[600px]">
          <h3 className="font-bold">LLM Response:</h3>
          <textarea
            className="w-full h-[160px] mt-2 p-2 border border-gray-300 rounded"
            value={JSON.stringify(sortJsonRecursive(answer), null, 2) ?? ''}
            readOnly
          />

          <h3 className="font-bold mt-4">Extracted Answers:</h3>
          <div className="mt-2">
            {answer.answersInText?.map((ans: any, index: number) => (
              <div key={index} className="mb-2">
                <span className="font-semibold">[{ans.number}]</span>{' '}
                <span className="whitespace-pre-wrap break-words">{ans.relevantTextFromDocument}</span>
                {!isLoading && ans.sourceLink && (
                  <Link href={ans.sourceLink} className="text-blue-500 ml-2">
                    {ans.documentTitle}
                  </Link>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default LLMSearchBar;


