<template>
	<Dialog
		v-model="show"
		:options="{
			title: chapterDetail ? __('Edit Chapter') : __('Add Chapter'),
			size: 'xl',
			actions: [
				{
					label: chapterDetail ? __('Update Chapter') : __('Create Chapter'),
					variant: 'solid',
					onClick: (close) =>
						chapterDetail ? editChapter(close) : addChapter(close),
					class: '!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200 !outline-none focus:!outline-none focus:!ring-2 focus:!ring-[#ed8e22] focus:!ring-offset-2',
				},
			],
		}"
	>
		<template #body-content>
			<div class="space-y-6">
				<!-- Chapter Details Section -->
				<div class="bg-gradient-to-br from-gray-50 to-gray-100/50 rounded-xl p-6 border border-gray-200/50">
					<div class="flex items-center space-x-3 mb-6">
						<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
							<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
							</svg>
						</div>
						<h3 class="text-lg font-bold text-gray-900">{{ __('Chapter Information') }}</h3>
					</div>
					<FormControl 
						:label="__('Title')" 
						v-model="chapter.title" 
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
				</div>

				<!-- SCORM Package Section -->
				<div class="bg-gradient-to-br from-orange-50 to-orange-100/30 rounded-xl p-6 border border-orange-200/50">
					<div class="flex items-center space-x-3 mb-4">
						<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
							<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
							</svg>
						</div>
						<div class="flex-1">
							<h3 class="text-lg font-bold text-gray-900">{{ __('SCORM Package') }}</h3>
							<p class="text-sm text-gray-600 mt-1">
								{{ __('Enable this only if you want to upload a SCORM package as a chapter.') }}
							</p>
						</div>
					</div>
					<div class="mt-4">
						<Switch
							size="md"
							:label="__('Enable SCORM Package Upload')"
							v-model="chapter.is_scorm_package"
						/>
					</div>
					
					<!-- File Upload Section -->
					<div v-if="chapter.is_scorm_package" class="mt-6">
						<div v-if="!chapter.scorm_package" class="border-2 border-dashed border-orange-200 rounded-lg p-8 text-center bg-white hover:border-orange-300 transition-colors duration-200">
							<FileUploader
								:fileTypes="['.zip']"
								:validateFile="validateFile"
								@success="(file) => (chapter.scorm_package = file)"
							>
								<template v-slot="{ file, progress, uploading, openFileSelector }">
									<div class="flex flex-col items-center">
										<div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-3">
											<svg class="w-6 h-6 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
											</svg>
										</div>
										<Button 
											@click="openFileSelector" 
											:loading="uploading"
											class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-md hover:shadow-lg transition-all duration-200 !border-0"
										>
											<template #prefix>
												<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
												</svg>
											</template>
											{{ uploading ? `${__('Uploading')} ${progress}%` : __('Upload ZIP File') }}
										</Button>
										<p class="text-sm text-gray-500 mt-3">{{ __('Only .zip files are supported') }}</p>
									</div>
								</template>
							</FileUploader>
						</div>
						<div v-else class="bg-white rounded-lg border border-gray-200 p-4 hover:border-orange-300 transition-colors duration-200">
							<div class="flex items-center">
								<div class="bg-orange-100 rounded-lg p-3 mr-3">
									<FileText class="h-6 w-6 stroke-1.5 text-[#ed8e22]" />
								</div>
								<div class="flex-1">
									<span class="font-medium text-gray-900 block">
										{{ chapter.scorm_package.file_name }}
									</span>
									<span class="text-sm text-gray-500 mt-1 block">
										{{ getFileSize(chapter.scorm_package.file_size) }}
									</span>
								</div>
								<button
									@click="() => (chapter.scorm_package = null)"
									class="bg-red-50 hover:bg-red-100 rounded-lg cursor-pointer p-2 ml-4 transition-colors duration-200 group"
								>
									<X class="w-5 h-5 text-red-500 group-hover:text-red-600" />
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import {
	Button,
	createResource,
	Dialog,
	FileUploader,
	FormControl,
	Switch,
	toast,
} from 'frappe-ui'
import { reactive, watch, inject } from 'vue'
import { getFileSize } from '@/utils/'
import { capture } from '@/telemetry'
import { FileText, X } from 'lucide-vue-next'
import { useOnboarding } from 'frappe-ui/frappe'

const show = defineModel()
const outline = defineModel('outline')
const user = inject('$user')
const { updateOnboardingStep } = useOnboarding('learning')

const props = defineProps({
	course: {
		type: String,
		required: true,
	},
	chapterDetail: {
		type: Object,
	},
})

const chapter = reactive({
	title: '',
	is_scorm_package: 0,
	scorm_package: null,
})

const chapterResource = createResource({
	url: 'lms.lms.api.upsert_chapter',
	makeParams(values) {
		return {
			title: chapter.title,
			course: props.course,
			is_scorm_package: chapter.is_scorm_package,
			scorm_package: chapter.scorm_package,
			name: props.chapterDetail?.name,
		}
	},
})

const chapterReference = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'Chapter Reference',
				chapter: values.name,
				parent: props.course,
				parenttype: 'LMS Course',
				parentfield: 'chapters',
			},
		}
	},
})

const addChapter = async (close) => {
	chapterResource.submit(
		{},
		{
			validate() {
				return validateChapter()
			},
			onSuccess: (data) => {
				if (user.data?.is_system_manager)
					updateOnboardingStep('create_first_chapter')

				capture('chapter_created')
				chapterReference.submit(
					{ name: data.name },
					{
						onSuccess(data) {
							cleanChapter()
							outline.value.reload()
							toast.success(__('Chapter added successfully'))
						},
						onError(err) {
							toast.error(err.messages?.[0] || err)
						},
					}
				)
				close()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const validateChapter = () => {
	if (!chapter.title) {
		return __('Title is required')
	}
	if (chapter.is_scorm_package && !chapter.scorm_package) {
		return __('Please upload a SCORM package')
	}
}

const cleanChapter = () => {
	chapter.title = ''
	chapter.is_scorm_package = 0
	chapter.scorm_package = null
}

const editChapter = (close) => {
	chapterResource.submit(
		{},
		{
			validate() {
				if (!chapter.title) {
					return 'Title is required'
				}
			},
			onSuccess() {
				outline.value.reload()
				toast.success(__('Chapter updated successfully'))
				close()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

watch(
	() => props.chapterDetail,
	(newChapter) => {
		chapter.title = newChapter?.title
		chapter.is_scorm_package = newChapter?.is_scorm_package
		chapter.scorm_package = newChapter?.scorm_package
	}
)

const validateFile = (file) => {
	let extension = file.name.split('.').pop().toLowerCase()
	if (extension !== 'zip') {
		return __('Only zip files are allowed')
	}
}
</script>
