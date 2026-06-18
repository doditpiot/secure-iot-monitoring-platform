<!--
  Latest telemetry table.
  Author: HAMAILI Ahmed-Imad
-->

<script setup lang="ts">
import type { Measurement } from '../types'

function formatDate(value: string): string {
  /** Convert API timestamps into the local browser format. */
  return new Date(value).toLocaleString()
}

function formatNullable(value: number | null, suffix = ''): string {
  /** Keep table cells readable when optional sensor values are missing. */
  if (value === null || value === undefined) return '-'
  return `${value}${suffix}`
}

const props = defineProps<{
  measurements: Measurement[]
}>()
</script>

<template>
  <section class="panel-card">
    <div class="mb-3">
      <h2 class="h5 fw-bold mb-1">Latest telemetry</h2>
      <p class="text-muted small mb-0">Most recent measurements received from the MQTT broker.</p>
    </div>

    <div class="table-responsive">
      <table class="table table-sm align-middle mb-0">
        <thead>
          <tr>
            <th>Device</th>
            <th>Temperature</th>
            <th>Humidity</th>
            <th>Battery</th>
            <th>RSSI</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="measurement in props.measurements" :key="measurement.id">
            <td class="fw-semibold">{{ measurement.device_id }}</td>
            <td>{{ formatNullable(measurement.temperature, '°C') }}</td>
            <td>{{ formatNullable(measurement.humidity, '%') }}</td>
            <td>{{ formatNullable(measurement.battery, '%') }}</td>
            <td>{{ formatNullable(measurement.rssi, ' dBm') }}</td>
            <td>{{ formatDate(measurement.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
