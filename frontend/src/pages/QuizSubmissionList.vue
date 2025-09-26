<template>
	<header
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center space-x-4">
			<div class="w-10 h-10 bg-[#ed8e22] rounded-xl flex items-center justify-center">
				<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
				</svg>
			</div>
			<div>
				<h1 class="text-2xl font-bold text-gray-900">
					{{ submissions.data?.[0]?.quiz_title || __('Quiz Submissions') }}
				</h1>
				<p class="text-gray-600 text-sm">Review student quiz submissions</p>
			</div>
		</div>
	</header>
	<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
		<div v-if="submissions.data?.length" class="max-w-6xl mx-auto">
			<!-- Submissions Grid -->
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				<router-link
					v-for="submission in submissions.data"
					:key="submission.name"
					:to="{
						name: 'QuizSubmission',
						params: {
							submission: submission.name,
						},
					}"
					class="group"
				>
					<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 hover:shadow-md hover:border-gray-300/50 transition-all duration-200 overflow-hidden">
						<!-- Card Header -->
						<div class="p-6 border-b border-gray-100">
							<div class="flex items-center space-x-3 mb-3">
								<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
									<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
									</svg>
								</div>
								<h3 class="text-lg font-semibold text-gray-900 group-hover:text-[#ed8e22] transition-colors duration-200">
									{{ submission.member_name }}
								</h3>
							</div>
							<div class="flex items-center space-x-2">
								<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-[#ed8e22]">
									Submission
								</span>
								<span v-if="submission.percentage >= 70" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
									Passed
								</span>
								<span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
									Failed
								</span>
							</div>
						</div>

						<!-- Card Body -->
						<div class="p-6">
							<div class="grid grid-cols-2 gap-4">
								<div class="text-center">
									<div class="text-2xl font-bold text-gray-900">{{ submission.score }}</div>
									<div class="text-xs text-gray-500">Score</div>
								</div>
								<div class="text-center">
									<div class="text-2xl font-bold text-gray-900">{{ submission.percentage }}%</div>
									<div class="text-xs text-gray-500">Percentage</div>
								</div>
							</div>
						</div>
					</div>
				</router-link>
			</div>
			<!-- Load More Button -->
			<div v-if="submissions.hasNextPage" class="flex justify-center mt-8">
				<Button 
					class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 hover:border-gray-400 shadow-sm hover:shadow transition-all duration-200 px-6 py-2.5 rounded-lg font-medium"
					@click="submissions.next()"
				>
					{{ __('Load More Submissions') }}
				</Button>
			</div>
		</div>

		<!-- Empty State -->
		<div v-else class="p-12 text-center">
			<div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
				<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
				</svg>
			</div>
			<h3 class="text-lg font-semibold text-gray-900 mb-2">No submissions yet</h3>
			<p class="text-gray-600">Students haven't submitted this quiz yet</p>
		</div>
	</div>
</template>
<script setup>
import {
	createListResource,
	Breadcrumbs,
	Button,
	ListView,
	ListRow,
	ListRows,
	ListHeader,
	ListHeaderItem,
	usePageMeta,
} from 'frappe-ui'
import { computed, onMounted, inject } from 'vue'
import { sessionStore } from '../stores/session'
import { useRouter } from 'vue-router'
import EmptyState from '@/components/EmptyState.vue'

const { brand } = sessionStore()
const router = useRouter()
const user = inject('$user')

onMounted(() => {
	if (!user.data?.is_instructor && !user.data?.is_moderator)
		router.push({ name: 'Courses' })
})

const props = defineProps({
	quizID: {
		type: String,
		required: true,
	},
})

const submissions = createListResource({
	doctype: 'LMS Quiz Submission',
	filters: {
		quiz: props.quizID,
	},
	fields: ['name', 'member_name', 'score', 'percentage', 'quiz_title'],
	orderBy: 'creation desc',
	auto: true,
})

const quizColumns = computed(() => {
	return [
		{
			label: __('Member'),
			key: 'member_name',
			width: 1,
		},
		{
			label: __('Score'),
			key: 'score',
			width: 1,
			align: 'center',
		},
		{
			label: __('Percentage'),
			key: 'percentage',
			width: 1,
			align: 'center',
		},
	]
})

const breadcrumbs = computed(() => {
	return [{ label: __('Quiz Submissions') }]
})

usePageMeta(() => {
	return {
		title: __('Quiz Submissions'),
		icon: brand.favicon,
	}
})
</script>
