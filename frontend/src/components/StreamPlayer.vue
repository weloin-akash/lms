<template>
  <div class="stream-player">
    <!-- Auth Error -->
    <div v-if="authError" class="auth-error bg-red-50 rounded-lg p-8 text-center">
      <div class="text-red-500 font-semibold mb-2">Access Denied</div>
      <div class="text-gray-600">{{ authError }}</div>
    </div>

    <!-- Live Stream -->
    <div v-else-if="stream.status === 'Live'" class="video-wrapper relative">
      <video
        ref="videoElement"
        class="w-full rounded-lg bg-black"
        controls
        muted
        playsinline
      ></video>

      <!-- Play button overlay (shown when autoplay blocked) -->
      <div
        v-if="needsUserInteraction"
        class="play-overlay absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 cursor-pointer rounded-lg"
        @click="startPlayback"
      >
        <div class="text-center text-white">
          <div class="play-btn w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center mb-2 mx-auto hover:bg-opacity-100 transition">
            <svg class="w-10 h-10 text-black ml-1" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </div>
          <div class="text-sm">Click to play</div>
        </div>
      </div>

      <div class="stream-info mt-2 flex justify-between items-center">
        <span class="text-red-500 font-semibold flex items-center gap-1">
          <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          LIVE
        </span>
        <span class="text-gray-600">{{ viewerCount }} watching</span>
      </div>
    </div>

    <!-- Waiting -->
    <div v-else-if="stream.status === 'Scheduled'" class="waiting bg-gray-100 rounded-lg p-8 text-center">
      <div class="text-gray-500 mb-2">Stream not started yet</div>
      <div v-if="stream.scheduled_date" class="text-lg">
        Scheduled: {{ stream.scheduled_date }} at {{ stream.scheduled_time }}
      </div>
    </div>

    <!-- Ended -->
    <div v-else class="ended bg-gray-100 rounded-lg p-8 text-center">
      <div class="text-gray-500">Stream has ended</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { call } from 'frappe-ui'
import mpegts from 'mpegts.js'

const props = defineProps({
  stream: { type: Object, required: true }
})

const videoElement = ref(null)
const viewerCount = ref(props.stream.viewer_count || 0)
const authPlaybackUrl = ref(null)
const authError = ref('')
const needsUserInteraction = ref(false)
let player = null
let pollInterval = null

onMounted(async () => {
  if (props.stream.status === 'Live') {
    await getAuthenticatedUrl()
    initPlayer()
    startPolling()
  }
})

onUnmounted(() => {
  destroyPlayer()
  stopPolling()
})

watch(() => props.stream.status, async (newStatus) => {
  if (newStatus === 'Live') {
    await getAuthenticatedUrl()
    initPlayer()
    startPolling()
  } else {
    destroyPlayer()
    stopPolling()
  }
})

async function getAuthenticatedUrl() {
  try {
    const res = await call('lms.lms.api.get_playback_token', {
      stream_name: props.stream.name
    })
    authPlaybackUrl.value = res.playback_url
    authError.value = ''
  } catch (err) {
    console.error('Failed to get playback token:', err)
    authError.value = 'You do not have permission to view this stream'
    authPlaybackUrl.value = null
  }
}

let retryCount = 0
const MAX_RETRIES = 3

function initPlayer() {
  if (!videoElement.value || !authPlaybackUrl.value) {
    return
  }

  destroyPlayer()

  const playbackUrl = authPlaybackUrl.value

  if (mpegts.isSupported()) {
    player = mpegts.createPlayer({
      type: 'flv',
      isLive: true,
      url: playbackUrl
    }, {
      enableWorker: true,
      enableStashBuffer: false,
      stashInitialSize: 128,
      liveBufferLatencyChasing: true,
      liveBufferLatencyMaxLatency: 1.5,
      liveBufferLatencyMinRemain: 0.3
    })

    player.attachMediaElement(videoElement.value)
    player.load()
    tryPlay()

    player.on(mpegts.Events.ERROR, (errorType, errorDetail) => {
      console.error('FLV player error:', errorType, errorDetail)

      // Only retry a few times, then show error
      if (retryCount < MAX_RETRIES) {
        retryCount++
        setTimeout(() => {
          destroyPlayer()
          initPlayer()
        }, 5000)
      } else {
        authError.value = 'Stream is not available. The broadcaster may not be streaming yet.'
        destroyPlayer()
      }
    })
  } else {
    authError.value = 'Your browser does not support live streaming playback'
  }
}

async function tryPlay() {
  if (!player || !videoElement.value) return

  try {
    await videoElement.value.play()
    needsUserInteraction.value = false
  } catch (err) {
    console.log('Autoplay blocked, showing play button:', err.name)
    needsUserInteraction.value = true
  }
}

async function startPlayback() {
  needsUserInteraction.value = false
  if (videoElement.value) {
    videoElement.value.muted = false
    try {
      await videoElement.value.play()
    } catch (err) {
      console.error('Play failed:', err)
    }
  }
}

function destroyPlayer() {
  if (player) {
    player.pause()
    player.unload()
    player.detachMediaElement()
    player.destroy()
    player = null
  }
}

// Poll viewer count every 10 seconds
async function startPolling() {
  if (pollInterval) return

  await pollViewerCount()

  pollInterval = setInterval(async () => {
    await pollViewerCount()
  }, 10000)
}

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

async function pollViewerCount() {
  try {
    const res = await call('lms.lms.api.get_viewer_count', {
      stream_name: props.stream.name
    })
    viewerCount.value = res.viewer_count
  } catch (err) {
    console.error('Failed to get viewer count:', err)
  }
}
</script>

<style scoped>
.video-wrapper video {
  aspect-ratio: 16 / 9;
  max-height: 70vh;
}
</style>
