<template>
	<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 overflow-hidden">
		<!-- Modern Header -->
		<div class="bg-[#fef9f3] px-6 py-4 border-b border-gray-200/50">
			<div class="flex items-center justify-between">
				<div class="flex items-center space-x-3">
					<div class="w-8 h-8 bg-[#ed8e22] rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
						</svg>
					</div>
					<div>
						<h3 class="text-lg font-semibold text-gray-900">{{ __('Assessments') }}</h3>
						<p class="text-sm text-gray-600">Manage assignments, quizzes, and evaluations</p>
					</div>
				</div>
				<Button 
					v-if="canAddAssessments()" 
					@click="showModal = true"
					class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium !border-0"
				>
					<template #prefix>
						<Plus class="h-4 w-4" />
					</template>
					{{ __('Add Assessment') }}
				</Button>
			</div>
		</div>
		<!-- Assessments Content -->
		<ListView
			v-if="assessments.data?.length"
			:columns="assessmentColumns"
			:rows="assessments.data"
			row-key="name"
			:options="{ showTooltip: false, selectable: canAddAssessments() }"
			class="modern-assessment-list"
		>
			<ListHeader class="border-b border-gray-200 bg-gray-50 py-3">
				<ListHeaderItem :item="item" v-for="item in assessmentColumns">
					<template #prefix="{ item }">
						<div class="w-6 h-6 bg-orange-100 rounded-lg flex items-center justify-center mr-2">
							<svg v-if="item.key === 'title'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
							</svg>
							<svg v-else-if="item.key === 'assessment_type'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
							</svg>
							<svg v-else class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
							</svg>
						</div>
					</template>
				</ListHeaderItem>
			</ListHeader>
			<ListRows>
				<router-link
					v-for="row in assessments.data"
					:key="row.name"
					:to="getRowRoute(row)"
					class="block"
				>
					<ListRow :row="row" class="hover:bg-gray-50 transition-colors duration-200 group border-b border-gray-100 py-3">
						<template #default="{ column, item }">
							<ListRowItem :item="row[column.key]" :align="column.align">
								<div v-if="column.key == 'title'" class="flex items-center space-x-3">
									<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center flex-shrink-0">
										<svg v-if="row.assessment_type === 'LMS Assignment'" class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
										</svg>
										<svg v-else-if="row.assessment_type === 'LMS Quiz'" class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
										<svg v-else class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
										</svg>
									</div>
									<span class="font-medium text-gray-900 group-hover:text-[#ed8e22] transition-colors">{{ item }}</span>
								</div>
								<div v-else-if="column.key == 'assessment_type'" class="text-center">
									<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-[#ed8e22]">
										{{ getAssessmentTypeLabel(item) }}
									</span>
								</div>
								<div v-else-if="column.key == 'status'" class="text-center">
									<div v-if="!user.data?.is_moderator && item && isNaN(item)">
										<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border"
											:class="{
												'bg-green-100 text-green-800 border-green-200': getStatusTheme(item) === 'green',
												'bg-blue-100 text-blue-800 border-blue-200': getStatusTheme(item) === 'blue',
												'bg-red-100 text-red-800 border-red-200': getStatusTheme(item) === 'red',
												'bg-orange-100 text-orange-800 border-orange-200': getStatusTheme(item) === 'orange'
											}"
										>
											{{ item }}
										</span>
									</div>
									<div v-else-if="!user.data?.is_moderator && item && !isNaN(item)">
										<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 border border-blue-200">
											{{ item }}%
										</span>
									</div>
									<span v-else class="text-sm text-gray-500">-</span>
								</div>
								<div v-else>{{ item }}</div>
							</ListRowItem>
						</template>
					</ListRow>
				</router-link>
			</ListRows>
			<ListSelectBanner>
				<template #actions="{ unselectAll, selections }">
					<div class="flex gap-2">
						<Button
							variant="ghost"
							@click="removeAssessments(selections, unselectAll)"
							class="text-red-600 hover:bg-red-50"
						>
							<template #prefix>
								<Trash2 class="w-4 h-4" />
							</template>
							{{ __('Delete') }}
						</Button>
					</div>
				</template>
			</ListSelectBanner>
		</ListView>
		
		<!-- Empty State -->
		<div v-else class="p-12 text-center">
			<div class="max-w-md mx-auto">
				<div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
					<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
					</svg>
				</div>
				<h3 class="text-lg font-semibold text-gray-900 mb-2">No Assessments Available</h3>
				<p class="text-gray-600">There are no assessments configured for this batch yet.</p>
			</div>
		</div>
	</div>
	<AssessmentModal
		v-model="showModal"
		v-model:assessments="assessments"
		:batch="props.batch"
	/>
</template>
<script setup>
import {
	ListView,
	ListRow,
	ListRows,
	ListHeader,
	ListHeaderItem,
	ListRowItem,
	ListSelectBanner,
	createResource,
	Button,
	Badge,
} from 'frappe-ui'
import { inject, ref, computed } from 'vue'
import AssessmentModal from '@/components/Modals/AssessmentModal.vue'
import { Plus, Trash2 } from 'lucide-vue-next'

const user = inject('$user')
const showModal = ref(false)
const readOnlyMode = window.read_only_mode

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
	rows: {
		type: Array,
	},
	columns: {
		type: Array,
	},
	options: {
		type: Object,
		default: () => ({
			selectable: true,
			totalCount: 0,
			rowCount: 0,
		}),
	},
})

const assessments = createResource({
	url: 'lms.lms.utils.get_assessments',
	params: {
		batch: props.batch,
	},
	auto: true,
})

const deleteAssessments = createResource({
	url: 'lms.lms.api.delete_documents',
	makeParams(values) {
		return {
			doctype: 'LMS Assessment',
			documents: values.assessments,
		}
	},
})

const removeAssessments = (selections, unselectAll) => {
	deleteAssessments.submit(
		{ assessments: Array.from(selections) },
		{
			onSuccess(data) {
				assessments.reload()
				unselectAll()
			},
		}
	)
}

const getRowRoute = (row) => {
	if (user.data?.is_evaluator && !user.data?.is_student) {
		if (row.assessment_type == 'LMS Assignment') {
			return {
				name: 'AssignmentSubmissionList',
				query: {
					assignmentID: row.assessment_name,
				},
			}
		} else if (row.assessment_type == 'LMS Programming Exercise') {
			return {
				name: 'ProgrammingExerciseSubmissions',
			}
		} else {
			return {
				name: 'QuizSubmissionList',
				params: {
					quizID: row.assessment_name,
				},
			}
		}
	}

	// For students and moderators, handle submission creation/viewing
	if (row.assessment_type == 'LMS Assignment') {
		if (row.submission) {
			return {
				name: 'AssignmentSubmission',
				params: {
					assignmentID: row.assessment_name,
					submissionName: row.submission.name,
				},
			}
		} else {
			return {
				name: 'AssignmentSubmission',
				params: {
					assignmentID: row.assessment_name,
					submissionName: 'new',
				},
			}
		}
	} else if (row.assessment_type == 'LMS Programming Exercise') {
		if (row.submission) {
			return {
				name: 'ProgrammingExerciseSubmission',
				params: {
					exerciseID: row.assessment_name,
					submissionID: row.submission.name,
				},
			}
		} else {
			return {
				name: 'ProgrammingExerciseSubmission',
				params: {
					exerciseID: row.assessment_name,
					submissionID: 'new',
				},
			}
		}
	} else {
		return {
			name: 'QuizPage',
			params: {
				quizID: row.assessment_name,
			},
		}
	}
}

const canAddAssessments = () => {
	if (readOnlyMode) return false
	return user.data?.is_moderator || user.data?.is_evaluator
}

const assessmentColumns = computed(() => {
	let columns = [
		{
			label: __('Assessment'),
			key: 'title',
			width: 2,
		},
		{
			label: __('Type'),
			key: 'assessment_type',
			width: 1,
			align: 'center',
		},
	]

	if (!user.data?.is_moderator) {
		columns.push({
			label: __('Status/Percentage'),
			key: 'status',
			align: 'center',
			width: 1,
		})
	}
	return columns
})

const getStatusTheme = (status) => {
	if (status === 'Pass' || status === 'Passed') {
		return 'green'
	} else if (status === 'Not Graded') {
		return 'orange'
	} else {
		return 'red'
	}
}

const getAssessmentTypeLabel = (type) => {
	if (type == 'LMS Assignment') {
		return __('Assignment')
	} else if (type == 'LMS Quiz') {
		return __('Quiz')
	} else if (type == 'LMS Programming Exercise') {
		return __('Programming Exercise')
	}
}

</script>
