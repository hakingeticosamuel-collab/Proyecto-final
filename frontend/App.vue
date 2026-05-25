<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm backdrop-blur-xl sm:p-8">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Docker first</p>
        <h2 class="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Paipa Smart Light, versión estable para contenedor</h2>
        <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
          Esta edición deja fuera login, sincronización con base de datos, Power BI y visualizaciones dependientes de servicios externos. El objetivo es validar una base sólida, reproducible y fácil de desplegar en Docker.
        </p>
        <div class="mt-6 flex flex-wrap gap-3">
          <a href="#arquitectura" class="rounded-2xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">Ver arquitectura</a>
          <a href="#estado" class="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">Ver estado</a>
        </div>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Modo" value="Docker" description="La interfaz está pensada para levantar dentro de un contenedor reproducible." />
      <MetricCard subtitle="Backend" value="Flask" description="Sirve la SPA y expone solo rutas mínimas de salud." />
      <MetricCard subtitle="Frontend" value="Vue" description="Una landing estática con navegación interna y sin dependencias externas." />
      <MetricCard subtitle="Objetivo" value="Estabilidad" description="Reducir puntos de falla y aislar el problema original por capas." />
    </template>

    <section id="dashboard" class="space-y-6">
      <div class="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Resumen</p>
          <h3 class="mt-2 text-2xl font-semibold text-slate-950">Aplicativo simplificado</h3>
          <p class="mt-3 text-sm leading-7 text-slate-600">
            Ya no se ejecutan consultas al inicio, ni se cargan tableros embebidos, ni se requiere autenticación para ver el portal. La página queda enfocada en diseño, despliegue y verificación del contenedor.
          </p>
          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Riesgo reducido</p>
              <p class="mt-3 text-2xl font-semibold text-slate-950">Menos dependencias</p>
              <p class="mt-2 text-sm text-slate-600">No depende de Somee para mostrar contenido inicial.</p>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Despliegue</p>
              <p class="mt-3 text-2xl font-semibold text-slate-950">Más predecible</p>
              <p class="mt-2 text-sm text-slate-600">La app arranca aunque un servicio externo no responda.</p>
            </div>
          </div>
        </div>

        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Ruta de validación</p>
          <div class="mt-4 space-y-4">
            <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
              <p class="text-sm font-semibold text-slate-950">1. Contenedor</p>
              <p class="mt-1 text-sm text-slate-600">Construcción reproducible con Docker y un solo punto de entrada.</p>
            </div>
            <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
              <p class="text-sm font-semibold text-slate-950">2. UI</p>
              <p class="mt-1 text-sm text-slate-600">Verificar que el layout, la tipografía y la navegación renderizan sin fallos.</p>
            </div>
            <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
              <p class="text-sm font-semibold text-slate-950">3. Aislamiento</p>
              <p class="mt-1 text-sm text-slate-600">Eliminar el acoplamiento a autenticación, datos externos y consultas en tiempo real.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="arquitectura" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Arquitectura base</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-950">Flujo mínimo para pruebas</h2>
          </div>
          <span class="rounded-full bg-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-slate-600">sin dependencias externas</span>
        </div>
        <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">1. Contenedor</p>
            <p class="mt-3 text-lg font-semibold text-slate-950">Docker</p>
            <p class="mt-2 text-sm text-slate-600">Empaqueta frontend y backend en una unidad verificable.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">2. Backend</p>
            <p class="mt-3 text-lg font-semibold text-slate-950">Flask</p>
            <p class="mt-2 text-sm text-slate-600">Sirve la SPA y un endpoint de salud simple.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">3. Frontend</p>
            <p class="mt-3 text-lg font-semibold text-slate-950">Vue</p>
            <p class="mt-2 text-sm text-slate-600">Landing clara, sobria y sin consultas dinámicas.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">4. Validación</p>
            <p class="mt-3 text-lg font-semibold text-slate-950">Health check</p>
            <p class="mt-2 text-sm text-slate-600">Permite confirmar que el contenedor está vivo.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="estado" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Estado actual</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-950">Qué sigue fuera de esta versión</h2>
          </div>
          <span class="rounded-full bg-amber-50 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-amber-800">fase de aislamiento</span>
        </div>
        <div class="mt-6 grid gap-4 lg:grid-cols-3">
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-sm font-semibold text-slate-950">Aislamiento</p>
            <p class="mt-2 text-sm text-slate-600">La versión Docker no depende de sesiones ni validaciones externas.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-sm font-semibold text-slate-950">Estabilidad</p>
            <p class="mt-2 text-sm text-slate-600">No se cargan métricas ni sincronizaciones en la pantalla inicial.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-sm font-semibold text-slate-950">Visualización externa</p>
            <p class="mt-2 text-sm text-slate-600">No se embeben tableros ni gráficos dependientes de servicios remotos.</p>
          </div>
        </div>
      </div>
    </section>
  </BaseLayout>
</template>

<script setup>
import { ref } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'

const selectedSection = ref('dashboard')

function handleNavigate(section) {
  selectedSection.value = section
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>
