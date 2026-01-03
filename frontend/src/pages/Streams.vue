<template>
      <AppHeader :title="__('Live Streams')" :description="__('Create Your Live Streams')">
        <template #icon>
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
        </template>

        <template #actions>
            <Button
            v-if="canCreateStream"
            @click="showCreateModal = true"
            class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg px-4 py-2 rounded-lg font-medium border-0 flex items-center gap-2"
          >
            <Plus class="h-4 w-4 stroke-1.5" />
            {{ __('New Stream') }}
          </Button>
        </template>
    </AppHeader>
  <div class="streams-page container mx-auto px-4 py-8">

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-500">Loading streams...</div>
    </div>

    <!-- Streams List -->
    <div v-else-if="streams.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="stream in streams"
        :key="stream.name"
        class="stream-card border rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
        @click="goToStream(stream.name)"
      >
        <div class="relative bg-gray-200 aspect-video flex items-center justify-center overflow-hidden">
          <!-- Thumbnail Image -->
          <img
            v-if="stream.thumbnail"
            :src="stream.thumbnail"
            :alt="stream.title"
            class="w-full h-full object-contain bg-white"
          />
          <!-- Default Icon -->
          <svg v-else class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <!-- Status Badges -->
          <div v-if="stream.status === 'Live'" class="absolute top-2 left-2 px-2 py-1 bg-red-500 text-white text-xs rounded flex items-center gap-1">
            <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
            LIVE
          </div>
          <div v-else-if="stream.status === 'Scheduled'" class="absolute top-2 left-2 px-2 py-1 bg-yellow-500 text-white text-xs rounded">
            Scheduled
          </div>
          <div v-else class="absolute top-2 left-2 px-2 py-1 bg-gray-500 text-white text-xs rounded">
            Ended
          </div>
        </div>
        <div class="p-4">
          <h3 class="font-semibold text-lg mb-1">{{ stream.title }}</h3>
          <div class="text-sm text-gray-500 mb-2">{{ stream.host }}</div>
          <div v-if="stream.status === 'Live'" class="text-sm text-gray-600">
            {{ stream.viewer_count }} viewers
          </div>
          <div v-else-if="stream.scheduled_date" class="text-sm text-gray-600">
            {{ stream.scheduled_date }} at {{ stream.scheduled_time }}
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-16 bg-gray-50 rounded-lg">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
      <div class="text-gray-500 mb-4">No streams yet</div>
      <button
        v-if="canCreateStream"
        @click="showCreateModal = true"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        Create your first stream
      </button>
    </div>

    <!-- Create Stream Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">Create New Stream</h2>
        <form @submit.prevent="createStream">
          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Title *</label>
            <input
              v-model="newStream.title"
              type="text"
              required
              class="w-full p-2 border rounded"
              placeholder="Enter stream title"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Thumbnail</label>
            <div class="border-2 border-dashed rounded-lg p-4 text-center">
              <div v-if="thumbnailPreview" class="relative">
                <img :src="thumbnailPreview" class="max-h-32 mx-auto rounded" />
                <button
                  type="button"
                  @click="clearThumbnail"
                  class="absolute top-0 right-0 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm"
                >
                  ×
                </button>
              </div>
              <div v-else>
                <input
                  ref="thumbnailInput"
                  type="file"
                  accept="image/*"
                  @change="handleThumbnailSelect"
                  class="hidden"
                />
                <button
                  type="button"
                  @click="$refs.thumbnailInput.click()"
                  class="text-blue-500 hover:text-blue-600"
                >
                  <svg class="w-8 h-8 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Click to upload thumbnail
                </button>
                <p class="text-xs text-gray-400 mt-1">PNG, JPG up to 2MB</p>
              </div>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Scheduled Date</label>
            <input
              v-model="newStream.scheduled_date"
              type="date"
              class="w-full p-2 border rounded"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Scheduled Time</label>
            <input
              v-model="newStream.scheduled_time"
              type="time"
              class="w-full p-2 border rounded"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-1">Duration (minutes)</label>
            <input
              v-model="newStream.duration"
              type="number"
              class="w-full p-2 border rounded"
              placeholder="60"
            />
          </div>
          <div class="mb-4 p-3 bg-gray-50 rounded-lg">
            <label class="block text-sm font-semibold mb-2">Access Restriction (Optional)</label>
            <p class="text-xs text-gray-500 mb-3">Restrict this stream to enrolled students only</p>

            <div class="space-y-2 mb-3">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="restrictionType" value="none" class="w-4 h-4" />
                <span class="text-sm">No restriction (visible to all)</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="restrictionType" value="batch" class="w-4 h-4" />
                <span class="text-sm">Restrict to Batch</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="restrictionType" value="course" class="w-4 h-4" />
                <span class="text-sm">Restrict to Course</span>
              </label>
            </div>

            <div v-if="restrictionType === 'batch'">
              <select
                v-model="newStream.batch_name"
                class="w-full p-2 border rounded"
              >
                <option value="">Select a batch</option>
                <option v-for="batch in batches" :key="batch.name" :value="batch.name">
                  {{ batch.title }}
                </option>
              </select>
            </div>
            <div v-if="restrictionType === 'course'">
              <select
                v-model="newStream.course"
                class="w-full p-2 border rounded"
              >
                <option value="">Select a course</option>
                <option v-for="course in courses" :key="course.name" :value="course.name">
                  {{ course.title }}
                </option>
              </select>
            </div>
          </div>
          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="showCreateModal = false"
              class="px-4 py-2 border rounded hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="creating"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300"
            >
              {{ creating ? 'Creating...' : 'Create Stream' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'
import { usersStore } from '@/stores/user'
import { sessionStore } from '@/stores/session'

const router = useRouter()
const { userResource } = usersStore()
const { user } = sessionStore()

const streams = ref([])
const loading = ref(true)
const canCreateStream = ref(false)
const showCreateModal = ref(false)
const creating = ref(false)
const batches = ref([])
const courses = ref([])
const restrictionType = ref('none')
const thumbnailFile = ref(null)
const thumbnailPreview = ref('')

const newStream = ref({
  title: '',
  scheduled_date: '',
  scheduled_time: '',
  duration: 60,
  batch_name: '',
  course: ''
})

let refreshInterval = null

onMounted(async () => {
  await loadStreams()
  await loadBatchesAndCourses()
  checkPermissions()
  // Refresh streams every 10 seconds to update viewer counts
  refreshInterval = setInterval(loadStreams, 10000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})

async function loadBatchesAndCourses() {
  try {
    const res = await call('lms.lms.api.get_stream_restriction_options')
    batches.value = res.batches || []
    courses.value = res.courses || []
  } catch (err) {
    console.error('Failed to load batches/courses:', err)
  }
}

// Watch for userResource to load
watch(() => userResource.data, () => {
  checkPermissions()
}, { immediate: true })

async function loadStreams(showLoading = true) {
  if (showLoading && streams.value.length === 0) {
    loading.value = true
  }
  try {
    const res = await call('lms.lms.api.get_all_streams')
    streams.value = res || []
  } catch (err) {
    console.error('Failed to load streams:', err)
  }
  loading.value = false
}

function checkPermissions() {
  // Check if user can create streams (Moderator, System Manager, or Instructor)
  if (userResource.data) {
    canCreateStream.value =
      userResource.data.is_moderator ||
      userResource.data.is_system_manager ||
      userResource.data.is_instructor ||
      user === 'Administrator'
  }
}

function goToStream(streamName) {
  router.push({ name: 'StreamPage', params: { streamName } })
}

function handleThumbnailSelect(event) {
  const file = event.target.files[0]
  if (file) {
    // Check file size (2MB max)
    if (file.size > 2 * 1024 * 1024) {
      alert('File size must be less than 2MB')
      return
    }
    thumbnailFile.value = file
    thumbnailPreview.value = URL.createObjectURL(file)
  }
}

function clearThumbnail() {
  thumbnailFile.value = null
  thumbnailPreview.value = ''
}

async function uploadThumbnail() {
  if (!thumbnailFile.value) return null

  const formData = new FormData()
  formData.append('file', thumbnailFile.value)
  formData.append('is_private', '0')
  formData.append('folder', 'Home')

  try {
    const response = await fetch('/api/method/upload_file', {
      method: 'POST',
      body: formData
    })
    const result = await response.json()
    if (result.message && result.message.file_url) {
      return result.message.file_url
    }
    return null
  } catch (err) {
    console.error('Failed to upload thumbnail:', err)
    return null
  }
}

async function createStream() {
  if (!newStream.value.title) return

  creating.value = true
  try {
    // Upload thumbnail first if selected
    let thumbnailUrl = null
    if (thumbnailFile.value) {
      thumbnailUrl = await uploadThumbnail()
    }

    // Only send batch_name or course based on restriction type
    const batchName = restrictionType.value === 'batch' ? newStream.value.batch_name : null
    const course = restrictionType.value === 'course' ? newStream.value.course : null

    const res = await call('lms.lms.api.create_stream', {
      title: newStream.value.title,
      scheduled_date: newStream.value.scheduled_date || null,
      scheduled_time: newStream.value.scheduled_time || null,
      duration: newStream.value.duration || 60,
      batch_name: batchName,
      course: course,
      thumbnail: thumbnailUrl
    })

    showCreateModal.value = false
    newStream.value = { title: '', scheduled_date: '', scheduled_time: '', duration: 60, batch_name: '', course: '' }
    restrictionType.value = 'none'
    clearThumbnail()

    // Go to the new stream
    router.push({ name: 'StreamPage', params: { streamName: res.name } })
  } catch (err) {
    console.error('Failed to create stream:', err)
    alert('Failed to create stream')
  }
  creating.value = false
}
</script>
