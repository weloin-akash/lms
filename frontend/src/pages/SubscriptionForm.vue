<template>
  <div class="min-h-screen flex flex-col">
    <!-- Main grid responsive -->
    <div class="grid grid-cols-1 lg:grid-cols-[65%,35%] gap-6 h-full">

      <!-- LEFT SECTION -->
      <div class="w-full">
        <AppHeader :title="__('Subscription Create')" :description="__('Create a plan that fits your needs')">
          <template #icon>
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </template>

          <template #actions>
            <Button variant="solid" @click="submitSubscription"
              class="ml-2 !bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium">
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </template>
              {{ __('Save') }}
            </Button>
          </template>
        </AppHeader>

        <!-- MAIN FORM AREA -->
        <div class="w-full px-4 md:px-6 lg:px-8 py-6 bg-gray-50/40">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 md:p-8">

            <!-- Header -->
            <div class="flex items-center space-x-3 mb-6">
              <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 class="text-xl font-bold text-gray-900">Subscription Details</h2>
            </div>

            <div class="space-y-6">
              <!-- Row 1 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <FormControl v-model="subscription.name1" :label="__('Name')" required />

                <FormControl v-model="subscription.duration_type" type="select" :options="durationTypeOptions"
                  :label="__('Duration Type')" />
              </div>

              <!-- Row 2 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <FormControl v-model="subscription.amount" type="number" :label="__('Amount')" />

                <FormControl v-model="subscription.description" type="textarea" :label="__('Description')" rows="3" />
              </div>

              <!-- Row 3 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <FormControl v-model="subscription.features" type="textarea" rows="3" :label="__('Features')" />

                <!-- <FormControl v-model="subscription.duration_type" type="select" :options="durationTypeOptions"
                  :label="__('Duration Type')" /> -->
              </div>

              <!-- Row 4 -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
                <FormControl type="checkbox" v-model="subscription.active" :label="__('Active')" />

                <FormControl type="checkbox" v-model="subscription.is_discount" :label="__('Discount Available')" />

                <div v-if="subscription.is_discount">
                  <FormControl v-model="subscription.discount_percentage" type="number" :label="__('Discount (%)')"
                    placeholder="0–100" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT SIDEBAR -->
      <div class="w-full h-full lg:border-l bg-gray-50">
        
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
  usePageMeta
} from 'frappe-ui'
import { reactive, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import { getMetaInfo, updateMetaInfo } from '@/utils'

const router = useRouter()
const userInfo = ref(null)

const props = defineProps({
  subscriptionName: String,
  profile: {
    type: Object,
    required: true,
  },
})

const profile = createResource({
  url: "frappe.client.get_list",
  params: {
    doctype: "User",
    filters: {
      username: props.profile?.data?.username,
    },
    fields: ["*"],
    limit: 1
  },
  auto: true,
})
watch(
  () => profile.data,
  (val) => {
    if (Array.isArray(val) && val.length > 0) {
      userInfo.value = val[0]
    }
  }
)
// console.log(profile.data.val.email)

const planTypeOptions = [
  { label: "Basic", value: "Basic" },
  { label: "Pro", value: "Pro" }
]

const durationTypeOptions = [
  { label: "Monthly", value: "Month" },
  { label: "Yearly", value: "Year" }
]
const subscription = reactive({
  name1: '',
  plan_type: '',
  is_discount: false,
  duration_type: '',
  description: '',
  amount: '',
  features: '',
  discount_percentage: 0,
  discount: 0,
  active: true,
})

const meta = reactive({
  description: '',
  keywords: '',
})

const subscriptionResource = createResource({
  url: 'frappe.client.get',
  auto: false,
  makeParams() {
    return {
      doctype: 'LMS Subscription',
      name: props.subscriptionName
    }
  },
  onSuccess(data) {
    Object.assign(subscription, data)
    getMetaInfo('subscriptions', props.subscriptionName, meta)
  }
})

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

const editSubscriptionResource = createResource({
  url: 'frappe.client.set_value',
  auto: false,
  makeParams() {
    return {
      doctype: 'LMS Subscription',
      name: props.subscriptionName,
      fieldname: { ...subscription }
    }
  }
})

const submitSubscription = () => {
  if (props.subscriptionName === 'new') {
    createSubscription()
  } else {
    updateSubscription()
  }
}

const createSubscription = () => {
  createSubscriptionResource.submit(
    {},
    {
      onSuccess: (data) => {
        updateMetaInfo('subscriptions', data.name, meta)
        toast.success('Subscription created successfully.')
        router.push({
          name: 'SubscriptionForm',
          params: { subscriptionName: data.name }
        })
      },
      onError: (err) => toast.error(err.messages?.[0] || err)
    }
  )
}

const updateSubscription = () => {
  editSubscriptionResource.submit(
    {},
    {
      onSuccess: () => {
        updateMetaInfo('subscriptions', props.subscriptionName, meta)
        toast.success('Subscription updated successfully.')
      },
      onError: (err) => toast.error(err.messages?.[0] || err)
    }
  )
}

onMounted(() => {
  if (props.subscriptionName !== 'new') {
    subscriptionResource.reload()
  }
})

usePageMeta(() => ({
  title: subscription.name1 || 'New Subscription'
}))
</script>
