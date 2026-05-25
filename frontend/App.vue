<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm backdrop-blur-xl sm:p-8">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Entrega 3 · Proyecto Paipa Smart Light</p>
        <h2 class="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Integración total: Publicación Web, Prototipo y Sustentación</h2>
        <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
          Portal de demostración que conecta el prototipo IoT, el almacenamiento en Somee/SQL Server, el modelo analítico en Power BI y la publicación en Flask. Use la navegación para recorrer la arquitectura completa.
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
      <MetricCard subtitle="Backend" value="Flask" description="Sirve la SPA, el health check y la capa de integración mínima." />
      <MetricCard subtitle="Frontend" value="Vue" description="Landing sobria con navegación interna, Power BI y Leaflet." />
      <MetricCard subtitle="Objetivo" value="Conexión" description="Relacionar IoT, base de datos, analítica y publicación web." />
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

    <section id="introduccion" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Introducción</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Relación entre los componentes</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600">
          La propuesta integra captura de datos desde un prototipo IoT, almacenamiento operacional en Somee/SQL Server, procesamiento ETL, visualización en Power BI y una publicación web con Flask. El resultado es una demostración completa de ciudad inteligente aplicada al alumbrado público.
        </p>
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
            <p class="text-sm text-slate-600">La aplicación se publica en Render usando Docker. El contenedor incluye el build del frontend y un servidor Flask que sirve la SPA, expone `/health` y documenta el estado de la fuente de datos.</p>
            <p class="mt-3 text-sm text-slate-600">Comandos y archivos clave: `Dockerfile`, `render.yaml`, `requirements.txt`, `app.py`.</p>
          </div>
          <div>
            <p class="text-sm text-slate-600">Power BI queda embebido en el portal para que el jurado vea el dashboard dentro del flujo de la entrega. Si el servicio bloquea el iframe, el botón externo abre el reporte publicado.</p>
          </div>
        </div>
        <div class="mt-4 rounded-[22px] border border-slate-200 bg-slate-50 p-4">
          <p class="text-sm font-semibold text-slate-950">Estado de la fuente de datos</p>
          <p class="mt-1 text-sm text-slate-600">{{ sourceStatus.source }} · {{ sourceStatus.configured ? 'configurada' : 'pendiente de credenciales' }} · modo {{ sourceStatus.mode }}</p>
        </div>
      </div>
    </section>

    <section id="dashboard-publicado" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Dashboard publicado</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Acceso público y filtros</h2>
        <p class="mt-3 text-sm text-slate-600">URL pública: <span class="font-medium">https://proyecto-final-24st.onrender.com</span></p>
        <p class="mt-2 text-sm text-slate-600">Filtros disponibles: rango de fechas, zona/ubicación, dispositivo y estado de alertas.</p>
        <div class="mt-4">
          <div class="rounded-md border border-slate-200 bg-white overflow-hidden">
            <iframe src="https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9" class="w-full h-[480px] bg-white" loading="lazy" title="Power BI Report" frameborder="0"></iframe>
            <div class="p-4">
              <a href="https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9" target="_blank" rel="noopener" class="inline-flex items-center rounded-2xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800">Abrir en Power BI</a>
              <p class="mt-2 text-sm text-slate-500">Si el embed no carga por permisos o CSP, use el botón para abrir el reporte en una nueva pestaña.</p>
            </div>
          </div>
        </div>
        <div class="mt-5 rounded-[22px] border border-slate-200 bg-slate-50 p-4">
          <p class="text-sm font-semibold text-slate-950">Estado de la fuente de datos</p>
          <p class="mt-1 text-sm text-slate-600">{{ sourceStatus.source }} · {{ sourceStatus.configured ? 'configurada' : 'pendiente de credenciales' }} · modo {{ sourceStatus.mode }}</p>
        </div>
        <div class="mt-4 grid gap-4 md:grid-cols-3">
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Mediciones</p>
            <p class="mt-2 text-2xl font-semibold text-slate-950">{{ dataSummary.counts?.mediciones?.total_mediciones ?? '—' }}</p>
            <p class="mt-1 text-sm text-slate-600">Última: {{ dataSummary.counts?.mediciones?.ultima_medicion ?? 'sin datos' }}</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Dispositivos</p>
            <p class="mt-2 text-2xl font-semibold text-slate-950">{{ dataSummary.counts?.dispositivos?.total_dispositivos ?? '—' }}</p>
            <p class="mt-1 text-sm text-slate-600">Activos: {{ dataSummary.counts?.dispositivos?.dispositivos_activos ?? '—' }}</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-500">DW</p>
            <p class="mt-2 text-2xl font-semibold text-slate-950">{{ dataSummary.counts?.fact_mediciones?.total_fact_mediciones ?? '—' }}</p>
            <p class="mt-1 text-sm text-slate-600">Carga: {{ dataSummary.counts?.fact_mediciones?.ultima_carga ?? 'sin datos' }}</p>
          </div>
        </div>
        <div class="mt-5 rounded-[22px] border border-slate-200 bg-white p-4">
          <p class="text-sm font-semibold text-slate-950">Últimas mediciones</p>
          <div class="mt-3 overflow-x-auto">
            <table class="min-w-full text-left text-sm text-slate-600">
              <thead class="text-xs uppercase tracking-[0.2em] text-slate-500">
                <tr>
                  <th class="pb-2 pr-4">ID</th>
                  <th class="pb-2 pr-4">Sensor</th>
                  <th class="pb-2 pr-4">Fecha</th>
                  <th class="pb-2 pr-4">Valor</th>
                  <th class="pb-2 pr-4">Calidad</th>
                  <th class="pb-2 pr-4">Fuente</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in dataSummary.latest_mediciones" :key="row.id_medicion" class="border-t border-slate-100">
                  <td class="py-2 pr-4">{{ row.id_medicion }}</td>
                  <td class="py-2 pr-4">{{ row.id_sensor }}</td>
                  <td class="py-2 pr-4">{{ row.fecha_hora }}</td>
                  <td class="py-2 pr-4">{{ row.valor }}</td>
                  <td class="py-2 pr-4">{{ row.calidad_dato }}</td>
                  <td class="py-2 pr-4">{{ row.fuente }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <section id="mapa-interactivo" class="space-y-6">
      <LeafletMap />
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

    <section id="conclusiones" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Conclusiones</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Cierre de la entrega</h2>
        <p class="mt-3 text-sm text-slate-600">La publicación web une presentación, analítica y evidencia operativa en un solo recorrido. La parte conectada a Power BI, Somee/SQL Server y Leaflet deja visible la relación entre infraestructura, datos y visualización.</p>
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
    
    <section id="evidencias" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Evidencias</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Capturas y pruebas</h2>
        <p class="mt-3 text-sm text-slate-600">La captura final se incluirá en la versión enviada. Reemplazar los placeholders con imágenes reales en `frontend/assets/images/`.</p>
        <div class="mt-4 grid gap-4 md:grid-cols-3">
          <div class="rounded-[18px] border border-slate-200 bg-slate-50 p-3">
            <img src="/assets/images/evidence-dashboard.png" alt="evidence dashboard" class="h-40 w-full object-cover rounded-md" />
            <p class="mt-2 text-sm text-slate-600">Dashboard público (placeholder)</p>
          </div>
          <div class="rounded-[18px] border border-slate-200 bg-slate-50 p-3">
            <img src="/assets/images/evidence-prototype.jpg" alt="evidence prototype" class="h-40 w-full object-cover rounded-md" />
            <p class="mt-2 text-sm text-slate-600">Maqueta / prototipo (placeholder)</p>
          </div>
          <div class="rounded-[18px] border border-slate-200 bg-slate-50 p-3">
            <img src="/assets/images/evidence-deploy.png" alt="evidence deploy" class="h-40 w-full object-cover rounded-md" />
            <p class="mt-2 text-sm text-slate-600">Evidencia de despliegue (placeholder)</p>
          </div>
        </div>
      </div>
    </section>
  </BaseLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'
import LeafletMap from './components/LeafletMap.vue'

const selectedSection = ref('portada')
const sourceStatus = ref({ source: 'Somee/SQL Server', configured: false, mode: 'unconfigured' })
const dataSummary = ref({ configured: false, counts: {}, latest_mediciones: [] })

onMounted(async () => {
  try {
    const response = await fetch('/api/source-status')
    if (response.ok) {
      sourceStatus.value = await response.json()
    }
  } catch {
    sourceStatus.value = { source: 'Somee/SQL Server', configured: false, mode: 'offline' }
  }

  try {
    const response = await fetch('/api/dw-summary')
    if (response.ok) {
      dataSummary.value = await response.json()
    }
  } catch {
    dataSummary.value = { configured: false, counts: {}, latest_mediciones: [] }
  }
})

function handleNavigate(section) {
  selectedSection.value = section
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>
