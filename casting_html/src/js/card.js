
const app = document.getElementById('app');
const template = document.getElementById('card-template');
const activeCards = {};
let ws;

window.LEADER_MAP = {};

function getLeaderIcon(name) {
    if (!name) return 'leaders/placeholder.webp';
    const cleanName = name.trim();
    const mapped = window.LEADER_MAP[cleanName];
    if (mapped) return `leaders/${mapped}.webp`;
    return `leaders/${cleanName.toLowerCase().replace(/ /g, '_')}.webp`;
}

function connect() {
    ws = new WebSocket('ws://localhost:7305/card');
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === 'show_card') showCard(msg.data);
        else if (msg.type === 'config') window.LEADER_MAP = msg.leader_map || {};
    };
    ws.onclose = () => setTimeout(connect, 3000);
}
connect();

function showCard(data) {
    const slot = data.slot || 1;
    const teamSize = data.team_size || 1;
    const side = data.side || 'left';
    let cardEl;
    let isNew = false;

    if (activeCards[slot]) {
        cardEl = activeCards[slot].element;
        gsap.killTweensOf(cardEl);
        if (activeCards[slot].timer) clearTimeout(activeCards[slot].timer);
    } else {
        cardEl = template.cloneNode(true);
        cardEl.id = `card-${slot}`;
        cardEl.style.display = 'flex';
        app.appendChild(cardEl);
        activeCards[slot] = { element: cardEl };
        isNew = true;
    }

    cardEl.querySelector('.p-name').innerText = data.name || "Unknown";
    cardEl.querySelector('.p-rank').innerText = data.rank || "-";
    cardEl.querySelector('.p-mmr').innerText = data.mmr || "-";
    cardEl.querySelector('.p-style').innerText = data.playstyle || "-";
    cardEl.querySelector('.p-leader').innerText = data.main_leader || "-";
    cardEl.querySelector('.lbl-rank').innerText = `Rango en ${teamSize}v${teamSize}`;

    const imgEl = cardEl.querySelector('.leader-img');
    const primarySrc = getLeaderIcon(data.main_leader || "Atriox");
    imgEl.src = `${primarySrc}?v=${Date.now()}`;
    imgEl.onerror = () => {
        if (imgEl.src.includes('placeholder')) {
            imgEl.onerror = null;
            return;
        }
        if (imgEl.src.includes('.webp')) imgEl.src = imgEl.src.replace('.webp', '.png');
        else if (imgEl.src.includes('.png')) imgEl.src = `leaders/placeholder.webp?v=${Date.now()}`;
    };

    let startX = side === 'right' ? 50 : -50;
    if (side === 'right') {
        cardEl.style.left = 'auto'; cardEl.style.right = '50px';
        cardEl.style.flexDirection = 'row-reverse';
    } else {
        cardEl.style.left = '50px'; cardEl.style.right = 'auto';
        cardEl.style.flexDirection = 'row';
    }

    let topPos = '50%';
    if (teamSize > 1) {
        if (slot <= 2) topPos = '35%';
        else if (slot <= 4) topPos = '55%';
        else topPos = '75%';
    }
    cardEl.style.top = topPos; cardEl.style.marginTop = '-75px';
    activeCards[slot].exitX = startX;

    if (isNew || cardEl.style.opacity == 0) gsap.set(cardEl, { x: startX, opacity: 0, scale: 0.9 });
    gsap.to(cardEl, { duration: 0.5, opacity: 1, x: 0, scale: 1, ease: "back.out(1.2)" });
    activeCards[slot].timer = setTimeout(() => hideCard(slot), 8000);
}

function hideCard(slot) {
    const card = activeCards[slot];
    if (!card) return;
    gsap.to(card.element, { duration: 0.4, opacity: 0, x: card.exitX, scale: 0.9, ease: "power2.in" });
}
