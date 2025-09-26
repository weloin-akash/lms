<template>
	<div class="font-selector flex items-center gap-1">
		<button
			v-for="option in fontOptions"
			:key="option.value"
			@click="setFontSize(option.value)"
			class="flex items-center justify-center w-6 h-6 font-bold transition-colors duration-200 hover:text-blue-600"
			:class="[
				currentFontSize === option.value 
					? 'text-blue-600' 
					: 'text-gray-600',
				option.sizeClass
			]"
			:title="`Font Size: ${option.title}`"
		>
			A
		</button>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentFontSize = ref('normal')

const fontOptions = [
	{ 
		value: 'small', 
		size: '14px', 
		title: 'Small',
		sizeClass: 'text-xs'
	},
	{ 
		value: 'normal', 
		size: '16px', 
		title: 'Normal',
		sizeClass: 'text-base'
	},
	{ 
		value: 'big', 
		size: '18px', 
		title: 'Large',
		sizeClass: 'text-lg'
	}
]

const setFontSize = (size) => {
	currentFontSize.value = size
	const selectedOption = fontOptions.find(option => option.value === size)
	
	if (selectedOption) {
		
		document.documentElement.style.fontSize = selectedOption.size
		localStorage.setItem('lms-font-size', size)
	}
}


onMounted(() => {
	const savedFontSize = localStorage.getItem('lms-font-size')
	if (savedFontSize && fontOptions.find(option => option.value === savedFontSize)) {
		setFontSize(savedFontSize)
	} else {
		
		setFontSize('normal')
	}
})
</script>
