<template>
	<div v-if="batch.data" class="">
		<div class="w-full flex items-center justify-between pb-4">
			<div class="font-medium text-ink-gray-7">
				{{ __('Statistics') }}
			</div>
		</div>
		<div class="grid grid-cols-2 md:grid-cols-4 gap-5 mb-8">
			<NumberChart
				class="border rounded-md"
				:config="{ title: __('Students'), value: students.data?.length || 0 }"
			/>

			<NumberChart
				class="border rounded-md"
				:config="{
					title: __('Certified'),
					value: certificationCount.data || 0,
				}"
			/>

			<NumberChart
				class="border rounded-md"
				:config="{
					title: __('Courses'),
					value: batch.data.courses?.length || 0,
				}"
			/>

			<NumberChart
				class="border rounded-md"
				:config="{ title: __('Assessments'), value: assessmentCount || 0 }"
			/>
		</div>

		<AxisChart
			v-if="showProgressChart"
			:config="{
				data: chartData,
				title: __('Batch Summary'),
				subtitle: __('Progress of students in courses and assessments'),
				xAxis: {
					key: 'task',
					title: 'Tasks',
					type: 'category',
				},
				yAxis: {
					title: __('Number of Students'),
					echartOptions: {
						minInterval: 1,
					},
				},
				swapXY: true,
				series: [
					{
						name: 'value',
						type: 'bar',
					},
				],
			}"
		/>
	</div>

	<!-- Students Section -->
	<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6">
		<div class="flex items-center justify-between mb-6">
			<div class="flex items-center space-x-3">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
					</svg>
				</div>
				<div>
					<h2 class="text-xl font-bold text-gray-900">{{ __('Students') }}</h2>
					<p class="text-sm text-gray-600">
						{{ students.data?.length ? `${students.data.length} students enrolled` : 'No students enrolled yet' }}
					</p>
				</div>
			</div>
			<Button 
				v-if="!readOnlyMode" 
				@click="openStudentModal()"
				class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium !border-0"
			>
				<template #prefix>
					<Plus class="h-4 w-4" />
				</template>
				{{ __('Add') }}
			</Button>
		</div>

		<div v-if="students.data?.length">
			<ListView
				:columns="getStudentColumns()"
				:rows="students.data"
				row-key="name"
				:options="{
					showTooltip: false,
					selectable: true,
				}"
				class="modern-student-list"
			>
				<ListHeader class="border-b border-gray-200 bg-gray-50 py-3">
					<ListHeaderItem
						:item="item"
						v-for="item in getStudentColumns()"
					>
						<template #prefix="{ item }">
							<div class="w-6 h-6 bg-orange-100 rounded-lg flex items-center justify-center mr-2">
								<svg v-if="item.key === 'full_name'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
								</svg>
								<svg v-else-if="item.key === 'progress'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
								</svg>
								<svg v-else class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
						</template>
					</ListHeaderItem>
				</ListHeader>
				<ListRows>
					<ListRow
						:row="row"
						v-for="row in students.data"
						class="hover:bg-gray-50 transition-colors duration-200 group cursor-pointer border-b border-gray-100 py-3"
						@click="openStudentProgressModal(row)"
					>
						<template #default="{ column, item }">
							<ListRowItem
								:item="row[column.key]"
								:align="column.align"
							>
								<div v-if="column.key == 'full_name'" class="flex items-center space-x-3">
									<Avatar
										class="flex items-center flex-shrink-0"
										:image="row['user_image']"
										:label="item"
										size="md"
									/>
									<span class="font-medium text-gray-900 group-hover:text-[#ed8e22] transition-colors">{{ item }}</span>
								</div>
								<div
									v-else-if="column.key == 'progress'"
									class="flex items-center space-x-3 w-full"
								>
									<div class="flex-1">
										<ProgressBar :progress="row[column.key]" size="md" />
									</div>
									<div class="text-sm font-medium text-gray-700 min-w-[3rem] text-right">{{ row[column.key] }}%</div>
								</div>
								<div v-else-if="column.key == 'last_active'" class="text-center">
									<span class="text-sm text-gray-700">{{ row[column.key] }}</span>
								</div>
								<div v-else>
									{{ row[column.key] }}
								</div>
							</ListRowItem>
						</template>
					</ListRow>
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="removeStudents(selections, unselectAll)"
								class="text-red-600 hover:bg-red-50"
							>
								<template #prefix>
									<Trash2 class="h-4 w-4 stroke-1.5" />
								</template>
								{{ __('Remove') }}
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>
		
		<!-- Empty State -->
		<div v-else class="text-center py-12">
			<div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
				<svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
				</svg>
			</div>
			<h3 class="text-lg font-semibold text-gray-900 mb-2">{{ __('No students in this batch') }}</h3>
			<p class="text-gray-600 mb-6">{{ __('Get started by adding your first student to this batch') }}</p>
			<Button 
				v-if="!readOnlyMode" 
				@click="openStudentModal()"
				class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium !border-0"
			>
				<template #prefix>
					<Plus class="h-4 w-4" />
				</template>
				{{ __('Add Your First Student') }}
			</Button>
		</div>
	</div>

	<StudentModal
		:batch="props.batch.data.name"
		v-model="showStudentModal"
		v-model:reloadStudents="students"
		v-model:batchModal="props.batch"
	/>
	<BatchStudentProgress
		:student="selectedStudent"
		v-model="showStudentProgressModal"
	/>
</template>
<script setup>
import {
	Avatar,
	AxisChart,
	Button,
	createResource,
	FeatherIcon,
	ListHeader,
	ListHeaderItem,
	ListSelectBanner,
	ListRow,
	ListRows,
	ListView,
	ListRowItem,
	NumberChart,
	toast,
} from 'frappe-ui'
import {
	BookOpen,
	GraduationCap,
	Plus,
	ShieldCheck,
	Trash2,
	User,
} from 'lucide-vue-next'
import { ref, watch } from 'vue'
import StudentModal from '@/components/Modals/StudentModal.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import BatchStudentProgress from '@/components/Modals/BatchStudentProgress.vue'
import ApexChart from 'vue3-apexcharts'
import { theme } from '@/utils/theme'

const showStudentModal = ref(false)
const showStudentProgressModal = ref(false)
const selectedStudent = ref(null)
const chartData = ref(null)
const showProgressChart = ref(false)
const assessmentCount = ref(0)
const readOnlyMode = window.read_only_mode

const props = defineProps({
	batch: {
		type: Object,
		default: null,
	},
})

const students = createResource({
	url: 'lms.lms.utils.get_batch_students',
	params: {
		batch: props.batch?.data?.name,
	},
	auto: true,
	onSuccess(data) {
		chartData.value = getChartData()
		showProgressChart.value =
			data.length &&
			(props.batch?.data?.courses?.length || assessmentCount.value)
	},
})

const getStudentColumns = () => {
	let columns = [
		{
			label: 'Full Name',
			key: 'full_name',
			width: 2,
			icon: 'user',
		},
		{
			label: 'Progress',
			key: 'progress',
			width: 2,
			icon: 'activity',
		},
		{
			label: 'Last Active',
			key: 'last_active',
			width: 1,
			align: 'center',
			icon: 'clock',
		},
	]

	return columns
}

const openStudentModal = () => {
	showStudentModal.value = true
}

const openStudentProgressModal = (row) => {
	showStudentProgressModal.value = true
	selectedStudent.value = row
}

const deleteStudents = createResource({
	url: 'lms.lms.api.delete_documents',
	makeParams(values) {
		return {
			doctype: 'LMS Batch Enrollment',
			documents: values.students,
		}
	},
})

const removeStudents = (selections, unselectAll) => {
	deleteStudents.submit(
		{
			students: Array.from(selections),
		},
		{
			onSuccess(data) {
				students.reload()
				props.batch.reload()
				toast.success(__('Students deleted successfully'))
				unselectAll()
			},
		}
	)
}

const getChartData = () => {
	let tasks = []
	let data = []

	students.data.forEach((row) => {
		tasks = countAssessments(row, tasks)
		tasks = countCourses(row, tasks)
	})

	tasks.forEach((task) => {
		data.push({
			task: task.label,
			value: task.value,
		})
	})
	return data
}

const countAssessments = (row, tasks) => {
	Object.keys(row.assessments).forEach((assessment) => {
		if (row.assessments[assessment].result === 'Pass') {
			tasks.filter((task) => task.label === assessment).length
				? tasks.filter((task) => task.label === assessment)[0].value++
				: tasks.push({
						value: 1,
						label: assessment,
				  })
		}
	})
	return tasks
}

const countCourses = (row, tasks) => {
	Object.keys(row.courses).forEach((course) => {
		if (row.courses[course] === 100) {
			tasks.filter((task) => task.label === course).length
				? tasks.filter((task) => task.label === course)[0].value++
				: tasks.push({
						value: 1,
						label: course,
				  })
		}
	})
	return tasks
}

watch(students, () => {
	if (students.data?.length) {
		assessmentCount.value = Object.keys(students.data?.[0].assessments).length
	}
})

const certificationCount = createResource({
	url: 'frappe.client.get_count',
	params: {
		doctype: 'LMS Certificate',
		filters: {
			batch_name: props.batch?.data?.name,
		},
	},
	auto: true,
})
</script>
