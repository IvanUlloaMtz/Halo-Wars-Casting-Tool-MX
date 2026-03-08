
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
    ws = new WebSocket('ws://localhost:7305/intro');
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === 'show_intro') {
            updateIntro(msg.data);
            showIntro();
            setTimeout(hideIntro, 5000);
        } else if (msg.type === 'config') window.LEADER_MAP = msg.leader_map || {};
    };
    ws.onclose = () => setTimeout(connect, 3000);
}
connect();

function updateIntro(data) {
    document.getElementById('p-name').innerText = data.player;
    document.getElementById('p-team').innerText = data.team;
    const icon = getLeaderIcon(data.leader);
    document.getElementById('p-leader').style.backgroundImage = `url('${icon}?v=${Date.now()}')`;
}

function showIntro() {
    gsap.to('#intro', { duration: 0.5, opacity: 1, x: 0, ease: 'power2.out' });
}

function hideIntro() {
    gsap.to('#intro', { duration: 0.5, opacity: 0, x: -300, ease: 'power2.in' });
}
