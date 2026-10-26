/**
 * DevOn Frontend Client Logic
 * Integrates with FastAPI backend for live profile analysis,
 * matchmaking, developer comparison, and AI pitch generation.
 */

const API_BASE = '/api/v1';

// Application State
const state = {
  currentUser: 'SoroushSoleimani',
  pairingMode: 'complementary',
  roleFilter: '',
  rhythmFilter: '',
  userProfile: null,
  matches: [],
  selectedCandidate: null,
};

// DOM Elements
const elements = {
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
 * Initialize application
 */
async function init() {
  bindEvents();
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
    } catch (err) {
      appendChatMessage('Sorry, unable to connect with AI assistant right now.', 'ai');
    }
  });
}

/**
 * Fetch and display the active user's synthesized profile
 */
async function loadUserProfile(username) {
  try {
    const res = await fetch(`${API_BASE}/profiles/${encodeURIComponent(username)}`);
    if (!res.ok) throw new Error('Failed to load profile');
    const profile = await res.json();
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
  } catch (err) {
    console.error('Error fetching user profile:', err);
  }
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

  try {
    let url = `${API_BASE}/matches/find/${encodeURIComponent(state.currentUser)}?pairing_mode=${state.pairingMode}`;
    if (state.roleFilter) url += `&primary_role=${encodeURIComponent(state.roleFilter)}`;
    if (state.rhythmFilter) url += `&coding_rhythm=${encodeURIComponent(state.rhythmFilter)}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to load matches');
    const matches = await res.json();
    state.matches = matches;
    elements.matchesCount.innerText = matches.length;

    renderMatches(matches);
  } catch (err) {
    elements.matchesGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 48px; color: var(--accent-rose);">
        Unable to load matches. Please make sure the backend is running.
      </div>
    `;
  }
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
  const candidate = state.matches.find(m => m.developer.username.toLowerCase() === candidateUsername.toLowerCase())?.developer;
  if (!candidate) return;
  state.selectedCandidate = candidate;

  try {
    const res = await fetch(`${API_BASE}/matches/compare?developer_a=${encodeURIComponent(state.currentUser)}&developer_b=${encodeURIComponent(candidateUsername)}`);
    const comp = await res.json();

    elements.compAvatarA.src = comp.developer_a.avatar_url;
    elements.compNameA.innerText = comp.developer_a.name || comp.developer_a.username;
    elements.compRoleA.innerText = comp.developer_a.primary_role;

    elements.compAvatarB.src = comp.developer_b.avatar_url;
    elements.compNameB.innerText = comp.developer_b.name || comp.developer_b.username;
    elements.compRoleB.innerText = comp.developer_b.primary_role;

    const bd = comp.breakdown;
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

    elements.compSynergiesList.innerHTML = comp.synergy_highlights.map(s => `<li>${s}</li>`).join('');

    elements.compareModal.classList.add('active');
  } catch (err) {
    console.error('Error fetching comparison:', err);
  }
}

/**
 * Open Collaboration Pitch modal
 */
async function openPitchModal(candidateOrUsername) {
  const username = typeof candidateOrUsername === 'string' ? candidateOrUsername : candidateOrUsername.username;
  elements.pitchTextBox.innerText = 'Crafting personalized AI outreach pitch and shared project concepts...';
  elements.pitchModal.classList.add('active');

  try {
    const res = await fetch(`${API_BASE}/collaboration/pitch?developer_a=${encodeURIComponent(state.currentUser)}&developer_b=${encodeURIComponent(username)}`);
    const pitch = await res.json();

    elements.pitchTextBox.innerText = pitch.icebreaker_text;

    if (pitch.suggested_project_ideas && pitch.suggested_project_ideas.length > 0) {
      const idea = pitch.suggested_project_ideas[0];
      elements.ideaTitle.innerText = idea.title;
      elements.ideaDesc.innerText = idea.description;
      elements.ideaStackChips.innerHTML = idea.recommended_tech_stack.map(s => `<span class="chip">${s}</span>`).join('');
    }
  } catch (err) {
    elements.pitchTextBox.innerText = 'Unable to generate collaboration pitch at this time.';
  }
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
