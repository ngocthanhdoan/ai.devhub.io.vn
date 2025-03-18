import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const getData = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};

export const postData = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}`, data);
    return response.data;
  } catch (error) {
    console.error('Error posting data:', error);
    throw error;
  }
};

export const getStats = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stats`);
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    console.error('Error performing health check:', error);
    throw error;
  }
};