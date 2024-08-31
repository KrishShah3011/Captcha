document.getElementById('checkButton').addEventListener('click', async () => {
    const fingerprint = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        screenResolution: `${window.screen.width}x${window.screen.height}`,
        colorDepth: window.screen.colorDepth,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        platform: navigator.platform,
        plugins: Array.from(navigator.plugins).map(plugin => plugin.filename),
        cookiesEnabled: navigator.cookieEnabled,
        doNotTrack: navigator.doNotTrack,
        canvas: (() => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const txt = 'CANVAS_FINGERPRINT';
            ctx.textBaseline = 'top';
            ctx.font = '14px "Arial"';
            ctx.textBaseline = 'alphabetic';
            ctx.fillStyle = '#f60';
            ctx.fillRect(125, 1, 62, 20);
            ctx.fillStyle = '#069';
            ctx.fillText(txt, 2, 15);
            ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
            ctx.fillText(txt, 4, 17);
            return canvas.toDataURL();
        })(),
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(fingerprint),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const result = await response.json();
        document.getElementById('result').innerText = `Prediction: ${result.prediction}`;
    } catch (error) {
        document.getElementById('result').innerText = 'Error: Unable to get prediction.';
        console.error('Error:', error);
        console.log(fingerprint)
    }
});
