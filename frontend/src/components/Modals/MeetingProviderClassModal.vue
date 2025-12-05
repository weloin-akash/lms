<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Create a Live Class'),
			size: 'xl',
			actions: [
				{
					label: 'Submit',
					variant: 'solid',
					class: '!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200 !outline-none focus:!outline-none focus:!ring-2 focus:!ring-[#4285f4] focus:!ring-offset-2',
					onClick: ({ close }) => submitLiveClass(close),
				},
			],
		}"
	>
		<template #body-content>
			<div class="flex flex-col gap-4">
				<!-- Meeting Provider Selection -->
				<div class="space-y-1.5">
					<label class="block text-ink-gray-5 text-xs">
						{{ __('Select Provider') }}
						<span class="text-ink-red-3">*</span>
					</label>
					<Autocomplete
						@update:modelValue="(opt) => selectMeetingProvider(opt)"
						:modelValue="liveClass.meeting_provider"
						:options="meetingProviderOptions"
						:required="true"
						:placeholder="__('Select Google Meet, Microsoft Teams...')"
					/>
					<div
						v-if="!meetingProviders.data?.length"
						class="text-xs text-ink-amber-3 mt-1"
					>
						{{ __('No meeting providers configured. Please add one in Settings > Meeting Providers.') }}
					</div>
					<div
						v-else-if="liveClass.meeting_provider"
						class="text-xs text-ink-gray-5 mt-1"
					>
						{{ __('Provider Type:') }} <span class="font-medium">{{ selectedProviderType }}</span>
					</div>
				</div>

				<div class="grid grid-cols-2 gap-4">
					<div class="space-y-4">
						<FormControl
							type="text"
							v-model="liveClass.title"
							:label="__('Title')"
							:required="true"
						/>
						<FormControl
							v-model="liveClass.date"
							type="date"
							:label="__('Date')"
							:required="true"
						/>
						<Tooltip :text="__('Duration of the live class in minutes')">
							<FormControl
								type="number"
								v-model="liveClass.duration"
								:label="__('Duration')"
								:required="true"
							/>
						</Tooltip>
					</div>
					<div class="space-y-4">
						<Tooltip
							:text="
								__(
									'Time must be in 24 hour format (HH:mm). Example 11:30 or 22:00'
								)
							"
						>
							<FormControl
								v-model="liveClass.time"
								type="time"
								:label="__('Time')"
								:required="true"
							/>
						</Tooltip>

						<div class="space-y-1.5">
							<label class="block text-ink-gray-5 text-xs" for="batchTimezone">
								{{ __('Timezone') }}
								<span class="text-ink-red-3">*</span>
							</label>
							<Autocomplete
								@update:modelValue="(opt) => (liveClass.timezone = opt.value)"
								:modelValue="liveClass.timezone"
								:options="getTimezoneOptions()"
								:required="true"
							/>
						</div>
					</div>
				</div>
				<FormControl
					v-model="liveClass.description"
					type="textarea"
					:label="__('Description')"
				/>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Dialog,
	createResource,
	createListResource,
	Tooltip,
	FormControl,
	Autocomplete,
	toast,
} from 'frappe-ui'
import { reactive, inject, onMounted, computed } from 'vue'
import { getTimezones, getUserTimezone } from '@/utils/'

const liveClasses = defineModel('reloadLiveClasses')
const show = defineModel()
const user = inject('$user')
const dayjs = inject('$dayjs')

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

let liveClass = reactive({
	title: '',
	description: '',
	date: '',
	time: '',
	duration: '',
	timezone: '',
	batch: props.batch,
	host: user.data.name,
	meeting_provider: '',
	meeting_provider_name: '',
})

const meetingProviders = createListResource({
	doctype: 'LMS Meeting Provider Settings',
	fields: ['name', 'account_name', 'provider_type', 'enabled', 'member'],
	filters: {
		enabled: 1,
	},
	auto: true,
})

const meetingProviderOptions = computed(() => {
	if (!meetingProviders.data?.length) return []

	return meetingProviders.data
		.filter((provider) => {
			// Only show providers the current user owns or if user is moderator
			if (user.data?.is_moderator) return true
			return provider.member === user.data?.name
		})
		.map((provider) => ({
			label: `${provider.name} (${provider.provider_type})`,
			value: provider.name,
			provider_type: provider.provider_type,
		}))
})

const selectedProviderType = computed(() => {
	if (!liveClass.meeting_provider || !meetingProviders.data?.length) return ''
	const provider = meetingProviders.data.find(p => p.name === liveClass.meeting_provider)
	return provider?.provider_type || ''
})

const selectMeetingProvider = (opt) => {
	if (opt) {
		liveClass.meeting_provider = opt.value
		liveClass.meeting_provider_name = opt.label
	}
}

onMounted(() => {
	liveClass.timezone = getUserTimezone()
})

const getTimezoneOptions = () => {
	return getTimezones().map((timezone) => {
		return {
			label: timezone,
			value: timezone,
		}
	})
}

const createLiveClass = createResource({
	url: 'lms.lms.doctype.lms_batch.lms_batch.create_meeting_provider_class',
	makeParams(values) {
		return {
			doctype: 'LMS Live Class',
			batch_name: values.batch,
			meeting_provider: values.meeting_provider,
			...values,
		}
	},
})

const submitLiveClass = (close) => {
	return createLiveClass.submit(liveClass, {
		validate() {
			validateFormFields()
		},
		onSuccess() {
			liveClasses.value.reload()
			refreshForm()
			close()
			toast.success(__('Live class created successfully!'))
		},
		onError(err) {
			toast.error(err.messages?.[0] || err)
		},
	})
}

const validateFormFields = () => {
	if (!liveClass.meeting_provider) {
		return __('Please select a meeting provider.')
	}
	if (!liveClass.title) {
		return __('Please enter a title.')
	}
	if (!liveClass.date) {
		return __('Please select a date.')
	}
	if (!liveClass.time) {
		return __('Please select a time.')
	}
	if (!liveClass.timezone) {
		return __('Please select a timezone.')
	}
	if (!valideTime()) {
		return __('Please enter a valid time in the format HH:mm.')
	}
	const liveClassDateTime = dayjs(`${liveClass.date}T${liveClass.time}`).tz(
		liveClass.timezone,
		true
	)
	if (
		liveClassDateTime.isSameOrBefore(
			dayjs().tz(liveClass.timezone, false),
			'minute'
		)
	) {
		return __('Please select a future date and time.')
	}
	if (!liveClass.duration) {
		return __('Please select a duration.')
	}
}

const valideTime = () => {
	let time = liveClass.time.split(':')
	if (time.length != 2) {
		return false
	}
	if (time[0] < 0 || time[0] > 23) {
		return false
	}
	if (time[1] < 0 || time[1] > 59) {
		return false
	}
	return true
}

const refreshForm = () => {
	liveClass.title = ''
	liveClass.description = ''
	liveClass.date = ''
	liveClass.time = ''
	liveClass.duration = ''
	liveClass.timezone = getUserTimezone()
	liveClass.meeting_provider = ''
	liveClass.meeting_provider_name = ''
}
</script>
