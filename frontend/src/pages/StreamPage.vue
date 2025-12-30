<template>
  <div class="stream-page container mx-auto px-4 py-8">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-500">Loading stream...</div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-8">
      <div class="text-red-500">{{ error }}</div>
      <button @click="loadStream" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
        Retry
      </button>
    </div>

    <!-- Stream Content -->
    <div v-else-if="stream">
      <!-- Back Button -->
      <button
        @click="$router.push({ name: 'Streams' })"
        class="mb-4 text-blue-500 hover:text-blue-600 flex items-center gap-1"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Streams
      </button>

      <!-- Stream Title & Status -->
      <div class="flex items-center gap-4 mb-6">
        <h1 class="text-2xl font-bold">{{ stream.title }}</h1>
        <span
          :class="[
            'px-3 py-1 rounded-full text-sm font-medium',
            stream.status === 'Live' ? 'bg-red-100 text-red-600' :
            stream.status === 'Scheduled' ? 'bg-yellow-100 text-yellow-600' :
            'bg-gray-100 text-gray-600'
          ]"
        >
          {{ stream.status }}
        </span>
      </div>

      <!-- Host View (Teacher) -->
      <div v-if="isHost">
        <TeacherBroadcast :stream="stream" />
      </div>

      <!-- Viewer (Student) -->
      <div v-else>
        <StreamPlayer :stream="stream" />
      </div>

      <!-- Live Comments Section -->
      <div class="mt-6 border rounded-lg">
        <div class="p-4 border-b bg-gray-50">
          <h3 class="font-semibold flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Live Chat
            <span class="text-sm font-normal text-gray-500">({{ comments.length }} messages)</span>
          </h3>
        </div>

        <!-- Comments List -->
        <div ref="commentsContainer" class="h-64 overflow-y-auto p-4 space-y-3 bg-white">
          <div v-if="commentsLoading" class="text-center text-gray-500">
            Loading comments...
          </div>
          <div v-else-if="comments.length === 0" class="text-center text-gray-400 py-8">
            No comments yet. Be the first to comment!
          </div>
          <div
            v-else
            v-for="comment in comments"
            :key="comment.name"
            class="flex gap-3"
          >
            <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-medium flex-shrink-0">
              {{ getInitials(comment.user_name) }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-medium text-sm">{{ comment.user_name }}</span>
                <span class="text-xs text-gray-400">{{ formatTime(comment.creation) }}</span>
              </div>
              <p class="text-sm text-gray-700 break-words">{{ comment.message }}</p>
            </div>
          </div>
        </div>

        <!-- Comment Input -->
        <div class="p-4 border-t bg-gray-50">
          <form @submit.prevent="sendComment" class="flex gap-2">
            <input
              v-model="newComment"
              type="text"
              placeholder="Type a message..."
              class="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="sendingComment"
            />
            <button
              type="submit"
              :disabled="!newComment.trim() || sendingComment"
              class="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject, nextTick } from 'vue'
import { call } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import TeacherBroadcast from '@/components/TeacherBroadcast.vue'
import StreamPlayer from '@/components/StreamPlayer.vue'

const props = defineProps({
  streamName: { type: String, required: true }
})

const { user } = sessionStore()
const socket = inject('$socket')

const stream = ref(null)
const loading = ref(true)
const error = ref('')

// Comments
const comments = ref([])
const commentsLoading = ref(false)
const newComment = ref('')
const sendingComment = ref(false)
const commentsContainer = ref(null)
let commentsPolling = null

const isHost = computed(() => {
  return stream.value && stream.value.host === user
})

onMounted(async () => {
  await loadStream()
  await loadComments()
  subscribeToUpdates()
  startCommentsPolling()
})

onUnmounted(() => {
  unsubscribe()
  stopCommentsPolling()
})

async function loadStream() {
  loading.value = true
  error.value = ''

  try {
    const res = await call('lms.lms.api.get_stream_info', {
      stream_name: props.streamName
    })
    stream.value = res
  } catch (err) {
    error.value = err.message || 'Failed to load stream'
    console.error('Failed to load stream:', err)
  }

  loading.value = false
}

function subscribeToUpdates() {
  if (!socket) return
  socket.on('stream_status_changed', (data) => {
    if (data.stream === props.streamName && stream.value) {
      stream.value.status = data.status
      stream.value.playback_url = data.playback_url
    }
  })

  socket.on('viewer_count_updated', (data) => {
    if (data.stream === props.streamName && stream.value) {
      stream.value.viewer_count = data.count
    }
  })
}

function unsubscribe() {
  if (!socket) return
  socket.off('stream_status_changed')
  socket.off('viewer_count_updated')
}

// Comments functions
let isInitialLoad = true

async function loadComments() {
  // Only show loading on first load
  if (isInitialLoad) {
    commentsLoading.value = true
  }

  try {
    const res = await call('lms.lms.api.get_stream_comments', {
      stream_name: props.streamName
    })
    const newComments = res || []

    // Check if there are new comments
    const hadNewComments = newComments.length > comments.value.length
    comments.value = newComments

    // Only scroll to bottom if new comments were added
    if (hadNewComments) {
      scrollToBottom()
    }
  } catch (err) {
    console.error('Failed to load comments:', err)
  }

  if (isInitialLoad) {
    commentsLoading.value = false
    isInitialLoad = false
  }
}

async function sendComment() {
  if (!newComment.value.trim() || sendingComment.value) return

  sendingComment.value = true
  try {
    const res = await call('lms.lms.api.post_stream_comment', {
      stream_name: props.streamName,
      message: newComment.value.trim()
    })
    newComment.value = ''
    // Add the new comment directly to the list
    comments.value.push(res)
    scrollToBottom()
  } catch (err) {
    console.error('Failed to send comment:', err)
    alert('Failed to send comment')
  }
  sendingComment.value = false
}

function startCommentsPolling() {
  // Poll for new comments every 3 seconds
  commentsPolling = setInterval(loadComments, 3000)
}

function stopCommentsPolling() {
  if (commentsPolling) {
    clearInterval(commentsPolling)
    commentsPolling = null
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (commentsContainer.value) {
      commentsContainer.value.scrollTop = commentsContainer.value.scrollHeight
    }
  })
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function formatTime(datetime) {
  if (!datetime) return ''
  const date = new Date(datetime)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`

  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
