<template>
  <div class="teacher-broadcast">
    <h2 class="text-xl font-semibold mb-4">{{ stream.title }}</h2>

    <!-- Stream Method Selection -->
    <div v-if="stream.status !== 'Live'" class="method-selection mb-6">
      <h3 class="text-lg mb-3">Choose streaming method:</h3>
      <div class="flex gap-4">
        <button
          @click="selectedMethod = 'browser'"
          :class="['px-4 py-3 rounded-lg border-2 transition-all',
                   selectedMethod === 'browser' ? 'border-blue-500 bg-blue-50' : 'border-gray-200']"
        >
          <div class="font-medium">Browser Webcam</div>
          <div class="text-sm text-gray-500">Stream directly from your browser</div>
        </button>
        <button
          @click="selectedMethod = 'obs'"
          :class="['px-4 py-3 rounded-lg border-2 transition-all',
                   selectedMethod === 'obs' ? 'border-blue-500 bg-blue-50' : 'border-gray-200']"
        >
          <div class="font-medium">OBS / Desktop App</div>
          <div class="text-sm text-gray-500">Use professional streaming software</div>
        </button>
      </div>
    </div>

    <!-- Loading Config -->
    <div v-if="loadingConfig" class="text-center py-8">
      <div class="text-gray-500">Loading stream configuration...</div>
    </div>

    <!-- Browser Streaming -->
    <div v-else-if="selectedMethod === 'browser' && config?.browser" class="browser-stream">
      <BrowserStreamer
        :stream-name="stream.name"
        :webrtc-url="config.browser.webrtc_url"
        :stream-key="config.browser.stream_key"
        @started="onStreamStarted"
        @stopped="onStreamStopped"
      />
    </div>

    <!-- OBS Configuration -->
    <div v-else-if="selectedMethod === 'obs' && config?.obs" class="obs-config">
      <OBSConfig
        :rtmp-url="config.obs.rtmp_url"
        :stream-key="config.obs.stream_key"
      />
    </div>

    <!-- Config Error -->
    <div v-else-if="!loadingConfig && !config" class="text-center py-8">
      <div class="text-red-500">Failed to load stream configuration</div>
      <button @click="loadConfig" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
        Retry
      </button>
    </div>

    <!-- Live Status -->
    <div v-if="stream.status === 'Live'" class="live-status mt-4 p-4 bg-red-50 rounded-lg">
      <div class="flex items-center gap-2 text-red-600 font-semibold">
        <span class="w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
        LIVE - {{ stream.stream_source === 'Browser' ? 'Browser' : 'OBS' }}
      </div>
      <div class="text-sm text-gray-600 mt-1">{{ viewerCount }} viewers</div>
      <button
        v-if="stream.stream_source === 'OBS'"
        @click="stopStream"
        class="mt-3 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
      >
        End Stream
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { call } from 'frappe-ui'
import BrowserStreamer from './BrowserStreamer.vue'
import OBSConfig from './OBSConfig.vue'

const props = defineProps({
  stream: { type: Object, required: true }
})

const selectedMethod = ref('browser')
const config = ref(null)
const loadingConfig = ref(true)
const viewerCount = ref(0)
let viewerPollInterval = null

async function loadConfig() {
  loadingConfig.value = true
  try {
    const res = await call('lms.lms.api.get_stream_config', {
      stream_name: props.stream.name
    })
    config.value = res
  } catch (err) {
    console.error('Failed to load stream config:', err)
    config.value = null
  }
  loadingConfig.value = false
}

async function pollViewerCount() {
  if (props.stream.status !== 'Live') return
  try {
    const res = await call('lms.lms.api.get_viewer_count', {
      stream_name: props.stream.name
    })
    viewerCount.value = res.viewer_count || 0
  } catch (err) {
    console.error('Failed to get viewer count:', err)
  }
}

function startViewerPolling() {
  pollViewerCount()
  viewerPollInterval = setInterval(pollViewerCount, 10000) // Every 10 seconds
}

function stopViewerPolling() {
  if (viewerPollInterval) {
    clearInterval(viewerPollInterval)
    viewerPollInterval = null
  }
}

onMounted(async () => {
  await loadConfig()
  // Start polling if stream is already live
  if (props.stream.status === 'Live') {
    startViewerPolling()
  }
})

onUnmounted(() => {
  stopViewerPolling()
})

function onStreamStarted() {
  props.stream.status = 'Live'
  props.stream.stream_source = 'Browser'
  startViewerPolling()
}

function onStreamStopped() {
  props.stream.status = 'Ended'
  stopViewerPolling()
}

async function stopStream() {
  await call('lms.lms.api.stop_stream', {
    stream_name: props.stream.name
  })
  props.stream.status = 'Ended'
}
</script>
