const scoreboard = document.getElementById('scoreboard');

window.LEADER_MAP = {};

function getLeaderIcon(name) {
  if (!name) return 'leaders/placeholder.webp';
  const cleanName = name.trim();
  // Try mapped name from config
  const mapped = window.LEADER_MAP[cleanName];
  if (mapped) return `leaders/${mapped}.webp`;
  // Normalization fallback
  const normalized = cleanName.toLowerCase().replace(/ /g, '_');
  return `leaders/${normalized}.webp`;
}

let isVisible = false;
let ws;
let reconnectInterval = 3000;
let lastDataStr = "";
let prevP1Score = -1;
let prevP2Score = -1;
let currentMapName = '';
let mapPopupTimer = null;
let mapPopupEnabled = true;
let prevHistoryState = []; // Track previous match winners for flash detection
let mapEnterMs = 3000;
let mapVisibleMs = 25000;
let mapExitMs = 3000;
let mapHiddenMs = 20000;
let prevDisconnection = false;

// ===== Background Animation removed by user request =====

// Initial calls
connect();

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

window.addEventListener('resize', () => { });

function triggerPointPulse(teamNum) {
  const pulseTarget = document.querySelector(`#p${teamNum}-pulse-overlay .pulse-circle`);
  if (!pulseTarget) return;

  const p1Color = getComputedStyle(document.getElementById('p1-block')).getPropertyValue('--team-color').trim() || '#cc2222';
  const p2Color = getComputedStyle(document.getElementById('p2-block')).getPropertyValue('--team-color').trim() || '#2244cc';
  const teamColor = teamNum === 1 ? p1Color : p2Color;

  gsap.killTweensOf(pulseTarget);
  gsap.set(pulseTarget, {
    backgroundColor: teamColor,
    scale: 0,
    opacity: 1,
    filter: 'blur(10px)',
    boxShadow: `0 0 80px 40px ${teamColor}`
  });

  // Slower, smoother pulse expansion
  gsap.to(pulseTarget, {
    scale: 15, // Large enough to fill the block but clipped
    opacity: 0,
    duration: 2.5,
    ease: 'power2.out'
  });
}

// ===== WebSocket =====
function connect() {
  ws = new WebSocket('ws://localhost:7305');

  ws.onopen = () => {
    console.log("Connected");
    reconnectInterval = 3000;
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'update_score') {
      const currentDataStr = JSON.stringify(msg.data);
      const forceUpdate = (currentDataStr !== lastDataStr);
      lastDataStr = currentDataStr;

      updateData(msg.data, forceUpdate);

      if (!isVisible) showAnimate();
      triggerScorePulse();
    } else if (msg.type === 'config') {
      console.log("[Score] Received config:", msg.leader_map);
      window.LEADER_MAP = msg.leader_map || {};
    } else if (msg.type === 'game_over') {
      // Game Over alert removed as per user request
    }
    /* mirror_match is now state-based in updateData, not event-based */
  };

  ws.onclose = () => {
    setTimeout(connect, reconnectInterval);
  };
  ws.onerror = (err) => ws.close();
}


function updateData(data, forceUpdate) {
  // Scores
  const p1Score = parseInt(data.p1.score);
  const p2Score = parseInt(data.p2.score);
  document.getElementById('p1-score').innerText = p1Score;
  document.getElementById('p2-score').innerText = p2Score;

  // Detect individual score changes and trigger pulse
  if (prevP1Score >= 0 && p1Score > prevP1Score) {
    triggerPointPulse(1);
  }
  if (prevP2Score >= 0 && p2Score > prevP2Score) {
    triggerPointPulse(2);
  }
  prevP1Score = p1Score;
  prevP2Score = p2Score;

  // Game Type
  let gameType = data.game_type || "DEATHMATCH";
  document.getElementById('game-type').innerText = gameType.toUpperCase();
  const boIndicator = document.querySelector('.bo-indicator');
  if (data.show_game_type === false) {
    boIndicator.style.display = 'none';
  } else {
    boIndicator.style.display = 'block'; // Or flex/inline-block based on original CSS, block is safe here
  }

  // Series Winner Logic
  const bestOf = parseInt(data.best_of) || 1;
  const winsNeeded = Math.ceil(bestOf / 2);

  const p1Block = document.getElementById('p1-block');
  const p2Block = document.getElementById('p2-block');

  // Reset
  p1Block.classList.remove('series-win');
  p2Block.classList.remove('series-win');

  if (bestOf > 1) { // Only show for series
    if (p1Score >= winsNeeded) {
      p1Block.classList.add('series-win');
    } else if (p2Score >= winsNeeded) {
      p2Block.classList.add('series-win');
    }
  }

  // Render Match History
  renderHistory(data);

  // Render Teams - Only re-render DOM if something changed to allow animations to play smoothly or if forced
  // For simplicity in this tool, we re-render to ensure latest names/leaders. 
  // The CSS animation 'pop-in' will trigger on new elements.
  const teamSize = data.team_size || 1;
  renderTeam(1, data, teamSize);
  renderTeam(2, data, teamSize);

  // Update Map Popup config
  const mp = data.map_popup || {};
  const newEnabled = mp.enabled !== false;
  const newEnter = (mp.enter_sec || 3) * 1000;
  const newVisible = (mp.visible_sec || 25) * 1000;
  const newExit = (mp.exit_sec || 3) * 1000;
  const newHidden = (mp.hidden_sec || 20) * 1000;
  const mapName = data.current_map || '';

  const configChanged = (newEnabled !== mapPopupEnabled ||
    newEnter !== mapEnterMs || newVisible !== mapVisibleMs ||
    newExit !== mapExitMs || newHidden !== mapHiddenMs);

  mapPopupEnabled = newEnabled;
  mapEnterMs = newEnter;
  mapVisibleMs = newVisible;
  mapExitMs = newExit;
  mapHiddenMs = newHidden;

  if (mapName !== currentMapName || configChanged) {
    currentMapName = mapName;
    const popup = document.getElementById('map-popup');
    popup.textContent = mapName ? 'Current Map: ' + mapName : '';
    restartMapPopupCycle();
  }

  // Disconnect Alert
  const dcActive = !!data.disconnection;
  const dcEl = document.getElementById('disconnect-alert');
  if (dcActive && !prevDisconnection) {
    // Show with animation
    dcEl.classList.add('active');
    gsap.fromTo(dcEl,
      { opacity: 0, y: -20, scale: 0.8 },
      { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(1.7)' }
    );
  } else if (!dcActive && prevDisconnection) {
    // Hide with animation
    gsap.to(dcEl, {
      opacity: 0, y: -20, scale: 0.8, duration: 0.3, ease: 'power2.in',
      onComplete: () => dcEl.classList.remove('active')
    });
  }
  prevDisconnection = dcActive;

  // Mirror Match Alert (Persistent)
  const mmActive = !!data.mirror_match;
  const mmEl = document.getElementById('mirror-match-alert');
  if (mmActive) {
    mmEl.classList.add('active');
    // Optional: Pulse animation or similar could go here if we wanted more than static
  } else {
    mmEl.classList.remove('active');
  }

  // Sync bg-anim removed.
}


function renderHistory(data) {
  const p1Container = document.getElementById('p1-history');
  const p2Container = document.getElementById('p2-history');
  p1Container.innerHTML = '';
  p2Container.innerHTML = '';

  const bestOf = data.best_of || 1;
  const matches = data.matches || [];

  for (let i = 0; i < bestOf; i++) {
    // Determine status for this match index
    let p1Status = 'tbd';
    let p2Status = 'tbd';
    let isNew = false;

    if (i < matches.length) {
      const m = matches[i];
      if (m.winner === 1) {
        p1Status = 'win';
        p2Status = 'loss';
      } else if (m.winner === 2) {
        p1Status = 'loss';
        p2Status = 'win';
      }
      // Check if this result is new compared to previous state
      const prevWinner = prevHistoryState[i] || 0;
      if (m.winner !== 0 && m.winner !== prevWinner) {
        isNew = true;
      }
    }

    // Create P1 Indicator
    const p1Ind = document.createElement('div');
    p1Ind.className = `h-ind ${p1Status}${isNew ? ' flash' : ''}`;
    if (isNew) {
      p1Ind.addEventListener('animationend', function () {
        this.classList.remove('flash');
      }, { once: true });
    }
    p1Container.appendChild(p1Ind);

    // Create P2 Indicator
    const p2Ind = document.createElement('div');
    p2Ind.className = `h-ind ${p2Status}${isNew ? ' flash' : ''}`;
    if (isNew) {
      p2Ind.addEventListener('animationend', function () {
        this.classList.remove('flash');
      }, { once: true });
    }
    p2Container.appendChild(p2Ind);
  }

  // Save current state for next comparison
  prevHistoryState = matches.map(m => m.winner || 0);
}

function renderTeam(teamNum, data, size) {
  const container = document.getElementById(teamNum === 1 ? 't1-container' : 't2-container');

  // We want to avoid full clear if possible to keep existing anims? 
  // Actually user WANTS animation on update/add. So clearing and re-adding triggers the CSS animation.
  container.innerHTML = '';

  // Apply size class for CSS scaling
  container.className = `content ${teamNum === 1 ? 'p1-content' : 'p2-content'} team-size-${size}`;

  // Team Name (if enabled)
  const showTeamNames = data.show_team_names !== false;
  const teamName = teamNum === 1 ? (data.team1_name || '') : (data.team2_name || '');
  if (showTeamNames && teamName) {
    const tnDiv = document.createElement('div');
    tnDiv.className = 'team-name-label';
    tnDiv.innerText = teamName.toUpperCase();
    container.appendChild(tnDiv);
  }

  // Define player indices
  let indices = [];
  if (teamNum === 1) {
    indices = [1];
    if (size >= 2) indices.push(3);
    if (size >= 3) indices.push(5);
  } else {
    indices = [2];
    if (size >= 2) indices.push(4);
    if (size >= 3) indices.push(6);
  }

  indices.forEach(idx => {
    const pKey = `p${idx}`;
    const pData = data[pKey];
    if (!pData) return;

    let leaderName = pData.leader;
    if (data.current_match) {
      const matchLeaderKey = `p${idx}_leader`;
      if (data.current_match[matchLeaderKey]) {
        leaderName = data.current_match[matchLeaderKey];
      }
    }

    const entryDiv = document.createElement('div');
    entryDiv.className = 'player-entry';

    // Alignment logic
    entryDiv.style.display = 'flex';
    entryDiv.style.alignItems = 'center';
    entryDiv.style.flexDirection = teamNum === 1 ? 'row' : 'row-reverse';

    // Leader Image
    const imgEl = document.createElement('img');
    imgEl.className = 'leader-img-small';
    const primarySrc = getLeaderIcon(leaderName);
    console.log(`[Score] Loading icon for ${leaderName} -> ${primarySrc}`);
    imgEl.src = `${primarySrc}?v=${Date.now()}`;

    imgEl.onerror = () => {
      console.error(`[Score] 404: ${imgEl.src}`);
      if (imgEl.src.includes('placeholder')) {
        imgEl.onerror = null; // Prevent infinite loop
        return;
      }
      
      if (imgEl.src.includes('.webp')) {
        // Try .png fallback
        imgEl.src = imgEl.src.replace('.webp', '.png');
      } else if (imgEl.src.includes('.png')) {
        // Try placeholder
        imgEl.src = `leaders/placeholder.webp?v=${Date.now()}`;
      }
    };

    const infoDiv = document.createElement('div');
    infoDiv.className = 'player-info';
    // Removed inline alignment overrides to let CSS handle centering

    const nameDiv = document.createElement('div');
    nameDiv.className = 'player-name';

    // Flag
    const showFlags = data.show_flags !== false;
    if (showFlags && pData.country && pData.country !== 'xx') {
      const flagSpan = document.createElement('span');
      flagSpan.className = `fi fi-${pData.country}`;
      nameDiv.appendChild(flagSpan);
    }

    const nameText = document.createTextNode(pData.name.toUpperCase());
    nameDiv.appendChild(nameText);

    const leaderDiv = document.createElement('div');
    leaderDiv.className = 'leader-name';
    leaderDiv.innerText = leaderName.toUpperCase();

    // Player color bar
    const colorBar = document.createElement('div');
    colorBar.className = 'player-color-bar';
    const pColor = pData.color || '#fff';
    colorBar.style.background = pColor;
    colorBar.style.color = pColor; // for currentColor in glow


    infoDiv.appendChild(nameDiv);
    infoDiv.appendChild(leaderDiv);
    infoDiv.appendChild(colorBar);

    entryDiv.appendChild(imgEl);
    entryDiv.appendChild(infoDiv);
    container.appendChild(entryDiv);
  });
}

function showAnimate() {
  isVisible = true;
  scoreboard.style.visibility = 'visible';
  scoreboard.classList.remove('exit-active');
  scoreboard.classList.add('enter-active');
  // Sync bg-anim removed
}

function hideAnimate() {
  isVisible = false;
  scoreboard.classList.remove('enter-active');
  scoreboard.classList.add('exit-active');
}

function triggerScorePulse() {
  const scores = document.querySelectorAll('.score-num');
  scores.forEach(el => {
    el.classList.remove('score-pulse');
    void el.offsetWidth; // Trigger reflow
    el.classList.add('score-pulse');
  });
}

/* ---- Map Popup Cycle ---- */
function restartMapPopupCycle() {
  clearTimeout(mapPopupTimer);
  const popup = document.getElementById('map-popup');
  if (!currentMapName || !mapPopupEnabled) { popup.className = 'map-popup'; return; }
  // Set CSS custom properties for animation durations
  popup.style.setProperty('--map-enter-dur', mapEnterMs + 'ms');
  popup.style.setProperty('--map-exit-dur', mapExitMs + 'ms');
  showMapPopup();
}

function showMapPopup() {
  if (!mapPopupEnabled) return;
  const popup = document.getElementById('map-popup');
  // Phase 1: Enter
  popup.className = 'map-popup enter';
  mapPopupTimer = setTimeout(() => {
    // Phase 2: Idle (breathing + float)
    popup.className = 'map-popup idle';
    mapPopupTimer = setTimeout(() => {
      // Phase 3: Exit
      popup.className = 'map-popup exit';
      mapPopupTimer = setTimeout(() => {
        // Phase 4: Hidden
        popup.className = 'map-popup';
        mapPopupTimer = setTimeout(showMapPopup, mapHiddenMs);
      }, mapExitMs);
    }, mapVisibleMs);
  }, mapEnterMs);
}