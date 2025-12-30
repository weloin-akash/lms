<template>
  <div class="obs-config p-4 border rounded-lg bg-gray-50">
    <h3 class="text-lg font-semibold mb-4">OBS / Streaming Software Settings</h3>

    <div class="space-y-4">
      <div>
        <label class="block text-sm text-gray-600 mb-1">Server URL</label>
        <div class="flex gap-2">
          <input
            type="text"
            :value="rtmpUrl"
            readonly
            class="flex-1 p-2 border rounded bg-white font-mono text-sm"
          />
          <button @click="copy(rtmpUrl)" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Copy
          </button>
        </div>
      </div>

      <div>
        <label class="block text-sm text-gray-600 mb-1">Stream Key</label>
        <div class="flex gap-2">
          <input
            :type="showKey ? 'text' : 'password'"
            :value="streamKey"
            readonly
            class="flex-1 p-2 border rounded bg-white font-mono text-sm"
          />
          <button @click="showKey = !showKey" class="px-3 py-2 bg-gray-200 rounded">
            {{ showKey ? 'Hide' : 'Show' }}
          </button>
          <button @click="copy(streamKey)" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Copy
          </button>
        </div>
      </div>
    </div>

    <div class="mt-6 p-4 bg-blue-50 rounded-lg">
      <h4 class="font-semibold mb-2">OBS Setup Instructions:</h4>
      <ol class="list-decimal ml-4 space-y-1 text-sm">
        <li>Open OBS Studio</li>
        <li>Go to <strong>Settings -> Stream</strong></li>
        <li>Set Service to <strong>Custom...</strong></li>
        <li>Paste the <strong>Server URL</strong> above</li>
        <li>Paste the <strong>Stream Key</strong> above</li>
        <li>Click <strong>Apply</strong> and <strong>OK</strong></li>
        <li>Click <strong>Start Streaming</strong> in OBS</li>
      </ol>
    </div>

    <div class="mt-4 p-4 bg-yellow-50 rounded-lg text-sm">
      <strong>Recommended OBS Settings:</strong>
      <ul class="mt-2 space-y-1">
        <li>- Output: x264, CBR, 2500-4000 Kbps</li>
        <li>- Video: 1280x720, 30fps</li>
        <li>- Keyframe Interval: 2 seconds</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  rtmpUrl: { type: String, required: true },
  streamKey: { type: String, required: true }
})

const showKey = ref(false)

function copy(text) {
  navigator.clipboard.writeText(text)
}
</script>
