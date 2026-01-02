<template>
	<Dialog
		v-model="show"
		:options="{
			title:
				accountID === 'new'
					? __('New Meeting Provider')
					: __('Edit Meeting Provider'),
			size: 'xl',
			actions: [
				{
					label: __('Save'),
					class: '!bg-[#66bb6a] hover:!bg-[#088304] text-white transition-all duration-200 rounded-lg px-3 py-1.5 border-0',
					variant: 'solid',
					onClick: ({ close }) => {
						saveAccount(close)
					},
				},
			],
		}"
	>
		<template #body-content>
			<div class="mb-4">
				<FormControl
					v-model="account.enabled"
					:label="__('Enabled')"
					type="checkbox"
				/>
			</div>
			<div class="grid grid-cols-2 gap-5">
				<FormControl
					v-model="account.account_name"
					:label="__('Account Name')"
					type="text"
					:required="true"
				/>
				<FormControl
					v-model="account.provider_type"
					:label="__('Provider Type')"
					type="select"
					:options="providerOptions"
					:required="true"
				/>
				<Link
					v-model="account.member"
					:label="__('Member')"
					doctype="Course Evaluator"
					:onCreate="(value: string, close: () => void) => openSettings('Members', close)"
					:required="true"
				/>
				<FormControl
					v-model="account.client_id"
					:label="__('Client ID')"
					type="text"
					:required="true"
				/>
				<FormControl
					v-model="account.client_secret"
					:label="__('Client Secret')"
					type="password"
					:required="true"
				/>
				<FormControl
					v-if="account.provider_type === 'Zoom'"
					v-model="account.account_id"
					:label="__('Account ID')"
					type="text"
					:required="true"
					:description="__('Required for Zoom Server-to-Server OAuth')"
				/>
				<FormControl
					v-if="account.provider_type === 'Microsoft Teams'"
					v-model="account.tenant_id"
					:label="__('Tenant ID')"
					type="text"
					:description="__('Azure AD Tenant ID (use \'common\' for multi-tenant apps)')"
				/>
			</div>

			<!-- Authorization Section - Only show for existing Google Meet or Microsoft Teams accounts -->
			<div
				v-if="accountID !== 'new' && (account.provider_type === 'Google Meet' || account.provider_type === 'Microsoft Teams')"
				class="mt-6 p-4 border rounded-lg bg-surface-gray-1"
			>
				<div class="flex items-center justify-between">
					<div class="flex flex-col space-y-1">
						<div class="font-semibold text-ink-gray-9">
							{{ __('Authorization Status') }}
						</div>
						<div class="text-sm text-ink-gray-6">
							<span v-if="isCheckingAuth" class="flex items-center space-x-2">
								<Loader2 class="h-4 w-4 animate-spin" />
								<span>{{ __('Checking authorization...') }}</span>
							</span>
							<span v-else-if="isAuthorized" class="flex items-center space-x-2 text-green-600">
								<CheckCircle class="h-4 w-4" />
								<span>{{ __('Authorized and ready to use') }}</span>
							</span>
							<span v-else class="flex items-center space-x-2 text-amber-600">
								<AlertCircle class="h-4 w-4" />
								<span>{{ __('Authorization required') }}</span>
							</span>
						</div>
					</div>
					<div class="flex items-center space-x-2">
						<Button
							v-if="!isAuthorized"
							@click="authorizeProvider"
							:loading="isAuthorizing"
							class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white !border-0"
						>
							<template #prefix>
								<Key class="h-4 w-4" />
							</template>
							{{ __('Authorize') }}
						</Button>
						<Button
							v-else
							variant="subtle"
							theme="red"
							@click="revokeAuthorization"
							:loading="isRevoking"
						>
							<template #prefix>
								<XCircle class="h-4 w-4" />
							</template>
							{{ __('Revoke') }}
						</Button>
					</div>
				</div>
			</div>

			<!-- Zoom Info Section - Show for Zoom accounts -->
			<div
				v-if="account.provider_type === 'Zoom'"
				class="mt-6 p-4 border rounded-lg bg-surface-gray-1"
			>
				<div class="flex items-center space-x-2">
					<CheckCircle class="h-4 w-4 text-green-600" />
					<div class="flex flex-col space-y-1">
						<div class="font-semibold text-ink-gray-9">
							{{ __('Server-to-Server OAuth') }}
						</div>
						<div class="text-sm text-ink-gray-6">
							{{ __('Zoom uses Server-to-Server OAuth. No additional authorization needed after saving credentials.') }}
						</div>
					</div>
				</div>
			</div>

			<!-- Help text for new accounts -->
			<div
				v-if="accountID === 'new' && account.provider_type === 'Google Meet'"
				class="mt-4 p-3 bg-surface-blue-1 border border-outline-blue-2 rounded-lg text-sm text-ink-blue-3"
			>
				<div class="flex items-start space-x-2">
					<Info class="h-4 w-4 mt-0.5 flex-shrink-0" />
					<span>
						{{ __('After saving, you can authorize the provider to enable meeting creation.') }}
					</span>
				</div>
			</div>
			<div
				v-if="accountID === 'new' && account.provider_type === 'Zoom'"
				class="mt-4 p-3 bg-surface-orange-1 border border-outline-orange-2 rounded-lg text-sm text-ink-orange-3"
			>
				<div class="flex items-start space-x-2">
					<Info class="h-4 w-4 mt-0.5 flex-shrink-0" />
					<span>
						{{ __('Zoom credentials are validated when creating a meeting. Make sure your Account ID, Client ID, and Client Secret are correct.') }}
					</span>
				</div>
			</div>
			<div
				v-if="accountID === 'new' && account.provider_type === 'Microsoft Teams'"
				class="mt-4 p-3 bg-surface-blue-1 border border-outline-blue-2 rounded-lg text-sm text-ink-blue-3"
			>
				<div class="flex items-start space-x-2">
					<Info class="h-4 w-4 mt-0.5 flex-shrink-0" />
					<span>
						{{ __('After saving, you can authorize the provider to enable Microsoft Teams meeting creation. Use "common" for Tenant ID if your app supports multiple tenants.') }}
					</span>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup lang="ts">
import { call, Dialog, FormControl, toast } from 'frappe-ui'
import { inject, reactive, ref, watch } from 'vue'
import { User } from '@/components/Settings/types'
import { openSettings, cleanError } from '@/utils'
import Link from '@/components/Controls/Link.vue'
import {
	Key,
	CheckCircle,
	AlertCircle,
	XCircle,
	Loader2,
	Info,
} from 'lucide-vue-next'
import { Button } from 'frappe-ui'

interface MeetingProvider {
	name: string
	account_name: string
	enabled: boolean
	provider_type: string
	member: string
	client_id: string
	client_secret: string
	account_id?: string
	tenant_id?: string
	refresh_token?: string
}

interface MeetingProviders {
	data: MeetingProvider[]
	reload: () => void
	insert: {
		submit: (
			data: MeetingProvider,
			options: { onSuccess: () => void; onError: (err: any) => void }
		) => void
	}
	setValue: {
		submit: (
			data: MeetingProvider,
			options: { onSuccess: () => void; onError: (err: any) => void }
		) => void
	}
}

const show = defineModel('show')
const user = inject<User | null>('$user')
const meetingProviders = defineModel<MeetingProviders>('meetingProviders')

const isAuthorized = ref(false)
const isCheckingAuth = ref(false)
const isAuthorizing = ref(false)
const isRevoking = ref(false)

const providerOptions = [
	{ label: 'Google Meet', value: 'Google Meet' },
	{ label: 'Zoom', value: 'Zoom' },
	{ label: 'Microsoft Teams', value: 'Microsoft Teams' },
]

const account = reactive({
	name: '',
	account_name: '',
	enabled: false,
	provider_type: 'Google Meet',
	member: user?.data?.name || '',
	client_id: '',
	client_secret: '',
	account_id: '',
	tenant_id: 'common',
})

const props = defineProps({
	accountID: {
		type: String,
		default: 'new',
	},
})

watch(
	() => props.accountID,
	async (val) => {
		if (val != 'new') {
			meetingProviders.value?.data.forEach((acc) => {
				if (acc.name === val) {
					account.name = acc.name
					account.account_name = acc.account_name || acc.name
					account.enabled = acc.enabled || false
					account.provider_type = acc.provider_type || 'Google Meet'
					account.member = acc.member
					account.client_id = acc.client_id
					account.client_secret = acc.client_secret
					// Only set account_id for Zoom
					if (acc.provider_type === 'Zoom') {
						account.account_id = acc.account_id || ''
					}
					// Only set tenant_id for Microsoft Teams
					if (acc.provider_type === 'Microsoft Teams') {
						account.tenant_id = acc.tenant_id || 'common'
					}
				}
			})
			// Check authorization for Google Meet or Microsoft Teams
			if (account.provider_type === 'Google Meet' || account.provider_type === 'Microsoft Teams') {
				await checkAuthorizationStatus()
			}
		}
	}
)

watch(show, async (val) => {
	if (val && props.accountID !== 'new') {
		// Modal opened - load data
		meetingProviders.value?.data.forEach((acc) => {
			if (acc.name === props.accountID) {
				account.name = acc.name
				account.account_name = acc.account_name || acc.name
				account.enabled = acc.enabled || false
				account.provider_type = acc.provider_type || 'Google Meet'
				account.member = acc.member
				account.client_id = acc.client_id
				account.client_secret = acc.client_secret
				if (acc.provider_type === 'Zoom') {
					account.account_id = acc.account_id || ''
				}
				if (acc.provider_type === 'Microsoft Teams') {
					account.tenant_id = acc.tenant_id || 'common'
				}
			}
		})
		if (account.provider_type === 'Google Meet' || account.provider_type === 'Microsoft Teams') {
			await checkAuthorizationStatus()
		}
	} else if (!val) {
		// Modal closed - reset form
		account.name = ''
		account.account_name = ''
		account.enabled = false
		account.provider_type = 'Google Meet'
		account.member = user?.data?.name || ''
		account.client_id = ''
		account.client_secret = ''
		account.account_id = ''
		account.tenant_id = 'common'
		isAuthorized.value = false
	}
})

const checkAuthorizationStatus = async () => {
	if (props.accountID === 'new') return

	isCheckingAuth.value = true
	try {
		const apiMethod = account.provider_type === 'Microsoft Teams'
			? 'lms.lms.api.microsoft_teams_check_authorization'
			: 'lms.lms.api.google_meet_check_authorization'

		const result = await call(apiMethod, {
			settings_name: props.accountID,
		})
		isAuthorized.value = result.is_authorized
	} catch (err) {
		isAuthorized.value = false
	} finally {
		isCheckingAuth.value = false
	}
}

const authorizeProvider = async () => {
	isAuthorizing.value = true
	try {
		const currentUrl = window.location.origin
		const isTeams = account.provider_type === 'Microsoft Teams'
		const redirectUri = isTeams
			? `${currentUrl}/lms/microsoft/auth`
			: `${currentUrl}/lms/google/auth`

		const apiMethod = isTeams
			? 'lms.lms.api.microsoft_teams_get_auth_url'
			: 'lms.lms.api.google_meet_get_auth_url'

		const result = await call(apiMethod, {
			settings_name: props.accountID,
			redirect_uri: redirectUri,
		})

		if (result.authorization_url) {
			// Open authorization URL in a new window
			const authWindow = window.open(
				result.authorization_url,
				isTeams ? 'MicrosoftAuth' : 'GoogleAuth',
				'width=600,height=700,scrollbars=yes'
			)

			// Poll to check if authorization completed
			const checkAuth = setInterval(async () => {
				try {
					if (authWindow?.closed) {
						clearInterval(checkAuth)
						await checkAuthorizationStatus()
						if (isAuthorized.value) {
							toast.success(__('Authorization successful!'))
						}
						isAuthorizing.value = false
					}
				} catch (e) {
					// Window might be on different origin during auth
				}
			}, 1000)
		}
	} catch (err: any) {
		toast.error(cleanError(err.message) || __('Error starting authorization'))
		isAuthorizing.value = false
	}
}

const revokeAuthorization = async () => {
	isRevoking.value = true
	try {
		const apiMethod = account.provider_type === 'Microsoft Teams'
			? 'lms.lms.api.microsoft_teams_revoke_authorization'
			: 'lms.lms.api.google_meet_revoke_authorization'

		await call(apiMethod, {
			settings_name: props.accountID,
		})
		isAuthorized.value = false
		toast.success(__('Authorization revoked successfully'))
	} catch (err: any) {
		toast.error(cleanError(err.message) || __('Error revoking authorization'))
	} finally {
		isRevoking.value = false
	}
}

const saveAccount = (close: () => void) => {
	if (props.accountID == 'new') {
		createAccount(close)
	} else {
		updateAccount(close)
	}
}

const createAccount = (close: () => void) => {
	meetingProviders.value?.insert.submit(
		{
			...account,
		},
		{
			onSuccess() {
				meetingProviders.value?.reload()
				close()
				toast.success(__('Meeting provider created successfully'))
			},
			onError(err) {
				close()
				toast.error(
					cleanError(err.messages[0]) || __('Error creating meeting provider')
				)
			},
		}
	)
}

const updateAccount = async (close: () => void) => {
	if (props.accountID != account.account_name) {
		await renameDoc()
	}
	setValue(close)
}

const renameDoc = async () => {
	await call('frappe.client.rename_doc', {
		doctype: 'LMS Meeting Provider Settings',
		old_name: props.accountID,
		new_name: account.account_name,
	})
}

const setValue = (close: () => void) => {
	meetingProviders.value?.setValue.submit(
		{
			...account,
			name: account.account_name,
		},
		{
			onSuccess() {
				meetingProviders.value?.reload()
				close()
				toast.success(__('Meeting provider updated successfully'))
			},
			onError(err: any) {
				close()
				toast.error(
					cleanError(err.messages[0]) || __('Error updating meeting provider')
				)
			},
		}
	)
}
</script>
