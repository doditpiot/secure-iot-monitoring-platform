/**
 * Shared frontend types matching the FastAPI response schemas.
 *
 * Author: HAMAILI Ahmed-Imad
 */

export type Device = {
  id: number
  device_id: string
  name: string
  location: string | null
  protocol: string
  status: string
  is_active: boolean
  created_at: string
  last_seen_at: string | null
}

export type Measurement = {
  id: number
  device_id: string
  temperature: number | null
  humidity: number | null
  battery: number | null
  rssi: number | null
  status: string | null
  timestamp: string
  server_received_at: string
}

export type Alert = {
  id: number
  device_id: string
  severity: string
  alert_type: string
  message: string
  created_at: string
}

export type PlatformSummary = {
  devices: number
  online_devices: number
  measurements: number
  alerts: number
}
