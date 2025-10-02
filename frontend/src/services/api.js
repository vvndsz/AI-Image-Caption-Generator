import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const generateCaption = async (imageFile, tone, additionalContext = null) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const params = new URLSearchParams({
    tone: tone,
  });
  
  if (additionalContext) {
    params.append('additional_context', additionalContext);
  }

  try {
    const response = await api.post(`/caption?${params}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const prepareSocialPost = async (imageFile, platform, tone) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const params = new URLSearchParams({
    platform: platform,
    tone: tone,
  });

  try {
    const response = await api.post(`/social/prepare?${params}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getAvailableTones = async () => {
  try {
    const response = await api.get('/tones');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const generateBatchCaptions = async (images, tone) => {
  try {
    const response = await api.post('/caption/batch', {
      images: images,
      tone: tone,
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};