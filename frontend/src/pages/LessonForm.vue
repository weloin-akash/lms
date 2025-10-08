<template>
	<AppHeader>
		<template #breadcrumbs>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #icon>
			<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
			</svg>
		</template>
		<template #actions>
			<div class="flex items-center space-x-3">
				<Button 
					class="!bg-[#ed8e22] hover:!bg-[#d47a1a] !text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium !border-0"
					@click="saveLesson({ showSuccessMessage: true })"
				>
					<template #prefix>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					</template>
					{{ __('Save') }}
				</Button>
			</div>
		</template>
	</AppHeader>
	<div class="grid md:grid-cols-[75%,25%] min-h-screen">
		<div class="bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
			<!-- Lesson Details Card -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
				<div class="flex items-center space-x-3 mb-6">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<h2 class="text-xl font-bold text-gray-900">{{ __('Lesson Details') }}</h2>
				</div>
				<div class="space-y-6">
					<FormControl
						v-model="lesson.title"
						:label="__('Title')"
						:required="true"
						class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22] transition-all duration-200"
					/>
					<FormControl
						v-model="lesson.include_in_preview"
						type="checkbox"
						:label="__('Include in Preview')"
					/>
				</div>
			</div>

			<!-- Instructor Notes Card -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
				<div 
					class="flex items-center justify-between cursor-pointer"
					@click="openInstructorEditor = !openInstructorEditor"
				>
					<div class="flex items-center space-x-3">
						<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
							<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
							</svg>
						</div>
						<h2 class="text-xl font-bold text-gray-900">{{ __('Instructor Notes') }}</h2>
					</div>
					<ChevronRight
						class="stroke-2 h-5 w-5 text-gray-500 transition-transform duration-200"
						:class="{
							'rotate-90': openInstructorEditor,
						}"
					/>
				</div>
				<div
					v-show="openInstructorEditor"
					id="instructor-notes"
					class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal pt-6"
				></div>
			</div>

			<!-- Content Card -->
			<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8">
				<div class="flex items-center space-x-3 mb-6">
					<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
						<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
					</div>
					<h2 class="text-xl font-bold text-gray-900">{{ __('Content') }}</h2>
				</div>
				<div
					id="content"
					class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal"
				></div>
			</div>
		</div>
		<div class="bg-white border-l">
			<div class="sticky top-0 p-5">
				<LessonHelp />
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	createResource,
	FormControl,
	usePageMeta,
	toast,
} from 'frappe-ui'
import {
	computed,
	reactive,
	onMounted,
	inject,
	ref,
	onBeforeUnmount,
} from 'vue'
import { sessionStore } from '../stores/session'
import EditorJS from '@editorjs/editorjs'
import AppHeader from '@/components/AppHeader.vue'
import LessonHelp from '@/components/LessonHelp.vue'
import { ChevronRight } from 'lucide-vue-next'
import { getEditorTools, enablePlyr } from '@/utils'
import { capture, startRecording, stopRecording } from '@/telemetry'
import { useOnboarding } from 'frappe-ui/frappe'

const { brand } = sessionStore()
const editor = ref(null)
const instructorEditor = ref(null)
const user = inject('$user')
const openInstructorEditor = ref(false)
const { updateOnboardingStep } = useOnboarding('learning')
let autoSaveInterval
let showSuccessMessage = false

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
	chapterNumber: {
		type: String,
		required: true,
	},
	lessonNumber: {
		type: String,
		required: true,
	},
})

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		window.location.href = '/login'
	}
	capture('lesson_form_opened')
	startRecording()
	editor.value = renderEditor('content')
	instructorEditor.value = renderEditor('instructor-notes')
	window.addEventListener('keydown', keyboardShortcut)
	enablePlyr()
})

const renderEditor = (holder) => {
	return new EditorJS({
		holder: holder,
		tools: getEditorTools(true),
		autofocus: true,
		defaultBlock: 'markdown',
		onChange: async (api, event) => {
			enablePlyr()
		},
	})
}

const lesson = reactive({
	title: '',
	include_in_preview: false,
	body: '',
	instructor_notes: '',
	content: '',
})

const lessonDetails = createResource({
	url: 'lms.lms.utils.get_lesson_creation_details',
	params: {
		course: props.courseName,
		chapter: props.chapterNumber,
		lesson: props.lessonNumber,
	},
	auto: true,
	onSuccess(data) {
		if (data.lesson) {
			Object.keys(data.lesson).forEach((key) => {
				lesson[key] = data.lesson[key]
			})
			lesson.include_in_preview = data?.lesson?.include_in_preview
				? true
				: false
			addLessonContent(data)
			addInstructorNotes(data)
			enableAutoSave()
		}
	},
})

const addLessonContent = (data) => {
	editor.value.isReady.then(() => {
		if (data.lesson.content) {
			editor.value.render(JSON.parse(data.lesson.content))
		} else if (data.lesson.body) {
			let blocks = convertToJSON(data.lesson)
			editor.value.render({
				blocks: blocks,
			})
		}
	})
}

const addInstructorNotes = (data) => {
	instructorEditor.value.isReady.then(() => {
		if (data.lesson.instructor_content) {
			instructorEditor.value.render(JSON.parse(data.lesson.instructor_content))
		} else if (data.lesson.instructor_notes) {
			let blocks = convertToJSON(data.lesson)
			instructorEditor.value.render({
				blocks: blocks,
			})
		}
	})
}

const enableAutoSave = () => {
	autoSaveInterval = setInterval(() => {
		saveLesson({ showSuccessMessage: false })
	}, 10000)
}

const keyboardShortcut = (e) => {
	if (
		e.key === 's' &&
		(e.ctrlKey || e.metaKey) &&
		!e.target.classList.contains('ProseMirror')
	) {
		saveLesson({ showSuccessMessage: true })
		e.preventDefault()
	}
}

onBeforeUnmount(() => {
	clearInterval(autoSaveInterval)
	window.removeEventListener('keydown', keyboardShortcut)
	stopRecording()
})

const newLessonResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'Course Lesson',
				course: props.courseName,
				chapter: lessonDetails.data?.chapter.name,
				...lesson,
			},
		}
	},
})

const editLesson = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'Course Lesson',
			name: values.lesson,
			fieldname: lesson,
		}
	},
})

const lessonReference = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'Lesson Reference',
				parent: lessonDetails.data?.chapter.name,
				parenttype: 'Course Chapter',
				parentfield: 'lessons',
				lesson: values.lesson,
				idx: props.lessonNumber,
			},
		}
	},
})

const convertToJSON = (lessonData) => {
	let blocks = []
	if (lessonData.youtube) {
		let youtubeID = lessonData.youtube.split('/').pop()
		blocks.push({
			type: 'embed',
			data: {
				service: 'youtube',
				embed: `https://www.youtube.com/embed/${youtubeID}`,
			},
		})
	}
	lessonData.body.split('\n').forEach((block) => {
		if (block.includes('{{ YouTubeVideo')) {
			let youtubeID = block.match(/\(["']([^"']+?)["']\)/)[1]
			if (!youtubeID.includes('https://'))
				youtubeID = `https://www.youtube.com/embed/${youtubeID}`
			blocks.push({
				type: 'embed',
				data: {
					service: 'youtube',
					embed: youtubeID,
				},
			})
		} else if (block.includes('{{ Quiz')) {
			let quiz = block.match(/\(["']([^"']+?)["']\)/)[1]
			blocks.push({
				type: 'quiz',
				data: {
					quiz: quiz,
				},
			})
		} else if (block.includes('{{ Video')) {
			let video = block.match(/\(["']([^"']+?)["']\)/)[1]
			blocks.push({
				type: 'upload',
				data: {
					file_url: video,
					file_type: video.split('.').pop(),
				},
			})
		} else if (block.includes('{{ Audio')) {
			let audio = block.match(/\(["']([^"']+?)["']\)/)[1]
			blocks.push({
				type: 'upload',
				data: {
					file_url: audio,
					file_type: audio.split('.').pop(),
				},
			})
		} else if (block.includes('{{ PDF')) {
			let pdf = block.match(/\(["']([^"']+?)["']\)/)[1]
			blocks.push({
				type: 'upload',
				data: {
					file_url: pdf,
					file_type: 'pdf',
				},
			})
		} else if (block.includes('{{ Embed')) {
			let embed = block.match(/\(["']([^"']+?)["']\)/)[1]
			blocks.push({
				type: 'embed',
				data: {
					service: embed.split('|||')[0],
					embed: embed.split('|||')[1],
				},
			})
		} else if (block.includes('![]')) {
			let image = block.match(/\((.*?)\)/)[1]
			blocks.push({
				type: 'upload',
				data: {
					file_url: image,
					file_type: 'image',
				},
			})
		} else if (block.includes('#')) {
			let level = (block.match(/#/g) || []).length
			blocks.push({
				type: 'header',
				data: {
					text: block.replace(/#/g, '').trim(),
					level: level,
				},
			})
		} else {
			blocks.push({
				type: 'paragraph',
				data: {
					text: block,
				},
			})
		}
	})

	if (lessonData.quizId) {
		blocks.push({
			type: 'quiz',
			data: {
				quiz: lessonData.quizId,
			},
		})
	}

	return blocks
}

const saveLesson = (e) => {
	showSuccessMessage = false
	if (typeof e != 'undefined' && e.showSuccessMessage) {
		showSuccessMessage = true
	}
	editor.value.save().then((outputData) => {
		outputData = removeEmptyBlocks(outputData)
		lesson.content = JSON.stringify(outputData)
		instructorEditor.value.save().then((outputData) => {
			outputData = removeEmptyBlocks(outputData)
			lesson.instructor_content = JSON.stringify(outputData)
			if (lessonDetails.data?.lesson) {
				editCurrentLesson()
			} else {
				createNewLesson()
			}
		})
	})
}

const removeEmptyBlocks = (outputData) => {
	let blocks = outputData.blocks.filter((block) => {
		return Object.keys(block.data).length > 0 || block.type == 'paragraph'
	})
	outputData.blocks = blocks
	return outputData
}

const createNewLesson = () => {
	newLessonResource.submit(
		{},
		{
			validate() {
				return validateLesson()
			},
			onSuccess(data) {
				lessonReference.submit(
					{ lesson: data.name },
					{
						onSuccess() {
							if (user.data?.is_system_manager)
								updateOnboardingStep('create_first_lesson')

							capture('lesson_created')
							toast.success(__('Lesson created successfully'))
							lessonDetails.reload()
						},
					}
				)
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const editCurrentLesson = () => {
	editLesson.submit(
		{
			lesson: lessonDetails.data.lesson.name,
		},
		{
			validate() {
				return validateLesson()
			},
			onSuccess() {
				showSuccessMessage
					? toast.success(__('Lesson updated successfully'))
					: ''
			},
			onError(err) {
				toast.error(err.message)
			},
		}
	)
}

const validateLesson = () => {
	if (!lesson.title) {
		return 'Title is required'
	}
	if (!lesson.content) {
		return 'Content is required'
	}
}

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: 'Courses',
			route: { name: 'Courses' },
		},
		{
			label: lessonDetails.data?.course_title,
			route: { name: 'CourseForm', params: { courseName: props.courseName } },
		},
	]

	if (lessonDetails?.data?.lesson) {
		crumbs.push({
			label: lessonDetails.data.lesson.title,
			route: {
				name: 'Lesson',
				params: {
					courseName: props.courseName,
					chapterNumber: props.chapterNumber,
					lessonNumber: props.lessonNumber,
				},
			},
		})
	}
	crumbs.push({
		label: lessonDetails?.data?.lesson ? 'Edit Lesson' : 'Create Lesson',
		route: {
			name: 'LessonForm',
			params: {
				courseName: props.courseName,
				chapterNumber: props.chapterNumber,
				lessonNumber: props.lessonNumber,
			},
		},
	})
	return crumbs
})

usePageMeta(() => {
	return {
		title: lessonDetails?.data?.lesson
			? lessonDetails.data.lesson.title
			: 'New Lesson',
		icon: brand.favicon,
	}
})
</script>
<style>
.embed-tool__caption,
.cdx-simple-image__caption {
	display: none;
}

.ce-block__content {
	max-width: none;
}

.codex-editor--narrow .ce-toolbar__actions {
	right: 100%;
}

.ce-toolbar__content {
	max-width: none;
}

.codeBoxHolder {
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
}

.codeBoxTextArea {
	width: 100%;
	min-height: 30px;
	padding: 10px;
	border-radius: 2px 2px 2px 0;
	border: none !important;
	outline: none !important;
	font: 14px monospace;
}

.codeBoxSelectDiv {
	display: flex;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
	position: relative;
}

.codeBoxSelectInput {
	border-radius: 0 0 20px 2px;
	padding: 2px 26px;
	padding-top: 0;
	padding-right: 0;
	text-align: left;
	cursor: pointer;
	border: none !important;
	outline: none !important;
}

.codeBoxSelectDropIcon {
	position: absolute !important;
	left: 10px !important;
	bottom: 0 !important;
	width: unset !important;
	height: unset !important;
	font-size: 16px !important;
}

.codeBoxSelectPreview {
	display: none;
	flex-direction: column;
	justify-content: flex-start;
	align-items: flex-start;
	border-radius: 2px;
	box-shadow: 0 3px 15px -3px rgba(13, 20, 33, 0.13);
	position: absolute;
	top: 100%;
	margin: 5px 0;
	max-height: 30vh;
	overflow-x: hidden;
	overflow-y: auto;
	z-index: 10000;
}

.codeBoxSelectItem {
	width: 100%;
	padding: 5px 20px;
	margin: 0;
	cursor: pointer;
}

.codeBoxSelectedItem {
	background-color: lightblue !important;
}

.codeBoxShow {
	display: flex !important;
}

.dark {
	color: #abb2bf;
	background-color: #282c34;
}

.light {
	color: #383a42;
	background-color: #fafafa;
}

.codeBoxTextArea {
	line-height: 1.7;
}

.prose :where(pre):not(:where([class~='not-prose'], [class~='not-prose'] *)) {
	overflow-x: unset;
}

iframe {
	border: none !important;
}

.tc-table {
	border-left: 1px solid #e8e8eb;
}

.ce-toolbox__button[data-tool='markdown'] {
	display: none !important;
}

.ce-popover-item[data-item-name='markdown'] {
	display: none !important;
}

.plyr__volume input[type='range'] {
	display: none;
}

.plyr__control--overlaid {
	background: radial-gradient(
		circle,
		rgba(0, 0, 0, 0.4) 0%,
		rgba(0, 0, 0, 0.5) 50%
	);
}

.plyr__control:hover {
	background: none;
}

.plyr--video {
	border: 1px solid theme('colors.gray.200');
	border-radius: 8px;
}

.ce-popover__container {
	border-radius: 12px;
	padding: 8px;
}

.cdx-search-field {
	border: none;
}

.cdx-search-field__input {
	font-weight: 400;
	font-size: 13px;
}

.cdx-search-field__input::before {
	font-weight: 400;
}

.cdx-search-field__input:focus {
	--tw-ring-color: theme('colors.gray.100');
}

.ce-popover-item__title {
	font-size: 13px;
	font-weight: 400;
}

.ce-popover-item__icon svg {
	width: 15px;
	height: 15px;
}

.ce-popover--opened > .ce-popover__container {
	max-height: unset;
}

.cdx-search-field__icon svg {
	width: 15px;
	height: 15px;
}

.cdx-search-field__icon {
	margin-right: 5px;
}

.cdx-block.embed-tool {
	position: relative;
	display: inline-block;
	width: 100%;
}

:root {
	--plyr-range-fill-background: white;
	--plyr-video-control-background-hover: transparent;
}

/* Ensure Plyr settings button is visible */
.plyr__controls .plyr__control[data-plyr="settings"] {
	display: block !important;
}

/* Style the settings menu */
.plyr__menu {
	display: block;
}

.plyr__menu__container {
	min-width: 150px;
}
</style>
