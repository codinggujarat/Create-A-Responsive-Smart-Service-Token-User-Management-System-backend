import axios from 'axios'

// Use relative URLs for API calls when on Vercel (will be rewritten to backend)
// Use environment variable for local development or custom deployments
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

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

export const userApi = {
  submitUser: (userData) => api.post('/submit', userData),
  getNextToken: () => api.get('/next-token')
}

export const adminApi = {
  login: (credentials) => api.post('/admin/login', credentials),
  getUsers: (params) => api.get('/admin/users', { params }),
  updateUserStatus: (userId, status) => api.put(`/admin/users/${userId}`, { status }),
  getStats: () => api.get('/admin/stats'),
  exportExcel: () => api.get('/admin/export/excel', { responseType: 'blob' }),
  exportCSV: () => api.get('/admin/export/csv', { responseType: 'blob' }),
  exportPDF: () => api.get('/admin/export/pdf', { responseType: 'blob' })
}

export default api