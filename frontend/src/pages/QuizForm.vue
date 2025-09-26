<template>
	<AppHeader >
		<template #breadcrumbs>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #icon>
			<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
		</template>
		<template #actions>
			<div v-if="!readOnlyMode" class="flex items-center space-x-3">
				<Badge v-if="quizDetails.isDirty" theme="orange">
					{{ __('Not Saved') }}
				</Badge>
				<router-link
					v-if="quizDetails.doc?.name"
					:to="{
						name: 'QuizPage',
						params: {
							quizID: quizDetails.doc.name,
						},
					}"
				>
					<Button class="!bg-white hover:!bg-gray-50 !text-gray-700 !border-gray-300 hover:!border-gray-400 shadow-sm hover:shadow transition-all duration-200 px-4 py-2 rounded-lg font-medium">
						<template #prefix>
							<ListChecks class="size-4 stroke-1.5" />
						</template>
						{{ __('Test Quiz') }}
					</Button>
				</router-link>
				<router-link
					v-if="quizDetails.doc?.name"
					:to="{
						name: 'QuizSubmissionList',
						params: {
							quizID: quizDetails.doc.name,
						},
					}"
				>
					<Button class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium !border-0">
						<template #prefix>
							<ClipboardList class="size-4 stroke-1.5" />
						</template>
						{{ __('Check Submissions') }}
					</Button>
				</router-link>
				<Button class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium !border-0" @click="submitQuiz()">
					<template #prefix>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</template>
					{{ __('Save') }}
				</Button>
			</div>
		</template>
	</AppHeader>
	<div v-if="quizDetails.doc" class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
		<!-- Quiz Details Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Quiz Details') }}</h2>
			</div>
			<div class="grid grid-cols-2 gap-8">
				<div class="space-y-6">
					<FormControl
						v-model="quizDetails.doc.title"
						:label="__('Quiz Title')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						type="number"
						v-model="quizDetails.doc.max_attempts"
						:label="__('Maximum Attempts')"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						type="number"
						v-model="quizDetails.doc.duration"
						:label="__('Duration (in minutes)')"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>
				<div class="space-y-6">
					<FormControl
						v-model="quizDetails.doc.total_marks"
						:label="__('Total Marks')"
						disabled
						class="rounded-lg border-gray-300 bg-gray-50"
					/>
					<FormControl
						v-model="quizDetails.doc.passing_percentage"
						:label="__('Passing Percentage')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>
			</div>
		</div>
		<!-- Quiz Settings Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Quiz Settings') }}</h2>
			</div>
			<div class="grid grid-cols-3 gap-8">
				<div class="space-y-6">
					<div class="bg-gray-50 rounded-lg p-4">
						<h3 class="text-sm font-semibold text-gray-700 mb-3">Display Options</h3>
						<div class="space-y-4">
							<FormControl
								v-model="quizDetails.doc.show_answers"
								type="checkbox"
								:label="__('Show Answers')"
							/>
							<FormControl
								v-model="quizDetails.doc.show_submission_history"
								type="checkbox"
								:label="__('Show Submission History')"
							/>
						</div>
					</div>
				</div>
				<div class="space-y-6">
					<div class="bg-gray-50 rounded-lg p-4">
						<h3 class="text-sm font-semibold text-gray-700 mb-3">Question Options</h3>
						<div class="space-y-4">
							<FormControl
								v-model="quizDetails.doc.shuffle_questions"
								type="checkbox"
								:label="__('Shuffle Questions')"
							/>
							<FormControl
								v-if="quizDetails.doc.shuffle_questions"
								v-model="quizDetails.doc.limit_questions_to"
								:label="__('Limit Questions To')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
							/>
						</div>
					</div>
				</div>
				<div class="space-y-6">
					<div class="bg-gray-50 rounded-lg p-4">
						<h3 class="text-sm font-semibold text-gray-700 mb-3">Scoring Options</h3>
						<div class="space-y-4">
							<FormControl
								v-model="quizDetails.doc.enable_negative_marking"
								type="checkbox"
								:label="__('Enable Negative Marking')"
							/>
							<FormControl
								v-if="quizDetails.doc.enable_negative_marking"
								v-model="quizDetails.doc.marks_to_cut"
								:label="__('Marks to Deduct')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
							/>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Questions Section -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8">
			<div class="flex items-center justify-between mb-6">
				<div class="flex items-center space-x-3">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<div>
						<h2 class="text-xl font-bold text-gray-900">{{ __('Questions') }}</h2>
						<p class="text-gray-600 text-sm">{{ questions.length }} questions added</p>
					</div>
				</div>
				<Button 
					v-if="!readOnlyMode" 
					class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0"
					@click="openQuestionModal()"
				>
					<template #prefix>
						<Plus class="w-4 h-4" />
					</template>
					{{ __('Add Question') }}
				</Button>
			</div>
			
			<!-- Questions List -->
			<div v-if="questions.length" class="space-y-4">
				<div 
					v-for="(question, index) in questions" 
					:key="question.name"
					class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors duration-200 cursor-pointer group"
					@click="openQuestionModal(question)"
				>
					<div class="flex items-center justify-between">
						<div class="flex-1">
							<div class="flex items-center space-x-3 mb-2">
								<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-[#ed8e22]">
									Question {{ index + 1 }}
								</span>
								<span class="text-sm font-medium text-gray-900">{{ question.marks }} marks</span>
							</div>
							<div 
								class="text-sm text-gray-700 truncate group-hover:text-[#ed8e22] transition-colors duration-200"
								v-html="question.question_detail || question.question"
							></div>
						</div>
						<div class="flex items-center space-x-2">
							<Button 
								variant="ghost" 
								size="sm"
								class="opacity-0 group-hover:opacity-100 transition-opacity duration-200"
								@click.stop="deleteQuestions([question.name], () => {})"
							>
								<Trash2 class="h-4 w-4 text-red-500" />
							</Button>
						</div>
					</div>
				</div>
			</div>
			
			<!-- Empty State -->
			<div v-else class="text-center py-12">
				<div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
					<svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<h3 class="text-lg font-semibold text-gray-900 mb-2">No questions added yet</h3>
				<p class="text-gray-600 mb-6">Get started by adding your first quiz question</p>
				<Button 
					v-if="!readOnlyMode" 
					class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0"
					@click="openQuestionModal()"
				>
					<template #prefix>
						<Plus class="w-4 h-4" />
					</template>
					{{ __('Add Your First Question') }}
				</Button>
			</div>
		</div>
	</div>

	<Question
		v-model="showQuestionModal"
		:questionDetail="currentQuestion"
		v-model:quiz="quizDetails"
		:title="
			currentQuestion.question
				? __('Edit the question')
				: __('Add a new question')
		"
	/>
</template>
<script setup>
import {
	Breadcrumbs,
	createResource,
	FormControl,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListRows,
	ListRow,
	ListRowItem,
	ListSelectBanner,
	Button,
	usePageMeta,
	toast,
	createDocumentResource,
	Badge,
} from 'frappe-ui'
import AppHeader from '@/components/AppHeader.vue'
import {
	computed,
	reactive,
	ref,
	onMounted,
	inject,
	onBeforeUnmount,
	watch,
} from 'vue'
import { sessionStore } from '../stores/session'
import { ClipboardList, ListChecks, Plus, Trash2 } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import Question from '@/components/Modals/Question.vue'

const { brand } = sessionStore()
const showQuestionModal = ref(false)
const currentQuestion = reactive({
	question: '',
	marks: 0,
	name: '',
})
const user = inject('$user')
const router = useRouter()
const readOnlyMode = window.read_only_mode

const props = defineProps({
	quizID: {
		type: String,
		required: true,
	},
})

const questions = ref([])

onMounted(() => {
	if (
		props.quizID == 'new' &&
		!user.data?.is_moderator &&
		!user.data?.is_instructor
	) {
		router.push({ name: 'Courses' })
	}
	if (props.quizID !== 'new') {
		quizDetails.reload()
	}
	window.addEventListener('keydown', keyboardShortcut)
})

const keyboardShortcut = (e) => {
	if (e.key === 's' && (e.ctrlKey || e.metaKey)) {
		submitQuiz()
		e.preventDefault()
	}
}

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

watch(
	() => props.quizID !== 'new',
	(newVal) => {
		if (newVal) {
			quizDetails.reload()
		}
	}
)

const quizDetails = createDocumentResource({
	doctype: 'LMS Quiz',
	name: props.quizID,
	auto: false,
	onSuccess(doc) {
		if (doc.questions && doc.questions.length > 0) {
			questions.value = doc.questions.map((question) => question)
		}
	},
})

const submitQuiz = () => {
	quizDetails.setValue.submit(
		{
			...quizDetails.doc,
			total_marks: calculateTotalMarks(),
		},
		{
			onSuccess(data) {
				quizDetails.doc.total_marks = data.total_marks
				toast.success(__('Quiz updated successfully'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const calculateTotalMarks = () => {
	let totalMarks = 0
	if (
		quizDetails.doc?.limit_questions_to &&
		quizDetails.doc?.questions.length > 0
	)
		return (
			quizDetails.doc.questions[0].marks * quizDetails.doc.limit_questions_to
		)

	quizDetails.doc?.questions.forEach((question) => {
		totalMarks += question.marks
	})
	return totalMarks
}

const questionColumns = computed(() => {
	return [
		{
			label: __('ID'),
			key: 'question',
			width: '10rem',
		},
		{
			label: __('Question'),
			key: __('question_detail'),
			width: '40rem',
		},
		{
			label: __('Marks'),
			key: 'marks',
			width: '5rem',
		},
	]
})

const openQuestionModal = (question = null) => {
	if (question) {
		currentQuestion.question = question.question
		currentQuestion.marks = question.marks
		currentQuestion.name = question.name
	} else {
		currentQuestion.question = ''
		currentQuestion.marks = 0
		currentQuestion.name = ''
	}
	showQuestionModal.value = true
}

const deleteQuestionResource = createResource({
	url: 'lms.lms.api.delete_documents',
	makeParams(values) {
		return {
			doctype: 'LMS Quiz Question',
			documents: values.questions,
		}
	},
})

const deleteQuestions = (selections, unselectAll) => {
	deleteQuestionResource.submit(
		{
			questions: Array.from(selections),
		},
		{
			onSuccess() {
				toast.success(__('Questions deleted successfully'))
				quizDetails.reload()
				unselectAll()
			},
		}
	)
}

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: __('Quizzes'),
			route: {
				name: 'Quizzes',
			},
		},
	]

	crumbs.push({
		label: props.quizID == 'new' ? __('New Quiz') : quizDetails.doc?.title,
		route: { name: 'QuizForm', params: { quizID: props.quizID } },
	})
	return crumbs
})

usePageMeta(() => {
	return {
		title: props.quizID == 'new' ? __('New Quiz') : quizDetails.doc?.title,
		icon: brand.favicon,
	}
})
</script>
