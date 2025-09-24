<template>
	<Dialog
		v-model="show"
		:options="{
			size: 'lg',
		}"
	>
		<template #body>
			<div class="p-6">
				<!-- Modern Header -->
				<div class="text-center mb-8 bg-[#fef9f3] -m-6 mb-2 p-6 rounded-t-lg">
					<div class="w-16 h-16 mx-auto mb-4 bg-[#ed8e22] rounded-full flex items-center justify-center">
						<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
					</div>
					<h2 class="text-2xl font-bold text-gray-900 mb-2">
						{{
							assignmentID === 'new'
								? __('Create an Assignment')
								: __('Edit Assignment')
						}}
					</h2>
					<p class="text-gray-600 text-sm">
						{{ assignmentID === 'new' ? 'Create a new assignment for your students' : 'Update assignment details and requirements' }}
					</p>
				</div>

				<!-- Form Fields -->
				<div class="space-y-6 max-h-[60vh] overflow-y-auto">
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Title') }} <span class="text-red-500">*</span></label>
						<FormControl
							v-model="assignment.title"
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
						/>
					</div>
					
					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Submission Type') }} <span class="text-red-500">*</span></label>
						<FormControl
							v-model="assignment.type"
							type="select"
							:options="assignmentOptions"
							:required="true"
							class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
						/>
					</div>

					<div>
						<label class="block text-sm font-medium text-gray-700 mb-2">
							{{ __('Question') }} <span class="text-red-500">*</span>
						</label>
						<div class="bg-white rounded-lg border border-gray-300 overflow-hidden focus-within:border-[#ed8e22] focus-within:ring-1 focus-within:ring-[#ed8e22]">
							<TextEditor
								:content="assignment.question"
								@change="(val) => (assignment.question = val)"
								:editable="true"
								:fixedMenu="true"
								editorClass="prose-sm max-w-none bg-white rounded-lg py-3 px-4 min-h-[8rem] max-h-[18rem] overflow-y-auto focus:outline-none"
							/>
						</div>
					</div>
				</div>

				<!-- Action Buttons -->
				<div class="flex justify-end space-x-3 mt-8 pt-6 border-t border-gray-200">
					<router-link
						v-if="assignmentID !== 'new'"
						:to="{
							name: 'AssignmentSubmissionList',
							query: {
								assignmentID: assignmentID,
							},
						}"
					>
						<Button 
							variant="subtle"
							class="px-6 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors duration-200"
						>
							{{ __('Check Submissions') }}
						</Button>
					</router-link>
					<Button 
						variant="solid" 
						@click="saveAssignment"
						class="bg-[#ed8e22] hover:bg-[#d47a1a] text-white shadow-md hover:shadow-lg transition-all duration-200 px-6 py-2 rounded-lg font-medium"
					>
						{{ __('Save') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup lang="ts">
import { Button, Dialog, FormControl, TextEditor, toast } from 'frappe-ui'
import { computed, reactive, watch } from 'vue'

const show = defineModel()
const assignments = defineModel<Assignments>('assignments')

interface Assignment {
	title: string
	type: string
	question: string
}

interface Assignments {
	data: Assignment[]
	get: (params: { doctype: string; name: string }) => Promise<Assignment>
	insert: {
		submit: (params: Assignment, options: { onSuccess: () => void }) => void
	}
}

const assignment = reactive({
	title: '',
	type: '',
	question: '',
})

const props = defineProps({
	assignmentID: {
		type: String,
		default: 'new',
	},
})

watch(
	() => props.assignmentID,
	(val) => {
		if (val === 'new') {
			// Clear form for new assignment
			assignment.title = ''
			assignment.type = ''
			assignment.question = ''
		} else {
			// Populate form for editing existing assignment
			assignments.value?.data.forEach((row) => {
				if (row.name === val) {
					assignment.title = row.title
					assignment.type = row.type
					assignment.question = row.question
				}
			})
		}
	},
	{ flush: 'post' }
)

const saveAssignment = () => {
	if (props.assignmentID == 'new') {
		assignments.value.insert.submit(
			{
				...assignment,
			},
			{
				onSuccess() {
					show.value = false
					toast.success(__('Assignment created successfully'))
				},
			}
		)
	} else {
		assignments.value.setValue.submit(
			{
				...assignment,
				name: props.assignmentID,
			},
			{
				onSuccess() {
					show.value = false
					toast.success(__('Assignment updated successfully'))
				},
			}
		)
	}
}

const assignmentOptions = computed(() => {
	return [
		{ label: 'PDF', value: 'PDF' },
		{ label: 'Image', value: 'Image' },
		{ label: 'Document', value: 'Document' },
		{ label: 'Text', value: 'Text' },
		{ label: 'URL', value: 'URL' },
	]
})
</script>
