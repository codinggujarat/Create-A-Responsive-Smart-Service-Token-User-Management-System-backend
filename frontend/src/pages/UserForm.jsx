import React, { useState, useEffect } from 'react'
import { userApi } from '../services/api'

const UserForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    address: '',
    contact_number: '',
    work_description: ''
  })
  const [nextToken, setNextToken] = useState(1)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    fetchNextToken()
  }, [])

  const fetchNextToken = async () => {
    try {
      const response = await userApi.getNextToken()
      setNextToken(response.data.next_token)
    } catch (error) {
      console.error('Error fetching next token:', error)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      console.log('Submitting form data:', formData)
      const response = await userApi.submitUser(formData)
      console.log('Submission response:', response)

      setMessage({
        type: 'success',
        text: `Success! Your token number is #${response.data.token_number}. A confirmation email has been sent to ${formData.email}.`
      })

      setFormData({
        name: '',
        email: '',
        address: '',
        contact_number: '',
        work_description: ''
      })

      fetchNextToken()
    } catch (error) {
      console.error('Submission error:', error)
      const errorMessage = error.response?.data?.error ||
        error.response?.data?.message ||
        error.message ||
        'Failed to submit. Please try again.'

      setMessage({
        type: 'error',
        text: errorMessage
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Smart Service Token Management
          </h1>
          <p className="text-lg text-gray-600">
            Register for your service and receive a unique token number
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <div className="bg-primary-600 text-white rounded-lg p-6 mb-8 text-center">
            <h2 className="text-2xl font-semibold mb-2">Your Next Token Number</h2>
            <div className="text-6xl font-bold">#{nextToken}</div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Full Name *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="input-field"
                placeholder="Enter your full name"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="input-field"
                placeholder="your.email@example.com"
              />
            </div>

            <div>
              <label htmlFor="contact_number" className="block text-sm font-medium text-gray-700 mb-2">
                Contact Number *
              </label>
              <input
                type="tel"
                id="contact_number"
                name="contact_number"
                value={formData.contact_number}
                onChange={handleChange}
                required
                className="input-field"
                placeholder="+1 (555) 123-4567"
              />
            </div>

            <div>
              <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-2">
                Address *
              </label>
              <textarea
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                required
                rows="3"
                className="input-field"
                placeholder="Enter your full address"
              />
            </div>

            <div>
              <label htmlFor="work_description" className="block text-sm font-medium text-gray-700 mb-2">
                Work Description *
              </label>
              <textarea
                id="work_description"
                name="work_description"
                value={formData.work_description}
                onChange={handleChange}
                required
                rows="4"
                className="input-field"
                placeholder="Describe the service you need"
              />
            </div>

            {message.text && (
              <div className={`p-4 rounded-lg ${message.type === 'success'
                  ? 'bg-green-50 text-green-800 border border-green-200'
                  : 'bg-red-50 text-red-800 border border-red-200'
                }`}>
                {message.text}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Submitting...' : 'Submit Request'}
            </button>
          </form>
        </div>

        <div className="text-center">
          <a
            href="/admin/login"
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Admin Login
          </a>
        </div>
      </div>
    </div>
  )
}

export default UserForm