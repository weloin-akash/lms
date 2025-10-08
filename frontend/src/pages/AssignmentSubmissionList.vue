<template>
	<!-- Modern Header with Glass Effect -->
	<!-- <header
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center justify-between">
			<Breadcrumbs :items="breadcrumbs" />
		</div>
	</header> -->
	<AppHeader>
		<template #breadcrumbs>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
	</AppHeader>

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
			<!-- Submission List with Built-in Selection -->
							<div v-if="submissions.loading || submissions.data?.length" class="bg-white rounded-xl shadow-sm border border-gray-200/50 overflow-hidden">
				<ListView
					:columns="submissionColumns"
					:rows="submissions.data"
					row-key="name"
					:options="{ showTooltip: false, selectable: true }"
					class="modern-submission-list"
				>
					<ListHeader class="border-b border-gray-200 bg-gray-50 py-3">
						<ListHeaderItem :item="item" v-for="item in submissionColumns">
							<template #prefix="{ item }">
								<div class="w-6 h-6 bg-orange-100 rounded-lg flex items-center justify-center mr-2">
									<svg v-if="item.key === 'member_name'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
									</svg>
									<svg v-else-if="item.key === 'assignment_title'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
									</svg>
									<svg v-else-if="item.key === 'status'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
									<svg v-else class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
								</div>
							</template>
						</ListHeaderItem>
					</ListHeader>
					<ListRows>
						<router-link
							v-for="row in submissions.data"
							:key="row.name"
							:to="{
								name: 'AssignmentSubmission',
								params: {
									assignmentID: row.assignment,
									submissionName: row.name,
								},
							}"
							class="block"
						>
							<ListRow :row="row" class="hover:bg-gray-50 transition-colors duration-200 group border-b border-gray-100 py-3">
								<template #default="{ column, item }">
									<ListRowItem :item="row[column.key]" :align="column.align">
										<div v-if="column.key == 'member_name'" class="flex items-center space-x-2">
											<div class="w-6 h-6 bg-orange-100 rounded flex items-center justify-center flex-shrink-0">
												<svg class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
												</svg>
											</div>
											<span class="font-medium text-gray-900 group-hover:text-[#ed8e22] transition-colors">{{ item }}</span>
										</div>
										<div v-else-if="column.key == 'assignment_title'" class="flex items-center space-x-2">
											<div class="w-6 h-6 bg-orange-100 rounded flex items-center justify-center flex-shrink-0">
												<svg class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
												</svg>
											</div>
											<span class="font-medium text-gray-900">{{ item }}</span>
										</div>
										<div v-else-if="column.key == 'status'" class="text-center">
											<div class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border"
												:class="{
													'bg-green-100 text-green-800 border-green-200': getStatusTheme(item) === 'green',
													'bg-blue-100 text-blue-800 border-blue-200': getStatusTheme(item) === 'blue',
													'bg-red-100 text-red-800 border-red-200': getStatusTheme(item) === 'red'
												}"
											>
												{{ item }}
											</div>
										</div>
										<div v-else-if="column.key == 'creation'" class="text-center">
											<span class="text-sm text-gray-700">{{ item }}</span>
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
									@click="deleteSubmissions(selections, unselectAll)"
									class="text-red-600 hover:bg-red-50"
								>
									<template #prefix>
										<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
										</svg>
									</template>
									{{ __('Delete') }}
								</Button>
							</div>
						</template>
					</ListSelectBanner>
				</ListView>
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
	Button,
	createListResource,
	FormControl,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListRows,
	ListRow,
	ListRowItem,
	ListSelectBanner,
	toast,
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
			label: __('Student'),
			key: 'member_name',
			width: 2,
		},
		{
			label: __('Assignment'),
			key: 'assignment_title',
			width: 2,
		},
		{
			label: __('Submitted'),
			key: 'creation',
			width: 1,
			align: 'center',
		},
		{
			label: __('Status'),
			key: 'status',
			width: 1,
			align: 'center',
		},
	]
})

const deleteSubmissions = (selections, unselectAll) => {
	Array.from(selections).forEach(async (submissionName) => {
		await submissions.delete.submit(submissionName)
	})
	unselectAll()
	toast.success(__('Submissions deleted successfully'))
}

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
