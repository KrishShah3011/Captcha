document.getElementById('checkButton').addEventListener('click', async () => {
    const getWebGLFingerprint = () => {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (!gl) return { vendor: null, renderer: null };
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        return {
            vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : null,
            renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : null,
        };
    };

    const getFontFingerprint = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const fonts = ['Arial', 'Verdana', 'Times New Roman', 'Courier New', 'Georgia'];
        const fontData = {};
        fonts.forEach(font => {
            ctx.font = `72px ${font}`;
            const width = ctx.measureText('abcdefghijklmnopqrstuvwxyz').width;
            fontData[font] = width;
        });
        return fontData;
    };

    function isBot(fingerprint) {
        const { userAgent, canvas, webgl, fonts, screenResolution, hardwareConcurrency, maxTouchPoints, connection } = fingerprint;
    
        const knownBotUserAgents = ['bot', 'crawler', 'spider'];
        const isBotUserAgent = knownBotUserAgents.some(pattern => userAgent.toLowerCase().includes(pattern));
        
        const defaultCanvasFingerprint = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...';

        const isCanvasFingerprintDefault = canvas === defaultCanvasFingerprint;

        const unusualResolutions = [
            "320x240", "480x320", "800x480", "1280x768", 
            "1440x900", "1536x960", "1600x900", "2048x1152", "2560x1440", 
            "3840x2160", "5120x1440", "7680x4320"
        ];
        const isUnusualScreenResolution = unusualResolutions.includes(screenResolution);
        const isLowFontCount = fonts.length < 5;

        const isBot = isBotUserAgent || isCanvasFingerprintDefault || isUnusualScreenResolution || isLowFontCount;

        const isUnusualHardwareConcurrency = hardwareConcurrency < 2 || hardwareConcurrency > 16;
        const isUnusualTouchPoints = maxTouchPoints > 1;

        return isBot || isUnusualHardwareConcurrency || isUnusualTouchPoints;
    }

    const fingerprint = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        screenResolution: `${window.screen.width}x${window.screen.height}`,
        colorDepth: window.screen.colorDepth,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        platform: navigator.platform,
        plugins: Array.from(navigator.plugins).map(plugin => plugin.name),
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
        webgl: getWebGLFingerprint(),
        fonts: getFontFingerprint(),
        hardwareConcurrency: navigator.hardwareConcurrency,
        maxTouchPoints: navigator.maxTouchPoints,
        connection: navigator.connection ? {
            effectiveType: navigator.connection.effectiveType,
            rtt: navigator.connection.rtt
        } : {},
    };

    // try {
    //     const response = await fetch('/predict', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(fingerprint),
    //     });

    //     if (!response.ok) {
    //         throw new Error('Network response was not ok.');
    //     }

    //     const result = await response.json();
    //     document.getElementById('result').innerText = `Prediction: ${result.prediction}`;
    // } catch (error) {
    //     document.getElementById('result').innerText = 'Error: Unable to get prediction.';
    //     console.error('Error:', error);
    //     console.log('Fingerprint Data:', fingerprint);
    // }

    console.log('Fingerprint Data:', fingerprint);
    document.getElementById('result').innerText = `Prediction: ${isBot(fingerprint) ? 'Bot' : 'Human'}`;
});
