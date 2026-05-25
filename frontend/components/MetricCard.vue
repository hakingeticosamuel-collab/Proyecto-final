<template>
  <div class="group overflow-hidden rounded-[24px] border border-slate-200/80 bg-white/90 p-5 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-2xl">
    <div class="flex items-start justify-between gap-4">
      <div class="flex h-12 w-12 items-center justify-center rounded-3xl bg-indigo-600/10 text-indigo-700 shadow-sm">
        <slot name="icon">
          <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19h16" />
            <path d="M4 14h10" />
            <path d="M4 9h16" />
          </svg>
        </slot>
      </div>
      <div class="text-right">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">{{ subtitle }}</p>
        <p class="mt-2 text-3xl font-semibold text-slate-950">{{ value }}</p>
      </div>
    </div>
    <p class="mt-4 text-sm leading-6 text-slate-600">{{ description }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  subtitle: {
    type: String,
    default: 'Métrica',
  },
  value: {
    type: [String, Number],
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
})
</script>
