/**
 * REST API client used by the Vue dashboard.
 *
 * Author: HAMAILI Ahmed-Imad
 */

import type { Alert, Device, Measurement, PlatformSummary } from '../types'

// The URL is injected at build time in Docker. A localhost fallback keeps local
// development simple when the frontend is started outside Docker.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string): Promise<T> {
  /**
   * Execute a typed GET request against the backend.
   *
   * The helper keeps error handling in one place so components can stay focused
   * on displaying data rather than repeating fetch logic.
   */
  const response = await fetch(`${API_BASE_URL}${path}`)

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`)
  }

  return response.json() as Promise<T>
}

export const api = {
  // Summary counters for the top dashboard cards.
  getSummary: () => request<PlatformSummary>('/stats/summary'),

  // Registered devices and their latest operational status.
  getDevices: () => request<Device[]>('/devices'),

  // Recent telemetry table. The limit keeps the dashboard readable.
  getLatestMeasurements: () => request<Measurement[]>('/measurements/latest?limit=20'),

  // Latest generated alerts from the rule-based anomaly detector.
  getAlerts: () => request<Alert[]>('/alerts?limit=20'),
}
