<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm backdrop-blur-xl sm:p-8">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Entrega 3 · Proyecto Paipa Smart Light</p>
        <h2 class="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Integración total: Publicación Web, Prototipo y Sustentación</h2>
        <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
          Portal de demostración estático que resume la arquitectura, el prototipo IoT, la integración analítica (Power BI) y la guía de sustentación. Use la navegación para recorrer las secciones del informe de entrega.
        </p>
        <div class="mt-6 flex flex-wrap gap-3">
          <a href="#portada" class="rounded-2xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">Portada</a>
          <a href="#arquitectura" class="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">Arquitectura</a>
          <a href="#publicacion-web" class="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">Publicación</a>
        </div>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Modo" value="Docker" description="La interfaz está pensada para levantar dentro de un contenedor reproducible." />
      <MetricCard subtitle="Backend" value="Flask" description="Sirve la SPA y expone solo rutas mínimas de salud." />
      <MetricCard subtitle="Frontend" value="Vue" description="Una landing estática con navegación interna y sin dependencias externas." />
      <MetricCard subtitle="Objetivo" value="Estabilidad" description="Reducir puntos de falla y aislar el problema original por capas." />
    </template>

    <section id="portada" class="space-y-6">
      <div class="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Portada</p>
          <h3 class="mt-2 text-2xl font-semibold text-slate-950">Sistema Inteligente de Alumbrado Público — Paipa</h3>
          <p class="mt-3 text-sm leading-7 text-slate-600">
            Entrega 3: integración total. Este portal acompaña la sustentación con evidencia del prototipo IoT, la arquitectura de datos y la publicación web.
          </p>
          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Equipo</p>
              <p class="mt-3 text-2xl font-semibold text-slate-950">[Nombres del equipo]</p>
              <p class="mt-2 text-sm text-slate-600">Programa: [Programa académico] · Fecha: [Fecha de entrega]</p>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Entrega</p>
              <p class="mt-3 text-2xl font-semibold text-slate-950">Publicación Web + Prototipo + Sustentación</p>
              <p class="mt-2 text-sm text-slate-600">URL pública y evidencias listadas en la sección 'Dashboard publicado'.</p>
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
        <div class="mt-6">
          <pre class="rounded-md bg-slate-50 p-4 text-sm text-slate-600">IoT → SQL Server (Somee para pruebas) → ETL → DW (dw schema) → Power BI → Flask (Web)</pre>
        </div>
      </div>
    </section>

    <section id="prototipo-iot" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Prototipo IoT</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Descripción y dispositivos</h2>
        <div class="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <p class="text-sm text-slate-600">Maqueta que representa sectores de Paipa con postes de alumbrado. El prototipo simula condiciones de día/noche y presencia.</p>
            <ul class="mt-4 list-inside list-disc text-sm text-slate-600">
              <li>ESP32 (microcontrolador)</li>
              <li>BH1750 (luminosidad), PIR (movimiento)</li>
              <li>SCT-013 (corriente), DS18B20 (temperatura)</li>
            </ul>
          </div>
          <div>
            <p class="text-sm text-slate-600">Funcionamiento: lectura periódica, envío simulado a SQL Server y almacenamiento para ETL. En la documentación adjunta se muestran scripts y ejemplos de payloads.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="publicacion-web" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Publicación Web</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Arquitectura y evidencia de despliegue</h2>
        <div class="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <p class="text-sm text-slate-600">La aplicación se publica en Render usando Docker. El contenedor incluye build del frontend y servidor Flask que sirve la SPA y endpoints mínimos (`/health`, `/app`).</p>
            <p class="mt-3 text-sm text-slate-600">Comandos y archivo clave: `Dockerfile`, `render.yaml`, `requirements.txt`.</p>
          </div>
          <div>
            <p class="text-sm text-slate-600">Power BI: inserte aquí el enlace de inserción o documente la URL pública del reporte. Si el embed no es posible, capture pantallas y pegue enlaces en la sección de evidencias.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="dashboard-publicado" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Dashboard publicado</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Acceso público y filtros</h2>
        <p class="mt-3 text-sm text-slate-600">URL pública: <span class="font-medium">https://proyecto-final-24st.onrender.com</span></p>
        <p class="mt-2 text-sm text-slate-600">Filtros disponibles: rango de fechas, zona/ubicación, dispositivo y estado de alertas (si aplica).</p>
      </div>
    </section>

    <section id="sustentacion" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Sustentación</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Guía de presentación</h2>
        <ul class="mt-3 list-inside list-disc text-sm text-slate-600">
          <li>Duración sugerida: 10–15 minutos.</li>
          <li>Estructura: presentación, demo maqueta, ETL/SQL, Power BI, sitio Flask, conclusiones.</li>
          <li>Roles: dividir la demostración entre integrantes según secciones.</li>
        </ul>
      </div>
    </section>

    <section id="demostracion-tecnica" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Demostración técnica</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Qué mostrar en vivo</h2>
        <ol class="mt-3 list-inside list-decimal text-sm text-slate-600">
          <li>Acceso al servidor SQL (Somee o local) y muestra de tablas.</li>
          <li>Ejecutar o explicar los scripts ETL y confirmar carga en `dw`.</li>
          <li>Abrir Power BI y mostrar el reporte conectado al DW.</li>
          <li>Navegar el portal Flask y el mapa (si aplica).</li>
          <li>Demostrar la maqueta IoT en funcionamiento.</li>
        </ol>
      </div>
    </section>

    <section id="resultados" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Resultados y conclusiones</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Impacto y aprendizajes</h2>
        <p class="mt-3 text-sm text-slate-600">Resumir beneficios, análisis y recomendaciones para escalado futuro. Enfatizar la utilidad para ciudades inteligentes y la reproducibilidad del despliegue en Docker/Render.</p>
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
