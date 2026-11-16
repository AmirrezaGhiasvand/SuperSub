// Load a fresh entry module and surface startup failures instead of a dead UI.
(async function () {
  function failed(error) {
    console.error('SuperSub startup failed:', error);
    const target = document.getElementById('message');
    if (target) {
      target.textContent = 'SuperSub could not start: ' + (error.message || error) + '. Stop the server, restart Start.cmd, then refresh. If this repeats, send this error.';
      target.setAttribute('role', 'alert');
      target.style.color = '#ffb2b2';
    }
  }
  try {
    await import('./app.js?v=studio-3-' + Date.now());
  } catch (error) {
    failed(error);
  }
})();
