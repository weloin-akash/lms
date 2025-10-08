<template>
	<div class="h-full">
		<div class="grid grid-cols-1 md:grid-cols-[70%,30%] h-full">
			<div>
				<!-- <header
					class="sticky top-0 z-10 flex flex-col md:flex-row md:items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
				>
					<Breadcrumbs class="h-7" :items="breadcrumbs" />
					<div class="flex items-center mt-3 md:mt-0">
						<Button v-if="courseResource.data?.name" @click="trashCourse()">
							<template #icon>
								<Trash2 class="w-4 h-4 stroke-1.5" />
							</template>
						</Button>
						<Button variant="solid" @click="submitCourse()" class="ml-2">
							<span>
								{{ __('Save') }}
							</span>
						</Button>
					</div>
				</header> -->
				<AppHeader>
					<template #icon>
						<svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
						</svg>
					</template>
					<template #breadcrumbs>
						<Breadcrumbs :items="breadcrumbs" />
					</template>
					<template #actions>
						<Button variant="solid" @click="submitCourse()" class="ml-2 !bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0">
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
					<!-- Course Details Card -->
					<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
						<div class="flex items-center space-x-3 mb-6">
							<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
								<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<h2 class="text-xl font-bold text-gray-900">{{ __('Course Details') }}</h2>
						</div>
						<div class="space-y-6">
							<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
								<FormControl
									v-model="course.title"
									:label="__('Title')"
									:required="true"
									class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
								/>
								<Link
									doctype="LMS Category"
									v-model="course.category"
									:label="__('Category')"
									:onCreate="(value, close) => openSettings('Categories', close)"
								/>
							</div>
							<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
								<MultiSelect
									v-model="instructors"
									doctype="User"
									:label="__('Instructors')"
									:filters="{ ignore_user_type: 1 }"
									:onCreate="(close) => openSettings('Members', close)"
									:required="true"
								/>
								<div>
									<div class="text-xs text-ink-gray-5">
										{{ __('Tags') }}
									</div>
									<FormControl
										v-model="newTag"
										:placeholder="__('Add a keyword and then press enter')"
										:class="['w-full', 'flex-1', 'my-1']"
										@keyup.enter="updateTags()"
										id="tags"
										class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
									/>
									<div>
										<div class="flex items-center flex-wrap gap-2 mt-2">
											<div
												v-if="course.tags"
												v-for="tag in course.tags?.split(', ')"
												class="flex items-center bg-orange-50 text-[#ed8e22] px-3 py-1.5 rounded-lg border border-orange-200"
											>
												{{ tag }}
												<X
													class="stroke-1.5 w-3 h-3 ml-2 cursor-pointer hover:text-red-600"
													@click="removeTag(tag)"
												/>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
							<div class="mb-4">
								<div class="text-xs text-ink-gray-5 mb-2">
									{{ __('Course Image') }}
								</div>
								<FileUploader
									v-if="!course.course_image"
									:fileTypes="['image/*']"
									:validateFile="validateFile"
									@success="(file) => saveImage(file)"
								>
									<template
										v-slot="{ file, progress, uploading, openFileSelector }"
									>
										<div class="flex items-center">
											<div
												class="border rounded-md w-fit py-5 px-20 cursor-pointer"
												@click="openFileSelector"
											>
												<Image class="size-5 stroke-1 text-ink-gray-7" />
											</div>
											<div class="ml-4">
												<Button @click="openFileSelector">
													{{ __('Upload') }}
												</Button>
												<div class="mt-1 text-ink-gray-5 text-sm leading-5">
													{{
														__('Appears on the course card in the course list')
													}}
												</div>
											</div>
										</div>
									</template>
								</FileUploader>
								<div v-else class="mb-4">
									<div class="flex items-center">
										<img
											:src="course.course_image.file_url"
											class="border rounded-md w-40"
										/>
										<div class="ml-4">
											<Button @click="removeImage()">
												{{ __('Remove') }}
											</Button>
											<div class="mt-2 text-ink-gray-5 text-sm">
												{{
													__('Appears on the course card in the course list')
												}}
											</div>
										</div>
									</div>
								</div>
							</div>

								<ColorSwatches
									v-model="course.card_gradient"
									:label="__('Color')"
									:description="__('Choose a color for the course card')"
									class="w-full"
								/>
							</div>
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
							<h2 class="text-xl font-bold text-gray-900">{{ __('Course Settings') }}</h2>
						</div>
						<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
							<div
								v-if="user.data?.is_moderator"
								class="flex flex-col space-y-5"
							>
								<FormControl
									type="checkbox"
									v-model="course.published"
									:label="__('Published')"
								/>
								<FormControl
									v-model="course.published_on"
									:label="__('Published On')"
									type="date"
								/>
							</div>
							<div class="flex flex-col space-y-5">
								<FormControl
									type="checkbox"
									v-model="course.upcoming"
									:label="__('Upcoming')"
								/>
								<FormControl
									type="checkbox"
									v-model="course.featured"
									:label="__('Featured')"
								/>
									<FormControl
										type="checkbox"
										v-model="course.disable_self_learning"
										:label="__('Disable Self Enrollment')"
									/>
								</div>
							</div>
					</div>

					<!-- About the Course Card -->
					<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
						<div class="flex items-center space-x-3 mb-6">
							<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
								<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
								</svg>
							</div>
							<h2 class="text-xl font-bold text-gray-900">{{ __('About the Course') }}</h2>
						</div>
						<div class="space-y-6">
							<FormControl
								v-model="course.short_introduction"
								type="textarea"
								:rows="5"
								:label="__('Short Introduction')"
								:placeholder="
									__(
										'A one line introduction to the course that appears on the course card'
									)
								"
								:required="true"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
							<div class="">
								<div class="mb-1.5 text-sm text-ink-gray-5">
									{{ __('Course Description') }}
									<span class="text-ink-red-3">*</span>
								</div>
								<TextEditor
									:content="course.description"
									@change="(val) => (course.description = val)"
									:editable="true"
									:fixedMenu="true"
									editorClass="prose-sm max-w-none border-b border-x bg-surface-gray-2 rounded-b-md py-1 px-2 min-h-[7rem]"
								/>
							</div>

							<FormControl
								v-model="course.video_link"
								:label="__('Preview Video')"
								:placeholder="
									__(
										'Paste the youtube link of a short video introducing the course'
									)
								"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>

							<MultiSelect
								v-model="related_courses"
								doctype="LMS Course"
								:label="__('Related Courses')"
								:filters="{ name: ['!=', courseResource.data?.name] }"
								:onCreate="
									(close) => {
										router.push({
											name: 'CourseForm',
											params: { courseName: 'new' },
										})
									}
								"
							/>
						</div>
					</div>

					<!-- Pricing and Certification Card -->
					<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
						<div class="flex items-center space-x-3 mb-6">
							<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
								<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<h2 class="text-xl font-bold text-gray-900">{{ __('Pricing and Certification') }}</h2>
						</div>
						<div class="space-y-6">
							<div class="grid grid-cols-1 md:grid-cols-3 gap-5">
								<FormControl
									type="checkbox"
									v-model="course.paid_course"
									:label="__('Paid Course')"
								/>
								<FormControl
									type="checkbox"
									v-model="course.enable_certification"
									:label="__('Completion Certificate')"
								/>
								<FormControl
									type="checkbox"
									v-model="course.paid_certificate"
									:label="__('Paid Certificate')"
								/>
							</div>
							<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
								<div class="space-y-5">
									<FormControl
										v-if="course.paid_course || course.paid_certificate"
										v-model="course.course_price"
										:label="__('Amount')"
										class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
									/>
									<Link
										v-if="course.paid_certificate"
										doctype="Course Evaluator"
										v-model="course.evaluator"
										:label="__('Evaluator')"
										:onCreate="
											(value, close) => openSettings('Evaluators', close)
										"
									/>
								</div>
								<Link
									v-if="course.paid_course || course.paid_certificate"
									doctype="Currency"
									v-model="course.currency"
									:filters="{ enabled: 1 }"
									:label="__('Currency')"
								/>
							</div>
						</div>
					</div>

					<!-- Meta Tags Card -->
					<div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
						<div class="flex items-center space-x-3 mb-6">
							<div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
								<svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
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
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
							<FormControl
								v-model="meta.keywords"
								:label="__('Meta Keywords')"
								type="textarea"
								:rows="7"
								:placeholder="__('Comma separated keywords for SEO')"
								class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
							/>
						</div>
					</div>
				</div>
			</div>
			<div class="border-l">
				<CourseOutline
					v-if="courseResource.data"
					:courseName="courseResource.data.name"
					:title="__('Course Outline')"
					:allowEdit="true"
				/>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Breadcrumbs,
	call,
	TextEditor,
	Button,
	createResource,
	FormControl,
	FileUploader,
	usePageMeta,
	toast,
} from 'frappe-ui'
import {
	inject,
	onMounted,
	onBeforeUnmount,
	computed,
	ref,
	reactive,
	watch,
	getCurrentInstance,
} from 'vue'
import { Image, Trash2, X } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { capture, startRecording, stopRecording } from '@/telemetry'
import { useOnboarding } from 'frappe-ui/frappe'
import { sessionStore } from '../stores/session'
import {
	openSettings,
	getMetaInfo,
	updateMetaInfo,
	validateFile,
} from '@/utils'
import Link from '@/components/Controls/Link.vue'
import CourseOutline from '@/components/CourseOutline.vue'
import MultiSelect from '@/components/Controls/MultiSelect.vue'
import ColorSwatches from '@/components/Controls/ColorSwatches.vue'
import AppHeader from '@/components/AppHeader.vue'

const user = inject('$user')
const newTag = ref('')
const { brand } = sessionStore()
const router = useRouter()
const instructors = ref([])
const related_courses = ref([])
const app = getCurrentInstance()
const { updateOnboardingStep } = useOnboarding('learning')
const { $dialog } = app.appContext.config.globalProperties

const props = defineProps({
	courseName: {
		type: String,
	},
})

const course = reactive({
	title: '',
	short_introduction: '',
	description: '',
	video_link: '',
	course_image: null,
	card_gradient: '',
	tags: '',
	category: '',
	published: false,
	published_on: '',
	featured: false,
	upcoming: false,
	disable_self_learning: false,
	enable_certification: false,
	paid_course: false,
	paid_certificate: false,
	course_price: '',
	currency: '',
	evaluator: '',
})

const meta = reactive({
	description: '',
	keywords: '',
})

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	}

	if (props.courseName !== 'new') {
		fetchCourseInfo()
	} else {
		capture('course_form_opened')
		startRecording()
	}
	window.addEventListener('keydown', keyboardShortcut)
})

const fetchCourseInfo = () => {
	courseResource.reload()
	getMetaInfo('courses', props.courseName, meta)
}

const keyboardShortcut = (e) => {
	if (
		e.key === 's' &&
		(e.ctrlKey || e.metaKey) &&
		!e.target.classList.contains('ProseMirror')
	) {
		submitCourse()
		e.preventDefault()
	}
}

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
	stopRecording()
})

const courseCreationResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Course',
				image: course.course_image?.file_url || '',
				instructors: instructors.value.map((instructor) => ({
					instructor: instructor,
				})),
				related_courses: related_courses.value.map((course) => ({
					course: course,
				})),
				...values,
			},
		}
	},
})

const courseEditResource = createResource({
	url: 'frappe.client.set_value',
	auto: false,
	makeParams(values) {
		return {
			doctype: 'LMS Course',
			name: values.course,
			fieldname: {
				image: course.course_image?.file_url || '',
				instructors: instructors.value.map((instructor) => ({
					instructor: instructor,
				})),
				related_courses: related_courses.value.map((course) => ({
					course: course,
				})),
				...course,
			},
		}
	},
})

const courseResource = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'LMS Course',
			name: props.courseName,
		}
	},
	auto: false,
	onSuccess(data) {
		Object.keys(data).forEach((key) => {
			if (key == 'instructors') {
				instructors.value = []
				data.instructors.forEach((instructor) => {
					instructors.value.push(instructor.instructor)
				})
			} else if (key == 'related_courses') {
				related_courses.value = []
				data.related_courses.forEach((course) => {
					related_courses.value.push(course.course)
				})
			} else if (Object.hasOwn(course, key)) course[key] = data[key]
		})
		let checkboxes = [
			'published',
			'upcoming',
			'disable_self_learning',
			'paid_course',
			'featured',
			'enable_certification',
			'paid_certificate',
		]
		for (let idx in checkboxes) {
			let key = checkboxes[idx]
			course[key] = course[key] ? true : false
		}

		if (data.image) imageResource.reload({ image: data.image })
		check_permission()
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
		course.course_image = data
	},
})

const submitCourse = () => {
	if (courseResource.data) {
		editCourse()
	} else {
		createCourse()
	}
}

const createCourse = () => {
	courseCreationResource.submit(course, {
		onSuccess(data) {
			updateMetaInfo('courses', data.name, meta)
			if (user.data?.is_system_manager) {
				updateOnboardingStep('create_first_course', true, false, () => {
					localStorage.setItem('firstCourse', data.name)
				})
			}

			capture('course_created')
			toast.success(__('Course created successfully'))
			router.push({
				name: 'CourseForm',
				params: { courseName: data.name },
			})
		},
		onError(err) {
			toast.error(err.messages?.[0] || err)
		},
	})
}

const editCourse = () => {
	courseEditResource.submit(
		{
			course: courseResource.data.name,
		},
		{
			onSuccess() {
				updateMetaInfo('courses', props.courseName, meta)
				toast.success(__('Course updated successfully'))
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

const deleteCourse = createResource({
	url: 'lms.lms.api.delete_course',
	makeParams(values) {
		return {
			course: props.courseName,
		}
	},
	onSuccess() {
		toast.success(__('Course deleted successfully'))
		router.push({ name: 'Courses' })
	},
})

const trashCourse = () => {
	$dialog({
		title: __('Delete Course'),
		message: __(
			'Deleting the course will also delete all its chapters and lessons. Are you sure you want to delete this course?'
		),
		actions: [
			{
				label: __('Delete'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					deleteCourse.submit()
					close()
				},
			},
		],
	})
}

watch(
	() => props.courseName !== 'new',
	(newVal) => {
		if (newVal) {
			fetchCourseInfo()
		}
	}
)

const updateTags = () => {
	if (newTag.value) {
		course.tags = course.tags ? `${course.tags}, ${newTag.value}` : newTag.value
		newTag.value = ''
	}
}

const removeTag = (tag) => {
	course.tags = course.tags
		?.split(', ')
		.filter((t) => t !== tag)
		.join(', ')
	newTag.value = ''
}

const saveImage = (file) => {
	course.course_image = file
}

const removeImage = () => {
	course.course_image = null
}

const check_permission = () => {
	let user_is_instructor = false
	if (user.data?.is_moderator) return

	instructors.value.forEach((instructor) => {
		if (!user_is_instructor && instructor == user.data?.name) {
			user_is_instructor = true
		}
	})

	if (!user_is_instructor) {
		router.push({ name: 'Courses' })
	}
}

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: 'Courses',
			route: { name: 'Courses' },
		},
	]
	if (courseResource.data) {
		crumbs.push({
			label: course.title,
			route: { name: 'CourseDetail', params: { courseName: props.courseName } },
		})
	}
	crumbs.push({
		label: props.courseName == 'new' ? 'New Course' : 'Edit Course',
		route: { name: 'CourseForm', params: { courseName: props.courseName } },
	})
	return crumbs
})

usePageMeta(() => {
	return {
		title: courseResource.data?.title || __('New Course'),
		icon: brand.favicon,
	}
})
</script>
