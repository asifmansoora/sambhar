import { Group, Text, useMantineTheme, Stack, rem } from '@mantine/core';
import { Dropzone } from '@mantine/dropzone';
import { IconUpload, IconX, IconCheck } from '@tabler/icons-react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}

export function FileUpload({ onFileUpload }: FileUploadProps) {
  const theme = useMantineTheme();

  return (
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
      }}
    >
      <Group justify="center" gap="xl" style={{ minHeight: 220, pointerEvents: 'none' }}>
        <Dropzone.Accept>
          <IconCheck
            size={rem(50)}
            stroke={1.5}
            color={theme.colors[theme.primaryColor][6]}
            style={{ transition: 'transform 200ms ease' }}
          />
        </Dropzone.Accept>
        <Dropzone.Reject>
          <IconX
            size={rem(50)}
            stroke={1.5}
            color={theme.colors.red[6]}
            style={{ transition: 'transform 200ms ease' }}
          />
        </Dropzone.Reject>
        <Dropzone.Idle>
          <IconUpload 
            size={rem(50)} 
            stroke={1.5}
            style={{ 
              transition: 'transform 200ms ease',
              color: theme.colors.gray[6]
            }}
          />
        </Dropzone.Idle>

        <Stack gap="xs" style={{ maxWidth: rem(400) }}>
          <Text size="xl" fw={700} ta="center">
            Drop your data file here
          </Text>
          <Text size="sm" c="dimmed" ta="center">
            Drag and drop your file or click to browse. We support CSV, Excel, Parquet, and JSON formats.
          </Text>
          <Text size="xs" c="dimmed" ta="center">
            Maximum file size: 100MB
          </Text>
        </Stack>
      </Group>
    </Dropzone>
  );
} 