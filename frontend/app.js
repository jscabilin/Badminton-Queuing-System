const statusEl = document.getElementById("status");
const refreshBtn = document.getElementById("refresh");
const API_URL = "http://127.0.0.1:8001";

async function loadHealth() {
  statusEl.textContent = "Checking backend...";

  try {
    const response = await fetch(`${API_URL}/health`);
    const data = await response.json();
    statusEl.textContent = `Backend says: ${data.status}`;
  } catch (error) {
    statusEl.textContent = `Backend not reachable: ${error.message}`;
  }
}

refreshBtn.addEventListener("click", loadHealth);
loadHealth();
