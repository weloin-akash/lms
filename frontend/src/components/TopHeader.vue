<template>
	<div class="bg-gray-100 border-b border-gray-200 px-4 py-1 flex-shrink-0">
		<div class="flex items-center justify-end">
			<div class="flex items-center space-x-2">
				<span class="text-sm text-gray-600 mr-2">Font Size:</span>
				<FontSelector />
			</div>
		</div>
	</div>
</template>

<script setup>
import FontSelector from '@/components/FontSelector.vue'
</script>
