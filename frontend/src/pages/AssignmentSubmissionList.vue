<template>
	<!-- Modern Header with Glass Effect -->
	<header
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center justify-between">
			<Breadcrumbs :items="breadcrumbs" />
		</div>
	</header>

	<!-- Modern Container with Better Spacing -->
	<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50">
		<div class="max-w-7xl mx-auto px-6 py-8">
			<!-- Header Section with Modern Typography -->
			<div class="mb-8">
				<div class="mb-6">
					<h1 class="text-3xl font-bold text-gray-900 mb-2">Assignment Submissions</h1>
					<p class="text-gray-600">Review and evaluate student assignment submissions</p>
				</div>

				<!-- Modern Filter Section -->
				<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-6">
					<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
						<div class="space-y-2">
							<label class="block text-sm font-medium text-gray-700">Filter by Assignment</label>
							<Link
								doctype="LMS Assignment"
								v-model="assignmentID"
								:placeholder="__('Select Assignment')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
						<div class="space-y-2">
							<label class="block text-sm font-medium text-gray-700">Filter by Member</label>
							<Link 
								doctype="User" 
								v-model="member" 
								:placeholder="__('Select Member')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
						<div class="space-y-2">
							<label class="block text-sm font-medium text-gray-700">Filter by Status</label>
							<FormControl
								v-model="status"
								type="select"
								:options="statusOptions"
								:placeholder="__('All Statuses')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
					</div>
				</div>
			</div>
			<!-- Modern Card-based Submission List -->
			<div v-if="submissions.loading || submissions.data?.length" class="space-y-4">
				<div
					v-for="row in submissions.data"
					:key="row.name"
					class="bg-white rounded-xl shadow-sm border border-gray-200/50 hover:shadow-md hover:border-gray-300/50 transition-all duration-200 overflow-hidden group cursor-pointer"
				>
					<router-link
						:to="{
							name: 'AssignmentSubmission',
							params: {
								assignmentID: row.assignment,
								submissionName: row.name,
							},
						}"
						class="block p-6 no-underline"
					>
						<div class="flex items-start justify-between">
							<div class="flex-1 min-w-0">
								<div class="flex items-center space-x-3 mb-3">
									<div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
										<svg class="w-5 h-5 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
										</svg>
									</div>
									<div class="flex-1">
										<h3 class="text-lg font-semibold text-gray-900 group-hover:text-[#ed8e22] transition-colors duration-200 mb-1">
											{{ row.member_name }}
										</h3>
										<p class="text-sm text-gray-600">{{ row.assignment_title }}</p>
									</div>
								</div>
								<div class="flex items-center space-x-4 text-sm text-gray-500">
									<div class="flex items-center">
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
										Submitted {{ row.creation }}
									</div>
								</div>
							</div>
							
							<div class="flex items-center space-x-3 ml-4">
								<!-- Status Badge -->
								<div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border"
									:class="{
										'bg-green-100 text-green-800 border-green-200': getStatusTheme(row.status) === 'green',
										'bg-blue-100 text-blue-800 border-blue-200': getStatusTheme(row.status) === 'blue',
										'bg-red-100 text-red-800 border-red-200': getStatusTheme(row.status) === 'red'
									}"
								>
									{{ row.status }}
								</div>
								
								<svg class="w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
								</svg>
							</div>
						</div>
					</router-link>
				</div>
			</div>
			<!-- Modern Empty State -->
			<div v-else class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-12 text-center">
				<div class="max-w-md mx-auto">
					<div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
						<Pencil class="w-12 h-12 text-gray-400" />
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">No Submissions Found</h3>
					<p class="text-gray-600">
						There are no assignment submissions matching your current filters. 
						Try adjusting your search criteria or check back later.
					</p>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Badge,
	Breadcrumbs,
	createListResource,
	FormControl,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListRows,
	ListRow,
	ListRowItem,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Pencil } from 'lucide-vue-next'
import { sessionStore } from '../stores/session'
import Link from '@/components/Controls/Link.vue'

const user = inject('$user')
const dayjs = inject('$dayjs')
const { brand } = sessionStore()
const router = useRouter()
const assignmentID = ref('')
const member = ref('')
const status = ref('')

onMounted(() => {
	if (!user.data?.is_instructor && !user.data?.is_moderator) {
		router.push({ name: 'Courses' })
	}
	assignmentID.value = router.currentRoute.value.query.assignmentID
	member.value = router.currentRoute.value.query.member
	status.value = router.currentRoute.value.query.status
	reloadSubmissions()
})

const getAssignmentFilters = () => {
	let filters = {}
	if (assignmentID.value) {
		filters.assignment = assignmentID.value
	}
	if (member.value) {
		filters.member = member.value
	}
	if (status.value) {
		filters.status = status.value
	}
	return filters
}

const submissions = createListResource({
	doctype: 'LMS Assignment Submission',
	fields: [
		'name',
		'assignment',
		'assignment_title',
		'member_name',
		'creation',
		'status',
	],
	orderBy: 'creation desc',
	transform(data) {
		return data.map((row) => {
			return {
				...row,
				creation: dayjs(row.creation).fromNow(),
			}
		})
	},
})

watch([assignmentID, member, status], () => {
	router.push({
		query: {
			assignmentID: assignmentID.value,
			member: member.value,
			status: status.value,
		},
	})
	reloadSubmissions()
})

const reloadSubmissions = () => {
	submissions.update({
		filters: getAssignmentFilters(),
	})
	submissions.reload()
}

const submissionColumns = computed(() => {
	return [
		{
			label: 'Member',
			key: 'member_name',
			width: 1,
		},
		{
			label: 'Assignment',
			key: 'assignment_title',
			width: 2,
		},
		{
			label: 'Submitted',
			key: 'creation',
			width: 1,
			align: 'left',
		},
		{
			label: 'Status',
			key: 'status',
			width: 1,
			align: 'center',
		},
	]
})

const statusOptions = computed(() => {
	return [
		{ label: '', value: '' },
		{ label: 'Pass', value: 'Pass' },
		{ label: 'Fail', value: 'Fail' },
		{ label: 'Not Graded', value: 'Not Graded' },
	]
})

const getStatusTheme = (status) => {
	if (status === 'Pass') {
		return 'green'
	} else if (status === 'Not Graded') {
		return 'blue'
	} else {
		return 'red'
	}
}

const breadcrumbs = computed(() => {
	return [
		{
			label: 'Assignment Submissions',
		},
	]
})

usePageMeta(() => {
	return {
		title: __('Assignment Submissions'),
		icon: brand.favicon,
	}
})
</script>
