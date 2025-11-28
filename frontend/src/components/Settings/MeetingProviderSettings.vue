<template>
	<div class="flex flex-col min-h-0 text-base">
		<div class="flex items-center justify-between mb-5">
			<div class="flex flex-col space-y-2">
				<div class="text-xl font-semibold text-ink-gray-9">
					{{ label }}
				</div>
				<div class="text-ink-gray-6 leading-5">
					{{ __(description) }}
				</div>
			</div>
			<div class="flex items-center space-x-5">
				<Button @click="openForm('new')">
					<template #prefix>
						<Plus class="h-3 w-3 stroke-1.5" />
					</template>
					{{ __('New') }}
				</Button>
			</div>
		</div>
		<div v-if="meetingProviders.data?.length" class="overflow-y-scroll">
			<ListView
				:columns="columns"
				:rows="meetingProviders.data"
				row-key="name"
				:options="{
					showTooltip: false,
					onRowClick: (row) => {
						openForm(row.name)
					},
				}"
			>
				<ListHeader
					class="mb-2 grid items-center space-x-4 rounded bg-surface-gray-2 p-2"
				>
					<ListHeaderItem :item="item" v-for="item in columns">
						<template #prefix="{ item }">
							<FeatherIcon
								v-if="item.icon"
								:name="item.icon"
								class="h-4 w-4 stroke-1.5"
							/>
						</template>
					</ListHeaderItem>
				</ListHeader>

				<ListRows>
					<ListRow :row="row" v-for="row in meetingProviders.data">
						<template #default="{ column, item }">
							<ListRowItem :item="row[column.key]" :align="column.align">
								<template #prefix>
									<div v-if="column.key == 'member_name'">
										<Avatar
											class="flex items-center"
											:image="row['member_image']"
											:label="item"
											size="sm"
										/>
									</div>
								</template>
								<div v-if="column.key == 'enabled'">
									<Badge v-if="row[column.key]" theme="green">
										{{ __('Enabled') }}
									</Badge>
									<Badge v-else theme="gray">
										{{ __('Disabled') }}
									</Badge>
								</div>
								<div v-else-if="column.key == 'provider_type'">
									<Badge
										:theme="getProviderBadgeTheme(row[column.key])"
									>
										{{ row[column.key] }}
									</Badge>
								</div>
								<div v-else class="leading-5 text-sm">
									{{ row[column.key] }}
								</div>
							</ListRowItem>
						</template>
					</ListRow>
				</ListRows>

				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								@click="removeAccount(selections, unselectAll)"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>
		<div v-else class="text-sm italic text-ink-gray-5 mt-2">
			{{ __('No meeting providers configured') }}
		</div>
	</div>
	<MeetingProviderModal
		v-model="showForm"
		v-model:meetingProviders="meetingProviders"
		:accountID="currentAccount"
	/>
</template>
<script setup lang="ts">
import {
	Avatar,
	Button,
	Badge,
	call,
	createListResource,
	FeatherIcon,
	ListView,
	ListHeader,
	ListHeaderItem,
	ListRows,
	ListRow,
	ListRowItem,
	ListSelectBanner,
	toast,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { Plus, Trash2 } from 'lucide-vue-next'
import { cleanError } from '@/utils'
import { User } from '@/components/Settings/types'
import MeetingProviderModal from '@/components/Modals/MeetingProviderModal.vue'

// Accept show model from parent (Settings.vue)
const show = defineModel('show')

const user = inject<User | null>('$user')
const showForm = ref(false)
const currentAccount = ref<string | null>(null)

const props = defineProps({
	label: String,
	description: String,
})

const meetingProviders = createListResource({
	doctype: 'LMS Meeting Provider Settings',
	fields: [
		'name',
		'enabled',
		'provider_type',
		'account_name',
		'member',
		'member_name',
		'member_image',
		'client_id',
		'client_secret',
		'account_id',
		'refresh_token',
	],
	cache: ['meetingProviders'],
})

onMounted(() => {
	fetchMeetingProviders()
})

const fetchMeetingProviders = () => {
	if (!user?.data?.is_moderator && !user?.data?.is_evaluator) return

	if (!user?.data?.is_moderator) {
		meetingProviders.update({
			filters: {
				member: user.data.name,
			},
		})
	}
	meetingProviders.reload()
}

const openForm = (accountID: string) => {
	currentAccount.value = accountID
	showForm.value = true
}

// Reset currentAccount when modal closes so the watch triggers on reopen
watch(showForm, (val) => {
	if (!val) {
		currentAccount.value = 'new'
	}
})

const removeAccount = (selections, unselectAll) => {
	call('lms.lms.api.delete_documents', {
		doctype: 'LMS Meeting Provider Settings',
		documents: Array.from(selections),
	})
		.then(() => {
			meetingProviders.reload()
			toast.success(__('Meeting providers deleted successfully'))
			unselectAll()
		})
		.catch((err) => {
			toast.error(
				cleanError(err.messages[0]) || __('Error deleting meeting providers')
			)
		})
}

const getProviderBadgeTheme = (providerType: string) => {
	switch (providerType) {
		case 'Google Meet':
			return 'blue'
		case 'Zoom':
			return 'orange'
		case 'Microsoft Teams':
			return 'green'
		default:
			return 'gray'
	}
}

const columns = computed(() => {
	return [
		{
			label: __('Member'),
			key: 'member_name',
			icon: 'user',
		},
		{
			label: __('Account Name'),
			key: 'name',
			icon: 'video',
		},
		{
			label: __('Provider'),
			key: 'provider_type',
			icon: 'globe',
		},
		{
			label: __('Status'),
			key: 'enabled',
			align: 'center',
			icon: 'check-square',
		},
	]
})
</script>
