import { Group, Text, useMantineTheme } from '@mantine/core';
import { Dropzone } from '@mantine/dropzone';
import { IconUpload, IconX, IconFile } from '@tabler/icons-react';

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
    >
      <Group justify="center" gap="xl" style={{ minHeight: 220, pointerEvents: 'none' }}>
        <Dropzone.Accept>
          <IconUpload
            size="3.2rem"
            stroke={1.5}
            color={theme.colors[theme.primaryColor][6]}
          />
        </Dropzone.Accept>
        <Dropzone.Reject>
          <IconX
            size="3.2rem"
            stroke={1.5}
            color={theme.colors.red[6]}
          />
        </Dropzone.Reject>
        <Dropzone.Idle>
          <IconFile size="3.2rem" stroke={1.5} />
        </Dropzone.Idle>

        <div>
          <Text size="xl" inline>
            Drag files here or click to select
          </Text>
          <Text size="sm" c="dimmed" inline mt={7}>
            Upload your data file (CSV, Excel, Parquet, or JSON) - Max size 100MB
          </Text>
        </div>
      </Group>
    </Dropzone>
  );
} 