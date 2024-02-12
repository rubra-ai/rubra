const { invoke } = window.__TAURI__.tauri;

window.addEventListener('DOMContentLoaded', () => {
  window.__TAURI__.invoke('check_docker_and_compose')
    .then((versions) => {
      document.getElementById('docker-status').textContent = `Docker Status: Installed (${versions[0]})`;
      document.getElementById('compose-status').textContent = `Docker Compose Status: Installed (${versions[1]})`;
      downloadModelFile();
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('docker-status').textContent = `Docker Status: Not Installed`;
      document.getElementById('compose-status').textContent = `Docker Compose Status: Not Installed`;
      document.getElementById('download-docker').style.display = 'inline';
      document.getElementById('status-error').style.display = 'block';
      document.getElementById('status-error').textContent = `Error: ${error}`;
      console.log("Error Message:", error);
    });

  updateRubraStatus();
});

setInterval(() => {
  updateRubraStatus(); // Updates the Rubra action button based on current status
}, 30000);

function downloadModelFile() {
  window.__TAURI__.invoke('download_rubra_llamafile')
    .catch(error => console.error(error));
}

window.__TAURI__.event.listen('download-progress', (event) => {
  const progress = event.payload * 100;
  console.log(`Download progress: ${progress.toFixed(2)}%`);

  document.getElementById('progress-bar').style.width = `${progress}%`;
  document.getElementById('llama-status').textContent = `Downloading model file...`;
});

window.__TAURI__.event.listen('download-complete', (event) => {
  document.getElementById('progress-bar').style.width = `100%`;
  document.getElementById('llama-status').textContent = `Downloaded model file`;
  document.getElementById('rubra-action').style.display = 'inline';
  startRubra();
});

document.getElementById('rubra-action').addEventListener('click', function () {
  const button = document.getElementById('rubra-action');
  const action = button.getAttribute('data-action');

  if (action === 'start') {
    startRubra();
  } else {
    stopRubra();
  }
});

document.getElementById('ui-btn').addEventListener('click', () => {
  window.__TAURI__.shell.open('http://localhost:8501');
});

document.getElementById('download-docker').addEventListener('click', () => {
  window.__TAURI__.shell.open('https://www.docker.com/products/docker-desktop/');
});

function startRubra() {
  window.__TAURI__.invoke('rubra_event', { event: 'start' })
    .then((containers) => {
      updateRubraStatus();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function stopRubra() {
  window.__TAURI__.invoke('rubra_event', { event: 'stop' })
    .then(() => {
      updateRubraStatus();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function updateRubraStatus() {
  const rubraLlamafileReadyPromise = window.__TAURI__.invoke('check_rubra_llamafile_ready');
  const rubraContainerStatusPromise = window.__TAURI__.invoke('check_rubra_container_status');

  Promise.all([rubraLlamafileReadyPromise, rubraContainerStatusPromise])
    .then(([llamafileReadyResult, rubraStatusResult]) => {
      updateModelStatus(true);

      let status = checkContainerHealthy(rubraStatusResult);
      updateContainerStatus(status);
      updateFooterButtons(status);
    })
    .catch((error) => {
      console.warn('warn:', error)
      updateContainerStatus(false);
      updateFooterButtons(false);
      updateModelStatus(false);
    });
}

function checkContainerHealthy(containers) {
  if (containers.length === 0) {
    return false;
  }
  containers.forEach(([id, state]) => {
    if (state !== 'running') {
      return false;
    }
  });
  return true;
}

function updateFooterButtons(status) {
  const rubraAction = document.getElementById('rubra-action');
  const uiBtn = document.getElementById('ui-btn');

  if (status) {
    rubraAction.textContent = 'Stop Rubra';
    rubraAction.setAttribute('data-action', 'stop');
    rubraAction.style.display = 'inline';
    rubraAction.disabled = false;
    rubraAction.classList.remove('disabled');

    uiBtn.style.display = 'inline';
  } else {
    rubraAction.textContent = 'Start Rubra';
    rubraAction.setAttribute('data-action', 'start');

    uiBtn.style.display = 'none';
  }
}

function getStatusColor(status) {
  switch (status) {
    case 'running': return '#4CAF50';
    case 'stopped': return '#f44336';
    // Add more cases as needed
    default: return '#757575'; // Default color
  }
}

function updateModelStatus(isHealthy) {
  const modelStatusText = document.getElementById('model-status-text');
  const modelStatusDot = modelStatusText.previousElementSibling;
  modelStatusDot.className = `status-dot ${isHealthy ? 'healthy' : 'unhealthy'}`; // Update class to reflect current status
  modelStatusText.textContent = `Model Status: ${isHealthy ? 'Healthy' : 'Unhealthy'}`;
}

function updateContainerStatus(isHealthy) {
  const containerStatusText = document.querySelector('#container-statuses p');
  const containerStatusDot = containerStatusText.previousElementSibling; // Assuming the dot is the next sibling
  containerStatusDot.className = `status-dot ${isHealthy ? 'healthy' : 'unhealthy'}`; // Update class to reflect current status
  containerStatusText.textContent = `Container Status: ${isHealthy ? 'Healthy' : 'Unhealthy'}`;
}
