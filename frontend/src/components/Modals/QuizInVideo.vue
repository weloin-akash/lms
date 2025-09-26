<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Add quiz to this video'),
			size: '2xl',
		}"
	>
		<template #body-title>
			<div class="flex items-center space-x-3 bg-[#fef9f3] px-6 py-4 border-b border-gray-200/50">
				<div class="w-10 h-10 bg-[#ed8e22] rounded-xl flex items-center justify-center">
					<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1a3 3 0 000-6h-1m0 6V4m0 6v6m6-10h1a3 3 0 000-6h-1m0 6V4m0 6v6" />
					</svg>
				</div>
				<div>
					<h2 class="text-xl font-bold text-gray-900">{{ __('Add quiz to this video') }}</h2>
					<p class="text-gray-600 text-sm">Configure quiz timing and selection</p>
				</div>
			</div>
		</template>
		<template #body-content>
			<div class="px-6 py-6">
				<!-- Add Quiz Form -->
				<div class="bg-white rounded-lg border border-gray-200 p-6 mb-8">
					<div class="flex items-end gap-4">
						<FormControl
							:label="__('Time in Video')"
							v-model="quiz.time"
							type="text"
							placeholder="2:15"
							class="flex-1 rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
						<Link
							v-model="quiz.quiz"
							:label="__('Quiz')"
							doctype="LMS Quiz"
							class="flex-1 rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
						<Button @click="addQuiz()" class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium">
							<template #prefix>
								<Plus class="w-4 h-4" />
							</template>
							{{ __('Add Quiz') }}
						</Button>
					</div>
				</div>

				<!-- Quizzes List -->
				<div>
					<div class="flex items-center space-x-3 mb-6">
						<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
							<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
							</svg>
						</div>
						<h3 class="text-lg font-semibold text-gray-900">{{ __('Quizzes in this video') }}</h3>
					</div>

					<div v-if="allQuizzes.length" class="space-y-4">
						<div 
							v-for="(quiz, index) in allQuizzes" 
							:key="quiz.quiz"
							class="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors duration-200 group"
						>
							<div class="flex items-center justify-between">
								<div class="flex-1">
									<div class="flex items-center space-x-3 mb-2">
										<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-[#ed8e22]">
											{{ formatTimestamp(quiz.time) }}
										</span>
										<span class="text-sm font-medium text-gray-900">{{ quiz.quiz }}</span>
									</div>
								</div>
								<div class="flex items-center space-x-2">
									<Button 
										variant="ghost" 
										size="sm"
										class="opacity-0 group-hover:opacity-100 transition-opacity duration-200"
										@click="removeQuiz([quiz.quiz], () => {})"
									>
										<Trash2 class="h-4 w-4 text-red-500" />
									</Button>
								</div>
							</div>
						</div>
					</div>

					<div v-else class="text-center py-8">
						<div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
							<svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
							</svg>
						</div>
						<p class="text-gray-500 text-sm">{{ __('No quizzes added yet.') }}</p>
					</div>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup lang="ts">
import {
	Dialog,
	Button,
	FormControl,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListRows,
	ListRow,
	ListRowItem,
	ListSelectBanner,
	toast,
} from 'frappe-ui'
import { computed, reactive, ref, watch } from 'vue'
import { Plus, Trash2 } from 'lucide-vue-next'
import { formatTimestamp } from '@/utils'
import Link from '@/components/Controls/Link.vue'

type Quiz = {
	time: string
	quiz: string
}

const show = defineModel()
const allQuizzes = ref<Quiz[]>([])
const quiz = reactive<Quiz>({
	time: '',
	quiz: '',
})

const props = defineProps({
	quizzes: {
		type: Array as () => Quiz[],
		default: () => [],
	},
	saveQuizzes: {
		type: Function,
		required: true,
	},
	duration: {
		type: Number,
		default: 0,
	},
})

const addQuiz = () => {
	quiz.time = `${getTimeInSeconds()}`
	if (!isTimeValid() || !isFormComplete()) return

	allQuizzes.value.push({
		time: quiz.time,
		quiz: quiz.quiz,
	})

	props.saveQuizzes(allQuizzes.value)

	quiz.time = ''
	quiz.quiz = ''
}

const getTimeInSeconds = () => {
	if (quiz.time && !quiz.time.includes(':')) {
		quiz.time = `${quiz.time}:00`
	}
	const timeParts = quiz.time.split(':')
	const timeInSeconds = parseInt(timeParts[0]) * 60 + parseInt(timeParts[1])

	return timeInSeconds
}

const isTimeValid = () => {
	if (parseInt(quiz.time) > props.duration) {
		toast.error(__('Time in video exceeds the total duration of the video.'))
		return false
	}
	return true
}

const isFormComplete = () => {
	if (!quiz.time) {
		toast.error(__('Please enter a valid timestamp'))
		return false
	}

	if (!quiz.quiz) {
		toast.error(__('Please select a quiz'))
		return false
	}

	return true
}

const removeQuiz = (selections: string, unselectAll: () => void) => {
	Array.from(selections).forEach((selection) => {
		const index = allQuizzes.value.findIndex((q) => q.quiz === selection)
		if (index !== -1) {
			allQuizzes.value.splice(index, 1)
		}
		unselectAll()
	})
	props.saveQuizzes(allQuizzes.value)
}

watch(
	() => props.quizzes,
	(newQuizzes) => {
		allQuizzes.value = newQuizzes
	},
	{ immediate: true }
)

const columns = computed(() => {
	return [
		{
			key: 'quiz',
			label: __('Quiz'),
		},
		{
			key: 'time',
			label: __('Time in Video (minutes)'),
			align: 'center',
		},
	]
})
</script>
