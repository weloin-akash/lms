<template>
  <div class="h-full">
    <div class="grid grid-cols-1 md:grid-cols-[70%,30%] h-full">
      <div>
        <AppHeader>
          <template #icon>
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </template>
          <!-- <template #breadcrumbs>
            <Breadcrumbs :items="breadcrumbs" />
          </template> -->
          <template #actions>
            <Button variant="solid" @click="saveSubscription"
              class="ml-2 !bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-6 py-2.5 rounded-lg font-medium border-0">
              <template #prefix>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M5 13l4 4L19 7" />
                </svg>
              </template>
              {{ __('Save') }}
            </Button>
          </template>
        </AppHeader>

        <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100/50 py-8 px-6">
          <!-- Subscription Details Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
            <div class="flex items-center space-x-3 mb-6">
              <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 class="text-xl font-bold text-gray-900">{{ __('Subscription Details') }}</h2>
            </div>

            <div class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <FormControl
                  v-model="subscription.name"
                  :label="__('Name')"
                  :required="true"
                  class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
                />
                <FormControl
                  v-model="subscription.type"
                  :label="__('Type')"
                  placeholder="Monthly / Yearly / Lifetime"
                  class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
                />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <FormControl
                  v-model="subscription.price"
                  type="number"
                  :label="__('Price')"
                  placeholder="Enter amount"
                  class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
                />
                <FormControl
                  v-model="subscription.description"
                  type="textarea"
                  :label="__('Description')"
                  rows="4"
                  placeholder="Enter subscription description"
                  class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
                />
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <FormControl
                  type="checkbox"
                  v-model="subscription.active"
                  :label="__('Active')"
                />
                <FormControl
                  type="checkbox"
                  v-model="subscription.featured"
                  :label="__('Featured')"
                />
              </div>
            </div>
          </div>

          <!-- Meta Tags Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200/50 p-8 mb-8">
            <div class="flex items-center space-x-3 mb-6">
              <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-[#ed8e22]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                </svg>
              </div>
              <h2 class="text-xl font-bold text-gray-900">{{ __('Meta Tags') }}</h2>
            </div>
            <div class="space-y-6">
              <FormControl
                v-model="meta.description"
                :label="__('Meta Description')"
                type="textarea"
                :rows="4"
                class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
              />
              <FormControl
                v-model="meta.keywords"
                :label="__('Meta Keywords')"
                type="textarea"
                :rows="4"
                placeholder="Comma separated keywords for SEO"
                class="rounded-lg border-gray-300 focus:border-[#ed8e22] focus:ring-[#ed8e22]"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="border-l">
        <!-- Placeholder sidebar -->
        <div class="p-6 text-gray-400 text-center">Subscription Sidebar</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { FormControl, Button, Breadcrumbs } from 'frappe-ui'
import AppHeader from '@/components/AppHeader.vue'

const props = defineProps({
  subscriptionName: String,
})

const subscription = reactive({
  name: '',
  type: '',
  price: '',
  description: '',
  active: true,
  featured: false,
})

const meta = reactive({
  description: '',
  keywords: '',
})

const saveSubscription = () => {
  console.log('Saving subscription:', subscription)
  alert('Subscription saved! (Static form)')
}

const breadcrumbs = [
  { label: 'Subscriptions', route: { name: 'Subscriptions' } },
  { label: props.subscriptionName === 'new' ? 'New Subscription' : 'Edit Subscription', route: { name: 'SubscriptionForm', params: { subscriptionName: props.subscriptionName } } },
]
</script>
