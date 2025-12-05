<template>
    <AppHeader :title="__('Subscription Plans')" :description="__('Choose a plan that fits your needs')">
        <template #icon>
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
        </template>

        <template #actions>
            <router-link v-if="canCreateSubscription()" :to="{
                name: 'SubscriptionForm',
                params: { subscriptionName: 'new' },
            }">
                <Button
                    class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg hover:shadow-xl transition-all duration-200 px-4 py-2 rounded-lg font-medium border-0">
                    <template #prefix>
                        <Plus class="h-4 w-4 stroke-1.5" />
                    </template>
                    {{ __('Create') }}
                </Button>
            </router-link>
        </template>
    </AppHeader>

    <div class="p-5 pb-10">

        <div class="flex justify-center mb-10">
            <div class="inline-flex rounded-lg border p-1">
                <!-- <button class="px-4 py-2 rounded-md text-sm"
                    :class="billingCycle === 'weekly' ? activeTab : inactiveTab" @click="billingCycle = 'weekly'">
                    Weekly
                </button> -->
                <button class="px-4 py-2 rounded-md text-sm"
                    :class="billingCycle === 'monthly' ? activeTab : inactiveTab" @click="billingCycle = 'monthly'">
                    Monthly
                </button>
                <button class="px-4 py-2 rounded-md text-sm"
                    :class="billingCycle === 'yearly' ? activeTab : inactiveTab" @click="billingCycle = 'yearly'">
                    Yearly
                </button>
            </div>
        </div>
        <!-- <div class="text-lg text-ink-gray-9 font-semibold mb-6">
            {{ __('Available Plans') }}
        </div> -->

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 items-stretch">
            <div v-for="plan in plans" :key="plan.name"
                class="rounded-xl border p-6 shadow-sm hover:shadow-lg transition-all flex flex-col h-full relative">
                <span v-if="plan.badge"
                    class="absolute top-4 right-4 bg-orange-500 text-white text-xs font-semibold px-2 py-1 rounded">
                    {{ plan.badge }}
                </span>

                <h3 class="text-xl font-semibold mb-2">{{ plan.name }}</h3>
                <p class="text-sm text-gray-500 mb-4">{{ plan.description }}</p>

                <div class="mb-4">
                    <span v-if="billingCycle === 'monthly'" class="text-sm line-through text-gray-600 mr-2">
                        ₹{{ plan.oldMonthlyPrice }}
                    </span>

                    <span v-if="billingCycle === 'yearly'" class="text-sm line-through text-gray-600 mr-2">
                        ₹{{ plan.oldYearlyPrice }}
                    </span>

                    <span class="text-3xl font-bold text-ink-gray-9">
                        ₹{{ billingCycle === 'monthly' ? plan.monthlyPrice : plan.yearlyPrice }}
                        <span class="text-sm font-medium text-gray-500">
                            / {{ billingCycle }}
                        </span>
                    </span>
                </div>

                <!-- Features -->
                <ul class="space-y-2 text-sm mb-6 flex-1">
                    <li class="flex item-center gap-2 whitespace-nowrap" v-for="feature in plan.features"
                        :key="feature">
                        <CircleCheck /> <span>{{ feature }}</span>
                    </li>
                </ul>

                <!-- Button -->
                <Button :class="plan.buttonClass + ' w-full mt-auto'">
                    {{ plan.buttonText }}
                </Button>
            </div>
        </div>
    </div>

    <!-- CTA Section -->
    <div class="mt-16 to-orange-100 rounded-xl p-8 pb-4 text-center">
        <h1 class="text-2xl font-bold text-black mb-2 text-left">
            Have Questions About the Subscriptions?
        </h1>

        <p class="text-gray-700 mb-6 text-left">
            Our expert can answer all of your questions.
        </p>

        <div class="flex flex-col md:flex-row items-start md:items-center gap-4">

            <a href='mailto:{{ company_mail }}' target="__blank"
                class="inline-flex items-center gap-2 border border-black text-black px-6 py-3 rounded-lg font-medium hover:bg-black hover:text-white transition">
                <MailIcon class="w-5 h-5" />
                Message Now
            </a>

        </div>
    </div>
</template>

<script setup>
import { Button, usePageMeta } from 'frappe-ui'
import { ref } from 'vue'
import { Plus, CircleCheck, PhoneCallIcon, MailIcon } from 'lucide-vue-next'
import AppHeader from '@/components/AppHeader.vue'
import VueApexCharts from 'vue3-apexcharts'
import { canCreateSubscription } from '@/utils'
import { sessionStore } from '@/stores/session'
const { brand } = sessionStore()

usePageMeta(() => {
    return {
        title: __('Subscription'),
        icon: brand.favicon
    }
})

const billingCycle = ref('monthly')

const plans = [
    {
        name: 'Basic',
        description: 'For individual learners',
        monthlyPrice: 99,
        yearlyPrice: 99 * 10, // 2 months free
        oldMonthlyPrice: 199,
        oldYearlyPrice: 199 * 12,
        badge: '33% OFF',
        features: ['Access to free courses', 'Community support', 'Limited downloads'],
        buttonText: 'Buy Now',
        buttonClass: '!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white'
    },
    {
        name: 'Pro',
        description: 'Best for professionals',
        monthlyPrice: 199,
        yearlyPrice: 199 * 10, // 2 months free
        oldMonthlyPrice: 399,
        oldYearlyPrice: 399 * 12,
        badge: '33% OFF',
        features: ['All Basic features', 'Premium courses', 'Certificates', 'Priority support'],
        buttonText: 'Get Pro',
        buttonClass: '!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white'
    }
]


const activeTab = 'bg-[#ed8e22] text-white shadow-sm'
const inactiveTab = 'text-grey-600 hover:text-black'
const company_mail = 'test@gmail.com'

</script>