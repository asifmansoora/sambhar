import { useState, useEffect } from 'react'
import { Container, Title, LoadingOverlay, Alert } from '@mantine/core'
import { FileUpload } from './components/FileUpload'
import { DataProfile } from './components/DataProfile'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'https://sambhar-production.up.railway.app'

// Log the API URL during development
console.log('API URL:', API_URL)

interface ProfileData {
  profile: Record<string, any>
  visualizations: Record<string, any>
  summary: string
}

function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [profileData, setProfileData] = useState<ProfileData | null>(null)

  // Add initialization logging
  useEffect(() => {
    console.log('App initialized')
  }, [])

  const handleFileUpload = async (file: File) => {
    setLoading(true)
    setError(null)
    console.log('Starting file upload:', file.name)

    const formData = new FormData()
    formData.append('file', file)

    try {
      console.log('Making API request to:', `${API_URL}/profile`)
      const response = await axios.post(`${API_URL}/profile`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      console.log('API response received:', response.data)
      setProfileData(response.data)
    } catch (err) {
      console.error('API error:', err)
      setError(
        err instanceof Error 
          ? `Error: ${err.message}` 
          : 'An error occurred while processing the file'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container size="xl" py="xl">
      <Title order={1} mb="xl">Data Profiling and Analysis</Title>
      
      <div style={{ position: 'relative' }}>
        <LoadingOverlay visible={loading} />
        
        {error && (
          <Alert title="Error" color="red" mb="md">
            {error}
          </Alert>
        )}

        <FileUpload onFileUpload={handleFileUpload} />

        {profileData && (
          <div style={{ marginTop: '2rem' }}>
            <DataProfile
              profile={profileData.profile}
              visualizations={profileData.visualizations}
              summary={profileData.summary}
            />
          </div>
        )}
      </div>
    </Container>
  )
}

export default App
