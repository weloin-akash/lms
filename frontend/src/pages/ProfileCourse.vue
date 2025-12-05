<template>
    <div class="mt-10">
        <h2 class="mb-3 text-lg font-semibold text-ink-gray-9">
            {{ __('My Courses') }}
        </h2>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="text-center">
            <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
            <p class="mt-2 text-sm text-gray-600">{{ __('Loading courses...') }}</p>
        </div>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
        <p class="text-red-700">{{ __('Error loading courses:') }} {{ error }}</p>
        <button @click="fetchInstructorCourses" class="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
            {{ __('Retry') }}
        </button>
    </div>

    <div v-else-if="instructorCourses.length > 0" class="space-y-3 pb-20 sm:pb-10">
        <div class="flex flex-wrap items-center justify-end gap-3">
            <div class="flex space-x-0.5 rounded-md bg-surface-gray-2 h-8 items-center px-[2px] text-sm overflow-x-auto scrollbar-hide">
                <button 
                    v-for="t in tabs" 
                    :key="t.value" 
                    @click="activeTab = t.value"
                    :class="activeTab === t.value ? 'bg-white text-black shadow-sm' : 'text-ink-gray-7'"
                    class="px-3 whitespace-nowrap rounded h-7 inline-flex items-center justify-center font-medium transition">
                    {{ t.label }}
                </button>
            </div>

            <select 
                v-model="selectedCategory"
                class="border border-gray-300 rounded-md text-sm px-3 py-2 bg-white focus:outline-none focus:ring-1 focus:ring-gray-400 w-full sm:w-auto">
                <option value="">{{ __('All Categories') }}</option>
                <option v-for="cat in categories" :key="cat" :value="cat">
                    {{ cat }}
                </option>
            </select>

            <label class="flex items-center gap-2 text-sm cursor-pointer w-full sm:w-auto">
                <input type="checkbox" v-model="certificationOnly" class="w-4 h-4" />
                {{ __('Certification Only') }}
            </label>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
            <div 
                v-for="course in filteredCourses" 
                :key="course.name"
                class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden hover:shadow-md hover:-translate-y-1 transition-all duration-200 min-h-[300px] flex flex-col">
                
                <router-link 
                    class="w-full h-40 bg-cover bg-center bg-no-repeat" 
                    :style="course.image
                        ? { backgroundImage: `url('${encodeURI(course.image)}')` }
                        : {
                            backgroundImage: getGradientColor(course.card_gradient),
                            backgroundBlendMode: 'screen',
                        }
                    " 
                    :to="{ name: 'CourseDetail', params: { courseName: course.name } }" 
                    target="_blank">
                    <div 
                        v-if="!course.image"
                        class="flex items-center justify-center text-white flex-1 font-extrabold text-center h-full px-5 leading-6"
                        :class="course.title.length > 32
                            ? 'text-lg'
                            : course.title.length > 20
                                ? 'text-xl'
                                : 'text-2xl'
                        ">
                        {{ course.title }}
                    </div>
                </router-link>

                <div class="p-4">
                    <div class="flex items-center justify-between">
                        <div v-if="course.category">
                            <Tooltip :text="__('Category')">
                                <span class="flex items-center text-xs text-gray-600">
                                    <BookOpen class="h-4 w-4 stroke-1.5 mr-1" />
                                    {{ course.category }}
                                </span>
                            </Tooltip>
                        </div>

                        <div v-if="course.rating">
                            <Tooltip :text="__('Average Rating')">
                                <span class="flex items-center text-xs font-medium text-yellow-600">
                                    <Star class="h-3 w-3 stroke-1.5 mr-1 fill-yellow-400" />
                                    {{ course.rating }}
                                </span>
                            </Tooltip>
                        </div>
                    </div>

                    <h3 class="mt-3 text-lg font-semibold text-gray-900 line-clamp-2">
                        {{ course.title }}
                    </h3>

                    <p class="mt-2 text-sm text-gray-600 leading-5 line-clamp-2">
                        {{ expandedText[course.name] ? course.short_introduction : truncateReview(course.short_introduction, 7) }}
                        <span 
                            v-if="course.short_introduction && course.short_introduction.split(' ').length > 10" 
                            @click="toggleExpand(course.name)"
                            class="text-gray-600 cursor-pointer font-semibold ml-1">
                            {{ expandedText[course.name] ? ' Show Less' : '...' }}
                        </span>
                    </p>

                    <!-- Enrollments -->
                    <div class="flex items-center justify-between mt-4">
                        <div v-if="course.enrollments">
                            <Tooltip :text="__('Enrolled Students')">
                                <span class="flex items-center text-xs text-gray-600">
                                    <Users class="h-4 w-4 stroke-1.5 mr-1" />
                                    {{ course.enrollments }}
                                </span>
                            </Tooltip>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="filteredCourses.length === 0" class="col-span-full text-center py-10 text-gray-500">
                {{ __('No Courses Found') }}
            </div>
        </div>
    </div>

    <div v-else class="text-ink-gray-7 text-sm italic">
        {{ __('No Courses') }}
    </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>

<script setup>
import { computed, ref, reactive, watch, onMounted } from 'vue'
import { Tooltip } from 'frappe-ui'
import { Users, Star, BookOpen } from 'lucide-vue-next'
import { theme } from '@/utils/theme'
import dayjs from 'dayjs'

const props = defineProps({
    profile: {
        type: Object,
        required: true,
    },
})

const instructorCourses = ref([])
const loading = ref(false)
const error = ref(null)
const expandedText = reactive({})
const searchTitle = ref("")
const selectedCategory = ref("")
const certificationOnly = ref(false)
const activeTab = ref("all")

const tabs = [
    { label: "All", value: "all" },
    { label: "Live", value: "live" },
    { label: "New", value: "new" },
    { label: "Upcoming", value: "upcoming" },
    // { label: "Created", value: "created" }
]

const fetchInstructorCourses = async () => {
    loading.value = true
    error.value = null
    
    try {
        const response = await fetch('/api/method/lms.lms.api.get_instructor_courses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': window.csrf_token || ''
            },
            body: JSON.stringify({
                username: props.profile?.data?.username
            })
        })
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        
        if (Array.isArray(data)) {
            instructorCourses.value = data
        } else if (data && Array.isArray(data.message)) {
            instructorCourses.value = data.message
        } else {
            instructorCourses.value = []
        }
        
        console.log("Instructor Courses Loaded:", instructorCourses.value)
    } catch (err) {
        error.value = err.message
        console.error('Error fetching instructor courses:', err)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    if (props.profile?.data?.username) {
        fetchInstructorCourses()
    }
})

watch(() => props.profile?.data?.username, (newUsername) => {
    if (newUsername) {
        fetchInstructorCourses()
    }
})

const categories = computed(() => {
    if (!instructorCourses.value.length) return []
    const cats = instructorCourses.value
        .map(c => c.category)
        .filter(c => c && c.trim() !== "")
    return [...new Set(cats)]
})

const filteredCourses = computed(() => {
    if (!instructorCourses.value.length) return []

    return instructorCourses.value.filter(course => {
        if (searchTitle.value &&
            !course.title.toLowerCase().includes(searchTitle.value.toLowerCase())) {
            return false
        }

        if (selectedCategory.value && course.category !== selectedCategory.value) {
            return false
        }

        if (certificationOnly.value && course.certification !== 1) {
            return false
        }

        if (activeTab.value === "live" && course.status !== "Live") return false
        if (activeTab.value === "new" && !isNewCourse(course)) return false
        if (activeTab.value === "upcoming" && course.upcoming !== 1) return false
        // if (activeTab.value === "created" && course.owner !== props.profile?.data?.username) return false

        return true
    })
})

const toggleExpand = (id) => {
    expandedText[id] = !expandedText[id]
}

const getGradientColor = (card_gradient) => {
    let color = card_gradient?.toLowerCase() || 'blue'
    let colorMap = theme.backgroundColor[color]
    return `linear-gradient(to top right, black, ${colorMap?.[400] || '#3b82f6'})`
}

const isNewCourse = (course) => {
    if (!course.published_on) return false
    const publishedDate = dayjs(course.published_on)
    const threeDaysAgo = dayjs().subtract(3, 'month')
    return publishedDate.isAfter(threeDaysAgo)
}

const truncateReview = (text, wordLimit = 10) => {
    if (!text) return ''
    const words = text.split(' ')
    if (words.length <= wordLimit) return text
    return words.slice(0, wordLimit).join(' ')
}
</script>