<!--
  Dashboard summary cards.
  Author: HAMAILI Ahmed-Imad
-->

<script setup lang="ts">
import type { PlatformSummary } from '../types'

function formatNumber(value: number): string {
  /** Format large counters with separators for better readability. */
  return new Intl.NumberFormat('en-US').format(value)
}

function getCards(summary: PlatformSummary) {
  /** Convert the API summary object into small UI card definitions. */
  return [
    { label: 'Registered devices', value: summary.devices },
    { label: 'Online devices', value: summary.online_devices },
    { label: 'Measurements', value: summary.measurements },
    { label: 'Alerts', value: summary.alerts },
  ]
}

function cardClass(label: string): string {
  /** Give important cards a visual accent without duplicating template logic. */
  if (label.includes('Alerts')) return 'summary-card accent-danger'
  if (label.includes('Online')) return 'summary-card accent-success'
  return 'summary-card'
}

const props = defineProps<{
  summary: PlatformSummary
}>()
</script>

<template>
  <div class="row g-3">
    <div v-for="card in getCards(props.summary)" :key="card.label" class="col-12 col-md-6 col-xl-3">
      <div :class="cardClass(card.label)">
        <p class="text-muted small mb-1">{{ card.label }}</p>
        <strong class="fs-3">{{ formatNumber(card.value) }}</strong>
      </div>
    </div>
  </div>
</template>
