import { useState } from 'react'
import { Container, Title, LoadingOverlay, Alert } from '@mantine/core'
import { FileUpload } from './components/FileUpload'
import { DataProfile } from './components/DataProfile'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface ProfileData {
  profile: Record<string, any>
  visualizations: Record<string, any>
  summary: string
}

function App() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [profileData, setProfileData] = useState<ProfileData | null>(null)

  const handleFileUpload = async (file: File) => {
    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(`${API_URL}/profile`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setProfileData(response.data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while processing the file')
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
