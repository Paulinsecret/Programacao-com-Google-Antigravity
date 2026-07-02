document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.info-card');
    const factTitle = document.getElementById('fact-title');
    const factDesc = document.getElementById('fact-description');
    const statTemp = document.getElementById('stat-temp');
    const statPurity = document.getElementById('stat-purity');
    const statAlt = document.getElementById('stat-alt');

    const sourceData = {
        altitude: {
            title: "Glaciar de Altitude Extrema",
            desc: "Nossa água é extraída a mais de 3.200 metros de altitude, onde o ar é rarefeito e a pureza é intocada por poluentes urbanos. A altitude garante uma barreira natural contra qualquer interferência externa.",
            temp: "-4°C",
            purity: "99.9%",
            alt: "3.200m"
        },
        filtragem: {
            title: "Filtragem Natural de Mil Anos",
            desc: "A água percorre lentamente camadas subterrâneas de rochas vulcânicas e gelo milenar, um processo de filtragem natural de séculos que enriquece a água com minerais essenciais sem alterar sua leveza única.",
            temp: "2°C",
            purity: "99.98%",
            alt: "Subterrâneo"
        },
        sustentavel: {
            title: "Fonte 100% Sustentável",
            desc: "Coletamos apenas o excedente do fluxo natural de degelo, garantindo impacto ecológico zero. A garrafa térmica de alumínio reciclado protege o meio ambiente enquanto mantém o frescor glacial intacto.",
            temp: "5°C",
            purity: "100%",
            alt: "Preservado"
        }
    };

    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove active style from all cards
            cards.forEach(c => c.style.borderColor = 'rgba(255, 255, 255, 0.05)');
            
            // Set current card active
            card.style.borderColor = 'var(--accent-cyan)';
            
            const type = card.dataset.source;
            if (sourceData[type]) {
                const data = sourceData[type];
                
                // Fade out content, then fade in with new data
                factTitle.style.opacity = 0;
                factDesc.style.opacity = 0;
                
                setTimeout(() => {
                    factTitle.textContent = data.title;
                    factDesc.textContent = data.desc;
                    statTemp.textContent = data.temp;
                    statPurity.textContent = data.purity;
                    statAlt.textContent = data.alt;
                    
                    factTitle.style.opacity = 1;
                    factDesc.style.opacity = 1;
                }, 200);
            }
        });
    });
    
    // Set initial transition
    factTitle.style.transition = 'opacity 0.3s ease';
    factDesc.style.transition = 'opacity 0.3s ease';
});
