<template>
	<div class="">
		<!-- <header
			class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs :items="breadcrumbs" />
			<Button variant="solid" @click="saveJob()">
				{{ __('Save') }}
			</Button>
		</header> -->
		<AppHeader>
			<template #icon>
				<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
				</svg>
			</template>
			<template #breadcrumbs>
				<Breadcrumbs :items="breadcrumbs" />
			</template>
			<template #actions>
				<Button variant="solid" @click="saveJob()" class="!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200">
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
			<!-- Job Details Card -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
				<div class="flex items-center space-x-3 mb-6">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
						</svg>
					</div>
					<h2 class="text-xl font-bold text-gray-900">{{ __('Job Details') }}</h2>
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
					<div class="space-y-6">
						<FormControl
							v-model="job.job_title"
							:label="__('Title')"
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
						<FormControl
							v-model="job.type"
							:label="__('Type')"
							type="select"
							:options="jobTypes"
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
					</div>
					<div class="space-y-6">
						<FormControl
							v-model="job.location"
							:label="__('City')"
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
						<Link
							v-model="job.country"
							doctype="Country"
							:label="__('Country')"
							:required="true"
						/>
						<FormControl
							v-if="jobName != 'new'"
							v-model="job.status"
							:label="__('Status')"
							type="select"
							:options="jobStatuses"
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
						/>
					</div>
				</div>
			</div>
		<!-- Company Details Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Company Details') }}</h2>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
				<div class="space-y-6">
					<FormControl
						v-model="job.company_name"
						:label="__('Company Name')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						v-model="job.company_website"
						:label="__('Company Website')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>
				<div class="space-y-6">
					<FormControl
						v-model="job.company_email_address"
						:label="__('Company Email Address')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Company Logo') }}
							<span class="text-red-500">*</span>
						</label>
						<FileUploader
							v-if="!job.image"
							:fileTypes="['image/*']"
							:validateFile="validateFile"
							@success="(file) => saveImage(file)"
						>
							<template
								v-slot="{ file, progress, uploading, openFileSelector }"
							>
								<div>
									<Button @click="openFileSelector" :loading="uploading" class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white">
										{{
											uploading ? `Uploading ${progress}%` : 'Upload an image'
										}}
									</Button>
								</div>
							</template>
						</FileUploader>
						<div v-else class="">
							<div class="flex items-center bg-gray-50 rounded-lg p-4">
								<div class="border border-gray-300 rounded-lg p-2 mr-3">
									<FileText class="h-5 w-5 stroke-1.5 text-gray-600" />
								</div>
								<div class="flex flex-col flex-1">
									<span class="text-sm font-medium text-gray-900">
										{{ job.image.file_name }}
									</span>
									<span class="text-xs text-gray-500 mt-1">
										{{ getFileSize(job.image.file_size) }}
									</span>
								</div>
								<X
									@click="removeImage()"
									class="bg-gray-200 hover:bg-red-100 rounded-md cursor-pointer stroke-1.5 w-6 h-6 p-1 hover:text-red-500 transition-all duration-200"
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		
		<!-- Description Card -->
		<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8">
			<div class="flex items-center space-x-3 mb-6">
				<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
					<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
				</div>
				<h2 class="text-xl font-bold text-gray-900">{{ __('Description') }}</h2>
			</div>
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">
					{{ __('Job Description') }}
					<span class="text-red-500">*</span>
				</label>
				<TextEditor
					:content="job.description"
					@change="(val) => (job.description = val)"
					:editable="true"
					:fixedMenu="true"
					editorClass="prose-sm max-w-none border-b border-x bg-gray-50 rounded-b-md py-1 px-2 min-h-[7rem] max-h-[20rem] overflow-y-scroll"
				/>
			</div>
		</div>
		</div>
	</div>
</template>
<script setup>
import {
	Breadcrumbs,
	FormControl,
	createResource,
	Button,
	TextEditor,
	FileUploader,
	usePageMeta,
	toast,
} from 'frappe-ui'
import { computed, onMounted, reactive, inject } from 'vue'
import { FileText, X } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { useRouter } from 'vue-router'
import { getFileSize, validateFile } from '@/utils'
import Link from '@/components/Controls/Link.vue'
import AppHeader from '@/components/AppHeader.vue'

const user = inject('$user')
const router = useRouter()
const { brand } = sessionStore()

const props = defineProps({
	jobName: {
		type: String,
		default: 'new',
	},
})

const newJob = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'Job Opportunity',
				company_logo: job.image?.file_url,
				...job,
			},
		}
	},
})

const updateJob = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'Job Opportunity',
			name: props.jobName,
			fieldname: {
				company_logo: job.image.file_url,
				...job,
			},
		}
	},
})

const jobDetail = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'Job Opportunity',
			name: props.jobName,
		}
	},
	onSuccess(data) {
		Object.keys(data).forEach((key) => {
			if (Object.hasOwn(job, key)) job[key] = data[key]
		})
		if (data.company_logo) imageResource.reload({ image: data.company_logo })
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
		job.image = data
	},
})

const job = reactive({
	job_title: '',
	location: '',
	country: '',
	type: 'Full Time',
	status: 'Open',
	company_name: '',
	company_website: '',
	image: null,
	description: '',
	company_email_address: '',
})

onMounted(() => {
	if (!user.data) window.location.href = '/login'

	if (props.jobName != 'new') jobDetail.reload()
})

const saveJob = () => {
	if (jobDetail.data) {
		editJobDetails()
	} else {
		createNewJob()
	}
}

const createNewJob = () => {
	newJob.submit(
		{},
		{
			onSuccess(data) {
				router.push({
					name: 'JobDetail',
					params: {
						job: data.name,
					},
				})
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const editJobDetails = () => {
	updateJob.submit(
		{},
		{
			onSuccess(data) {
				router.push({
					name: 'JobDetail',
					params: {
						job: data.name,
					},
				})
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const saveImage = (file) => {
	job.image = file
}

const removeImage = () => {
	job.image = null
}

const jobTypes = computed(() => {
	return [
		{ label: 'Full Time', value: 'Full Time' },
		{ label: 'Part Time', value: 'Part Time' },
		{ label: 'Contract', value: 'Contract' },
		{ label: 'Freelance', value: 'Freelance' },
	]
})

const jobStatuses = computed(() => {
	return [
		{ label: 'Open', value: 'Open' },
		{ label: 'Closed', value: 'Closed' },
	]
})

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: 'Jobs',
			route: { name: 'Jobs' },
		},
		{
			label: props.jobName == 'new' ? 'New Job' : 'Edit Job',
			route: { name: 'JobForm' },
		},
	]
	return crumbs
})

usePageMeta(() => {
	return {
		title: props.jobName == 'new' ? 'New Job' : jobDetail.data?.title,
		icon: brand.favicon,
	}
})
</script>
