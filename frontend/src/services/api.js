import axios from 'axios'

// Use environment variable for API calls, fallback to relative URL for Vercel proxy
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response || error.message)
    return Promise.reject(error)
  }
)

export const userApi = {
  submitUser: (userData) => api.post('/api/submit', userData),
  getNextToken: () => api.get('/api/next-token')
}

export const adminApi = {
  login: (credentials) => api.post('/api/admin/login', credentials),
  getUsers: (params) => api.get('/api/admin/users', { params }),
  updateUserStatus: (userId, status) => api.put(`/api/admin/users/${userId}`, { status }),
  getStats: () => api.get('/api/admin/stats'),
  exportExcel: () => api.get('/api/admin/export/excel', { responseType: 'blob' }),
  exportCSV: () => api.get('/api/admin/export/csv', { responseType: 'blob' }),
  exportPDF: () => api.get('/api/admin/export/pdf', { responseType: 'blob' })
}

export default api