<template>
<AppHeader :title="__('Quizzes')" :description="__('Manage and create quiz assessments')">
		<template #icon>
			<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
		</template>
		<template #actions>
			<Button v-if="!readOnlyMode" class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0" @click="showForm = true">
				<template #prefix>
					<Plus class="w-4 h-4" />
				</template>
				{{ __('Create Quiz') }}
			</Button>
		</template>
	</AppHeader>
	<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
		<!-- Search and Filter Section -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-6 mb-8">
			<div class="flex items-center justify-between">
				<div>
					<h2 class="text-lg font-semibold text-gray-900 mb-1">
						{{
							quizzes.data?.length
								? __('{0} Quizzes').format(quizzes.data.length)
								: __('No Quizzes')
						}}
					</h2>
					<p class="text-gray-600 text-sm">Manage your quiz assessments</p>
				</div>
				<div class="w-80">
					<FormControl 
						v-model="search" 
						type="text" 
						placeholder="Search quizzes..."
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					>
						<template #prefix>
							<FeatherIcon name="search" class="size-4 text-gray-400" />
						</template>
					</FormControl>
				</div>
			</div>
		</div>
		<!-- Quiz List -->
		<div v-if="quizzes.data?.length" class="bg-white rounded-xl shadow-sm border border-gray-200/50 overflow-hidden">
			<ListView
				:columns="quizColumns"
				:rows="quizzes.data"
				row-key="name"
				:options="{ showTooltip: false, selectable: true }"
				class="modern-quiz-list"
			>
				<ListHeader class="border-b border-gray-200 bg-gray-50 py-3">
					<ListHeaderItem :item="item" v-for="item in quizColumns">
						<template #prefix="{ item }">
							<div class="w-6 h-6 bg-orange-100 rounded-lg flex items-center justify-center mr-2">
								<svg v-if="item.key === 'title'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
								</svg>
								<svg v-else-if="item.key === 'total_marks'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
								</svg>
								<svg v-else-if="item.key === 'passing_percentage'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
								</svg>
								<svg v-else-if="item.key === 'max_attempts'" class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
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
						v-for="row in quizzes.data" 
						:key="row.name" 
						:row="row" 
						class="hover:bg-gray-50 transition-colors duration-200 group border-b border-gray-100 py-3"
					>
						<template #default="{ column, item }">
							<ListRowItem :item="row[column.key]" :align="column.align">
								<div v-if="column.key == 'title'" class="flex items-center space-x-2">
									<div class="w-6 h-6 bg-orange-100 rounded flex items-center justify-center flex-shrink-0">
										<svg class="w-3 h-3 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
										</svg>
									</div>
									<router-link
										:to="{
											name: 'QuizForm',
											params: {
												quizID: row.name,
											},
										}"
										class="font-medium text-gray-900 group-hover:text-[#ed8e22] transition-colors"
									>
										{{ item }}
									</router-link>
								</div>
								<div v-else-if="column.key == 'total_marks'" class="text-center">
									<span class="text-sm font-medium text-gray-700">{{ item }}</span>
								</div>
								<div v-else-if="column.key == 'passing_percentage'" class="text-center">
									<span class="text-sm font-medium text-gray-700">{{ item }}%</span>
								</div>
								<div v-else-if="column.key == 'max_attempts'" class="text-center">
									<span class="text-sm font-medium text-gray-700">{{ item }}</span>
								</div>
								<div v-else-if="column.key == 'show_answers'" class="text-center">
									<span v-if="item" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Yes</span>
									<span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">No</span>
								</div>
								<div v-else-if="column.key == 'modified'" class="text-center">
									<span class="text-sm text-gray-700">{{ item }}</span>
								</div>
								<div v-else-if="column.key == 'actions'" class="text-center">
									<Button 
										class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-sm hover:shadow-md transition-all duration-200 px-4 py-2 rounded-lg font-medium !border-0"
										@click.stop="navigateToSubmissions(row)"
									>
										<template #prefix>
											<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
											</svg>
										</template>
										{{ __('Submissions') }}
									</Button>
								</div>
								<div v-else>{{ item }}</div>
							</ListRowItem>
						</template>
					</ListRow>
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="deleteQuiz(selections, unselectAll)"
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
			<h3 class="text-lg font-semibold text-gray-900 mb-2">No quizzes yet</h3>
			<p class="text-gray-600 mb-6">Get started by creating your first quiz assessment</p>
			<Button 
				v-if="!readOnlyMode" 
				class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0"
				@click="showForm = true"
			>
				<template #prefix>
					<Plus class="w-4 h-4" />
				</template>
				{{ __('Create Your First Quiz') }}
			</Button>
		</div>

		<!-- Load More Button -->
		<div v-if="quizzes.hasNextPage" class="flex justify-center mt-8">
			<Button 
				class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 hover:border-gray-400 shadow-sm hover:shadow transition-all duration-200 px-6 py-2.5 rounded-lg font-medium"
				@click="quizzes.next()"
			>
				{{ __('Load More Quizzes') }}
			</Button>
		</div>
	</div>
	<!-- Create Quiz Modal -->
	<Dialog
		v-model="showForm"
		:options="{
			title: __('Create a Quiz'),
			size: 'sm',
			actions: [
				{
					label: __('Save'),
					class: '!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white border-0',
					onClick({ close }) {
						insertQuiz(close)
					},
				},
			],
		}"
	>
		<template #body-content>
			<div class="px-6 py-6">
				<FormControl 
					v-model="title" 
					:label="__('Title')" 
					type="text" 
					placeholder="Enter quiz title..."
					class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
				/>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	createListResource,
	Dialog,
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
import { useRouter } from 'vue-router'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { Plus } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import EmptyState from '@/components/EmptyState.vue'

const { brand } = sessionStore()
const user = inject('$user')
const dayjs = inject('$dayjs')
const router = useRouter()
const search = ref('')
const readOnlyMode = window.read_only_mode
const quizFilters = ref({})
const showForm = ref(false)
const title = ref('')

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	} else if (!user.data?.is_moderator) {
		quizFilters.value['owner'] = user.data?.name
	}
})

watch(search, () => {
	quizFilters.value['title'] = ['like', `%${search.value}%`]
	quizzes.update({
		filters: quizFilters.value,
	})
	quizzes.reload()
})

const quizzes = createListResource({
	doctype: 'LMS Quiz',
	filters: quizFilters,
	fields: [
		'name',
		'title',
		'passing_percentage',
		'total_marks',
		'show_answers',
		'max_attempts',
		'modified',
	],
	auto: true,
	cache: ['quizzes', user.data?.name],
	orderBy: 'modified desc',
	transform(data) {
		return data.map((quiz) => {
			return {
				...quiz,
				modified: dayjs(quiz.modified).fromNow(),
			}
		})
	},
})

const insertQuiz = (close) => {
	quizzes.insert.submit(
		{
			title: title.value,
		},
		{
			onSuccess(data) {
				toast.success(__('Quiz created successfully'))
				close()
				title.value = ''
				router.push({
					name: 'QuizForm',
					params: {
						quizID: data.name,
					},
				})
			},
			onError(error) {
				toast.error(__('Error creating quiz: {0}', error.message))
			},
		}
	)
}

const deleteQuiz = (selections, unselectAll) => {
	Array.from(selections).forEach(async (quizName) => {
		await quizzes.delete.submit(quizName)
	})
	unselectAll()
	toast.success(__('Quizzes deleted successfully'))
}

const navigateToSubmissions = (quiz) => {
	router.push({
		name: 'QuizSubmissionList',
		params: {
			quizID: quiz.name,
		},
	})
}

const quizColumns = computed(() => {
	return [
		{
			label: __('Title'),
			key: 'title',
			width: 2,
			icon: 'file-text',
		},
		{
			label: __('Total Marks'),
			key: 'total_marks',
			width: 1,
			align: 'center',
			icon: 'hash',
		},
		{
			label: __('Passing Percentage'),
			key: 'passing_percentage',
			width: 1,
			align: 'center',
			icon: 'percent',
		},
		{
			label: __('Max Attempts'),
			key: 'max_attempts',
			width: 1,
			align: 'center',
			icon: 'repeat',
		},
		{
			label: __('Show Answers'),
			key: 'show_answers',
			width: 1,
			align: 'center',
			icon: 'eye',
		},
		{
			label: __('Modified'),
			key: 'modified',
			width: 1,
			align: 'center',
			icon: 'clock',
		},
		{
			label: __('Actions'),
			key: 'actions',
			width: 1,
			align: 'center',
		},
	]
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Quizzes'),
			route: {
				name: 'Quizzes',
			},
		},
	]
})

usePageMeta(() => {
	return {
		title: __('Quizzes'),
		icon: brand.favicon,
	}
})
</script>
