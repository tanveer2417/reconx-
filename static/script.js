async function runRecon() {
    const target = document.getElementById('targetInput').value.trim();
    const output = document.getElementById('output');
    const loading = document.getElementById('loading');

    if (!target) {
        output.textContent = "❌ Please enter a valid target domain or IP.";
        return;
    }

    output.textContent = "";
    loading.classList.remove("hidden");

    try {
        const response = await fetch('/run_recon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ target: target })
        });

        const data = await response.json();
        output.textContent = data.output || "No output received.";
    } catch (err) {
        output.textContent = `❌ Error: ${err.message}`;
    } finally {
        loading.classList.add("hidden");
    }
}
