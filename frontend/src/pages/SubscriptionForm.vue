<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <div class="grid grid-cols-1 lg:grid-cols-[100%,32%] gap-6 px-4 lg:px-6 py-6">

      <div class="w-full space-y-6">

        <AppHeader
          :title="__('Subscription Create')"
          :description="__('Create a plan that fits your needs')"
        >
          <template #icon>
            <div class="w-9 h-9 rounded-lg bg-orange-500 flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
						</svg>
            </div>
          </template>

          <template #actions>
            <Button
              variant="solid"
              @click="submitSubscription"
              class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white px-6 py-2.5 rounded-lg"
            >
              Save
            </Button>
          </template>
        </AppHeader>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 md:p-8">

          <h2 class="text-xl font-semibold mb-6">Subscription Details</h2>

          <div class="space-y-6">

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormControl v-model="subscription.name1" label="Name" required />
              <FormControl
                v-model="subscription.duration_type"
                type="select"
                :options="durationTypeOptions"
                label="Duration Type"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormControl v-model="subscription.amount" type="number" label="Amount" />
              <FormControl v-model="subscription.description" type="textarea" rows="3" label="Description" />
            </div>

            <FormControl v-model="subscription.features" type="textarea" rows="3" label="Features" />

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <FormControl type="checkbox" v-model="subscription.active" label="Active" />
              <FormControl type="checkbox" v-model="subscription.is_discount" label="Discount Available" />

              <FormControl
                v-if="subscription.is_discount"
                v-model="subscription.discount_percentage"
                type="number"
                label="Discount (%)"
              />
            </div>

          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 md:p-8">
          <h2 class="text-lg font-semibold mb-4">Subscription Access</h2>

          <div class="space-y-4">
            <div
              v-for="(item, index) in accessItems"
              :key="index"
              class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end"
            >
              <FormControl
                type="select"
                label="Reference Type"
                v-model="item.reference_doctype"
                :options="referenceTypeOptions"
                @update:modelValue="onReferenceTypeChange(index)"
                required
              />

              <FormControl
                type="select"
                label="Reference Name"
                v-model="item.reference_name"
                :options="item.referenceOptions || []"
                required
              />

              <Button
                v-if="accessItems.length > 1"
                variant="outline"
                theme="red"
                @click="accessItems.splice(index, 1)"
              >
                Remove
              </Button>
            </div>

            <Button
              variant="outline"
              @click="addAccessRow"
            >
              + Add Access
            </Button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import {
  FormControl,
  Button,
  createResource,
  toast,
  usePageMeta,
  call
} from 'frappe-ui'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'

const router = useRouter()

const subscription = reactive({
  name1: '',
  duration_type: '',
  description: '',
  amount: '',
  features: '',
  is_discount: false,
  discount_percentage: 0,
  active: true,
})

const durationTypeOptions = [
  { label: 'Monthly', value: 'Month' },
  { label: 'Yearly', value: 'Year' }
]

const referenceTypeOptions = [
  { label: 'Course', value: 'LMS Course' },
  { label: 'Batch', value: 'LMS Batch' },
  { label: 'Student Group', value: 'LMS Student Group' }
]

const accessItems = ref([
  {
    reference_doctype: '',
    reference_name: '',
    referenceOptions: []
  }
])

const addAccessRow = () => {
  accessItems.value.push({
    reference_doctype: '',
    reference_name: '',
    referenceOptions: []
  })
}

const onReferenceTypeChange = async (index) => {
  const item = accessItems.value[index]
  item.reference_name = ''
  item.referenceOptions = []

  if (!item.reference_doctype) return

  try {
    const data = await call('frappe.client.get_list', {
      doctype: item.reference_doctype,
      fields: ['name'],
      limit_page_length: 100
    })

    item.referenceOptions = (data || []).map(d => ({
      label: d.name,
      value: d.name
    }))
  } catch (err) {
    toast.error('Failed to load reference names')
    console.error(err)
  }
}

const createSubscriptionResource = createResource({
  url: 'frappe.client.insert',
  makeParams() {
    return {
      doc: {
        doctype: 'LMS Subscription',
        ...subscription
      }
    }
  }
})

const saveSubscriptionAccess = async (subscriptionId) => {
  const validItems = accessItems.value.filter(
    i => i.reference_doctype && i.reference_name
  )

  for (const item of validItems) {
    await call('frappe.client.insert', {
      doc: {
        doctype: 'LMS Subscription Access',
        subscription: subscriptionId,
        reference_doctype: item.reference_doctype,
        reference_name: item.reference_name,
        is_active: 1
      }
    })
  }
}

const submitSubscription = () => {
  createSubscriptionResource.submit({}, {
    onSuccess: async (data) => {
      await saveSubscriptionAccess(data.name)

      toast.success('Subscription created successfully')
      router.push({
        name: 'SubscriptionForm',
        params: { subscriptionName: data.name }
      })
    },
    onError: (err) => toast.error(err.messages?.[0] || err)
  })
}

usePageMeta(() => ({
  title: subscription.name1 || 'New Subscription'
}))
</script>