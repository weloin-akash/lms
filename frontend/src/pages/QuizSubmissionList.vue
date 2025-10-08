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
					<h1 class="text-3xl font-bold text-gray-900 mb-2">Quiz Submissions</h1>
					<p class="text-gray-600">Review student quiz results and performance</p>
				</div>

				<!-- Modern Filter Section -->
				<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-6">
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
							<label class="block text-sm font-medium text-gray-700">Minimum Percentage</label>
							<FormControl
								v-model="minPercentage"
								type="number"
								:placeholder="__('e.g., 50')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
					</div>
				</div>
			</div>

			<!-- Quiz Title Card -->
			<div v-if="submissions.data?.length" class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-6">
				<div class="flex items-center space-x-3">
					<div class="w-12 h-12 bg-gradient-to-br from-[#ed8e22] to-[#d87c1a] rounded-xl flex items-center justify-center">
						<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
						</svg>
					</div>
					<div>
						<h2 class="text-2xl font-bold text-gray-900">{{ submissions.data[0].quiz_title }}</h2>
						<p class="text-gray-600 text-sm">{{ submissions.data.length }} submission{{ submissions.data.length !== 1 ? 's' : '' }}</p>
					</div>
				</div>
			</div>

			<!-- Submission List with Built-in Selection -->
			<div v-if="submissions.loading || submissions.data?.length" class="bg-white rounded-xl shadow-sm border border-gray-200/50 overflow-hidden">
				<ListView
					:columns="quizColumns"
					:rows="submissions.data"
					row-key="name"
					:options="{ showTooltip: false, selectable: true }"
					class="modern-submission-list"
				>
					<ListHeader class="border-b border-gray-200 bg-gray-50 py-3">
						<ListHeaderItem :item="item" v-for="item in quizColumns">
							<template #prefix="{ item }">
								<div class="w-6 h-6 bg-orange-100 rounded-lg flex items-center justify-center mr-2">
									<svg v-if="item.key === 'member_name'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
									</svg>
									<svg v-else-if="item.key === 'score'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
									</svg>
									<svg v-else-if="item.key === 'percentage'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
						<router-link
							v-for="row in submissions.data"
							:key="row.name"
							:to="{
								name: 'QuizSubmission',
								params: {
									submission: row.name,
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
										<div v-else-if="column.key == 'score'" class="flex items-center justify-center">
											<div class="inline-flex items-center px-3 py-1.5 rounded-lg bg-blue-50 border border-blue-200">
												<svg class="w-4 h-4 text-blue-600 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
												</svg>
												<span class="font-semibold text-blue-800">{{ item }}</span>
											</div>
										</div>
										<div v-else-if="column.key == 'percentage'" class="text-center">
											<div class="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-semibold border"
												:class="{
													'bg-green-100 text-green-800 border-green-300': getPercentageTheme(item) === 'green',
													'bg-yellow-100 text-yellow-800 border-yellow-300': getPercentageTheme(item) === 'yellow',
													'bg-red-100 text-red-800 border-red-300': getPercentageTheme(item) === 'red'
												}"
											>
												<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
												</svg>
												{{ item }}%
											</div>
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

				<!-- Load More Button -->
				<div v-if="submissions.hasNextPage" class="p-6 border-t border-gray-200 bg-gray-50">
					<Button 
						@click="submissions.next()"
						class="w-full bg-gradient-to-r from-[#ed8e22] to-[#d87c1a] text-white hover:from-[#d87c1a] hover:to-[#c76f18] transition-all duration-200"
					>
						{{ __('Load More Submissions') }}
					</Button>
				</div>
			</div>

			<!-- Modern Empty State -->
			<div v-else class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-12 text-center">
				<div class="max-w-md mx-auto">
					<div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
						<ClipboardList class="w-12 h-12 text-gray-400" />
					</div>
					<h3 class="text-lg font-semibold text-gray-900 mb-2">No Quiz Submissions Found</h3>
					<p class="text-gray-600">
						There are no quiz submissions matching your current filters. 
						Try adjusting your search criteria or check back later.
					</p>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	createListResource,
	Breadcrumbs,
	Button,
	FormControl,
	ListView,
	ListRow,
	ListRows,
	ListHeader,
	ListHeaderItem,
	ListRowItem,
	ListSelectBanner,
	toast,
	usePageMeta,
} from 'frappe-ui'
import { computed, onMounted, inject, ref, watch } from 'vue'
import { sessionStore } from '../stores/session'
import { useRouter } from 'vue-router'
import { ClipboardList } from 'lucide-vue-next'
import Link from '@/components/Controls/Link.vue'

const { brand } = sessionStore()
const router = useRouter()
const user = inject('$user')
const member = ref('')
const minPercentage = ref('')

onMounted(() => {
	if (!user.data?.is_instructor && !user.data?.is_moderator)
		router.push({ name: 'Courses' })
	
	member.value = router.currentRoute.value.query.member || ''
	minPercentage.value = router.currentRoute.value.query.minPercentage || ''
	reloadSubmissions()
})

const props = defineProps({
	quizID: {
		type: String,
		required: true,
	},
})

const getQuizFilters = () => {
	let filters = {
		quiz: props.quizID,
	}
	if (member.value) {
		filters.member = member.value
	}
	return filters
}

const submissions = createListResource({
	doctype: 'LMS Quiz Submission',
	fields: ['name', 'member_name', 'score', 'percentage', 'quiz_title'],
	orderBy: 'creation desc',
	transform(data) {
		// Apply client-side filtering for percentage
		if (minPercentage.value) {
			const minPct = parseFloat(minPercentage.value)
			return data.filter(row => parseFloat(row.percentage) >= minPct)
		}
		return data
	},
})

watch([member, minPercentage], () => {
	router.push({
		query: {
			member: member.value,
			minPercentage: minPercentage.value,
		},
	})
	reloadSubmissions()
})

const reloadSubmissions = () => {
	submissions.update({
		filters: getQuizFilters(),
	})
	submissions.reload()
}

const quizColumns = computed(() => {
	return [
		{
			label: __('Student'),
			key: 'member_name',
			width: 2,
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

const getPercentageTheme = (percentage) => {
	const pct = parseFloat(percentage)
	if (pct >= 70) {
		return 'green'
	} else if (pct >= 50) {
		return 'yellow'
	} else {
		return 'red'
	}
}

const deleteSubmissions = (selections, unselectAll) => {
	Array.from(selections).forEach(async (submissionName) => {
		await submissions.delete.submit(submissionName)
	})
	unselectAll()
	toast.success(__('Submissions deleted successfully'))
}

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
