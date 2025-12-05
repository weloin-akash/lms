<template>
	<!-- <header
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-4">
				<div class="w-10 h-10 bg-[#ed8e22] rounded-xl flex items-center justify-center">
					<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
					</svg>
				</div>
				<div>
					<h1 class="text-2xl font-bold text-gray-900">
						{{ submissionDetails.doc?.quiz_title || __('Quiz Submission') }}
					</h1>
					<p class="text-gray-600 text-sm">Grade student quiz submission</p>
				</div>
			</div>
			<div class="flex items-center space-x-3">
				<Badge
					v-if="submissionDetails.isDirty"
					class="bg-orange-100 text-[#ed8e22] border border-orange-200"
				>
					{{ __('Not Saved') }}
				</Badge>
				<Button class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium" @click="saveSubmission()">
					{{ __('Save') }}
				</Button>
			</div>
		</div>
	</header> -->
	<AppHeader description="Grade student quiz submission" :breadcrumbs="breadcrumbs">
		<template #icon>
			<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
			</svg>
		</template>
		<!-- <template #breadcrumbs>
			<Breadcrumbs :items="breadcrumbs" />
		</template> -->
		<template #actions>
			<Badge
					v-if="submissionDetails.isDirty"
					class="bg-orange-100 text-[#ed8e22] border border-orange-200"
				>
					{{ __('Not Saved') }}
				</Badge>
			<Button class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium" @click="saveSubmission()">
				{{ __('Save') }}
			</Button>
		</template>
	</AppHeader>
	<div v-if="submissionDetails.doc" class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
		<div class="max-w-4xl mx-auto">
			<!-- Submission Details Card -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
				<div class="flex items-center space-x-3 mb-6">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
						</svg>
					</div>
					<div>
						<h2 class="text-xl font-bold text-gray-900">{{ submissionDetails.doc.member_name }}</h2>
						<p class="text-gray-600 text-sm">Submission details and score</p>
					</div>
				</div>
				<div class="grid grid-cols-2 gap-8">
					<div class="space-y-6">
						<FormControl
							v-model="submissionDetails.doc.quiz_title"
							:label="__('Quiz Title')"
							:disabled="true"
							class="rounded-lg border-gray-300 bg-gray-50"
						/>
						<FormControl
							v-model="submissionDetails.doc.member_name"
							:label="__('Student Name')"
							:disabled="true"
							class="rounded-lg border-gray-300 bg-gray-50"
						/>
					</div>
					<div class="space-y-6">
						<FormControl
							v-model="submissionDetails.doc.score"
							:label="__('Score')"
							:disabled="true"
							class="rounded-lg border-gray-300 bg-gray-50"
						/>
						<FormControl
							v-model="submissionDetails.doc.percentage"
							:label="__('Percentage')"
							:disabled="true"
							class="rounded-lg border-gray-300 bg-gray-50"
						/>
					</div>
				</div>
			</div>

			<!-- Questions and Answers -->
			<div class="space-y-6">
				<div
					v-for="(row, index) in submissionDetails.doc.result"
					:key="index"
					class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8"
				>
					<div class="flex items-center space-x-3 mb-6">
						<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
							<span class="text-sm font-bold text-[#ed8e22]">{{ index + 1 }}</span>
						</div>
						<h3 class="text-lg font-semibold text-gray-900">{{ __('Question {0}').format(index + 1) }}</h3>
					</div>
					
					<!-- Question -->
					<div class="mb-6">
						<div class="bg-gray-50 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-gray-700 mb-2">{{ __('Question') }}</h4>
							<div class="text-gray-900 leading-relaxed" v-html="row.question || ''"></div>
						</div>
					</div>

					<!-- Answer -->
					<div class="mb-6">
						<div class="bg-blue-50 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-gray-700 mb-2">{{ __('Student Answer') }}</h4>
							<div class="text-gray-900 leading-relaxed" v-html="row.answer || ''"></div>
						</div>
					</div>

					<!-- Grading -->
					<div class="grid grid-cols-2 gap-6">
						<FormControl 
							v-model="row.marks" 
							:label="__('Marks Awarded')" 
							type="number"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
						<FormControl
							v-model="row.marks_out_of"
							:label="__('Total Marks')"
							:disabled="true"
							class="rounded-lg border-gray-300 bg-gray-50"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	createDocumentResource,
	Breadcrumbs,
	FormControl,
	Button,
	Badge,
	usePageMeta,
	toast,
} from 'frappe-ui'
import { computed, onBeforeUnmount, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const router = useRouter()
const user = inject('$user')

onMounted(() => {
	if (!user.data?.is_instructor && !user.data?.is_moderator)
		router.push({ name: 'Courses' })

	window.addEventListener('keydown', keyboardShortcut)
})

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

const keyboardShortcut = (e) => {
	if (
		e.key === 's' &&
		(e.ctrlKey || e.metaKey) &&
		!e.target.classList.contains('ProseMirror')
	) {
		saveSubmission()
		e.preventDefault()
	}
}

const props = defineProps({
	submission: {
		type: String,
		required: true,
	},
})

const submissionDetails = createDocumentResource({
	doctype: 'LMS Quiz Submission',
	name: props.submission,
	auto: true,
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Quiz Submissions'),
			route: {
				name: 'QuizSubmissionList',
				params: {
					quizID: submissionDetails.doc.quiz,
				},
			},
		},
		{
			label: submissionDetails.doc.quiz_title,
		},
	]
})

const saveSubmission = () => {
	submissionDetails.save.submit(
		{},
		{
			onSuccess() {
				toast.success(__('Submission saved successfully.'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

usePageMeta(() => {
	return {
		title: `${submissionDetails.doc?.quiz_title}`,
		icon: brand.favicon,
	}
})
</script>
