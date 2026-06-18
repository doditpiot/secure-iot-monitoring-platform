<!--
  Alert list component.
  Author: HAMAILI Ahmed-Imad
-->

<script setup lang="ts">
import type { Alert } from '../types'

function formatDate(value: string): string {
  /** Display alert creation time using the user's local browser settings. */
  return new Date(value).toLocaleString()
}

function severityClass(severity: string): string {
  /** Map alert severity to Bootstrap badge classes. */
  if (severity === 'critical') return 'badge text-bg-danger'
  if (severity === 'warning') return 'badge text-bg-warning'
  return 'badge text-bg-secondary'
}

const props = defineProps<{
  alerts: Alert[]
}>()
</script>

<template>
  <section class="panel-card h-100">
    <div class="mb-3">
      <h2 class="h5 fw-bold mb-1">Alerts</h2>
      <p class="text-muted small mb-0">Rule-based anomalies detected from telemetry.</p>
    </div>

    <div v-if="props.alerts.length === 0" class="text-muted small">
      No alerts yet. The simulator injects rare anomalies, so alerts may appear after a few seconds.
    </div>

    <div v-else class="d-flex flex-column gap-2">
      <article v-for="alert in props.alerts" :key="alert.id" class="alert-card">
        <div class="d-flex justify-content-between gap-2 align-items-start">
          <div>
            <div class="fw-semibold">{{ alert.device_id }}</div>
            <div class="text-muted small">{{ alert.message }}</div>
          </div>
          <span :class="severityClass(alert.severity)">{{ alert.severity }}</span>
        </div>
        <div class="text-muted small mt-2">{{ alert.alert_type }} · {{ formatDate(alert.created_at) }}</div>
      </article>
    </div>
  </section>
</template>
