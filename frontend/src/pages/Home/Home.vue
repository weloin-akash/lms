<template>
	<AppHeader>
		<template #icon>
			<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
			</svg>
		</template>
		<template #title>
			<div class="flex items-center space-x-2">
				<span>{{ __('Hey') }}, {{ user.data?.full_name }}</span>
				<span class="text-2xl">👋</span>
			</div>
		</template>
		<template #description>
			{{ subtitle }}
		</template>
		<template #actions>
			<div class="flex items-center space-x-3">
				<TabButtons v-if="isAdmin" v-model="currentTab" :buttons="tabs" />
				<div
					v-else
					@click="showStreakModal = true"
					class="inline-flex items-center space-x-2 bg-gradient-to-r from-amber-100 to-orange-100 hover:from-amber-200 hover:to-orange-200 px-4 py-2 rounded-lg cursor-pointer transition-all duration-200 border border-orange-200 shadow-sm"
				>
					<span class="text-xl">🔥</span>
					<span class="font-semibold text-orange-800">
						{{ streakInfo.data?.current_streak }}
					</span>
					<span class="text-sm text-orange-700">day streak</span>
				</div>
			</div>
		</template>
	</AppHeader>

	<div class="w-full px-5 pb-10">
		<AdminHome
			v-if="isAdmin && currentTab === 'instructor'"
			:liveClasses="adminLiveClasses"
			:evals="adminEvals"
		/>
		<StudentHome v-else :myLiveClasses="myLiveClasses" />
	</div>
	<Streak v-model="showStreakModal" :streakInfo="streakInfo" />
</template>
<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import {
	Breadcrumbs,
	call,
	createResource,
	TabButtons,
	usePageMeta,
} from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import StudentHome from '@/pages/Home/StudentHome.vue'
import AdminHome from '@/pages/Home/AdminHome.vue'
import Streak from '@/pages/Home/Streak.vue'
import AppHeader from '@/components/AppHeader.vue'

const user = inject<any>('$user')
const { brand } = sessionStore()
const evalCount = ref(0)
const currentTab = ref<'student' | 'instructor'>('instructor')
const showStreakModal = ref(false)

onMounted(() => {
	call('lms.lms.utils.get_upcoming_evals').then((data: any) => {
		evalCount.value = data.length
	})
})

const isAdmin = computed(() => {
	return (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
})

const myLiveClasses = createResource({
	url: 'lms.lms.utils.get_my_live_classes',
	auto: !isAdmin.value ? true : false,
})

const adminLiveClasses = createResource({
	url: 'lms.lms.utils.get_admin_live_classes',
	auto: isAdmin.value ? true : false,
})

const adminEvals = createResource({
	url: 'lms.lms.utils.get_admin_evals',
	auto: isAdmin.value ? true : false,
})

const streakInfo = createResource({
	url: 'lms.lms.utils.get_streak_info',
	auto: true,
})

const subtitle = computed(() => {
	if (isAdmin.value) {
		let liveClassSuffix =
			adminLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix =
			adminEvals.data?.length > 1 ? __('evaluations') : __('evaluation')
		if (adminLiveClasses.data?.length > 0 && adminEvals.data?.length > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
				adminEvals.data.length,
				evalSuffix
			)
		} else if (adminLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				adminLiveClasses.data.length,
				liveClassSuffix
			)
		} else if (adminEvals.data?.length > 0) {
			return __('You have {0} {1} scheduled.').format(
				adminEvals.data.length,
				evalSuffix
			)
		}
		return __('Manage your courses and batches at a glance')
	} else {
		let liveClassSuffix =
			myLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix = evalCount.value > 1 ? __('evaluations') : __('evaluation')
		if (myLiveClasses.data?.length > 0 && evalCount.value > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
				evalCount.value,
				evalSuffix
			)
		} else if (myLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				myLiveClasses.data.length,
				liveClassSuffix
			)
		} else if (evalCount.value > 0) {
			return __('You have {0} {1} scheduled.').format(
				evalCount.value,
				evalSuffix
			)
		}
		return __('Resume where you left off')
	}
})

const tabs = [
	{ label: __('Student'), value: 'student' },
	{ label: __('Instructor'), value: 'instructor' },
]

usePageMeta(() => {
	return {
		title: __('Home'),
		icon: brand.favicon,
	}
})
</script>
