<template>
	<header
		v-if="!fromLesson"
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center space-x-4">
			<div class="w-10 h-10 bg-[#ed8e22] rounded-xl flex items-center justify-center">
				<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
			</div>
			<div>
				<h1 class="text-2xl font-bold text-gray-900">
					{{ title.data?.title || __('Quiz') }}
				</h1>
				<p class="text-gray-600 text-sm">Take the quiz assessment</p>
			</div>
		</div>
	</header>
	<div
		class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8"
		:class="{ 'pt-4': fromLesson }"
	>
		<div class="max-w-4xl mx-auto px-6">
			<Quiz :quizName="quizID" />
		</div>
	</div>
</template>
<script setup>
import Quiz from '@/components/Quiz.vue'
import { createResource, Breadcrumbs, usePageMeta } from 'frappe-ui'
import { computed, inject, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { sessionStore } from '../stores/session'

const { brand } = sessionStore()
const user = inject('$user')
const router = useRouter()
const fromLesson = ref(false)

onMounted(() => {
	if (!user.data) {
		router.push({ name: 'Courses' })
	}

	if (new URLSearchParams(window.location.search).get('fromLesson')) {
		fromLesson.value = true
	}
})

const props = defineProps({
	quizID: {
		type: String,
		required: true,
	},
})

const title = createResource({
	url: 'frappe.client.get_value',
	params: {
		doctype: 'LMS Quiz',
		fieldname: 'title',
		filters: {
			name: props.quizID,
		},
	},
	auto: true,
})

const breadcrumbs = computed(() => {
	return [{ label: __('Quiz Submission') }, { label: title.data?.title }]
})

usePageMeta(() => {
	return {
		title: `${title.data?.title}`,
		icon: brand.favicon,
	}
})
</script>
