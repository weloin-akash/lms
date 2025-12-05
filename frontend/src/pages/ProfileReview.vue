<template>
    <div class="mt-10">
        <h2 class="mb-3 text-lg font-semibold text-ink-gray-9">
            {{ __('Student Reviews') }}
        </h2>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="text-center">
            <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
            <p class="mt-2 text-sm text-gray-600">
                {{ __('Loading reviews...') }}
            </p>
        </div>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
        <p class="text-red-700">
            {{ __('Error loading reviews:') }} {{ error }}
        </p>
        <button @click="fetchreviews" class="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
            {{ __('Retry') }}
        </button>
    </div>

    <div v-else-if="filteredReviews.length > 0" class="space-y-3 pb-20 sm:pb-10">
        <div class="flex flex-wrap items-center justify-end gap-3">

            <div class="flex space-x-0.5 rounded-md bg-surface-gray-2 h-8 items-center px-[2px] text-sm">
                <button @click="tab = 'all'" :class="tab === 'all' ? 'bg-white text-black shadow-sm' : 'text-ink-gray-7'" class="px-3 rounded h-7 inline-flex items-center justify-center font-medium transition">
                    All
                </button>

                <button @click="tab = 'newest'" :class="tab === 'newest' ? 'bg-white text-black shadow-sm' : 'text-ink-gray-7'" class="px-3 rounded h-7 inline-flex items-center justify-center font-medium transition">
                    New
                </button>

                <button @click="tab = 'oldest'" :class="tab === 'oldest' ? 'bg-white text-black shadow-sm' : 'text-ink-gray-7'" class="px-3 rounded h-7 inline-flex items-center justify-center font-medium transition">
                    Oldest
                </button>
            </div>

            <select v-if="coursesOptions.length" v-model="selectedCourse" class="border border-gray-300 rounded-md text-sm px-3 py-2 bg-white focus:outline-none focus:ring-1 focus:ring-gray-400">
                <option value="">
                    {{ __('All Courses') }}
                </option>
                <option v-for="course in coursesOptions" :key="course" :value="course">
                    {{ course.toUpperCase() }}
                </option>
            </select>
        </div>

        <div class="flex items-center gap-2 mt-6 ml-2">
            <Tooltip :text="__('Overall Average Rating')">
                <div class="flex items-center">
                    <Star v-for="n in filledStar(totalAvgRating)" :key="'filled-total-' + n" class="size-5 text-transparent fill-yellow-500" />
                    <Star v-for="n in emptyStar(totalAvgRating)" :key="'empty-total-' + n" class="size-5 text-transparent fill-grey-300" />
                </div>
            </Tooltip>

            <span class="text-sm text-ink-gray-7 font-semibold">
                {{ (totalAvgRating * 5).toFixed(1) }} / 5
            </span>
        </div>

        <div class="grid grid-cols-1 gap-6 mt-6">
            <div v-for="rev in visibleReviews" :key="rev.id || rev.reviewer + rev.course" class="bg-white border border-gray-200 rounded-xl shadow-sm p-5">

                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center bg-gray-200 overflow-hidden">
                        <img v-if="rev.u_img" :src="rev.u_img" class="w-full h-full object-cover" />
                        <span v-else class="text-lg font-semibold text-gray-700">
                            {{ rev.reviewer?.charAt(0)?.toUpperCase() }}
                        </span>
                    </div>

                    <div class="flex-1">
                        <div class="flex flex-wrap items-center gap-3 mb-1">
                            <h3 class="font-semibold text-ink-gray-9 text-base">
                                {{ rev.reviewer }}
                            </h3>

                            <span class="text-[10px] px-2 py-1 rounded-full bg-surface-gray-2 text-ink-gray-8 uppercase tracking-wide">
                                {{ rev.course }}
                            </span>
                        </div>

                        <div class="flex items-center mb-2">
                            <Star v-for="n in filledStar(rev.rating)" :key="'filled-' + n" class="size-4 text-transparent fill-yellow-500" />
                            <Star v-for="n in emptyStar(rev.rating)" :key="'empty-' + n" class="size-4 text-transparent fill-grey-300" />

                            <span class="text-xs text-ink-gray-6 ml-2">
                                {{ formatRelativeDate(rev.create_date) }}
                            </span>
                        </div>

                        <p class="text-sm text-ink-gray-8 leading-6 bg-surface-gray-2/40 p-3 rounded-lg">
                            {{ expandedReviews[rev.id] ? rev.review : truncateReview(rev.review, 60) }}

                            <span v-if="rev.review?.split(' ').length > 60" @click="toggleExpand(rev.id)" class="text-indigo-600 cursor-pointer font-semibold ml-1">
                                {{ expandedReviews[rev.id] ? ' Show Less' : '...' }}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="filteredReviews.length > 10" class="text-center mt-6">
            <button @click="showAll = !showAll" class="text-sm font-semibold text-indigo-600 hover:underline">
                {{ showAll ? "Show Less" : "Show More" }}
            </button>
        </div>
    </div>

    <div v-else class="text-ink-gray-7 text-sm italic">
        {{ __('No Reviews') }}
    </div>
</template>

<script setup>
import { computed, ref, reactive, onMounted, watch } from 'vue'
import { createResource, Tooltip } from 'frappe-ui'
import { Star } from 'lucide-vue-next'

const expandedReviews = reactive({})
const toggleExpand = (id) => {
    expandedReviews[id] = !expandedReviews[id]
}

const props = defineProps({
    profile: {
        type: Object,
        required: true,
    },
})

const reviews = ref([])
const loading = ref(false)
const error = ref(null)

const fetchreviews = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetch('/api/method/lms.lms.api.get_instructor_review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': window.csrf_token || ''
            },
            body: JSON.stringify({
                username: props.profile?.data?.username
            })
        })

        const data = await response.json()

        if (Array.isArray(data)) {
            reviews.value = data
        } else if (data && Array.isArray(data.message)) {
            reviews.value = data.message
        } else {
            reviews.value = []
        }
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    if (props.profile?.data?.username) {
        fetchreviews()
    }
})

watch(() => props.profile?.data?.username, (newUsername) => {
    if (newUsername) {
        fetchreviews()
    }
})

const selectedCourse = ref('')

const courses = createResource({
    url: 'lms.lms.api.get_all_course',
    auto: true,
    transform(data) {
        if (Array.isArray(data)) return data
        if (data && Array.isArray(data.message)) return data.message
        return []
    },
})

const coursesOptions = computed(() => {
    return (courses.data || []).map(c => c.name).filter(Boolean)
})

const tab = ref("all")

const dateFilter = computed(() => {
    let list = [...reviews.value]

    if (tab.value === "newest") {
        list.sort((a, b) => new Date(b.create_date) - new Date(a.create_date))
    }

    if (tab.value === "oldest") {
        list.sort((a, b) => new Date(a.create_date) - new Date(b.create_date))
    }

    return list
})

const filteredReviews = computed(() => {
    if (!selectedCourse.value) return dateFilter.value
    return dateFilter.value.filter(r => r.course === selectedCourse.value)
})

const showAll = ref(false)

const visibleReviews = computed(() => {
    return showAll.value ? filteredReviews.value : filteredReviews.value.slice(0, 10)
})

const truncateReview = (text, wordLimit = 60) => {
    if (!text) return ''
    const words = text.split(' ')
    if (words.length <= wordLimit) return text
    return words.slice(0, wordLimit).join(' ')
}

const formatRelativeDate = (dateStr) => {
    if (!dateStr) return ''
    const [d, t] = dateStr.split(' ')
    const iso = `${d}T${t.split('.')[0]}`
    const target = new Date(iso)
    if (isNaN(target)) return ''
    const today = new Date()
    const diff =
        (new Date(today.getFullYear(), today.getMonth(), today.getDate()) -
        new Date(target.getFullYear(), target.getMonth(), target.getDate())) /
        (1000 * 60 * 60 * 24)
    if (diff === 0) return 'Today'
    if (diff === 1) return 'Yesterday'
    if (diff > 1) return `${diff} days ago`
    return ''
}

const filledStar = (rating) => {
    const value = Number(rating)
    if (Number.isNaN(value)) return 0
    return Math.round(value * 5)
}

const emptyStar = (rating) => {
    const filled = filledStar(rating)
    return Math.max(5 - filled, 0)
}

const totalAvgRating = computed(() => {
    if (!filteredReviews.value.length) return 0
    const sum = filteredReviews.value.reduce((a, r) => a + Number(r.rating), 0)
    return sum / filteredReviews.value.length
})
</script>
