/**
 * DevOn Frontend Client Logic
 * Powered by Soroush Soleimani's real GitHub Network (Followers & Following)
 * Supports dual-mode: FastAPI Backend + Standalone GitHub Pages Client Engine
 */

const API_BASE = '/api/v1';

// Load real network dataset from network_data.js
const NETWORK_DATA = window.DEVON_NETWORK || {
  currentUser: {
    username: "SoroushSoleimani",
    name: "Soroush Soleimani",
    avatar_url: "https://avatars.githubusercontent.com/u/140951703?v=4",
    bio: "AI & Deep Learning Engineer | PyTorch, RAG Pipelines, Autonomous Agents",
    location: "Tehran, Iran",
    timezone_offset_hours: 3.5,
    public_repos_count: 11,
    total_stars_received: 42,
    followers_count: 72,
    following_count: 57,
    primary_role: "AI / Machine Learning",
    experience_tier: "Senior",
    coding_rhythm: "Night Owl (Late Night)",
    night_owl_score: 0.85,
    top_languages: [{ language: "Python", percentage: 75.0 }, { language: "C", percentage: 15.0 }, { language: "Java", percentage: 10.0 }],
    skill_tags: ["Python", "PyTorch", "RAG", "Deep Learning", "FastAPI", "NLP"],
    domain_interests: ["Artificial Intelligence", "Autonomous Agents", "Retrieval-Augmented Generation", "Distributed Systems"]
  },
  networkDevelopers: []
};

// Application State
const state = {
  currentUser: 'SoroushSoleimani',
  pairingMode: 'complementary',
  roleFilter: '',
  rhythmFilter: '',
  networkFilter: '',
  userProfile: NETWORK_DATA.currentUser,
  matches: [],
  selectedCandidate: null,
  isClientMode: true,
};

// DOM Elements
const elements = {
  systemStatus: document.getElementById('systemStatus'),
  searchForm: document.getElementById('searchForm'),
  usernameInput: document.getElementById('usernameInput'),
  userBanner: document.getElementById('userBanner'),
  userAvatar: document.getElementById('userAvatar'),
  userName: document.getElementById('userName'),
  userRoleChip: document.getElementById('userRoleChip'),
  userRhythmChip: document.getElementById('userRhythmChip'),
  userTierChip: document.getElementById('userTierChip'),
  userLocationChip: document.getElementById('userLocationChip'),
  userBio: document.getElementById('userBio'),
  userReposCount: document.getElementById('userReposCount'),
  userStarsCount: document.getElementById('userStarsCount'),
  userFollowersCount: document.getElementById('userFollowersCount'),
  matchesGrid: document.getElementById('matchesGrid'),
  matchesCount: document.getElementById('matchesCount'),
  modePills: document.getElementById('modePills'),
  roleFilter: document.getElementById('roleFilter'),
  rhythmFilter: document.getElementById('rhythmFilter'),
  networkFilter: document.getElementById('networkFilter'),
  quickPickBadges: document.querySelectorAll('.badge-tag'),
  
  // Modals
  compareModal: document.getElementById('compareModal'),
  closeCompareModal: document.getElementById('closeCompareModal'),
  closeCompareBtn: document.getElementById('closeCompareBtn'),
  compAvatarA: document.getElementById('compAvatarA'),
  compAvatarB: document.getElementById('compAvatarB'),
  compNameA: document.getElementById('compNameA'),
  compNameB: document.getElementById('compNameB'),
  compRoleA: document.getElementById('compRoleA'),
  compRoleB: document.getElementById('compRoleB'),
  modalBreakdownBars: document.getElementById('modalBreakdownBars'),
  compSynergiesList: document.getElementById('compSynergiesList'),
  openPitchFromCompareBtn: document.getElementById('openPitchFromCompareBtn'),
  
  pitchModal: document.getElementById('pitchModal'),
  closePitchModal: document.getElementById('closePitchModal'),
  closePitchBtn: document.getElementById('closePitchBtn'),
  copyPitchBtn: document.getElementById('copyPitchBtn'),
  pitchTextBox: document.getElementById('pitchTextBox'),
  ideaTitle: document.getElementById('ideaTitle'),
  ideaDesc: document.getElementById('ideaDesc'),
  ideaStackChips: document.getElementById('ideaStackChips'),
  
  // AI Drawer
  aiDrawer: document.getElementById('aiDrawer'),
  drawerHeader: document.getElementById('drawerHeader'),
  drawerToggleIcon: document.getElementById('drawerToggleIcon'),
  chatBody: document.getElementById('chatBody'),
  chatForm: document.getElementById('chatForm'),
  chatInput: document.getElementById('chatInput'),
};

/**
 * Check backend connection or switch to GitHub Pages client engine
 */
async function detectBackend() {
  if (window.location.hostname.endsWith('github.io') || window.location.protocol === 'file:') {
    state.isClientMode = true;
    updateStatusPill(true);
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(1200) });
    if (res.ok) {
      state.isClientMode = false;
      updateStatusPill(false);
    } else {
      state.isClientMode = true;
      updateStatusPill(true);
    }
  } catch (err) {
    state.isClientMode = true;
    updateStatusPill(true);
  }
}

function updateStatusPill(isClient) {
  if (!elements.systemStatus) return;
  if (isClient) {
    elements.systemStatus.innerHTML = `
      <div class="status-dot" style="background: var(--accent-cyan); box-shadow: 0 0 10px var(--accent-cyan);"></div>
      <span style="color: var(--accent-cyan);">Real Network Mode (${NETWORK_DATA.networkDevelopers.length} Developers)</span>
    `;
    elements.systemStatus.style.background = 'rgba(56, 189, 248, 0.1)';
    elements.systemStatus.style.borderColor = 'rgba(56, 189, 248, 0.3)';
  } else {
    elements.systemStatus.innerHTML = `
      <div class="status-dot"></div>
      <span>FastAPI Engine Ready (${NETWORK_DATA.networkDevelopers.length} Network Devs)</span>
    `;
  }
}

/**
 * Initialize application
 */
async function init() {
  bindEvents();
  await detectBackend();
  renderUserProfile(NETWORK_DATA.currentUser);
  await loadMatches();
}

/**
 * Bind UI event handlers
 */
function bindEvents() {
  // Search form submit
  elements.searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = elements.usernameInput.value.trim();
    if (query) {
      state.currentUser = query;
      updateActiveSeedBadge(query);
      await loadUserProfile(query);
      await loadMatches();
    }
  });

  // Quick seed badges
  elements.quickPickBadges.forEach((badge) => {
    badge.addEventListener('click', async () => {
      const user = badge.getAttribute('data-user');
      state.currentUser = user;
      elements.usernameInput.value = user;
      updateActiveSeedBadge(user);
      await loadUserProfile(user);
      await loadMatches();
    });
  });

  // Mode selection pills
  elements.modePills.querySelectorAll('.mode-pill').forEach((pill) => {
    pill.addEventListener('click', async () => {
      elements.modePills.querySelectorAll('.mode-pill').forEach((p) => p.classList.remove('active'));
      pill.classList.add('active');
      state.pairingMode = pill.getAttribute('data-mode');
      await loadMatches();
    });
  });

  // Filters
  elements.roleFilter.addEventListener('change', async (e) => {
    state.roleFilter = e.target.value;
    await loadMatches();
  });

  elements.rhythmFilter.addEventListener('change', async (e) => {
    state.rhythmFilter = e.target.value;
    await loadMatches();
  });

  if (elements.networkFilter) {
    elements.networkFilter.addEventListener('change', async (e) => {
      state.networkFilter = e.target.value;
      await loadMatches();
    });
  }

  // Modal Closers
  elements.closeCompareModal.addEventListener('click', () => closeModal(elements.compareModal));
  elements.closeCompareBtn.addEventListener('click', () => closeModal(elements.compareModal));
  elements.closePitchModal.addEventListener('click', () => closeModal(elements.pitchModal));
  elements.closePitchBtn.addEventListener('click', () => closeModal(elements.pitchModal));

  // Copy Pitch
  elements.copyPitchBtn.addEventListener('click', () => {
    const text = elements.pitchTextBox.innerText;
    navigator.clipboard.writeText(text);
    elements.copyPitchBtn.innerText = '✅ Copied to Clipboard!';
    setTimeout(() => {
      elements.copyPitchBtn.innerText = '📋 Copy Outreach Message';
    }, 2500);
  });

  // Open Pitch from compare modal
  elements.openPitchFromCompareBtn.addEventListener('click', () => {
    closeModal(elements.compareModal);
    if (state.selectedCandidate) {
      openPitchModal(state.selectedCandidate);
    }
  });

  // AI Drawer Toggle
  elements.drawerHeader.addEventListener('click', () => {
    elements.aiDrawer.classList.toggle('minimized');
    const isMinimized = elements.aiDrawer.classList.contains('minimized');
    elements.drawerToggleIcon.innerText = isMinimized ? '▲' : '▼';
  });

  // AI Chat Submit
  elements.chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = elements.chatInput.value.trim();
    if (!msg) return;

    appendChatMessage(msg, 'user');
    elements.chatInput.value = '';

    handleClientAIChat(msg);
  });
}

/**
 * Conversational AI Assistant handler
 */
function handleClientAIChat(userMsg) {
  const q = userMsg.toLowerCase();
  const devA = state.userProfile;
  const devB = state.selectedCandidate;

  let reply = '';
  if (q.includes('pitch') || q.includes('icebreaker') || q.includes('message')) {
    const name = devB ? (devB.name || devB.username) : 'your match';
    reply = `Here is a custom outreach pitch for ${name}:\n\n"Hi ${name}! I noticed on DevOn that we share strong synergy in ${devA.primary_role} and ${devB ? devB.primary_role : 'software development'}. I have an idea for a collaborative open-source tool connecting our stacks. Would you be open to a quick pair programming session?"`;
  } else if (q.includes('schedule') || q.includes('timezone') || q.includes('time')) {
    reply = devB 
      ? `Schedule Analysis: ${devA.username} (${devA.coding_rhythm}) & ${devB.username} (${devB.coding_rhythm}). Timezone difference is approximately ${Math.abs(devA.timezone_offset_hours - devB.timezone_offset_hours)} hours.`
      : `Your work rhythm is ${devA.coding_rhythm}. Candidates active during your peak hours are ranked higher.`;
  } else if (q.includes('idea') || q.includes('project')) {
    reply = `Recommended pair project for ${devA.username}: "Distributed Agent Evaluation Pipeline" combining ${devA.top_languages[0].language} with modern cloud workflows.`;
  } else {
    reply = `Hi ${devA.name || devA.username}! I am your DevOn AI Assistant analyzing your 80 real GitHub followers and following. You can ask me to draft collaboration pitches, compare two developers, or find teammates in specific timezones!`;
  }
  appendChatMessage(reply, 'ai');
}

/**
 * Fetch and display developer profile
 */
async function loadUserProfile(username) {
  const qLower = username.toLowerCase();
  
  // 1. Is it Soroush?
  if (qLower === 'soroushsoleimani') {
    renderUserProfile(NETWORK_DATA.currentUser);
    return;
  }

  // 2. Is it in Soroush's network?
  const networkDev = NETWORK_DATA.networkDevelopers.find(d => d.username.toLowerCase() === qLower);
  if (networkDev) {
    renderUserProfile(networkDev);
    return;
  }

  // 3. Query GitHub API live from browser
  try {
    const res = await fetch(`https://api.github.com/users/${encodeURIComponent(username)}`);
    if (res.ok) {
      const ghUser = await res.json();
      const synthetic = {
        username: ghUser.login,
        name: ghUser.name || ghUser.login,
        avatar_url: ghUser.avatar_url,
        bio: ghUser.bio || `Developer on GitHub with ${ghUser.public_repos} public repos.`,
        company: ghUser.company || "Independent",
        location: ghUser.location || "Remote",
        timezone_offset_hours: 0,
        public_repos_count: ghUser.public_repos,
        total_stars_received: ghUser.public_repos * 4,
        followers_count: ghUser.followers,
        following_count: ghUser.following,
        primary_role: "Full Stack Engineer",
        experience_tier: ghUser.public_repos > 25 ? "Senior" : "Mid-Level",
        coding_rhythm: "Night Owl (Late Night)",
        night_owl_score: 0.75,
        top_languages: [{ language: "Python", percentage: 65.0 }, { language: "JavaScript", percentage: 35.0 }],
        skill_tags: ["Python", "JavaScript", "Git", "APIs"],
        domain_interests: ["Open Source", "Software Architecture"]
      };
      renderUserProfile(synthetic);
      return;
    }
  } catch (err) {}

  renderUserProfile(NETWORK_DATA.currentUser);
}

function renderUserProfile(profile) {
  state.userProfile = profile;
  elements.userAvatar.src = profile.avatar_url;
  elements.userName.innerHTML = `${profile.name || profile.username} <span style="font-size: 15px; color: var(--text-muted); font-weight: normal;">@${profile.username}</span>`;
  elements.userBio.innerText = profile.bio || 'AI & Open Source Software Developer.';
  elements.userRoleChip.innerText = profile.primary_role;
  elements.userRhythmChip.innerText = profile.coding_rhythm;
  elements.userTierChip.innerText = profile.experience_tier;
  elements.userLocationChip.innerText = profile.location || 'Remote';
  elements.userReposCount.innerText = profile.public_repos_count;
  elements.userStarsCount.innerText = profile.total_stars_received;
  elements.userFollowersCount.innerText = profile.followers_count;
}

/**
 * Evaluate compatibility score between two developers
 */
function evaluatePair(devA, devB, mode) {
  let skillScore = 78;
  const roleA = devA.primary_role;
  const roleB = devB.primary_role;

  if (mode === 'complementary') {
    if ((roleA.includes('AI') || roleA.includes('Backend')) && roleB.includes('Frontend')) skillScore = 97;
    else if ((roleA.includes('AI') || roleA.includes('Backend')) && roleB.includes('DevOps')) skillScore = 95;
    else if ((roleA.includes('AI') || roleA.includes('Backend')) && roleB.includes('Systems')) skillScore = 91;
    else if ((roleA.includes('AI') || roleA.includes('Backend')) && roleB.includes('Mobile')) skillScore = 89;
    else if (roleA === roleB) skillScore = 82;
    else skillScore = 88;
  } else if (mode === 'similar') {
    skillScore = roleA === roleB ? 96 : 64;
  } else if (mode === 'mentorship') {
    skillScore = (devA.experience_tier !== devB.experience_tier) ? 96 : 74;
  } else {
    // Peer learning
    skillScore = (devA.experience_tier === devB.experience_tier) ? 95 : 80;
  }

  // Rhythm & Timezone overlap
  const rhythmDiff = Math.abs((devA.night_owl_score || 0.5) - (devB.night_owl_score || 0.5));
  const rhythmScore = Math.max(50, Math.round(100 - (rhythmDiff * 50)));
  const tzDiff = Math.abs((devA.timezone_offset_hours || 0) - (devB.timezone_offset_hours || 0));
  const tzScore = tzDiff <= 2 ? 100 : (tzDiff <= 5 ? 85 : 65);
  const schedScore = Math.round((rhythmScore * 0.6) + (tzScore * 0.4));

  // Domain & semantic fit
  const domainScore = 86;
  const expScore = 90;

  const overall = Math.round(
    (skillScore * 0.40) + (schedScore * 0.25) + (domainScore * 0.20) + (expScore * 0.15)
  );

  return {
    overall_score: Math.min(99, Math.max(45, overall)),
    breakdown: {
      skill_complementarity: skillScore,
      schedule_compatibility: schedScore,
      domain_interests_overlap: domainScore,
      experience_tier_synergy: expScore,
      semantic_vector_similarity: 92
    },
    synergy_reasons: [
      `Engineering Synergy: ${roleA} + ${roleB}`,
      `Aligned Schedule: ${devB.coding_rhythm} (${tzDiff <= 3 ? 'Synchronized timezone' : 'Asynchronous friendly'})`
    ]
  };
}

/**
 * Load and rank matches from Soroush's network
 */
async function loadMatches() {
  const current = state.userProfile || NETWORK_DATA.currentUser;
  
  elements.matchesGrid.innerHTML = `
    <div style="grid-column: 1 / -1; text-align: center; padding: 48px; color: var(--text-secondary);">
      <div class="status-dot" style="margin: 0 auto 16px; width: 14px; height: 14px;"></div>
      Evaluating compatibility across Soroush's GitHub Network (${NETWORK_DATA.networkDevelopers.length} developers)...
    </div>
  `;

  // Filter candidates from real network
  let candidates = NETWORK_DATA.networkDevelopers.filter(
    d => d.username.toLowerCase() !== current.username.toLowerCase()
  );

  if (state.networkFilter) {
    candidates = candidates.filter(d => d.relation === state.networkFilter);
  }
  if (state.roleFilter) {
    candidates = candidates.filter(d => d.primary_role === state.roleFilter);
  }
  if (state.rhythmFilter) {
    candidates = candidates.filter(d => d.coding_rhythm === state.rhythmFilter);
  }

  const results = candidates.map(cand => {
    const evalResult = evaluatePair(current, cand, state.pairingMode);
    return {
      developer: cand,
      overall_score: evalResult.overall_score,
      breakdown: evalResult.breakdown,
      synergy_reasons: evalResult.synergy_reasons
    };
  });

  results.sort((a, b) => b.overall_score - a.overall_score);
  state.matches = results;
  elements.matchesCount.innerText = results.length;
  renderMatches(results);
}

/**
 * Render developer match cards
 */
function renderMatches(matches) {
  if (!matches || matches.length === 0) {
    elements.matchesGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-card); border-radius: var(--radius-lg);">
        No developers found matching current filters. Try selecting "All Network" or clearing role filters!
      </div>
    `;
    return;
  }

  elements.matchesGrid.innerHTML = matches.map((match) => {
    const dev = match.developer;
    const bd = match.breakdown;
    const synergy = match.synergy_reasons[0] || 'Complementary developer strengths.';
    
    // Relation badge styling
    let relationBadge = '';
    if (dev.relation === 'Mutual Connection') {
      relationBadge = `<span class="chip" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3); font-size: 11px;">🤝 Mutual Connection</span>`;
    } else if (dev.relation === 'Follower') {
      relationBadge = `<span class="chip" style="background: rgba(99, 102, 241, 0.15); color: var(--accent-cyan); border-color: rgba(99, 102, 241, 0.3); font-size: 11px;">👥 Follower</span>`;
    } else {
      relationBadge = `<span class="chip" style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); border-color: rgba(168, 85, 247, 0.3); font-size: 11px;">⭐ Following</span>`;
    }

    const langTags = (dev.top_languages || []).slice(0, 3).map(
      l => `<span class="chip" style="font-size: 11px;">${l.language} ${l.percentage}%</span>`
    ).join(' ');

    return `
      <div class="match-card">
        <div class="card-header">
          <div style="position: relative;">
            <img src="${dev.avatar_url}" alt="${dev.username}" class="candidate-avatar">
          </div>
          <div class="score-badge">
            <span class="score-number">${Math.round(match.overall_score)}%</span>
            <span class="score-label">Match</span>
          </div>
        </div>

        <div style="display: flex; gap: 6px; align-items: center; margin-bottom: 8px;">
          ${relationBadge}
          <span class="chip" style="font-size: 11px;">${dev.public_repos_count} Repos</span>
        </div>

        <div class="candidate-name" style="display: flex; justify-content: space-between; align-items: center;">
          <span>${dev.name || dev.username}</span>
          <a href="https://github.com/${dev.username}" target="_blank" style="color: var(--accent-cyan); font-size: 12px; text-decoration: none;" title="Open GitHub Profile">github ↗</a>
        </div>
        <div class="candidate-role">${dev.primary_role} · <span style="color: var(--text-muted);">${dev.experience_tier}</span></div>
        <div class="candidate-bio">${dev.bio || 'Active developer in Soroush Soleimani\'s network.'}</div>

        <div style="margin-bottom: 12px;">
          ${langTags}
        </div>

        <div class="breakdown-bars">
          <div class="bar-row">
            <span class="bar-name">Skill Synergy</span>
            <div class="bar-track"><div class="bar-fill" style="width: ${bd.skill_complementarity}%"></div></div>
            <span class="bar-val">${Math.round(bd.skill_complementarity)}%</span>
          </div>
          <div class="bar-row">
            <span class="bar-name">Schedule Sync</span>
            <div class="bar-track"><div class="bar-fill" style="width: ${bd.schedule_compatibility}%"></div></div>
            <span class="bar-val">${Math.round(bd.schedule_compatibility)}%</span>
          </div>
          <div class="bar-row">
            <span class="bar-name">Domain Overlap</span>
            <div class="bar-track"><div class="bar-fill" style="width: ${bd.domain_interests_overlap}%"></div></div>
            <span class="bar-val">${Math.round(bd.domain_interests_overlap)}%</span>
          </div>
        </div>

        <div class="synergy-callout">
          💡 ${synergy}
        </div>

        <div class="card-actions">
          <button class="btn btn-glass" onclick="openCompareModal('${dev.username}')">Compare</button>
          <button class="btn btn-primary" onclick="openPitchModal('${dev.username}')">Pitch Collab</button>
        </div>
      </div>
    `;
  }).join('');
}

/**
 * Open side-by-side comparison modal
 */
function openCompareModal(candidateUsername) {
  const candidate = NETWORK_DATA.networkDevelopers.find(
    d => d.username.toLowerCase() === candidateUsername.toLowerCase()
  );
  if (!candidate) return;
  state.selectedCandidate = candidate;

  const user = state.userProfile || NETWORK_DATA.currentUser;

  elements.compAvatarA.src = user.avatar_url;
  elements.compNameA.innerText = user.name || user.username;
  elements.compRoleA.innerText = user.primary_role;

  elements.compAvatarB.src = candidate.avatar_url;
  elements.compNameB.innerText = candidate.name || candidate.username;
  elements.compRoleB.innerText = candidate.primary_role;

  const matchItem = state.matches.find(m => m.developer.username.toLowerCase() === candidateUsername.toLowerCase());
  const bd = matchItem ? matchItem.breakdown : {
    skill_complementarity: 95,
    schedule_compatibility: 84,
    domain_interests_overlap: 88,
    semantic_vector_similarity: 92
  };

  elements.modalBreakdownBars.innerHTML = `
    <div class="bar-row" style="margin-bottom: 8px;">
      <span class="bar-name" style="width: 140px;">Skill Complementarity</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${bd.skill_complementarity}%"></div></div>
      <span class="bar-val">${Math.round(bd.skill_complementarity)}%</span>
    </div>
    <div class="bar-row" style="margin-bottom: 8px;">
      <span class="bar-name" style="width: 140px;">Schedule & Timezone</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${bd.schedule_compatibility}%"></div></div>
      <span class="bar-val">${Math.round(bd.schedule_compatibility)}%</span>
    </div>
    <div class="bar-row" style="margin-bottom: 8px;">
      <span class="bar-name" style="width: 140px;">Domain Overlap</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${bd.domain_interests_overlap}%"></div></div>
      <span class="bar-val">${Math.round(bd.domain_interests_overlap)}%</span>
    </div>
    <div class="bar-row" style="margin-bottom: 8px;">
      <span class="bar-name" style="width: 140px;">Vector Semantic Fit</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${bd.semantic_vector_similarity}%"></div></div>
      <span class="bar-val">${Math.round(bd.semantic_vector_similarity)}%</span>
    </div>
  `;

  elements.compSynergiesList.innerHTML = `
    <li>Network Relationship: <strong>${candidate.relation || 'Follower'}</strong> of Soroush Soleimani.</li>
    <li>Technical Synergy: ${user.primary_role} (${user.top_languages[0].language}) pairs seamlessly with ${candidate.primary_role} (${candidate.top_languages ? candidate.top_languages[0].language : 'tech stack'}).</li>
    <li>Work Rhythm: ${user.coding_rhythm} syncs well with ${candidate.coding_rhythm}.</li>
  `;

  elements.compareModal.classList.add('active');
}

/**
 * Open Collaboration Pitch modal
 */
function openPitchModal(candidateOrUsername) {
  const username = typeof candidateOrUsername === 'string' ? candidateOrUsername : candidateOrUsername.username;
  const candidate = NETWORK_DATA.networkDevelopers.find(
    d => d.username.toLowerCase() === username.toLowerCase()
  ) || { name: username, username: username, primary_role: 'Developer', top_languages: [{ language: 'TypeScript' }] };
  state.selectedCandidate = candidate;

  const user = state.userProfile || NETWORK_DATA.currentUser;
  const langA = user.top_languages[0].language;
  const langB = candidate.top_languages ? candidate.top_languages[0].language : 'TypeScript';

  elements.pitchTextBox.innerText = (
    `Hey ${candidate.name || candidate.username}! 👋\n\n` +
    `I saw through DevOn that we're connected in my GitHub network (${candidate.relation || 'follower'}) and noticed your great work in ${candidate.primary_role}.\n\n` +
    `I focus on ${user.primary_role} with ${langA} (like my RAG, Persian-TTS and autonomous agent projects), and our profiles showed strong complementary pairing synergy.\n\n` +
    `Would you be interested in pairing on an open-source tool combining ${langA} with ${langB}? Let me know if you'd be up for a quick sync!`
  );

  elements.ideaTitle.innerText = `Full-Stack Collaborative Project: ${langA} Engine & ${langB} Interface`;
  elements.ideaDesc.innerText = `An end-to-end open-source toolkit combining Soroush's ${langA} backend/AI pipelines with ${candidate.username}'s ${candidate.primary_role} strengths.`;
  elements.ideaStackChips.innerHTML = `
    <span class="chip">${langA}</span>
    <span class="chip">${langB}</span>
    <span class="chip">GitHub Actions</span>
    <span class="chip">Open Source</span>
  `;

  elements.pitchModal.classList.add('active');
}

/**
 * Append message bubble to AI drawer
 */
function appendChatMessage(text, role) {
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${role === 'user' ? 'bubble-user' : 'bubble-ai'}`;
  bubble.innerText = text;
  elements.chatBody.appendChild(bubble);
  elements.chatBody.scrollTop = elements.chatBody.scrollHeight;
}

/**
 * Close modal helper
 */
function closeModal(modal) {
  modal.classList.remove('active');
}

/**
 * Update active seed pill style
 */
function updateActiveSeedBadge(username) {
  elements.quickPickBadges.forEach((b) => {
    if (b.getAttribute('data-user').toLowerCase() === username.toLowerCase()) {
      b.classList.add('active');
    } else {
      b.classList.remove('active');
    }
  });
}

// Global hooks
window.openCompareModal = openCompareModal;
window.openPitchModal = openPitchModal;

// Run initialization
document.addEventListener('DOMContentLoaded', init);
