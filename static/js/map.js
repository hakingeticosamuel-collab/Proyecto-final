document.addEventListener("DOMContentLoaded", function () {
  const map = L.map("map").setView([5.6680, -73.1204], 13);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(map);

  fetch("/api/public/locations")
    .then((response) => response.json())
    .then((locations) => {
      locations.forEach((item) => {
        if (!item.lat || !item.lng) {
          return;
        }

        const marker = L.circleMarker([item.lat, item.lng], {
          radius: item.alert_count > 0 || String(item.status).toLowerCase().includes("alert") ? 10 : 8,
          color: item.alert_count > 0 || String(item.status).toLowerCase().includes("alert") ? "#be123c" : "#2563eb",
          weight: 2,
          fillColor: item.alert_count > 0 || String(item.status).toLowerCase().includes("alert") ? "#fb7185" : "#60a5fa",
          fillOpacity: 0.9,
        }).addTo(map);
        const content = `
          <div style="min-width: 220px;">
            <strong>${item.name}</strong><br />
            Estado: ${item.status || "Desconocido"}<br />
            Consumo: ${item.consumo.toFixed(2)} kWh<br />
            Promedio: ${(item.average_consumption || 0).toFixed(2)} kWh<br />
            Alertas: ${item.alert_count || 0}<br />
            Última medición: ${item.last_measurement ? new Date(item.last_measurement).toLocaleString("es-CO") : "Sin dato reciente"}
          </div>`;
        marker.bindPopup(content);
      });
    })
    .catch(() => {
      console.error("No se pudieron cargar las ubicaciones del API.");
    });
});
