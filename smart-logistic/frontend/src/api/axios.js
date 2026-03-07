import axios from 'axios'

const API = axios.create({
  baseURL: 'http://localhost:8000',
})

// Attach JWT token to every request (and log for debugging)
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  console.debug('[axios] token from localStorage:', token)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default API
