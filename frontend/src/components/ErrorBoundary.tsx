import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { Alert, Button, Stack } from '@mantine/core';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <Stack align="center" mt="xl">
          <Alert title="Something went wrong" color="red">
            {this.state.error?.message || 'An unexpected error occurred'}
          </Alert>
          <Button onClick={() => window.location.reload()}>
            Reload Page
          </Button>
        </Stack>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary; 