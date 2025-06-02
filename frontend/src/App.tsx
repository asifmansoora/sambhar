import { useState, useEffect } from 'react'
import { Container, Title, LoadingOverlay, Alert, Paper, Box, Text, AppShell, MantineProvider, rem } from '@mantine/core'
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

  const appTheme = {
    primaryColor: 'blue',
    fontFamily: 'Inter, system-ui, sans-serif',
    headings: {
      fontFamily: 'Inter, system-ui, sans-serif',
    },
    components: {
      Title: {
        styles: {
          root: {
            fontWeight: 600,
          },
        },
      },
      Paper: {
        styles: {
          root: {
            transition: 'transform 0.2s ease, box-shadow 0.2s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 24px rgba(0, 0, 0, 0.1)',
            },
          },
        },
      },
    },
  };

  return (
    <MantineProvider theme={appTheme}>
      <AppShell
        header={{ height: 70 }}
        padding="md"
        styles={{
          main: {
            background: '#f8f9fa',
          },
        }}
      >
        <AppShell.Header>
          <Box 
            px="md" 
            style={{ 
              height: '70px', 
              display: 'flex', 
              alignItems: 'center',
              background: 'white',
              borderBottom: '1px solid #e9ecef',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
            }}
          >
            <Box style={{ display: 'flex', alignItems: 'center', gap: rem(8) }}>
              <Title order={2} c="blue.6">Sambhar</Title>
              <Text size="sm" c="dimmed" style={{ marginLeft: rem(16), paddingLeft: rem(16), borderLeft: '1px solid #e9ecef' }}>
                Data Profiling and Analysis Tool
              </Text>
            </Box>
          </Box>
        </AppShell.Header>

        <AppShell.Main>
          <Container size="xl" py="xl">
            <Paper 
              shadow="sm" 
              p="xl" 
              mb="xl" 
              radius="lg"
              style={{
                background: 'white',
                border: '1px solid #e9ecef',
              }}
            >
              <Box pos="relative">
                <LoadingOverlay 
                  visible={loading} 
                  zIndex={1000}
                  overlayProps={{ radius: "sm", blur: 2 }}
                />
                
                {error && (
                  <Alert 
                    title="Error" 
                    color="red" 
                    mb="md"
                    radius="md"
                    variant="light"
                  >
                    {error}
                  </Alert>
                )}

                <FileUpload onFileUpload={handleFileUpload} />
              </Box>
            </Paper>

            {profileData && (
              <Box mt="xl">
                <DataProfile
                  profile={profileData.profile}
                  visualizations={profileData.visualizations}
                  summary={profileData.summary}
                />
              </Box>
            )}
          </Container>
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  )
}

export default App
