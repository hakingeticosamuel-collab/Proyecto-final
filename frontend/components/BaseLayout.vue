<template>
  <div class="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(255,255,255,1),_rgba(248,250,252,1)_42%,_rgba(241,245,249,1))] text-slate-900">
    <div class="mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-4 sm:px-6 lg:px-8">
      <header class="sticky top-4 z-30 flex items-center justify-between gap-4 rounded-[22px] border border-slate-200/80 bg-white/90 p-4 shadow-sm backdrop-blur-xl sm:p-5">
        <div class="flex items-center gap-4">
          <button
            @click="toggleSidebar"
            class="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200/80 bg-white text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500/30"
            aria-label="Abrir menú"
          >
            <span class="block h-5 w-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-full w-full">
                <path d="M4 7h16M4 12h16M4 17h16" />
              </svg>
            </span>
          </button>
          <div class="space-y-1">
            <p class="text-sm uppercase tracking-wider text-slate-400">Paipa Smart Light</p>
            <h1 class="text-lg font-semibold tracking-tight text-slate-900">Portal público</h1>
          </div>
        </div>
        <div class="hidden items-center gap-3 sm:flex">
          <button @click="go('dashboard-publicado')" class="rounded-full bg-slate-950 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800">Abrir dashboard</button>
        </div>
      </header>

      <div class="mt-6 grid gap-6 lg:grid-cols-[260px_minmax(0,1fr)]">
        <aside
          :class="[
            'rounded-[24px] border border-slate-200/80 bg-white/90 p-5 shadow-sm backdrop-blur-xl transition-all lg:sticky lg:top-24 lg:self-start',
            sidebarOpen ? 'block' : 'hidden lg:block'
          ]"
        >
          <div class="flex items-center justify-between gap-4">
            <div>
              <p class="text-xs uppercase tracking-[0.26em] text-slate-500">Navegación</p>
              <p class="text-base font-semibold text-slate-950">Explora el sistema</p>
            </div>
            <button
              @click="sidebarOpen = false"
              class="inline-flex h-9 w-9 items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-600 transition hover:border-slate-300 hover:bg-slate-50 sm:hidden"
              aria-label="Cerrar menú"
            >
              ×
            </button>
          </div>
          <nav class="mt-6 space-y-2 text-sm">
            <button @click="go('introduccion')" type="button" :class="buttonClass('introduccion')">Introducción</button>
            <button @click="go('arquitectura')" type="button" :class="buttonClass('arquitectura')">Arquitectura</button>
            <button @click="go('prototipo-iot')" type="button" :class="buttonClass('prototipo-iot')">Prototipo IoT</button>
            <button @click="go('publicacion-web')" type="button" :class="buttonClass('publicacion-web')">Publicación web</button>
            <button @click="go('datos-publicos')" type="button" :class="buttonClass('datos-publicos')">Datos públicos</button>
            <button @click="go('dashboard-publicado')" type="button" :class="buttonClass('dashboard-publicado')">Dashboard publicado</button>
            <button @click="go('mapa-interactivo')" type="button" :class="buttonClass('mapa-interactivo')">Mapa interactivo</button>
            <button @click="go('resultados')" type="button" :class="buttonClass('resultados')">Resultados</button>
            <button @click="go('conclusiones')" type="button" :class="buttonClass('conclusiones')">Conclusiones</button>
            <button @click="go('evidencias')" type="button" :class="buttonClass('evidencias')">Evidencias</button>
          </nav>
          <div class="mt-8 rounded-[20px] border border-slate-200/80 bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Estado</p>
            <p class="mt-2 text-sm leading-6 text-slate-700">Vista pública optimizada para lectura rápida, responsive y con acciones concentradas en el dashboard.</p>
          </div>
        </aside>

        <main class="space-y-6 pb-10">
          <section class="space-y-4">
            <slot name="hero"></slot>
            <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <slot name="cards"></slot>
            </div>
          </section>

          <section class="space-y-6">
            <slot></slot>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({
  selectedSection: {
    type: String,
    default: 'portada',
  },
})
const emit = defineEmits(['navigate'])
const sidebarOpen = ref(false)

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

function go(section) {
  sidebarOpen.value = false
  emit('navigate', section)
}

function buttonClass(name) {
  const base = 'w-full text-left rounded-full px-4 py-3 transition duration-200'
  if (props.selectedSection === name) {
    return base + " bg-slate-950 text-white shadow-sm"
  }
  return base + " border border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50"
}
</script>
