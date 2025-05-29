document.addEventListener('DOMContentLoaded', () => {
    const hyperboloidElement = document.getElementById('hyperboloid');
    const numLinesDisplayElement = document.getElementById('num-lines-display');

    function getCssVariable(variableName, isFloat = false) {
        const value = getComputedStyle(document.documentElement).getPropertyValue(variableName).trim();
        if (value === '') {
            console.warn(`variabila CSS ${variableName} invalidă`);
            return isFloat ? 0.0 : 0;
        }
        return isFloat ? parseFloat(value) : parseInt(value);
    }

    const numLinesPerFamily = getCssVariable('--num-lines-per-family');
    const radiusString = getComputedStyle(document.documentElement).getPropertyValue('--hyperboloid-radius').trim();
    const lineHeightString = getComputedStyle(document.documentElement).getPropertyValue('--line-height').trim();
    const skewAngleDeg = getCssVariable('--skew-angle', true);

    const numericRadius = parseFloat(radiusString);
    const numericLineHeight = parseFloat(lineHeightString);

    console.log({ numLinesPerFamily, radiusString, lineHeightString, skewAngleDeg, numericRadius, numericLineHeight });

    if (!hyperboloidElement || !numLinesDisplayElement) {
        console.error("fișier HTML neidentificat");
        return;
    }
    if (numLinesPerFamily === 0 || numericRadius === 0 || numericLineHeight === 0) {
        console.error("variabile CSS invalide");
    }

    let totalLines = 0;
    const linesData = [];

    function createFamily(skewDirection, familyIndex) {
        const familyLines = [];
        const angleStep = 360 / numLinesPerFamily;

        const panelWidth = (2 * Math.PI * numericRadius) / numLinesPerFamily;

        for (let i = 0; i < numLinesPerFamily; i++) {
            const line = document.createElement('div');
            line.classList.add('line');

            const angleY = angleStep * i;
            familyLines.push({ angleY });

            const currentSkewAngle = skewAngleDeg * skewDirection;

            line.style.height = lineHeightString;
            line.style.top = `calc(50% - ${numericLineHeight / 2}px)`;
            line.style.left = `calc(50% - 1px)`;

            line.style.transform = `
                rotateY(${angleY}deg)
                translateZ(${radiusString})
                rotateX(${currentSkewAngle}deg)
            `;

            const hue = (angleY + (familyIndex === 0 ? 0 : 60)) % 360;
            line.style.backgroundColor = `hsl(${hue}, 80%, 60%)`;

            hyperboloidElement.appendChild(line);
            totalLines++;
        }

        for (let i = 0; i < numLinesPerFamily; i++) {
            const panel = document.createElement('div');
            panel.classList.add('hyperboloid-panel');

            const currentLineAngle = familyLines[i].angleY;
            const panelAngleY = currentLineAngle + angleStep / 2;
            
            const currentSkewAngle = skewAngleDeg * skewDirection;

            panel.style.width = `${panelWidth}px`;
            panel.style.height = lineHeightString;

            panel.style.top = `calc(50% - ${numericLineHeight / 2}px)`;
            panel.style.left = `calc(50% - ${panelWidth / 2}px)`;

            panel.style.transform = `
                rotateY(${panelAngleY}deg)
                translateZ(${radiusString})
                rotateX(${currentSkewAngle}deg)
            `;
            
            const panelHue = (180 + (familyIndex === 0 ? 0 : 60)) % 360;
            panel.style.backgroundColor = `hsla(${panelHue}, 70%, 50%, 0.35)`;

            hyperboloidElement.appendChild(panel);
        }
    }

    if (numLinesPerFamily > 0 && numericRadius > 0 && numericLineHeight > 0) {
        createFamily(1, 0);  
        createFamily(-1, 1);
        if (numLinesDisplayElement) numLinesDisplayElement.textContent = totalLines;
    } else if (numLinesDisplayElement) numLinesDisplayElement.textContent = "eroare de generare";
});