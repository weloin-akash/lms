<template>
	<div>
		<slot name="trigger" :open="openDialog"></slot>

		<!-- Dialog -->
		<div
			v-if="isOpen"
			class="fixed inset-0 z-50 overflow-y-auto"
			@click.self="closeDialog"
		>
			<div class="flex min-h-screen items-center justify-center p-4">
				<!-- Backdrop -->
				<div
					class="fixed inset-0 bg-black-overlay-200 transition-opacity dark:backdrop-filter dark:backdrop-blur-[1px]"
					@click="closeDialog"
				></div>

				<!-- Dialog Content -->
				<Transition
					enter-active-class="duration-200 ease-out"
					enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
					enter-to-class="opacity-100 translate-y-0 sm:scale-100"
					leave-active-class="duration-150 ease-in"
					leave-from-class="opacity-100 translate-y-0 sm:scale-100"
					leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
				>
					<Ucard
						v-if="isOpen"
						variant="elevated"
						rounded="xl"
						:divide="true"
						class="relative max-w-2xl w-full max-h-[90vh] overflow-hidden z-10 shadow-2xl"
						@click.stop
					>
						<!-- Header -->
						<template #header>
							<div class="flex items-center justify-between w-full">
								<h3 class="text-lg font-semibold text-gray-900">
									Add Students to Groups
								</h3>
								<button
									@click="closeDialog"
									class="text-gray-400 hover:text-gray-600 transition-colors"
								>
									<svg
										class="w-5 h-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M6 18L18 6M6 6l12 12"
										/>
									</svg>
								</button>
							</div>
					</template>

					<!-- Body -->
					<!-- Students Selection -->
					<div class="mb-6">
							<label class="block text-sm font-medium text-gray-700 mb-2">
								Select Students
							</label>
							<div class="relative">
								<input
									v-model="studentSearch"
									@input="searchStudents"
									@focus="showStudentDropdown = true"
									@blur="setTimeout(() => showStudentDropdown = false, 200)"
									type="text"
									placeholder="Search students..."
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
								/>
								<div
									v-if="showStudentDropdown && filteredStudents.length > 0"
									class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto"
								>
									<div
										v-for="student in filteredStudents"
										:key="student.name"
										@click="selectStudent(student)"
										class="px-4 py-2 hover:bg-gray-50 cursor-pointer flex items-center justify-between"
									>
										<div>
											<div class="font-medium text-gray-900">
												{{ student.full_name }}
											</div>
											<div class="text-sm text-gray-500">
												{{ student.name }}
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Selected Students -->
							<div
								v-if="selectedStudents.length > 0"
								class="mt-3 flex flex-wrap gap-2"
							>
								<div
									v-for="student in selectedStudents"
									:key="student.name"
									class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
								>
									<span>{{ student.full_name }}</span>
									<button
										@click="removeStudent(student)"
										class="ml-2 text-blue-600 hover:text-blue-800"
									>
										<svg
											class="w-4 h-4"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M6 18L18 6M6 6l12 12"
											/>
										</svg>
									</button>
								</div>
							</div>
						</div>

						<!-- Groups Selection -->
						<div class="mb-6">
							<label class="block text-sm font-medium text-gray-700 mb-2">
								Select Groups
							</label>
							<div class="relative">
								<input
									v-model="groupSearch"
									@input="searchGroups"
									@focus="showGroupDropdown = true"
									@blur="setTimeout(() => showGroupDropdown = false, 200)"
									type="text"
									placeholder="Search groups..."
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
								/>
								<div
									v-if="showGroupDropdown && filteredGroups.length > 0"
									class="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto"
								>
									<div
										v-for="group in filteredGroups"
										:key="group.name"
										@click="selectGroup(group)"
										class="px-4 py-2 hover:bg-gray-50 cursor-pointer"
									>
										<div class="font-medium text-gray-900">
											{{ group.group_name }}
										</div>
									</div>
								</div>
							</div>

							<!-- Selected Groups -->
							<div
								v-if="selectedGroups.length > 0"
								class="mt-3 flex flex-wrap gap-2"
							>
								<div
									v-for="group in selectedGroups"
									:key="group.name"
									class="inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
								>
									<span>{{ group.group_name }}</span>
									<button
										@click="removeGroup(group)"
										class="ml-2 text-green-600 hover:text-green-800"
									>
										<svg
											class="w-4 h-4"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M6 18L18 6M6 6l12 12"
											/>
										</svg>
									</button>
								</div>
							</div>
						</div>

						<!-- Loading State -->
						<div v-if="loading" class="text-center py-4">
							<div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
							<p class="mt-2 text-sm text-gray-600">Processing...</p>
						</div>

						<!-- Error Message -->
						<div
							v-if="errorMessage"
							class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg"
						>
							<div class="flex">
								<svg
									class="w-5 h-5 text-red-600 mr-2"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
									/>
								</svg>
							<span class="text-sm text-red-800">{{ errorMessage }}</span>
						</div>
					</div>

					<!-- Footer -->
					<template #footer>
							<div class="flex justify-between items-center w-full">
								<div class="text-sm text-gray-700 font-medium">
									<span v-if="selectedStudents.length > 0 && selectedGroups.length > 0">
										{{ selectedStudents.length }} student(s) → {{ selectedGroups.length }} group(s)
									</span>
									<span v-else class="text-gray-400">
										Select students and groups to enroll
									</span>
								</div>
								<div class="flex space-x-3">
									<button
										@click="closeDialog"
										:disabled="loading"
										class="px-6 py-2.5 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
									>
										Cancel
									</button>
									<button
										v-if="selectedStudents.length === 0 || selectedGroups.length === 0"
										disabled
										class="px-6 py-2.5 text-sm font-bold rounded-lg bg-gray-300 text-black cursor-not-allowed border-2 border-gray-400 opacity-60"
									>
										Enroll Students
									</button>
									<button
										v-else
										@click="enrollStudents"
										:disabled="loading"
										class="px-6 py-2.5 text-sm font-bold rounded-lg bg-[#ed8e22] hover:bg-[#d47a1a] text-black border-2 border-[#ed8e22] hover:border-[#d47a1a] shadow-lg hover:shadow-xl transition-all disabled:opacity-70"
									>
										<span v-if="loading" class="flex items-center">
											<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
												<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
												<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
											</svg>
											Enrolling...
										</span>
										<span v-else>Enroll Students</span>
									</button>
								</div>
							</div>
						</template>
					</Ucard>
				</Transition>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { call } from 'frappe-ui'
import Ucard from './nuxt/Ucard.vue'

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

const emit = defineEmits(['success', 'error'])

const isOpen = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const studentSearch = ref('')
const groupSearch = ref('')

const showStudentDropdown = ref(false)
const showGroupDropdown = ref(false)

const allStudents = ref([])
const allGroups = ref([])

const filteredStudents = ref([])
const filteredGroups = ref([])

const selectedStudents = ref([])
const selectedGroups = ref([])

const openDialog = () => {
	isOpen.value = true
	loadStudents()
	loadGroups()
}

const closeDialog = () => {
	isOpen.value = false
	resetForm()
}

const resetForm = () => {
	studentSearch.value = ''
	groupSearch.value = ''
	showStudentDropdown.value = false
	showGroupDropdown.value = false
	selectedStudents.value = []
	selectedGroups.value = []
	filteredStudents.value = []
	filteredGroups.value = []
	errorMessage.value = ''
}

const loadStudents = async () => {
	try {
		const response = await call('maxlms.maxlms.doctype.lms_group_enroll.lms_group_enroll.get_students', {
			doctype: 'User',
			txt: '',
			searchfield: 'name',
			start: 0,
			page_len: 100,
			filters: {},
		})

		// frappe-ui call returns {message: data}
		const data = response?.message || response
		if (data) {
			allStudents.value = data.map((s) => ({
				name: s[0],
				full_name: s[1],
			}))
			// Initialize filtered list
			searchStudents()
		}
	} catch (error) {
		console.error('Error loading students:', error)
		errorMessage.value = 'Failed to load students'
	}
}

const loadGroups = async () => {
	try {
		const response = await call('maxlms.maxlms.doctype.lms_student_group.lms_student_group.get_student_groups', {
			txt: '',
			page_len: 100,
		})

		// frappe-ui call returns {message: data}
		const data = response?.message || response
		if (data) {
			allGroups.value = data.map((g) => ({
				name: g.name,
				group_name: g.name1 || g.name,
			}))
			// Initialize filtered list
			searchGroups()
		}
	} catch (error) {
		console.error('Error loading groups:', error)
		errorMessage.value = 'Failed to load groups: ' + (error.message || error)
	}
}

const searchStudents = () => {
	const search = studentSearch.value.trim().toLowerCase()

	if (search === '') {
		// Show all students when search is empty
		filteredStudents.value = allStudents.value
			.filter((s) => !selectedStudents.value.find((sel) => sel.name === s.name))
		return
	}

	filteredStudents.value = allStudents.value
		.filter(
			(s) =>
				s.name.toLowerCase().includes(search) ||
				s.full_name.toLowerCase().includes(search)
		)
		.filter((s) => !selectedStudents.value.find((sel) => sel.name === s.name))
}

const searchGroups = () => {
	const search = groupSearch.value.trim().toLowerCase()

	if (search === '') {
		// Show all groups when search is empty
		filteredGroups.value = allGroups.value
			.filter((g) => !selectedGroups.value.find((sel) => sel.name === g.name))
		return
	}

	filteredGroups.value = allGroups.value
		.filter((g) => g.group_name.toLowerCase().includes(search))
		.filter((g) => !selectedGroups.value.find((sel) => sel.name === g.name))
}

const selectStudent = (student) => {
	selectedStudents.value.push(student)
	studentSearch.value = ''
	searchStudents()
	showStudentDropdown.value = false
}

const removeStudent = (student) => {
	selectedStudents.value = selectedStudents.value.filter(
		(s) => s.name !== student.name
	)
	searchStudents()
}

const selectGroup = (group) => {
	selectedGroups.value.push(group)
	groupSearch.value = ''
	searchGroups()
	showGroupDropdown.value = false
}

const removeGroup = (group) => {
	selectedGroups.value = selectedGroups.value.filter(
		(g) => g.name !== group.name
	)
	searchGroups()
}

const enrollStudents = async () => {
	if (selectedStudents.value.length === 0 || selectedGroups.value.length === 0) {
		errorMessage.value = 'Please select at least one student and one group'
		return
	}

	loading.value = true
	errorMessage.value = ''

	try {
		// Create enrollment for each student
		const promises = selectedStudents.value.map(async (student) => {
			// Check if enrollment record exists
			let enrollmentName = null
			try {
				const response = await call('frappe.client.get_list', {
					doctype: 'LMS Group Enroll',
					filters: {
						student: student.name,
					},
					fields: ['name'],
					limit_page_length: 1,
				})

				const existing = response?.message || response
				if (existing && existing.length > 0) {
					enrollmentName = existing[0].name
				}
			} catch (e) {
				console.log('No existing enrollment found')
			}

			if (enrollmentName) {
				// Update existing enrollment
				return call('frappe.client.set_value', {
					doctype: 'LMS Group Enroll',
					name: enrollmentName,
					fieldname: 'enrolled_groups',
					value: selectedGroups.value.map((g) => ({
						groups: g.name,
					})),
				})
			} else {
				// Create new enrollment
				return call('frappe.client.insert', {
					doc: {
						doctype: 'LMS Group Enroll',
						student: student.name,
						enrolled_groups: selectedGroups.value.map((g) => ({
							groups: g.name,
						})),
					},
				})
			}
		})

		await Promise.all(promises)

		emit('success', {
			students: selectedStudents.value,
			groups: selectedGroups.value,
		})

		closeDialog()
	} catch (error) {
		console.error('Error enrolling students:', error)
		errorMessage.value = error.message || 'Failed to enroll students'
		emit('error', error)
	} finally {
		loading.value = false
	}
}
</script>
