import { Card, Text, Grid, Paper, Title, Badge } from '@mantine/core';
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
    <div>
      <Paper p="md" mb="md">
        <Title order={2} mb="md">Dataset Summary</Title>
        <Text>{summary}</Text>
      </Paper>

      <Grid>
        {Object.entries(profile).map(([columnName, columnProfile]) => (
          <Grid.Col key={columnName} span={6}>
            <Card shadow="sm" p="lg" radius="md" withBorder>
              <Title order={3} mb="md">
                {columnName}
                <Badge ml="xs" variant="light">{columnProfile.data_type}</Badge>
              </Title>

              <Text mb="xs">
                Missing Values: {columnProfile.missing_count} ({columnProfile.missing_percentage.toFixed(2)}%)
              </Text>
              <Text mb="xs">Unique Values: {columnProfile.unique_count}</Text>

              {columnProfile.numeric_stats && (
                <>
                  <Text fw={500} mt="md">Numeric Statistics:</Text>
                  <Grid>
                    <Grid.Col span={6}>
                      <Text size="sm">Mean: {columnProfile.numeric_stats.mean.toFixed(2)}</Text>
                      <Text size="sm">Median: {columnProfile.numeric_stats.median.toFixed(2)}</Text>
                      <Text size="sm">Std Dev: {columnProfile.numeric_stats.std.toFixed(2)}</Text>
                    </Grid.Col>
                    <Grid.Col span={6}>
                      <Text size="sm">Min: {columnProfile.numeric_stats.min.toFixed(2)}</Text>
                      <Text size="sm">Max: {columnProfile.numeric_stats.max.toFixed(2)}</Text>
                    </Grid.Col>
                  </Grid>
                </>
              )}

              {columnProfile.temporal_stats && (
                <>
                  <Text fw={500} mt="md">Temporal Statistics:</Text>
                  <Text size="sm">Range: {columnProfile.temporal_stats.min_date} to {columnProfile.temporal_stats.max_date}</Text>
                  <Text size="sm">Duration: {columnProfile.temporal_stats.date_range_days} days</Text>
                </>
              )}

              <Text fw={500} mt="md">Top Values:</Text>
              {Object.entries(columnProfile.top_values).map(([value, count]) => (
                <Text key={value} size="sm">
                  {value}: {count}
                </Text>
              ))}
            </Card>
          </Grid.Col>
        ))}
      </Grid>

      <Title order={2} mt="xl" mb="md">Visualizations</Title>
      <Grid>
        {Object.entries(visualizations).map(([vizName, vizData]) => (
          <Grid.Col key={vizName} span={6}>
            <Card shadow="sm" p="lg" radius="md" withBorder>
              <Title order={3} mb="md">{vizName.replace(/_/g, ' ').toUpperCase()}</Title>
              <Plot
                data={vizData.data}
                layout={{
                  ...vizData.layout,
                  width: undefined,
                  height: 400,
                  margin: { t: 30, r: 30, b: 50, l: 50 },
                  autosize: true,
                }}
                style={{ width: '100%' }}
                useResizeHandler
              />
            </Card>
          </Grid.Col>
        ))}
      </Grid>
    </div>
  );
} 