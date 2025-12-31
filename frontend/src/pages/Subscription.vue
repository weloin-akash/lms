<template>
    <AppHeader :title="__('Subscription Plans')" :description="__('Choose a plan that fits your needs')">
        <template #icon>
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
        </template>

        <template #actions>
            <router-link v-if="canCreateSubscription()"
                :to="{ name: 'SubscriptionForm', params: { subscriptionName: 'new' } }">
                <Button
                    class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white shadow-lg px-4 py-2 rounded-lg font-medium border-0">
                    <template #prefix>
                        <Plus class="h-4 w-4 stroke-1.5" />
                    </template>
                    {{ __('Create') }}
                </Button>
            </router-link>
        </template>
    </AppHeader>

    <div class="p-5 pb-10">

        <!-- Billing Toggle -->
        <div class="flex justify-center mb-10">
            <div class="inline-flex rounded-lg border p-1">
                <button class="px-4 py-2 rounded-md text-sm"
                    :class="billingCycle === 'monthly' ? activeTab : inactiveTab"
                    @click="billingCycle = 'monthly'">Monthly</button>

                <button class="px-4 py-2 rounded-md text-sm"
                    :class="billingCycle === 'yearly' ? activeTab : inactiveTab"
                    @click="billingCycle = 'yearly'">Yearly</button>
            </div>
        </div>

        <!-- Plans Grid -->
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
                    <span v-if="plan.oldPrice" class="text-sm line-through text-gray-600 mr-2">
                        ₹{{ plan.price }}
                    </span>
                    <span class="text-3xl font-bold text-ink-gray-9">
                        ₹{{ plan.oldPrice ?? plan.price}}
                        <span class="text-sm font-medium text-gray-500">/ {{ billingCycle }}</span>
                    </span>
                </div>

                <ul class="space-y-2 text-sm mb-6 flex-1">
                    <li class="flex item-center gap-2 whitespace-nowrap" v-for="feature in plan.features"
                        :key="feature">
                        <CircleCheck /> <span>{{ feature }}</span>
                    </li>
                </ul>

                <Button class="!bg-[#ed8e22] hover:!bg-[#d47a1a] text-white w-full mt-auto" @click="makePayment(plan)">
                    {{ plan.buttonText }}
                </Button>
            </div>
        </div>

        <!-- Alerts -->
        <div v-if="paymentLoading"
            class="fixed top-4 right-4 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded shadow-md">
            Processing payment, please wait...
        </div>

        <div v-if="paymentError"
            class="custom-alert-container fixed top-4 right-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-md">
            {{ paymentError }}
        </div>
        <!-- <div id="custom-alert-container" class="fixed top-4 right-4 space-y-2 z-50"></div> -->


        <div v-if="paymentSuccess"
            class="fixed top-4 right-4 bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded shadow-md">
            {{ paymentSuccess }}
        </div>

    </div>


    <!-- Contact Section -->
    <div class="mt-16 to-orange-100 rounded-xl p-8 pb-4 text-center">
        <h1 class="text-2xl font-bold text-black mb-2 text-left">Have Questions About the Subscriptions?</h1>
        <p class="text-gray-700 mb-6 text-left">Our expert can answer all of your questions.</p>

        <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
            <a :href="'mailto:' + company_mail"
                class="inline-flex items-center gap-2 border border-black text-black px-6 py-3 rounded-lg font-medium hover:bg-black hover:text-white transition">
                <MailIcon class="w-5 h-5" />
                Message Now
            </a>
        </div>
    </div>
</template>

<script setup>
import { Button, createResource, usePageMeta } from 'frappe-ui'
import { ref, onMounted, watch } from 'vue'
import { Plus, CircleCheck, MailIcon } from 'lucide-vue-next'
import AppHeader from '@/components/AppHeader.vue'
import { canCreateSubscription } from '@/utils'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()

usePageMeta(() => ({
    title: __('Subscription'),
    icon: brand.favicon
}))

const billingCycle = ref('monthly')
const subscriptions = ref([])
const plans = ref([])
const paymentLoading = ref(false)
const paymentError = ref('')
const paymentSuccess = ref('')

const showError = (msg) => {
    frappe.msgprint({
        title: __('Error'),
        message: msg,
        indicator: 'red'
    });
    paymentError.value = msg
}

const extractServerError = (data) => {
    if (data.message?.error) return data.message.error

    if (data._server_messages) {
        try {
            const messages = JSON.parse(data._server_messages)
            return messages[0]?.message || messages[0] || "An error occurred."
        } catch {
            return "An unexpected error occurred."
        }
    }

    return data.error || "Something went wrong."
}

const mapSubscriptionsToPlans = () => {
    plans.value = subscriptions.value
        .filter(sub =>
            billingCycle.value === 'monthly'
                ? sub.duration_type === 'Month'
                : sub.duration_type === 'Year'
        )
        .map(sub => ({
            name: sub.name1,
            description: sub.description,
            oldPrice: sub.is_discount
                ? Math.round(sub.amount - (sub.amount * sub.discount_percentage / 100))
                : null,
            price: Number(sub.amount),
            badge: sub.is_discount ? `${sub.discount_percentage}% OFF` : null,
            features: sub.features
                ? sub.features.split(',').map(f => f.trim())
                : [],
            buttonText: 'Subscribe Now'
        }))
}

const fetchSubscriptions = async () => {
    try {
        const response = await fetch('/api/method/lms.lms.api.get_all_subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': window.csrf_token || ''
            }
        })

        const data = await response.json()
        subscriptions.value = Array.isArray(data.message) ? data.message : []

        // console.log("Fetched Subscriptions:", subscriptions.value)

        mapSubscriptionsToPlans()
    } catch (err) {
        showError("Failed to load subscription plans. Please refresh the page.")
    }
}

// fetch subscriptions on page load
onMounted(fetchSubscriptions)

// subscribe_data = ref(null)
// const subscription_data = createResource({
//   url: "frappe.client.get_list",
//   params: {
//     doctype: "LMS Subscription",
//     fields: ["*"]
//   },
//   auto: true,
// })
// watch(
//   () => subscription_data.data,
//   (val) => {
//     if (Array.isArray(val) && val.length > 0) {
//       subscribe_data.value = val[0]
//     }
//   }
// )
// console.log(subscrib_data)
// update plans when user switches monthly/yearly
watch(billingCycle, mapSubscriptionsToPlans)

const makePayment = async (plan) => {
    paymentLoading.value = true
    paymentError.value = ""
    paymentSuccess.value = ""

    try {
        const payload = {
            plan_name: plan.name,
            amount: plan.price,
            duration: billingCycle.value === "monthly" ? "Month" : "Year"
        }

        const res = await fetch('/api/method/lms.lms.api.create_subscription_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': window.csrf_token
            },
            body: JSON.stringify(payload)
        })

        const data = await res.json()

        if (data.message?.error) {
            showError(extractServerError(data))
            paymentLoading.value = false
            return
        }

        const order = data.message
        if (!order.order_id) {
            showError("Invalid order response from server.")
            paymentLoading.value = false
            return
        }

        if (typeof Razorpay === "undefined") {
            showError("Razorpay script not loaded.")
            paymentLoading.value = false
            return
        }

        const options = {
            key: order.razorpay_key,
            amount: order.amount,
            currency: "INR",
            name: plan.name,
            description: "Subscription Payment",
            order_id: order.order_id,
            prefill: {
                name: order.customer_name,
                email: order.customer_email
            },
            handler: async function (response) {
                try {
                    await frappe.call({
                        method: "lms.lms.api.verify_subscription_payment",
                        args: {
                            payment_id: response.payment_id,
                            order_id: order.order_id,
                            signature: response.razorpay_signature
                        }
                    })
                    paymentSuccess.value = "Payment successful! Thank you for subscribing."
                } catch {
                    showError("Payment verification failed.")
                } finally {
                    paymentLoading.value = false
                }
            },
            modal: {
                ondismiss: () => paymentLoading.value = false
            }
        }

        new Razorpay(options).open()

    } catch (err) {
        showError(err.message || "Something went wrong.")
        paymentLoading.value = false
    }
}

const activeTab = 'bg-[#ed8e22] text-white shadow-sm'
const inactiveTab = 'text-gray-600 hover:text-black'

const company_mail = 'test@gmail.com'
</script>

