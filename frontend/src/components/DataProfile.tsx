import { Card, Text, Grid, Paper, Title, Badge, Group, Stack, Box, Divider } from '@mantine/core';
import Plot from 'react-plotly.js';

interface ColumnProfile {
  data_type: string;
  missing_count: number;
  missing_percentage: number;
  unique_count: number;
  top_values: Record<string, number>;
  numeric_stats?: {
    mean: number;
    std: number;
    min: number;
    max: number;
    median: number;
    skewness: number;
    kurtosis: number;
  };
  temporal_stats?: {
    min_date: string;
    max_date: string;
    date_range_days: number;
  };
}

interface DataProfileProps {
  profile: Record<string, ColumnProfile>;
  visualizations: Record<string, any>;
  summary: string;
}

export function DataProfile({ profile, visualizations, summary }: DataProfileProps) {
  return (
    <Stack gap="xl">
      <Paper shadow="sm" p="xl" radius="md" withBorder>
        <Title order={2} mb="lg" c="blue">Dataset Overview</Title>
        <Text size="md" style={{ lineHeight: 1.6 }}>{summary}</Text>
      </Paper>

      <Box>
        <Title order={2} mb="lg" c="blue">Column Analysis</Title>
        <Grid>
          {Object.entries(profile).map(([columnName, columnProfile]) => (
            <Grid.Col key={columnName} span={{ base: 12, md: 6 }}>
              <Card shadow="sm" p="lg" radius="md" withBorder>
                <Group justify="space-between" mb="md">
                  <Title order={3} style={{ wordBreak: 'break-word' }}>
                    {columnName}
                  </Title>
                  <Badge size="lg" variant="light" radius="md">{columnProfile.data_type}</Badge>
                </Group>

                <Stack gap="xs">
                  <Group justify="space-between">
                    <Text c="dimmed">Missing Values:</Text>
                    <Text fw={500}>{columnProfile.missing_count} ({columnProfile.missing_percentage.toFixed(2)}%)</Text>
                  </Group>
                  <Group justify="space-between">
                    <Text c="dimmed">Unique Values:</Text>
                    <Text fw={500}>{columnProfile.unique_count}</Text>
                  </Group>
                </Stack>

                {columnProfile.numeric_stats && (
                  <>
                    <Divider my="md" variant="dashed" />
                    <Title order={4} mb="sm">Numeric Statistics</Title>
                    <Grid>
                      <Grid.Col span={6}>
                        <Stack gap="xs">
                          <Group justify="space-between">
                            <Text c="dimmed">Mean:</Text>
                            <Text fw={500}>{columnProfile.numeric_stats.mean.toFixed(2)}</Text>
                          </Group>
                          <Group justify="space-between">
                            <Text c="dimmed">Median:</Text>
                            <Text fw={500}>{columnProfile.numeric_stats.median.toFixed(2)}</Text>
                          </Group>
                          <Group justify="space-between">
                            <Text c="dimmed">Std Dev:</Text>
                            <Text fw={500}>{columnProfile.numeric_stats.std.toFixed(2)}</Text>
                          </Group>
                        </Stack>
                      </Grid.Col>
                      <Grid.Col span={6}>
                        <Stack gap="xs">
                          <Group justify="space-between">
                            <Text c="dimmed">Min:</Text>
                            <Text fw={500}>{columnProfile.numeric_stats.min.toFixed(2)}</Text>
                          </Group>
                          <Group justify="space-between">
                            <Text c="dimmed">Max:</Text>
                            <Text fw={500}>{columnProfile.numeric_stats.max.toFixed(2)}</Text>
                          </Group>
                        </Stack>
                      </Grid.Col>
                    </Grid>
                  </>
                )}

                {columnProfile.temporal_stats && (
                  <>
                    <Divider my="md" variant="dashed" />
                    <Title order={4} mb="sm">Temporal Statistics</Title>
                    <Stack gap="xs">
                      <Text size="sm">
                        <Text span c="dimmed">Range:</Text> {columnProfile.temporal_stats.min_date} to {columnProfile.temporal_stats.max_date}
                      </Text>
                      <Text size="sm">
                        <Text span c="dimmed">Duration:</Text> {columnProfile.temporal_stats.date_range_days} days
                      </Text>
                    </Stack>
                  </>
                )}

                <Divider my="md" variant="dashed" />
                <Title order={4} mb="sm">Top Values</Title>
                <Stack gap="xs">
                  {Object.entries(columnProfile.top_values).map(([value, count]) => (
                    <Group key={value} justify="space-between">
                      <Text c="dimmed">{value}:</Text>
                      <Text fw={500}>{count}</Text>
                    </Group>
                  ))}
                </Stack>
              </Card>
            </Grid.Col>
          ))}
        </Grid>
      </Box>

      <Box>
        <Title order={2} mb="lg" c="blue">Visualizations</Title>
        <Grid>
          {Object.entries(visualizations).map(([vizName, vizData]) => (
            <Grid.Col key={vizName} span={{ base: 12, md: 6 }}>
              <Card shadow="sm" p="lg" radius="md" withBorder>
                <Title order={3} mb="lg" tt="capitalize">
                  {vizName.replace(/_/g, ' ')}
                </Title>
                <Box style={{ height: 400 }}>
                  <Plot
                    data={vizData.data}
                    layout={{
                      ...vizData.layout,
                      width: undefined,
                      height: undefined,
                      margin: { t: 30, r: 30, b: 50, l: 50 },
                      autosize: true,
                      font: { family: 'inherit' },
                      paper_bgcolor: 'transparent',
                      plot_bgcolor: 'transparent',
                    }}
                    style={{ width: '100%', height: '100%' }}
                    useResizeHandler
                    config={{
                      responsive: true,
                      displayModeBar: true,
                      displaylogo: false,
                      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
                    }}
                  />
                </Box>
              </Card>
            </Grid.Col>
          ))}
        </Grid>
      </Box>
    </Stack>
  );
} 