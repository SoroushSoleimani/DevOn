/**
 * DevOn Frontend Client Logic
 * Supports dual-mode execution:
 * 1. Full API Mode (when connected to FastAPI backend)
 * 2. Standalone Client-Side Mode (when hosted on GitHub Pages / static hosting)
 */

const API_BASE = '/api/v1';

// Seed community developers for standalone / GitHub Pages execution
const CLIENT_COMMUNITY_DEVS = {
  "soroushsoleimani": {
    username: "SoroushSoleimani",
    name: "Soroush Soleimani",
    avatar_url: "https://avatars.githubusercontent.com/u/140951703?v=4",
    bio: "AI & Full-Stack Developer | Building autonomous systems & collaborative dev tools.",
    company: "Independent / Open Source",
    location: "Tehran, Iran",
    timezone_offset_hours: 3.5,
    public_repos_count: 18,
    total_stars_received: 42,
    followers_count: 34,
    following_count: 28,
    primary_role: "Backend Developer",
    experience_tier: "Senior",
    coding_rhythm: "Night Owl (Late Night)",
    night_owl_score: 0.85,
    top_languages: [
      { language: "Python", percentage: 52.0 },
      { language: "TypeScript", percentage: 24.0 },
      { language: "JavaScript", percentage: 14.0 },
      { language: "C++", percentage: 10.0 }
    ],
    skill_tags: ["FastAPI", "Python", "Docker", "PyTorch", "AsyncIO", "Next.js"],
    domain_interests: ["AI Agents", "Developer Tools", "Distributed Systems"]
  },
  "elena-codes": {
    username: "elena-codes",
    name: "Elena Rostova",
    avatar_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face",
    bio: "Frontend Architect & Design Systems Lead. Passionate about glassmorphism and micro-interactions.",
    company: "Voxel UI",
    location: "Berlin, Germany",
    timezone_offset_hours: 1.0,
    public_repos_count: 24,
    total_stars_received: 148,
    followers_count: 112,
    following_count: 45,
    primary_role: "Frontend Developer",
    experience_tier: "Senior",
    coding_rhythm: "Steady All-Day",
    night_owl_score: 0.40,
    top_languages: [
      { language: "TypeScript", percentage: 58.0 },
      { language: "CSS", percentage: 25.0 },
      { language: "JavaScript", percentage: 12.0 }
    ],
    skill_tags: ["React", "TypeScript", "TailwindCSS", "Design Systems", "Vite"],
    domain_interests: ["Design Systems", "Developer Tools", "Data Visualization"]
  },
  "marcus-devops": {
    username: "marcus-devops",
    name: "Marcus Vance",
    avatar_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
    bio: "Kubernetes whisperer, Terraform addict, and CI/CD pipeline architect.",
    company: "CloudNative Labs",
    location: "Austin, TX, USA",
    timezone_offset_hours: -6.0,
    public_repos_count: 31,
    total_stars_received: 210,
    followers_count: 89,
    following_count: 52,
    primary_role: "DevOps & Cloud",
    experience_tier: "Lead / Staff",
    coding_rhythm: "Early Bird (Morning)",
    night_owl_score: 0.15,
    top_languages: [
      { language: "Go", percentage: 48.0 },
      { language: "HCL", percentage: 26.0 },
      { language: "Python", percentage: 18.0 }
    ],
    skill_tags: ["Kubernetes", "Docker", "Terraform", "Go", "CI/CD", "AWS"],
    domain_interests: ["Cloud Infrastructure", "Distributed Systems", "Security"]
  },
  "priya-ai": {
    username: "priya-ai",
    name: "Priya Sharma",
    avatar_url: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&h=150&fit=crop&crop=face",
    bio: "ML Researcher & GenAI Engineer. Exploring retrieval-augmented generation and vector index optimization.",
    company: "DeepData AI",
    location: "Toronto, Canada",
    timezone_offset_hours: -5.0,
    public_repos_count: 16,
    total_stars_received: 95,
    followers_count: 76,
    following_count: 60,
    primary_role: "AI / Machine Learning",
    experience_tier: "Senior",
    coding_rhythm: "Night Owl (Late Night)",
    night_owl_score: 0.78,
    top_languages: [
      { language: "Python", percentage: 75.0 },
      { language: "Jupyter Notebook", percentage: 15.0 },
      { language: "Rust", percentage: 10.0 }
    ],
    skill_tags: ["PyTorch", "HuggingFace", "Python", "RAG", "FAISS", "FastAPI"],
    domain_interests: ["AI Agents", "LLMs", "Vector Databases"]
  },
  "alex-systems": {
    username: "alex-systems",
    name: "Alex Mercer",
    avatar_url: "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&h=150&fit=crop&crop=face",
    bio: "Low-level hacker, Rustacean, and database engine enthusiast. Zero-cost abstractions only.",
    company: "KernelByte",
    location: "Stockholm, Sweden",
    timezone_offset_hours: 1.0,
    public_repos_count: 28,
    total_stars_received: 340,
    followers_count: 190,
    following_count: 35,
    primary_role: "Systems / Low-Level",
    experience_tier: "Senior",
    coding_rhythm: "Night Owl (Late Night)",
    night_owl_score: 0.72,
    top_languages: [
      { language: "Rust", percentage: 70.0 },
      { language: "C", percentage: 20.0 },
      { language: "Python", percentage: 10.0 }
    ],
    skill_tags: ["Rust", "Systems Programming", "Concurrency", "Linux", "WASM"],
    domain_interests: ["Database Engines", "Distributed Systems", "WebAssembly"]
  }
};

// Application State
const state = {
  currentUser: 'SoroushSoleimani',
  pairingMode: 'complementary',
  roleFilter: '',
  rhythmFilter: '',
  userProfile: null,
  matches: [],
  selectedCandidate: null,
  isClientMode: false,
};

// DOM Elements
const elements = {
  systemStatus: document.getElementById('systemStatus'),
  searchForm: document.getElementById('searchForm'),
  usernameInput: document.getElementById('usernameInput'),
  userBanner: document.getElementById('userBanner'),
  userAvatar: document.getElementById('userAvatar'),
  userName: document.getElementById('userName'),
  userLogin: document.getElementById('userLogin'),
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
 * Check if backend API is available
 */
async function detectBackend() {
  if (window.location.hostname.endsWith('github.io') || window.location.protocol === 'file:') {
    state.isClientMode = true;
    updateStatusPill(true);
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(1500) });
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
      <span style="color: var(--accent-cyan);">GitHub Pages (Live Client Mode)</span>
    `;
    elements.systemStatus.style.background = 'rgba(56, 189, 248, 0.1)';
    elements.systemStatus.style.borderColor = 'rgba(56, 189, 248, 0.3)';
  } else {
    elements.systemStatus.innerHTML = `
      <div class="status-dot"></div>
      <span>FastAPI Engine Ready</span>
    `;
  }
}

/**
 * Initialize application
 */
async function init() {
  bindEvents();
  await detectBackend();
  await loadUserProfile(state.currentUser);
  await loadMatches();
}

/**
 * Bind user interface event handlers
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

  // Role & Rhythm Filter changes
  elements.roleFilter.addEventListener('change', async (e) => {
    state.roleFilter = e.target.value;
    await loadMatches();
  });

  elements.rhythmFilter.addEventListener('change', async (e) => {
    state.rhythmFilter = e.target.value;
    await loadMatches();
  });

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

    if (!state.isClientMode) {
      try {
        const res = await fetch(`${API_BASE}/ai/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            developer_username: state.currentUser,
            candidate_username: state.selectedCandidate ? state.selectedCandidate.username : null,
            messages: [{ role: 'user', content: msg }],
          }),
        });
        const data = await res.json();
        appendChatMessage(data.reply, 'ai');
        return;
      } catch (err) {
        // Fall back to client responder
      }
    }

    // Client-side AI Assistant Response
    handleClientAIChat(msg);
  });
}

function handleClientAIChat(userMsg) {
  const q = userMsg.toLowerCase();
  const devA = state.userProfile;
  const devB = state.selectedCandidate;

  let reply = '';
  if (q.includes('pitch') || q.includes('icebreaker') || q.includes('message')) {
    const name = devB ? devB.name : 'your match';
    reply = `Here is a custom outreach pitch for ${name}:\n\n"Hi ${name}! I noticed on DevOn that our coding patterns have strong synergy. I focus on ${devA.primary_role} while you specialize in ${devB ? devB.primary_role : 'your stack'}. Would you be open to an async pair-brainstorm on building an open-source tool together?"`;
  } else if (q.includes('schedule') || q.includes('timezone') || q.includes('time')) {
    reply = devB 
      ? `Schedule Sync: ${devA.username} (${devA.coding_rhythm}) & ${devB.username} (${devB.coding_rhythm}). Timezone offset is approx ${Math.abs(devA.timezone_offset_hours - devB.timezone_offset_hours)} hours.`
      : `Your peak rhythm is ${devA.coding_rhythm}. We prioritize candidates with overlapping working hours.`;
  } else if (q.includes('idea') || q.includes('project')) {
    reply = `Recommended project: "Cross-Stack Autonomous Studio" combining ${devA.top_languages[0].language} core APIs with reactive UI components.`;
  } else {
    reply = `Hi ${devA.name || devA.username}! I am your DevOn Pair Assistant running in client mode on GitHub Pages. Feel free to ask about pairing compatibility, project ideas, or custom icebreakers!`;
  }
  appendChatMessage(reply, 'ai');
}

/**
 * Fetch and display the active user's synthesized profile
 */
async function loadUserProfile(username) {
  if (!state.isClientMode) {
    try {
      const res = await fetch(`${API_BASE}/profiles/${encodeURIComponent(username)}`);
      if (res.ok) {
        const profile = await res.json();
        renderUserProfile(profile);
        return;
      }
    } catch (err) {
      state.isClientMode = true;
      updateStatusPill(true);
    }
  }

  // Client-Side lookup
  const key = username.toLowerCase();
  if (CLIENT_COMMUNITY_DEVS[key]) {
    renderUserProfile(CLIENT_COMMUNITY_DEVS[key]);
    return;
  }

  // Try live public GitHub API from browser
  try {
    const res = await fetch(`https://api.github.com/users/${encodeURIComponent(username)}`);
    if (res.ok) {
      const ghUser = await res.json();
      const syntheticProfile = {
        username: ghUser.login,
        name: ghUser.name || ghUser.login,
        avatar_url: ghUser.avatar_url,
        bio: ghUser.bio || 'Open source software developer.',
        company: ghUser.company,
        location: ghUser.location || 'Remote',
        timezone_offset_hours: 0,
        public_repos_count: ghUser.public_repos,
        total_stars_received: ghUser.public_repos * 3,
        followers_count: ghUser.followers,
        following_count: ghUser.following,
        primary_role: 'Full Stack Engineer',
        experience_tier: ghUser.public_repos > 30 ? 'Senior' : 'Mid-Level',
        coding_rhythm: 'Night Owl (Late Night)',
        night_owl_score: 0.7,
        top_languages: [{ language: 'Python', percentage: 60.0 }, { language: 'TypeScript', percentage: 40.0 }],
        skill_tags: ['Python', 'TypeScript', 'Docker', 'FastAPI'],
        domain_interests: ['Open Source', 'Software Engineering']
      };
      renderUserProfile(syntheticProfile);
      return;
    }
  } catch (e) {}

  // Fallback to default
  renderUserProfile(CLIENT_COMMUNITY_DEVS['soroushsoleimani']);
}

function renderUserProfile(profile) {
  state.userProfile = profile;
  elements.userAvatar.src = profile.avatar_url;
  elements.userName.innerHTML = `${profile.name || profile.username} <span style="font-size: 15px; color: var(--text-muted); font-weight: normal;">@${profile.username}</span>`;
  elements.userBio.innerText = profile.bio || 'Passionate open source developer.';
  elements.userRoleChip.innerText = profile.primary_role;
  elements.userRhythmChip.innerText = profile.coding_rhythm;
  elements.userTierChip.innerText = profile.experience_tier;
  elements.userLocationChip.innerText = profile.location || 'Remote';
  elements.userReposCount.innerText = profile.public_repos_count;
  elements.userStarsCount.innerText = profile.total_stars_received;
  elements.userFollowersCount.innerText = profile.followers_count;
}

/**
 * Fetch and render matching recommendations
 */
async function loadMatches() {
  elements.matchesGrid.innerHTML = `
    <div style="grid-column: 1 / -1; text-align: center; padding: 48px; color: var(--text-secondary);">
      <div class="status-dot" style="margin: 0 auto 16px; width: 14px; height: 14px;"></div>
      Analyzing GitHub graph and computing compatibility embeddings...
    </div>
  `;

  if (!state.isClientMode) {
    try {
      let url = `${API_BASE}/matches/find/${encodeURIComponent(state.currentUser)}?pairing_mode=${state.pairingMode}`;
      if (state.roleFilter) url += `&primary_role=${encodeURIComponent(state.roleFilter)}`;
      if (state.rhythmFilter) url += `&coding_rhythm=${encodeURIComponent(state.rhythmFilter)}`;

      const res = await fetch(url);
      if (res.ok) {
        const matches = await res.json();
        state.matches = matches;
        elements.matchesCount.innerText = matches.length;
        renderMatches(matches);
        return;
      }
    } catch (err) {
      state.isClientMode = true;
      updateStatusPill(true);
    }
  }

  // Client-Side Match Calculation
  const matches = computeClientMatches();
  state.matches = matches;
  elements.matchesCount.innerText = matches.length;
  renderMatches(matches);
}

function computeClientMatches() {
  const current = state.userProfile || CLIENT_COMMUNITY_DEVS['soroushsoleimani'];
  const candidates = Object.values(CLIENT_COMMUNITY_DEVS).filter(
    d => d.username.toLowerCase() !== current.username.toLowerCase()
  );

  const results = [];
  for (const cand of candidates) {
    if (state.roleFilter && cand.primary_role !== state.roleFilter) continue;
    if (state.rhythmFilter && cand.coding_rhythm !== state.rhythmFilter) continue;

    // Multi-factor client calculation
    let skillScore = 80;
    if (state.pairingMode === 'complementary') {
      if (current.primary_role.includes('Backend') && cand.primary_role.includes('Frontend')) skillScore = 96;
      else if (current.primary_role.includes('Frontend') && cand.primary_role.includes('Backend')) skillScore = 96;
      else if (cand.primary_role.includes('DevOps') || cand.primary_role.includes('AI')) skillScore = 92;
    } else if (state.pairingMode === 'similar') {
      skillScore = current.primary_role === cand.primary_role ? 94 : 62;
    }

    const rhythmDiff = Math.abs((current.night_owl_score || 0.5) - (cand.night_owl_score || 0.5));
    const schedScore = Math.max(50, Math.round(100 - (rhythmDiff * 55)));
    const domainScore = 88;
    const expScore = 92;

    const overall = Math.round(
      (skillScore * 0.40) + (schedScore * 0.25) + (domainScore * 0.20) + (expScore * 0.15)
    );

    results.push({
      developer: cand,
      overall_score: overall,
      breakdown: {
        skill_complementarity: skillScore,
        schedule_compatibility: schedScore,
        domain_interests_overlap: domainScore,
        experience_tier_synergy: expScore,
        semantic_vector_similarity: 90
      },
      synergy_reasons: [
        `Synergy superpower: ${current.primary_role} pairs with ${cand.primary_role}`,
        `Aligned active rhythm (${current.coding_rhythm})`
      ]
    });
  }

  results.sort((a, b) => b.overall_score - a.overall_score);
  return results;
}

/**
 * Render developer match cards into the grid
 */
function renderMatches(matches) {
  if (!matches || matches.length === 0) {
    elements.matchesGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-card); border-radius: var(--radius-lg);">
        No developer matches found matching the selected filters. Try switching pairing mode or clearing filters!
      </div>
    `;
    return;
  }

  elements.matchesGrid.innerHTML = matches.map((match) => {
    const dev = match.developer;
    const bd = match.breakdown;
    const synergy = match.synergy_reasons[0] || 'Complementary developer strengths.';

    return `
      <div class="match-card">
        <div class="card-header">
          <img src="${dev.avatar_url}" alt="${dev.username}" class="candidate-avatar">
          <div class="score-badge">
            <span class="score-number">${Math.round(match.overall_score)}%</span>
            <span class="score-label">Match</span>
          </div>
        </div>

        <div class="candidate-name">${dev.name || dev.username}</div>
        <div class="candidate-role">${dev.primary_role} · <span style="color: var(--text-muted);">${dev.experience_tier}</span></div>
        <div class="candidate-bio">${dev.bio || dev.ai_summary || 'Active software engineer.'}</div>

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
async function openCompareModal(candidateUsername) {
  const candidate = (state.matches.find(m => m.developer.username.toLowerCase() === candidateUsername.toLowerCase())?.developer) 
    || CLIENT_COMMUNITY_DEVS[candidateUsername.toLowerCase()];
  if (!candidate) return;
  state.selectedCandidate = candidate;

  const user = state.userProfile || CLIENT_COMMUNITY_DEVS['soroushsoleimani'];

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
      <span class="bar-name" style="width: 140px;">Domain Interests</span>
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
    <li>Full-stack synergy: ${user.primary_role} paired with ${candidate.primary_role}.</li>
    <li>Overlapping technical curiosity: shared interest in modern developer tools and open source.</li>
    <li>Aligned work rhythms: compatible schedule windows for asynchronous PR review and pair sessions.</li>
  `;

  elements.compareModal.classList.add('active');
}

/**
 * Open Collaboration Pitch modal
 */
async function openPitchModal(candidateOrUsername) {
  const username = typeof candidateOrUsername === 'string' ? candidateOrUsername : candidateOrUsername.username;
  const candidate = (state.matches.find(m => m.developer.username.toLowerCase() === username.toLowerCase())?.developer) 
    || CLIENT_COMMUNITY_DEVS[username.toLowerCase()] 
    || { name: username, username: username, primary_role: 'Developer' };
  state.selectedCandidate = candidate;

  const user = state.userProfile || CLIENT_COMMUNITY_DEVS['soroushsoleimani'];

  elements.pitchTextBox.innerText = (
    `Hey ${candidate.name || candidate.username}! 👋\n\n` +
    `I came across your profile through DevOn and was really impressed by your work in ${candidate.primary_role}. ` +
    `I specialize in ${user.primary_role} with ${user.top_languages[0].language}, and DevOn highlighted that our technical strengths have strong complementary synergy.\n\n` +
    `I would love to connect on building an open-source tool together or doing a weekend pair session. Are you open to a quick chat?`
  );

  elements.ideaTitle.innerText = `Collaborative Studio for ${user.top_languages[0].language} & ${candidate.top_languages ? candidate.top_languages[0].language : 'Modern Stack'}`;
  elements.ideaDesc.innerText = `An intelligent pair workspace combining high-performance ${user.top_languages[0].language} backend architecture with responsive client interactions.`;
  elements.ideaStackChips.innerHTML = `
    <span class="chip">${user.top_languages[0].language}</span>
    <span class="chip">${candidate.top_languages ? candidate.top_languages[0].language : 'TypeScript'}</span>
    <span class="chip">Docker</span>
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

// Global hook for inline onclick triggers
window.openCompareModal = openCompareModal;
window.openPitchModal = openPitchModal;

// Run initialization on DOM content ready
document.addEventListener('DOMContentLoaded', init);
