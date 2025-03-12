document.addEventListener('DOMContentLoaded', () => {
    const scriptInput = document.getElementById('script-input');
    const scriptOutput = document.getElementById('script-output');
    const saveButton = document.getElementById('save-button');

    scriptInput.addEventListener('input', () => {
        updateScriptOutput();
    });

    saveButton.addEventListener('click', () => {
        saveScript();
    });

    function updateScriptOutput() {
        const text = scriptInput.value;
        const pages = text.split('\n\n');
        scriptOutput.innerHTML = '';

        pages.forEach((page, pageIndex) => {
            const pageElement = document.createElement('div');
            pageElement.className = 'page';
            const pageHeader = document.createElement('h3');
            pageHeader.textContent = `Página ${pageIndex + 1}`;
            pageElement.appendChild(pageHeader);

            const lines = page.split('\n');
            lines.forEach((line, lineIndex) => {
                const vignette = document.createElement('p');
                vignette.textContent = `Viñeta ${lineIndex + 1}: ${line}`;
                pageElement.appendChild(vignette);
            });

            scriptOutput.appendChild(pageElement);
        });
    }

    function saveScript() {
        const scriptContent = scriptInput.value;
        const blob = new Blob([scriptContent], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'guion.txt';
        link.click();
    }
});