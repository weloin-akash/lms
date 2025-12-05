<template>
	<div class="min-h-screen flex items-center justify-center bg-surface-gray-2">
		<div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full mx-4">
			<!-- Loading State -->
			<div v-if="loading" class="text-center">
				<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
				<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Connecting to Google Meet...') }}</h2>
				<p class="text-ink-gray-5 mt-2">{{ __('Please wait while we complete the authorization.') }}</p>
			</div>

			<!-- Success State -->
			<div v-else-if="success" class="text-center">
				<div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
					<svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Authorization Successful!') }}</h2>
				<p class="text-ink-gray-5 mt-2">{{ __('Google Meet has been successfully connected.') }}</p>
				<p class="text-ink-gray-5 mt-1">{{ __('You can close this window now.') }}</p>
				<Button class="mt-6" variant="solid" @click="closeWindow">
					{{ __('Close Window') }}
				</Button>
			</div>

			<!-- Error State -->
			<div v-else-if="error" class="text-center">
				<div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
					<svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</div>
				<h2 class="text-lg font-semibold text-ink-gray-9">{{ __('Authorization Failed') }}</h2>
				<p class="text-red-600 mt-2">{{ errorMessage }}</p>
				<Button class="mt-6" variant="solid" @click="closeWindow">
					{{ __('Close Window') }}
				</Button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { createResource, Button } from 'frappe-ui'

const route = useRoute()

const loading = ref(true)
const success = ref(false)
const error = ref(false)
const errorMessage = ref('')

const exchangeToken = createResource({
	url: 'lms.lms.api.google_meet_oauth_callback',
	makeParams() {
		return {
			code: route.query.code,
			state: route.query.state,
			error: route.query.error,
			error_description: route.query.error_description,
		}
	},
	onSuccess(data) {
		loading.value = false
		success.value = true
	},
	onError(err) {
		loading.value = false
		error.value = true
		errorMessage.value = err.messages?.[0] || err.message || 'An unknown error occurred'
	},
})

onMounted(() => {
	// Check for error from Google
	if (route.query.error) {
		loading.value = false
		error.value = true
		errorMessage.value = route.query.error_description || route.query.error || 'Authorization was denied'
		return
	}

	// Check for required params
	if (!route.query.code || !route.query.state) {
		loading.value = false
		error.value = true
		errorMessage.value = 'Missing authorization code or state parameter'
		return
	}

	// Exchange code for tokens
	exchangeToken.submit()
})

const closeWindow = () => {
	window.close()
}
</script>
