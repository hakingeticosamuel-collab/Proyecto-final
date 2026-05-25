<template>
  <div class="group relative overflow-hidden rounded-[16px] border border-transparent bg-white/60 backdrop-blur-sm p-4 transition duration-300 hover:shadow-lg">
    <div class="flex items-start justify-between gap-4">
      <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-white/40 text-indigo-700">
        <slot name="icon">
          <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v20" />
            <path d="M5 12h14" />
          </svg>
        </slot>
      </div>
      <div class="text-right">
        <p class="text-xs uppercase tracking-wider text-slate-400">{{ subtitle }}</p>
        <p class="mt-1 text-2xl font-semibold text-slate-900">{{ value }}</p>
      </div>
    </div>
    <div class="mt-3">
      <div v-if="loading" class="h-4 w-3/4 animate-pulse rounded bg-slate-100"></div>
      <p v-else class="mt-3 text-sm leading-6 text-slate-500">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  subtitle: { type: String, default: 'Métrica' },
  value: { type: [String, Number], required: true },
  description: { type: String, default: '' },
})
const loading = false
</script>
