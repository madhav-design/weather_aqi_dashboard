document.addEventListener("DOMContentLoaded", () => {
  if (typeof lat !== "undefined" && typeof lon !== "undefined") {
    const map = L.map("map").setView([lat, lon], 10);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "Map data © OpenStreetMap",
    }).addTo(map);
    L.marker([lat, lon]).addTo(map).bindPopup("City").openPopup();
  }
});
