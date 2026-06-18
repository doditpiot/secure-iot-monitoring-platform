<!--
  Main Vue dashboard page.
  Author: HAMAILI Ahmed-Imad

  This component loads data from the FastAPI backend and passes it to smaller
  presentational components. The goal is to keep the dashboard easy to read.
-->

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import AlertList from './components/AlertList.vue'
import DeviceTable from './components/DeviceTable.vue'
import MeasurementTable from './components/MeasurementTable.vue'
import SummaryCards from './components/SummaryCards.vue'
import { api } from './services/api'
import type { Alert, Device, Measurement, PlatformSummary } from './types'

const loading = ref(true)
const error = ref<string | null>(null)
const summary = ref<PlatformSummary | null>(null)
const devices = ref<Device[]>([])
const measurements = ref<Measurement[]>([])
const alerts = ref<Alert[]>([])
let refreshTimer: number | undefined

async function refreshDashboard() {
  /**
   * Load all dashboard sections in parallel.
   *
   * Parallel requests keep the interface responsive and make the refresh cycle
   * faster than calling each endpoint one after another.
   */
  try {
    error.value = null
    const [summaryResponse, devicesResponse, measurementsResponse, alertsResponse] = await Promise.all([
      api.getSummary(),
      api.getDevices(),
      api.getLatestMeasurements(),
      api.getAlerts(),
    ])

    summary.value = summaryResponse
    devices.value = devicesResponse
    measurements.value = measurementsResponse
    alerts.value = alertsResponse
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load dashboard data.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // The first request fills the dashboard immediately. The interval then keeps
  // the interface close to real time without needing WebSockets in this version.
  refreshDashboard()
  refreshTimer = window.setInterval(refreshDashboard, 5000)
})

onUnmounted(() => {
  // Clearing the interval avoids a background timer if the component is ever
  // unmounted during development or future routing changes.
  if (refreshTimer) window.clearInterval(refreshTimer)
})
</script>

<template>
  <main class="app-shell">
    <!-- Hero section explaining the project value at first glance. -->
    <section class="hero-panel border rounded-4 p-4 mb-4 shadow-sm">
      <div class="d-flex flex-column flex-lg-row justify-content-between gap-3">
        <div>
          <p class="text-uppercase text-muted small fw-semibold mb-2">Secure IoT Monitoring Platform</p>
          <h1 class="display-6 fw-bold mb-2">Connected device monitoring for secure IoT systems.</h1>
          <p class="lead text-muted mb-0">
            MQTT telemetry ingestion, FastAPI APIs, PostgreSQL storage and operational alerts in one containerized platform.
          </p>
        </div>

        <div class="d-flex align-items-start">
          <button class="btn btn-dark px-4" type="button" @click="refreshDashboard">
            Refresh
          </button>
        </div>
      </div>
    </section>

    <div v-if="error" class="alert alert-danger border-0 shadow-sm">
      {{ error }}
    </div>

    <div v-if="loading" class="text-muted py-4">
      Loading platform data...
    </div>

    <template v-else>
      <SummaryCards v-if="summary" :summary="summary" />

      <div class="row g-4 mt-1">
        <div class="col-12 col-xl-7">
          <DeviceTable :devices="devices" />
        </div>
        <div class="col-12 col-xl-5">
          <AlertList :alerts="alerts" />
        </div>
        <div class="col-12">
          <MeasurementTable :measurements="measurements" />
        </div>
      </div>
    </template>
  </main>
</template>
