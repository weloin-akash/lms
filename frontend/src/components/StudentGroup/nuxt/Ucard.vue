<template>
    <div :class="cardClasses">
      <!-- Header -->
      <div v-if="$slots.header || title" :class="headerClasses">
        <slot name="header">
          <h3 v-if="title" class="card-title">{{ title }}</h3>
        </slot>
      </div>
  
      <!-- Body/Default Content -->
      <div :class="bodyClasses">
        <slot />
      </div>
  
      <!-- Footer -->
      <div v-if="$slots.footer" :class="footerClasses">
        <slot name="footer" />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue'
  
  interface Props {
    title?: string
    variant?: 'default' | 'outlined' | 'elevated' | 'flat'
    rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full'
    padding?: boolean
    divide?: boolean
    ring?: boolean
  }
  
  const props = withDefaults(defineProps<Props>(), {
    variant: 'default',
    rounded: 'lg',
    padding: true,
    divide: false,
    ring: false
  })
  
  const cardClasses = computed(() => {
    const classes = ['u-card']
    
    // Variant styles
    switch (props.variant) {
      case 'outlined':
        classes.push('u-card--outlined')
        break
      case 'elevated':
        classes.push('u-card--elevated')
        break
      case 'flat':
        classes.push('u-card--flat')
        break
      default:
        classes.push('u-card--default')
    }
    
    // Rounded corners
    classes.push(`u-card--rounded-${props.rounded}`)
    
    // Ring
    if (props.ring) {
      classes.push('u-card--ring')
    }
    
    // Divide sections
    if (props.divide) {
      classes.push('u-card--divide')
    }
    
    return classes.join(' ')
  })
  
  const headerClasses = computed(() => {
    const classes = ['u-card__header']
    if (props.padding) classes.push('u-card__header--padding')
    return classes.join(' ')
  })
  
  const bodyClasses = computed(() => {
    const classes = ['u-card__body']
    if (props.padding) classes.push('u-card__body--padding')
    return classes.join(' ')
  })
  
  const footerClasses = computed(() => {
    const classes = ['u-card__footer']
    if (props.padding) classes.push('u-card__footer--padding')
    return classes.join(' ')
  })
  </script>
  
  <style scoped>
  /* Base Card Styles */
  .u-card {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: all 0.2s ease-in-out;
  }
  
  /* Variants */
  .u-card--default {
    background-color: white;
    border: 1px solid #e5e7eb;
  }
  
  .u-card--outlined {
    background-color: transparent;
    border: 2px solid #e5e7eb;
  }
  
  .u-card--elevated {
    background-color: white !important;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  .u-card--elevated:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  
  .u-card--flat {
    background-color: #f9fafb;
    border: none;
  }
  
  /* Rounded corners */
  .u-card--rounded-none {
    border-radius: 0;
  }
  
  .u-card--rounded-sm {
    border-radius: 0.25rem;
  }
  
  .u-card--rounded-md {
    border-radius: 0.375rem;
  }
  
  .u-card--rounded-lg {
    border-radius: 0.5rem;
  }
  
  .u-card--rounded-xl {
    border-radius: 0.75rem;
  }
  
  .u-card--rounded-full {
    border-radius: 9999px;
  }
  
  /* Ring */
  .u-card--ring {
    outline: 2px solid transparent;
    outline-offset: 2px;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
  }
  
  /* Divide sections */
  .u-card--divide .u-card__header {
    border-bottom: 1px solid #e5e7eb;
  }
  
  .u-card--divide .u-card__footer {
    border-top: 1px solid #e5e7eb;
  }
  
  /* Header */
  .u-card__header {
    display: flex;
    align-items: center;
  }
  
  .u-card__header--padding {
    padding: 1rem 1.5rem;
  }
  
  .card-title {
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
  }
  
  /* Body */
  .u-card__body {
    flex: 1;
  }
  
  .u-card__body--padding {
    padding: 1.5rem;
  }
  
  /* Footer */
  .u-card__footer {
    display: flex;
    align-items: center;
  }
  
  .u-card__footer--padding {
    padding: 1rem 1.5rem;
  }
  
  /* Dark mode support - only apply when dark class is present */
</style>

<style>
  .dark .u-card--default,
  .dark .u-card--elevated {
    background-color: #1f2937 !important;
    border-color: #374151;
  }
  
  .dark .u-card--flat {
    background-color: #111827 !important;
  }
  
  .dark .card-title {
    color: #f9fafb;
  }
  
  .dark .u-card--divide .u-card__header,
  .dark .u-card--divide .u-card__footer {
    border-color: #374151;
  }
  
  .dark .u-card--outlined {
    border-color: #4b5563;
  }
  </style>