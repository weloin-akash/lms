<template>
	<Quiz v-if="user.data" :quizName="quiz"></Quiz>
	<div v-else class="bg-white rounded-xl shadow-sm border border-gray-200/50 text-center py-16">
		<div class="w-16 h-16 mx-auto mb-6 bg-[#ed8e22] rounded-full flex items-center justify-center">
			<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
			</svg>
		</div>
		<h3 class="text-xl font-bold text-gray-900 mb-3">{{ __('Login Required') }}</h3>
		<p class="text-gray-600 mb-6">{{ __('Please login to access the quiz.') }}</p>
		<Button @click="redirectToLogin()" class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium">
			<span>
				{{ __('Login') }}
			</span>
		</Button>
	</div>
</template>
<script setup>
import { inject } from 'vue'
import { Button } from 'frappe-ui'
import Quiz from '@/components/Quiz.vue'

const user = inject('$user')
const props = defineProps({
	quiz: {
		type: String,
		required: true,
	},
})

const redirectToLogin = () => {
	window.location.href = `/login`
}
</script>
