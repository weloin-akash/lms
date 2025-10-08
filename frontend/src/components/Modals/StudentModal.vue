<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Add a Student'),
			size: 'sm',
			actions: [
				{
					label: 'Submit',
					variant: 'solid',
					onClick: (close) => addStudent(close),
					class: '!bg-[#66bb6a] hover:!bg-[#088304] !text-white !border-0 shadow-lg hover:shadow-xl transition-all duration-200 !outline-none focus:!outline-none focus:!ring-2 focus:!ring-[#ed8e22] focus:!ring-offset-2',
				},
			],
		}"
	>
		<template #body-content>
			<div class="flex flex-col gap-4">
				<Link
					doctype="User"
					v-model="student"
					:filters="{ ignore_user_type: 1 }"
					:onCreate="
						(value, close) => {
							openSettings('Members', close)
						}
					"
				/>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { Dialog, createResource, toast } from 'frappe-ui'
import { ref, inject } from 'vue'
import Link from '@/components/Controls/Link.vue'
import { useOnboarding } from 'frappe-ui/frappe'
import { openSettings } from '@/utils'

const students = defineModel('reloadStudents')
const batchModal = defineModel('batchModal')
const student = ref()
const user = inject('$user')
const { updateOnboardingStep } = useOnboarding('learning')
const show = defineModel()

const props = defineProps({
	batch: {
		type: String,
		default: null,
	},
})

const studentResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Batch Enrollment',
				batch: props.batch,
				member: student.value,
			},
		}
	},
})

const addStudent = (close) => {
	studentResource.submit(
		{},
		{
			onSuccess() {
				if (user.data?.is_system_manager)
					updateOnboardingStep('add_batch_student')

				students.value.reload()
				batchModal.value.reload()
				student.value = null
				close()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}
</script>
