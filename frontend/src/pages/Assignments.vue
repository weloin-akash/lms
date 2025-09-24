<template>
	<!-- Modern Header with Glass Effect -->
	<header
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center justify-between">
			<Breadcrumbs :items="breadcrumbs" />
			<Button
				v-if="!readOnlyMode"
				variant="solid"
				class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium"
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
				{{ __('Create') }}
			</Button>
		</div>
	</header>

	<!-- Modern Container with Better Spacing -->
	<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50">
		<div class="max-w-7xl mx-auto px-6 py-8">
			<!-- Header Section with Modern Typography -->
			<div class="mb-8">
				<div class="flex items-center justify-between mb-6">
					<div>
						<h1 class="text-3xl font-bold text-gray-900 mb-2">Assignments</h1>
						<p v-if="assignmentCount" class="text-gray-600">
							{{ __('{0} assignments total').format(assignmentCount) }}
						</p>
					</div>
				</div>

				<!-- Modern Search and Filter Section -->
				<div
					v-if="assignments.data?.length || assignmentCount > 0"
					class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-6"
				>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div class="space-y-2">
							<label class="block text-sm font-medium text-gray-700">Search Assignments</label>
							<FormControl
								v-model="titleFilter"
								:placeholder="__('Search by title...')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
						<div class="space-y-2">
							<label class="block text-sm font-medium text-gray-700">Filter by Type</label>
							<FormControl
								v-model="typeFilter"
								type="select"
								:options="assignmentTypes"
								:placeholder="__('All Types')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
					</div>
				</div>
			</div>

			<!-- Modern Card-based Assignment List -->
			<div v-if="assignments.data?.length" class="space-y-4">
				<div
					v-for="row in assignments.data"
					:key="row.name"
					class="bg-white rounded-xl shadow-sm border border-gray-200/50 hover:shadow-md hover:border-gray-300/50 transition-all duration-200 overflow-hidden group cursor-pointer"
					@click="
						() => {
							if (readOnlyMode) return
							assignmentID = row.name
							showAssignmentForm = true
						}
					"
				>
					<div class="p-6">
						<div class="flex items-start justify-between">
							<div class="flex-1 min-w-0">
								<div class="flex items-center space-x-3 mb-2">
									<h3 class="text-lg font-semibold text-gray-900 group-hover:text-[#ed8e22] transition-colors duration-200">
										{{ row.title }}
									</h3>
									<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-[#ed8e22]">
										{{ row.type }}
									</span>
								</div>
								<div class="flex items-center space-x-4 text-sm text-gray-500">
									<div class="flex items-center">
										<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
										Created {{ row.creation }}
									</div>
								</div>
							</div>
							<div class="flex items-center space-x-3 ml-4">
								<Button
									variant="outline"
									size="sm"
									@click.stop="navigateToSubmissions(row)"
									class="hover:bg-orange-50 hover:border-orange-300 hover:text-[#ed8e22] transition-all duration-200 rounded-lg px-4 py-2"
								>
									<template #prefix>
										<ClipboardCheck class="h-4 w-4" />
									</template>
									{{ __('View Submissions') }}
								</Button>
								<div class="w-1 h-1 bg-gray-300 rounded-full"></div>
								<svg class="w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
								</svg>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Modern Empty State -->
			<div v-else class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-12 text-center">
				<div class="max-w-md mx-auto">
					<div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
						<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">No Assignments Yet</h3>
					<p class="text-gray-600 mb-6">Get started by creating your first assignment to engage your students.</p>
					<Button
						v-if="!readOnlyMode"
						variant="solid"
						class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium"
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
			</div>

			<!-- Modern Load More Button -->
			<div
				v-if="assignments.data && assignments.hasNextPage"
				class="flex justify-center mt-8"
			>
				<Button 
					@click="assignments.next()"
					class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-sm hover:shadow transition-all duration-200 px-6 py-3 rounded-lg font-medium"
				>
					{{ __('Load More Assignments') }}
				</Button>
			</div>
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
	FormControl,
	ListView,
	ListRows,
	ListRow,
	ListRowItem,
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
