import axios from 'axios';

// Create an Axios instance with the base URL from the environment variable
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers:{
        'Content-Type': 'application/json'
    }
});


// _______Request Interceptor to add Authorization header if token exists________
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },

    (error) => {
        return Promise.reject(error);
    }

)

// _______Response Interceptor to handle 401 Unauthorized errors________
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
 
export default apiClient;

