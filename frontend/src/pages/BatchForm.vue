<template>
	<div class="">
		<!-- <header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
			<div class="flex items-center space-x-2">
				<Button v-if="batchDetail.data?.name" @click="deleteBatch">
					<template #icon>
						<Trash2 class="size-4 stroke-1.5" />
					</template>
				</Button>
				<Button variant="solid" @click="saveBatch()" class="!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200 !outline-none focus:!outline-none focus:!ring-2 focus:!ring-[#ed8e22] focus:!ring-offset-2">
					{{ __('Save') }}
				</Button>
			</div>
		</header> -->
		<AppHeader>
			<template #icon>
				<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
				</svg>
			</template>
			<template #breadcrumbs>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #actions>
				<Button v-if="batchDetail.data?.name" @click="deleteBatch" class="hover:!bg-red-500 hover:!text-white">
					<template #icon>
						<Trash2 class="size-4 stroke-1.5" />
					</template>
				</Button>
				<Button variant="solid" @click="saveBatch()" class="!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200 !outline-none focus:!outline-none focus:!ring-2 focus:!ring-[#ed8e22] focus:!ring-offset-2">
					<template #prefix>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</template>
					{{ __('Save') }}
				</Button>
			</template>
		</AppHeader>
		<div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
			<!-- Details Card -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
				<div class="flex items-center space-x-3 mb-6">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Details') }}</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
				<div class="space-y-6">
					<FormControl
						v-model="batch.title"
						:label="__('Title')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<MultiSelect
						v-model="instructors"
						doctype="Course Evaluator"
						:label="__('Instructors')"
						:required="true"
						:onCreate="(close) => openSettings('Evaluators', close)"
						:filters="{ ignore_user_type: 1 }"
					/>
				</div>
				<FormControl
					v-model="batch.description"
					:label="__('Short Description')"
					type="textarea"
					:rows="8"
					:placeholder="__('Short description of the batch')"
					:required="true"
					class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
				/>
			</div>
		</div>

		<!-- Settings Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Settings') }}</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
				<div class="bg-gray-50 rounded-lg p-4">
					<FormControl
						v-model="batch.published"
						type="checkbox"
						:label="__('Published')"
					/>
				</div>
				<div class="bg-gray-50 rounded-lg p-4">
					<FormControl
						v-model="batch.allow_self_enrollment"
						type="checkbox"
						:label="__('Allow self enrollment')"
					/>
				</div>
				<div class="bg-gray-50 rounded-lg p-4">
					<FormControl
						v-model="batch.certification"
						type="checkbox"
						:label="__('Certification')"
					/>
				</div>
			</div>
		</div>

		<!-- Date and Time Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Date and Time') }}</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
				<div class="space-y-6">
					<FormControl
						v-model="batch.start_date"
						:label="__('Batch Start Date')"
						type="date"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						v-model="batch.end_date"
						:label="__('Batch End Date')"
						type="date"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>
				<div class="space-y-6">
					<FormControl
						v-model="batch.start_time"
						:label="__('Session Start Time')"
						type="time"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						v-model="batch.end_time"
						:label="__('Session End Time')"
						type="time"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>
				<div class="space-y-6">
					<FormControl
						v-model="batch.timezone"
						:label="__('Timezone')"
						type="text"
						:placeholder="__('Example: IST (+5:30)')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						v-model="batch.evaluation_end_date"
						:label="__('Evaluation End Date')"
						type="date"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>
			</div>
		</div>

		<!-- Batch Details Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Batch Details') }}</h2>
			</div>
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">
					{{ __('Batch Details') }}
					<span class="text-red-500">*</span>
				</label>
				<TextEditor
					:content="batch.batch_details"
					@change="(val) => (batch.batch_details = val)"
					:editable="true"
					:fixedMenu="true"
					editorClass="prose-sm max-w-none border-b border-x bg-gray-50 rounded-b-md py-1 px-2 min-h-[7rem] max-h-[20rem] overflow-y-scroll"
				/>
			</div>
		</div>

		<!-- Configurations Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Configurations') }}</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
				<div class="space-y-6">
					<FormControl
						v-model="batch.seat_count"
						:label="__('Seat Count')"
						type="number"
						:placeholder="__('Number of seats available')"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<Link
						doctype="Email Template"
						:label="__('Email Template')"
						v-model="batch.confirmation_email_template"
						:onCreate="
							(value, close) => {
								openSettings('Email Templates', close)
							}
						"
					/>
					<Link
						doctype="LMS Zoom Settings"
						:label="__('Zoom Account')"
						v-model="batch.zoom_account"
						:onCreate="
							(value, close) => {
								openSettings('Zoom Accounts', close)
							}
						"
					/>
				</div>
				<div class="space-y-6">
					<FormControl
						v-model="batch.medium"
						type="select"
						:options="[
							{
								label: 'Online',
								value: 'Online',
							},
							{
								label: 'Offline',
								value: 'Offline',
							},
						]"
						:label="__('Medium')"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<Link
						doctype="LMS Category"
						:label="__('Category')"
						v-model="batch.category"
						:onCreate="(value, close) => openSettings('Categories', close)"
					/>
				</div>
				<div class="space-y-6">
					<div>
						<div class="text-xs font-medium text-gray-700 mb-2">
							{{ __('Meta Image') }}
						</div>
						<FileUploader
							v-if="!batch.image"
							:fileTypes="['image/*']"
							:validateFile="validateFile"
							@success="(file) => saveImage(file)"
						>
							<template
								v-slot="{ file, progress, uploading, openFileSelector }"
							>
								<div class="flex items-center">
									<div
										class="border border-gray-300 rounded-lg w-fit py-5 px-5 md:px-20 cursor-pointer hover:border-[#ed8e22] transition-all duration-200"
										@click="openFileSelector"
									>
										<Image class="size-5 stroke-1 text-gray-600" />
									</div>
									<div class="ml-4">
										<Button @click="openFileSelector" class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white">
											{{ __('Upload') }}
										</Button>
										<div class="mt-1 text-gray-600 text-sm leading-5">
											{{
												__('Appears when the batch URL is shared on socials')
											}}
										</div>
									</div>
								</div>
							</template>
						</FileUploader>
						<div v-else>
							<div class="flex items-center">
								<img
									:src="batch.image.file_url"
									class="border border-gray-300 rounded-lg w-40"
								/>
								<div class="ml-4">
									<Button @click="removeImage()" class="hover:!bg-red-500 hover:!text-white">
										{{ __('Remove') }}
									</Button>
									<div class="mt-2 text-gray-600 text-sm">
										{{
											__(
												'Appears when the batch URL is shared on any online platform'
											)
										}}
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Pricing Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Pricing') }}</h2>
			</div>
			<div class="space-y-6">
				<div class="bg-gray-50 rounded-lg p-4">
					<FormControl
						v-model="batch.paid_batch"
						type="checkbox"
						:label="__('Paid Batch')"
					/>
				</div>
				<div
					v-if="batch.paid_batch"
					class="grid grid-cols-1 md:grid-cols-2 gap-6"
				>
					<FormControl
						v-model="batch.amount"
						:label="__('Amount')"
						type="number"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<Link
						doctype="Currency"
						v-model="batch.currency"
						:filters="{ enabled: 1 }"
						:label="__('Currency')"
					/>
				</div>
			</div>
		</div>

		<!-- Meta Tags Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Meta Tags') }}</h2>
			</div>
			<div class="space-y-6">
				<FormControl
					v-model="meta.description"
					:label="__('Meta Description')"
					type="textarea"
					:rows="7"
					class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
				/>
				<FormControl
					v-model="meta.keywords"
					:label="__('Meta Keywords')"
					type="textarea"
					:rows="7"
					:placeholder="__('Comma separated keywords for SEO')"
					class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
				/>
			</div>
		</div>
		</div>
	</div>
</template>
<script setup>
import {
	computed,
	getCurrentInstance,
	inject,
	onMounted,
	onBeforeUnmount,
	reactive,
	ref,
} from 'vue'
import {
	Breadcrumbs,
	FormControl,
	FileUploader,
	Button,
	TextEditor,
	createResource,
	usePageMeta,
	toast,
	call,
	Toast,
} from 'frappe-ui'
import { useRouter } from 'vue-router'
import { Image, Trash2 } from 'lucide-vue-next'
import { capture } from '@/telemetry'
import { useOnboarding } from 'frappe-ui/frappe'
import { sessionStore } from '../stores/session'
import MultiSelect from '@/components/Controls/MultiSelect.vue'
import Link from '@/components/Controls/Link.vue'
import {
	openSettings,
	getMetaInfo,
	updateMetaInfo,
	validateFile,
} from '@/utils'
import AppHeader from '@/components/AppHeader.vue'

const router = useRouter()
const user = inject('$user')
const { brand } = sessionStore()
const { updateOnboardingStep } = useOnboarding('learning')
const instructors = ref([])
const app = getCurrentInstance()
const { $dialog } = app.appContext.config.globalProperties

const props = defineProps({
	batchName: {
		type: String,
		required: true,
	},
})

const batch = reactive({
	title: '',
	published: false,
	description: '',
	batch_details: '',
	start_date: '',
	end_date: '',
	start_time: '',
	end_time: '',
	timezone: '',
	evaluation_end_date: '',
	confirmation_email_template: '',
	seat_count: '',
	medium: '',
	category: '',
	allow_self_enrollment: false,
	certification: false,
	image: null,
	paid_batch: false,
	currency: '',
	amount: 0,
	zoom_account: '',
})

const meta = reactive({
	description: '',
	keywords: '',
})

onMounted(() => {
	if (!user.data) window.location.href = '/login'
	if (props.batchName != 'new') {
		fetchBatchInfo()
	} else {
		capture('batch_form_opened')
	}
	window.addEventListener('keydown', keyboardShortcut)
})

const fetchBatchInfo = () => {
	batchDetail.reload()
	getMetaInfo('batches', props.batchName, meta)
}

const keyboardShortcut = (e) => {
	if (
		e.key === 's' &&
		(e.ctrlKey || e.metaKey) &&
		!e.target.classList.contains('ProseMirror')
	) {
		saveBatch()
		e.preventDefault()
	}
}

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

const newBatch = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Batch',
				meta_image: batch.image?.file_url,
				instructors: instructors.value.map((instructor) => ({
					instructor: instructor,
				})),
				...batch,
			},
		}
	},
})

const batchDetail = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'LMS Batch',
			name: props.batchName,
		}
	},
	onSuccess(data) {
		Object.keys(data).forEach((key) => {
			if (key == 'instructors') {
				data.instructors.forEach((instructor) => {
					instructors.value.push(instructor.instructor)
				})
			} else if (['start_time', 'end_time'].includes(key)) {
				let [hours, minutes, seconds] = data[key].split(':')
				hours = hours.length == 1 ? '0' + hours : hours
				batch[key] = `${hours}:${minutes}`
			} else if (Object.hasOwn(batch, key)) batch[key] = data[key]
		})
		let checkboxes = [
			'published',
			'paid_batch',
			'allow_self_enrollment',
			'certification',
		]
		for (let idx in checkboxes) {
			let key = checkboxes[idx]
			batch[key] = batch[key] ? true : false
		}
		if (data.meta_image) imageResource.reload({ image: data.meta_image })
	},
})

const editBatch = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'LMS Batch',
			name: props.batchName,
			fieldname: {
				meta_image: batch.image?.file_url,
				instructors: instructors.value.map((instructor) => ({
					instructor: instructor,
				})),
				...batch,
			},
		}
	},
})

const imageResource = createResource({
	url: 'lms.lms.api.get_file_info',
	makeParams(values) {
		return {
			file_url: values.image,
		}
	},
	auto: false,
	onSuccess(data) {
		batch.image = data
	},
})

const saveBatch = () => {
	if (batchDetail.data) {
		editBatchDetails()
	} else {
		createNewBatch()
	}
}

const createNewBatch = () => {
	newBatch.submit(
		{},
		{
			onSuccess(data) {
				if (user.data?.is_system_manager) {
					updateOnboardingStep('create_first_batch', true, false, () => {
						localStorage.setItem('firstBatch', data.name)
					})
				}
				updateMetaInfo('batches', data.name, meta)
				capture('batch_created')
				router.push({
					name: 'BatchDetail',
					params: {
						batchName: data.name,
					},
				})
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const editBatchDetails = () => {
	editBatch.submit(
		{},
		{
			onSuccess(data) {
				updateMetaInfo('batches', data.name, meta)
				router.push({
					name: 'BatchDetail',
					params: {
						batchName: data.name,
					},
				})
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const deleteBatch = () => {
	$dialog({
		title: __('Confirm your action to delete'),
		message: __(
			'Deleting this batch will also delete all its data including enrolled students, linked courses, assessments, feedback and discussions. Are you sure you want to continue?'
		),
		actions: [
			{
				label: __('Delete'),
				theme: 'red',
				variant: 'solid',
				onClick({ close }) {
					trashBatch(close)
					close()
				},
			},
		],
	})
}

const trashBatch = (close) => {
	call('lms.lms.api.delete_batch', {
		batch: props.batchName,
	}).then(() => {
		toast.success(__('Batch deleted successfully'))
		close()
		router.push({
			name: 'Batches',
		})
	})
}

const saveImage = (file) => {
	batch.image = file
}

const removeImage = () => {
	batch.image = null
}

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: 'Batches',
			route: {
				name: 'Batches',
			},
		},
	]
	if (batchDetail.data) {
		crumbs.push({
			label: batchDetail.data.title,
			route: {
				name: 'BatchDetail',
				params: {
					batchName: props.batchName,
				},
			},
		})
	}
	crumbs.push({
		label: props.batchName == 'new' ? 'New Batch' : 'Edit Batch',
		route: { name: 'BatchForm', params: { batchName: props.batchName } },
	})
	return crumbs
})

usePageMeta(() => {
	return {
		title: props.batchName == 'new' ? 'New Batch' : batchDetail.data?.title,
		icon: brand.favicon,
	}
})
</script>
