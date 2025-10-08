<script setup lang="ts">
import { Breadcrumbs } from 'frappe-ui'
import FontSelector from '@/components/FontSelector.vue'

const props = defineProps<{
	title?: string
	description?: string
	breadcrumbs?: any[]
}>()
</script>
<template>
    <!-- Modern header style (with icon, title, description) -->
    <header
		v-if="title || description || $slots.icon || $slots.breadcrumbs || breadcrumbs"
		class="sticky top-0 z-10 backdrop-blur-md bg-[#fef9f3]/80 border-b border-gray-200/50 px-6 py-4 shadow-sm"
	>
		<div class="flex items-center justify-between">
			<div class="flex items-center space-x-4">
				<div v-if="$slots.icon" class="w-10 h-10 bg-[#ed8e22] rounded-xl flex items-center justify-center">
					<slot name="icon" />
				</div>
				<div>
					<!-- Use breadcrumbs as title if provided, otherwise show regular title -->
					<h1 v-if="$slots.breadcrumbs || breadcrumbs" class="text-2xl font-bold text-gray-900">
						<slot v-if="$slots.breadcrumbs" name="breadcrumbs" />
						<Breadcrumbs v-else-if="breadcrumbs" class="h-7" :items="breadcrumbs" />
					</h1>
					<h1 v-else class="text-2xl font-bold text-gray-900">
						<slot v-if="$slots.title" name="title" />
						<template v-else>{{ title }}</template>
					</h1>
					<p v-if="description || $slots.description" class="text-gray-600 text-sm">
						<slot v-if="$slots.description" name="description" />
						<template v-else>{{ description }}</template>
					</p>
				</div>
			</div>
			<div class="flex items-center space-x-4">
				<FontSelector />
				<slot name="actions" />
			</div>
		</div>
	</header>
	
	<!-- Simple breadcrumb header style -->
	<header
		v-else
		class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<div class="flex items-center h-7">
			<slot v-if="$slots.breadcrumbs" name="breadcrumbs" />
			<Breadcrumbs v-else-if="breadcrumbs" class="h-7" :items="breadcrumbs" />
		</div>
		<div class="flex items-center space-x-2">
			<FontSelector />
			<slot name="actions" />
		</div>
	</header>
</template>