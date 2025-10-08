<template>
	<AppHeader :title="__('Assignments')" :description="__('Manage and create assignment assessments')">
		<template #icon>
			<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
			</svg>
		</template>
		<template #actions>
			<Button v-if="!readOnlyMode" class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0" @click="
					() => {
						assignmentID = 'new'
						showAssignmentForm = true
					}
				">
				<template #prefix>
					<Plus class="w-4 h-4" />
				</template>
				{{ __('Create Assignment') }}
			</Button>
		</template>
	</AppHeader>

	<!-- Modern Container with Better Spacing -->
	<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
		<!-- Search and Filter Section -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-8">
			<div class="flex items-center justify-between">
				<div>
					<h2 class="text-lg font-semibold text-gray-900 mb-1">
						{{
							assignments.data?.length
								? __('{0} Assignments').format(assignments.data.length)
								: __('No Assignments')
						}}
					</h2>
					<p class="text-gray-600 text-sm">Manage your assignment assessments</p>
				</div>
				<div class="w-80">
					<FormControl 
						v-model="titleFilter" 
						type="text" 
						placeholder="Search assignments..."
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					>
						<template #prefix>
							<FeatherIcon name="search" class="size-4 text-gray-400" />
						</template>
					</FormControl>
				</div>
			</div>
		</div>

			<!-- Assignment List with Built-in Selection -->
			<div v-if="assignments.data?.length" class="bg-white rounded-xl shadow-sm border border-gray-200/50 overflow-hidden">
				<ListView
					:columns="assignmentColumns"
					:rows="assignments.data"
					row-key="name"
					:options="{ showTooltip: false, selectable: true }"
					class="modern-assignment-list"
				>
					<ListHeader class="border-b border-gray-200 bg-gray-50 py-3">
						<ListHeaderItem :item="item" v-for="item in assignmentColumns">
							<template #prefix="{ item }">
								<div class="w-6 h-6 bg-orange-100 rounded-lg flex items-center justify-center mr-2">
									<svg v-if="item.key === 'title'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
									</svg>
									<svg v-else-if="item.key === 'type'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
									</svg>
									<svg v-else class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
								</div>
							</template>
						</ListHeaderItem>
					</ListHeader>
					<ListRows>
						<div
							v-for="row in assignments.data"
							:key="row.name"
							class="hover:bg-gray-50 transition-colors duration-200 group cursor-pointer border-b border-gray-100 py-3"
							@click="
								() => {
									if (readOnlyMode) return
									assignmentID = row.name
									showAssignmentForm = true
								}
							"
						>
							<ListRow :row="row">
								<template #default="{ column, item }">
									<ListRowItem :item="row[column.key]" :align="column.align">
										<div v-if="column.key == 'title'" class="flex items-center space-x-2">
											<div class="w-6 h-6 bg-orange-100 rounded flex items-center justify-center flex-shrink-0">
												<svg class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
												</svg>
											</div>
											<span class="font-medium text-gray-900 group-hover:text-[#ed8e22] transition-colors">{{ item }}</span>
										</div>
										<div v-else-if="column.key == 'type'" class="text-center">
											<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-[#ed8e22]">{{ item }}</span>
										</div>
										<div v-else-if="column.key == 'creation'" class="text-center">
											<span class="text-sm text-gray-700">{{ item }}</span>
										</div>
										<div v-else-if="column.key == 'actions'" class="flex items-center justify-end space-x-2">
											<Button
												size="sm"
												@click.stop="navigateToSubmissions(row)"
												class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white transition-all duration-200 rounded-lg px-3 py-1.5 border-0"
											>
												<template #prefix>
													<ClipboardCheck class="h-4 w-4" />
												</template>
												{{ __('Submissions') }}
											</Button>
										</div>
										<div v-else>{{ item }}</div>
									</ListRowItem>
								</template>
							</ListRow>
						</div>
					</ListRows>
					<ListSelectBanner>
						<template #actions="{ unselectAll, selections }">
							<div class="flex gap-2">
								<Button
									variant="ghost"
									@click="deleteAssignments(selections, unselectAll)"
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

		<!-- Empty State -->
		<div v-else class="p-12 text-center">
			<div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
				<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
				</svg>
			</div>
			<h3 class="text-lg font-semibold text-gray-900 mb-2">No assignments yet</h3>
			<p class="text-gray-600 mb-6">Get started by creating your first assignment assessment</p>
			<Button 
				v-if="!readOnlyMode" 
				class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0"
				@click="
					() => {
						assignmentID = 'new'
						showAssignmentForm = true
					}
				"
			>
				<template #prefix>
					<Plus class="w-4 h-4" />
				</template>
				{{ __('Create Your First Assignment') }}
			</Button>
		</div>

		<!-- Load More Button -->
		<div v-if="assignments.hasNextPage" class="flex justify-center mt-8">
			<Button 
				class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 hover:border-gray-400 shadow-sm hover:shadow transition-all duration-200 px-6 py-2.5 rounded-lg font-medium"
				@click="assignments.next()"
			>
				{{ __('Load More Assignments') }}
			</Button>
		</div>
	</div>
	<AssignmentForm
		v-model="showAssignmentForm"
		v-model:assignments="assignments"
		:assignmentID="assignmentID"
	/>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createListResource,
	FeatherIcon,
	FormControl,
	ListView,
	ListRows,
	ListRow,
	ListRowItem,
	ListHeader,
	ListHeaderItem,
	ListSelectBanner,
	toast,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { Plus, ClipboardCheck } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { sessionStore } from '../stores/session'
import AssignmentForm from '@/components/Modals/AssignmentForm.vue'
import EmptyState from '@/components/EmptyState.vue'

const user = inject('$user')
const dayjs = inject('$dayjs')
const titleFilter = ref('')
const typeFilter = ref('')
const showAssignmentForm = ref(false)
const assignmentID = ref('new')
const assignmentCount = ref(0)
const { brand } = sessionStore()
const router = useRouter()
const readOnlyMode = window.read_only_mode

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	}
	getAssignmentCount()
	titleFilter.value = router.currentRoute.value.query.title
	typeFilter.value = router.currentRoute.value.query.type
})

watch([titleFilter, typeFilter], () => {
	router.push({
		query: {
			title: titleFilter.value,
			type: typeFilter.value,
		},
	})
	reloadAssignments()
})

const reloadAssignments = () => {
	assignments.update({
		filters: assignmentFilter.value,
	})
	assignments.reload()
}

const assignmentFilter = computed(() => {
	let filters = {}
	if (titleFilter.value) {
		filters.title = ['like', `%${titleFilter.value}%`]
	}
	if (typeFilter.value) {
		filters.type = typeFilter.value
	}
	if (!user.data?.is_moderator) {
		filters.owner = user.data?.email
	}
	return filters
})

const assignments = createListResource({
	doctype: 'LMS Assignment',
	fields: ['name', 'title', 'type', 'creation', 'question'],
	orderBy: 'modified desc',
	cache: ['assignments'],
	transform(data) {
		return data.map((row) => {
			return {
				...row,
				creation: dayjs(row.creation).fromNow(),
			}
		})
	},
})

const assignmentColumns = computed(() => {
	return [
		{
			label: __('Title'),
			key: 'title',
			width: 2,
		},
		{
			label: __('Type'),
			key: 'type',
			width: 1,
			align: 'left',
		},
		{
			label: __('Created'),
			key: 'creation',
			width: 1,
			align: 'right',
		},
		{
			label: __('Actions'),
			key: 'actions',
			width: 1,
			align: 'right',
		},
	]
})

const getAssignmentCount = () => {
	call('frappe.client.get_count', {
		doctype: 'LMS Assignment',
	}).then((data) => {
		assignmentCount.value = data
	})
}

const assignmentTypes = computed(() => {
	let types = ['', 'Document', 'Image', 'PDF', 'URL', 'Text']
	return types.map((type) => {
		return {
			label: __(type),
			value: type,
		}
	})
})

const navigateToSubmissions = (assignment) => {
	router.push({
		name: 'AssignmentSubmissionList',
		query: {
			assignmentID: assignment.name,
		},
	})
}

const deleteAssignments = (selections, unselectAll) => {
	Array.from(selections).forEach(async (assignmentName) => {
		await assignments.delete.submit(assignmentName)
	})
	unselectAll()
	toast.success(__('Assignments deleted successfully'))
}

const breadcrumbs = computed(() => [
	{
		label: 'Assignments',
		route: { name: 'Assignments' },
	},
])

usePageMeta(() => {
	return {
		title: __('Assignments'),
		icon: brand.favicon,
	}
})
</script>
