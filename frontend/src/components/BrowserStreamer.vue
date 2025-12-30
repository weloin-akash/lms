<template>
  <div class="browser-streamer">
    <!-- Preview -->
    <div class="preview-container mb-4">
      <video
        ref="previewVideo"
        class="w-full max-w-2xl rounded-lg bg-black"
        autoplay
        muted
        playsinline
      ></video>
    </div>

    <!-- Controls -->
    <div class="controls flex flex-wrap gap-3 mb-4">
      <!-- Camera Selection -->
      <select v-if="cameras.length" v-model="selectedCamera" class="p-2 border rounded" @change="switchCamera">
        <option v-for="device in cameras" :key="device.deviceId" :value="device.deviceId">
          {{ device.label || `Camera ${cameras.indexOf(device) + 1}` }}
        </option>
      </select>
      <div v-else class="p-2 bg-yellow-100 text-yellow-800 rounded text-sm">
        No camera detected
      </div>

      <!-- Microphone Selection -->
      <select v-if="microphones.length" v-model="selectedMic" class="p-2 border rounded" @change="switchMic">
        <option v-for="device in microphones" :key="device.deviceId" :value="device.deviceId">
          {{ device.label || `Mic ${microphones.indexOf(device) + 1}` }}
        </option>
      </select>
      <div v-else class="p-2 bg-yellow-100 text-yellow-800 rounded text-sm">
        No microphone detected
      </div>

      <!-- Quality Selection -->
      <select v-model="quality" class="p-2 border rounded">
        <option value="720p">720p (HD)</option>
        <option value="480p">480p (SD)</option>
        <option value="360p">360p (Low)</option>
      </select>
    </div>

    <!-- Action Buttons -->
    <div class="actions flex gap-3">
      <button
        v-if="!isStreaming"
        @click="startStreaming"
        :disabled="!mediaStream"
        class="px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:bg-gray-300"
      >
        Start Streaming
      </button>

      <button
        v-else
        @click="stopStreaming"
        class="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
      >
        Stop Streaming
      </button>

      <button
        @click="toggleMute"
        :class="['px-4 py-3 rounded-lg', isMuted ? 'bg-red-100 text-red-600' : 'bg-gray-100']"
      >
        {{ isMuted ? 'Unmute' : 'Mute' }}
      </button>

      <button
        @click="toggleVideo"
        :class="['px-4 py-3 rounded-lg', isVideoOff ? 'bg-red-100 text-red-600' : 'bg-gray-100']"
      >
        {{ isVideoOff ? 'Camera On' : 'Camera Off' }}
      </button>
    </div>

    <!-- Status -->
    <div v-if="error" class="mt-4 p-3 bg-red-50 text-red-600 rounded">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  streamName: { type: String, required: true },
  webrtcUrl: { type: String, required: true },
  streamKey: { type: String, required: true }
})

const emit = defineEmits(['started', 'stopped'])

// Device refs
const previewVideo = ref(null)
const cameras = ref([])
const microphones = ref([])
const selectedCamera = ref('')
const selectedMic = ref('')

// Stream state
const mediaStream = ref(null)
const peerConnection = ref(null)
const isStreaming = ref(false)
const isMuted = ref(false)
const isVideoOff = ref(false)
const quality = ref('720p')
const error = ref('')

// Quality presets
const qualityPresets = {
  '720p': { width: 1280, height: 720, frameRate: 30 },
  '480p': { width: 854, height: 480, frameRate: 30 },
  '360p': { width: 640, height: 360, frameRate: 24 }
}

onMounted(async () => {
  await getDevices()
  await startPreview()
})

onUnmounted(() => {
  // Only cleanup local resources on unmount, don't end the stream on server
  cleanupLocalResources()
})

async function getDevices() {
  try {
    // First enumerate devices to see what's available
    let devices = await navigator.mediaDevices.enumerateDevices()

    // Check if we have any video/audio devices
    const hasVideo = devices.some(d => d.kind === 'videoinput')
    const hasAudio = devices.some(d => d.kind === 'audioinput')

    if (!hasVideo && !hasAudio) {
      error.value = 'No camera or microphone found on this device.'
      return
    }

    // Request permission for available devices
    const constraints = {}
    if (hasVideo) constraints.video = true
    if (hasAudio) constraints.audio = true

    const tempStream = await navigator.mediaDevices.getUserMedia(constraints)
    tempStream.getTracks().forEach(track => track.stop())

    // Re-enumerate after permission granted to get full device info
    devices = await navigator.mediaDevices.enumerateDevices()
    cameras.value = devices.filter(d => d.kind === 'videoinput')
    microphones.value = devices.filter(d => d.kind === 'audioinput')

    if (cameras.value.length) selectedCamera.value = cameras.value[0].deviceId
    if (microphones.value.length) selectedMic.value = microphones.value[0].deviceId
  } catch (err) {
    if (err.name === 'NotFoundError') {
      error.value = 'No camera or microphone found. Please connect a device.'
    } else if (err.name === 'NotAllowedError') {
      error.value = 'Camera/microphone access denied. Please grant permission in browser settings.'
    } else {
      error.value = 'Failed to access camera/microphone: ' + err.message
    }
    console.error(err)
  }
}

async function startPreview() {
  try {
    const preset = qualityPresets[quality.value]

    // Check what devices are available
    const hasCamera = cameras.value.length > 0
    const hasMic = microphones.value.length > 0

    if (!hasCamera && !hasMic) {
      error.value = 'No camera or microphone available'
      return
    }

    const constraints = {}

    // Video constraints
    if (hasCamera) {
      constraints.video = {
        width: { ideal: preset.width },
        height: { ideal: preset.height },
        frameRate: { ideal: preset.frameRate }
      }
      if (selectedCamera.value) {
        constraints.video.deviceId = { ideal: selectedCamera.value }
      }
    } else {
      constraints.video = false
    }

    // Audio constraints
    if (hasMic) {
      constraints.audio = {
        echoCancellation: true,
        noiseSuppression: true
      }
      if (selectedMic.value) {
        constraints.audio.deviceId = { ideal: selectedMic.value }
      }
    } else {
      constraints.audio = false
    }

    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)

    if (previewVideo.value) {
      previewVideo.value.srcObject = mediaStream.value
    }
    error.value = ''
  } catch (err) {
    error.value = 'Failed to start camera preview: ' + err.message
    console.error(err)
  }
}

async function switchCamera() {
  if (mediaStream.value) {
    mediaStream.value.getVideoTracks().forEach(track => track.stop())
  }
  await startPreview()
}

async function switchMic() {
  if (mediaStream.value) {
    mediaStream.value.getAudioTracks().forEach(track => track.stop())
  }
  await startPreview()
}

async function startStreaming() {
  if (!mediaStream.value || !props.webrtcUrl) return

  try {
    // Create peer connection for SRS WHIP
    peerConnection.value = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    })

    // Monitor connection state
    peerConnection.value.onconnectionstatechange = async () => {
      console.log('Connection state:', peerConnection.value.connectionState)
      if (peerConnection.value.connectionState === 'connected') {
        if (!isStreaming.value) {
          isStreaming.value = true
          error.value = ''
          console.log('Stream started successfully!')

          await call('lms.lms.api.start_browser_stream', {
            stream_name: props.streamName
          })
          emit('started')
        }
      } else if (peerConnection.value.connectionState === 'failed') {
        error.value = 'WebRTC connection failed'
      }
    }

    // Add local tracks
    mediaStream.value.getTracks().forEach(track => {
      peerConnection.value.addTrack(track, mediaStream.value)
    })

    // Create offer
    const offer = await peerConnection.value.createOffer()
    await peerConnection.value.setLocalDescription(offer)

    // Wait for ICE gathering to complete
    await new Promise((resolve) => {
      if (peerConnection.value.iceGatheringState === 'complete') {
        resolve()
      } else {
        peerConnection.value.onicegatheringstatechange = () => {
          if (peerConnection.value.iceGatheringState === 'complete') {
            resolve()
          }
        }
        // Timeout after 3 seconds
        setTimeout(resolve, 3000)
      }
    })

    // Send offer to SRS via WHIP (HTTP POST)
    console.log('Sending WHIP offer to:', props.webrtcUrl)
    const response = await fetch(props.webrtcUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/sdp'
      },
      body: peerConnection.value.localDescription.sdp
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`WHIP failed: ${response.status} - ${errorText}`)
    }

    // Get SRS answer
    const answerSdp = await response.text()
    console.log('SRS answer received')

    // Set remote description
    await peerConnection.value.setRemoteDescription({
      type: 'answer',
      sdp: answerSdp
    })

    console.log('WebRTC connection established')

  } catch (err) {
    error.value = 'Failed to start streaming: ' + err.message
    console.error(err)
  }
}

function cleanupLocalResources() {
  // Close WebRTC connection
  if (peerConnection.value) {
    peerConnection.value.close()
    peerConnection.value = null
  }
  // Stop media tracks
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  isStreaming.value = false
}

async function stopStreaming() {
  cleanupLocalResources()

  // End stream on server
  await call('lms.lms.api.stop_stream', {
    stream_name: props.streamName
  })

  emit('stopped')
}

function toggleMute() {
  if (mediaStream.value) {
    mediaStream.value.getAudioTracks().forEach(track => {
      track.enabled = !track.enabled
    })
    isMuted.value = !isMuted.value
  }
}

function toggleVideo() {
  if (mediaStream.value) {
    mediaStream.value.getVideoTracks().forEach(track => {
      track.enabled = !track.enabled
    })
    isVideoOff.value = !isVideoOff.value
  }
}
</script>

<style scoped>
.preview-container video {
  aspect-ratio: 16 / 9;
  transform: scaleX(-1); /* Mirror preview */
}
</style>
