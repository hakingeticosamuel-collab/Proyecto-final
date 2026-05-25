document.addEventListener("DOMContentLoaded", function () {
  const map = L.map("map").setView([5.6680, -73.1204], 13);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(map);

  fetch("/api/locations")
    .then((response) => response.json())
    .then((locations) => {
      locations.forEach((item) => {
        if (!item.lat || !item.lng) {
          return;
        }

        const marker = L.marker([item.lat, item.lng]).addTo(map);
        const content = `
          <div style="min-width: 220px;">
            <strong>${item.name}</strong><br />
            Estado: ${item.status || "Desconocido"}<br />
            Consumo: ${item.consumo.toFixed(2)} kWh
          </div>`;
        marker.bindPopup(content);
      });
    })
    .catch(() => {
      console.error("No se pudieron cargar las ubicaciones del API.");
    });
});
