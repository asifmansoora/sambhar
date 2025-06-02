import { Group, Text, useMantineTheme, Stack, rem, Box, Paper } from '@mantine/core';
import { Dropzone } from '@mantine/dropzone';
import { IconUpload, IconX, IconCheck } from '@tabler/icons-react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}

export function FileUpload({ onFileUpload }: FileUploadProps) {
  const theme = useMantineTheme();

  return (
    <Paper radius="lg" p="lg" withBorder>
      <Dropzone
        onDrop={(files) => onFileUpload(files[0])}
        onReject={(files) => console.log('rejected files', files)}
        maxSize={100 * 1024 ** 2} // 100MB
        accept={{
          'text/csv': ['.csv'],
          'application/json': ['.json'],
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
          'application/vnd.ms-excel': ['.xls'],
          'application/parquet': ['.parquet'],
        }}
        style={{
          borderWidth: rem(2),
          backgroundColor: theme.white,
          transition: 'all 0.2s ease',
          '&:hover': {
            borderColor: theme.colors.blue[6],
            backgroundColor: theme.colors.blue[0],
          },
        }}
      >
        <Group justify="center" gap="xl" style={{ minHeight: rem(220), pointerEvents: 'none' }}>
          <Box
            style={{
              width: rem(80),
              height: rem(80),
              borderRadius: '50%',
              backgroundColor: theme.colors.blue[0],
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease',
            }}
          >
            <Dropzone.Accept>
              <IconCheck
                size={rem(40)}
                stroke={2}
                color={theme.colors[theme.primaryColor][6]}
                style={{ 
                  transition: 'transform 0.2s ease',
                  transform: 'scale(1.1)',
                }}
              />
            </Dropzone.Accept>
            <Dropzone.Reject>
              <IconX
                size={rem(40)}
                stroke={2}
                color={theme.colors.red[6]}
                style={{ 
                  transition: 'transform 0.2s ease',
                  transform: 'scale(1.1)',
                }}
              />
            </Dropzone.Reject>
            <Dropzone.Idle>
              <IconUpload 
                size={rem(40)} 
                stroke={2}
                style={{ 
                  transition: 'all 0.2s ease',
                  color: theme.colors.blue[6],
                }}
              />
            </Dropzone.Idle>
          </Box>

          <Stack gap="xs" style={{ maxWidth: rem(400) }}>
            <Text size="xl" fw={700} ta="center" style={{ color: theme.colors.blue[7] }}>
              Drop your data file here
            </Text>
            <Text size="sm" c="dimmed" ta="center">
              Drag and drop your file or click to browse
            </Text>
            <Text size="xs" c="dimmed" ta="center">
              Supported formats: CSV, Excel, Parquet, JSON • Max size: 100MB
            </Text>
          </Stack>
        </Group>
      </Dropzone>
    </Paper>
  );
} 