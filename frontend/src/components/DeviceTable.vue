<!--
  Registered devices table.
  Author: HAMAILI Ahmed-Imad
-->

<script setup lang="ts">
import type { Device } from '../types'

function formatDate(value: string | null): string {
  /** Display a readable date, or a clean fallback when no telemetry arrived yet. */
  if (!value) return 'Never'
  return new Date(value).toLocaleString()
}

function statusClass(status: string): string {
  /** Map device status to Bootstrap badge classes. */
  return status === 'online' ? 'badge text-bg-success' : 'badge text-bg-secondary'
}

function protocolLabel(protocol: string): string {
  /** Display protocol values in a compact technical format. */
  return protocol.toUpperCase()
}

function isDeviceActive(device: Device): string {
  /** Convert the boolean active flag into a label for the UI. */
  return device.is_active ? 'active' : 'disabled'
}

function isDeviceActiveClass(device: Device): string {
  /** Style active and disabled devices differently. */
  return device.is_active ? 'badge text-bg-primary' : 'badge text-bg-secondary'
}

function locationLabel(device: Device): string {
  /** Avoid empty cells when a device has no location configured. */
  return device.location ?? 'No location'
}

function deviceTitle(device: Device): string {
  /** Build a tooltip that helps identify the device quickly. */
  return `${device.name} (${device.device_id})`
}

function deviceKey(device: Device): string {
  /** Stable Vue key for table rendering. */
  return `${device.id}-${device.device_id}`
}

function lastSeenTitle(device: Device): string {
  /** Tooltip explaining whether the device has sent telemetry. */
  return device.last_seen_at ? `Last seen at ${formatDate(device.last_seen_at)}` : 'No telemetry received yet'
}

const props = defineProps<{
  devices: Device[]
}>()
</script>

<template>
  <section class="panel-card h-100">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <h2 class="h5 fw-bold mb-1">Devices</h2>
        <p class="text-muted small mb-0">Registered MQTT devices and last activity.</p>
      </div>
    </div>

    <div class="table-responsive">
      <table class="table table-sm align-middle mb-0">
        <thead>
          <tr>
            <th>Device</th>
            <th>Location</th>
            <th>Protocol</th>
            <th>Status</th>
            <th>Last seen</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="device in props.devices" :key="deviceKey(device)" :title="deviceTitle(device)">
            <td>
              <div class="fw-semibold">{{ device.name }}</div>
              <div class="text-muted small">{{ device.device_id }}</div>
            </td>
            <td>{{ locationLabel(device) }}</td>
            <td><span class="badge text-bg-light border">{{ protocolLabel(device.protocol) }}</span></td>
            <td>
              <div class="d-flex gap-1 flex-wrap">
                <span :class="statusClass(device.status)">{{ device.status }}</span>
                <span :class="isDeviceActiveClass(device)">{{ isDeviceActive(device) }}</span>
              </div>
            </td>
            <td :title="lastSeenTitle(device)">{{ formatDate(device.last_seen_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
