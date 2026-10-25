# DevOn Matchmaking Algorithm Specification

DevOn uses a multi-factor mathematical compatibility scoring model to evaluate the pairing potential between two software engineers.

---

## 1. Overall Compatibility Formula

The final overall compatibility score $S_{total} \in [0, 100]$ is a linear combination of four weighted sub-scores:

$$S_{total} = w_{skill} \cdot S_{skill} + w_{sched} \cdot S_{sched} + w_{domain} \cdot S_{domain} + w_{exp} \cdot S_{exp}$$

Where default weights configured in `backend/core/config.py` are:
- $w_{skill} = 0.40$ (Skill Complementarity or Similarity)
- $w_{sched} = 0.25$ (Schedule & Timezone Overlap)
- $w_{domain} = 0.20$ (Domain Interests & Semantic Vector Similarity)
- $w_{exp} = 0.15$ (Experience Tier Synergy)

$$\sum w_i = 1.00$$

---

## 2. Factor Breakdown

### 2.1 Skill Compatibility ($S_{skill}$)
Depending on the requested `PairingMode`:
- **Complementary Mode (Default)**: Evaluates cross-stack synergy using the Role Synergy Matrix $M_{role}$.
  - Backend + Frontend: $96.0$
  - Backend + AI/ML: $92.0$
  - Backend + DevOps: $94.0$
  - Backend + Mobile: $90.0$
  - Backend + Systems: $86.0$
  A $+4.0$ bonus is awarded if developers share at least one common language (e.g., both know Python or TypeScript) to guarantee smooth communication.
- **Similar Mode**: Rewards identical primary roles and maximum Jaccard index on skill tags:
  $$J(A, B) = \frac{|T_A \cap T_B|}{|T_A \cup T_B|}$$
  $$S_{skill} = 85.0 + 15.0 \cdot J(A, B)$$

### 2.2 Schedule & Timezone Overlap ($S_{sched}$)
Evaluates circadian rhythm alignment and timezone offset:
$$S_{rhythm} = \max(40.0, 100.0 - 60.0 \cdot |\text{night\_owl}_A - \text{night\_owl}_B|)$$
$$S_{tz} = \begin{cases} 
100.0 & \text{if } |\Delta TZ| \le 2\text{h} \\ 
82.0 & \text{if } 2\text{h} < |\Delta TZ| \le 5\text{h} \\ 
65.0 & \text{if } 5\text{h} < |\Delta TZ| \le 8\text{h} \\ 
45.0 & \text{otherwise} 
\end{cases}$$
$$S_{sched} = 0.60 \cdot S_{rhythm} + 0.40 \cdot S_{tz}$$

### 2.3 Domain Interests & Vector Similarity ($S_{domain}$)
Combines topic intersection with dense 128-dimensional cosine vector similarity:
$$\text{CosSim}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \cdot \|\vec{v}\|_2}$$
$$S_{domain} = 0.50 \cdot (65.0 + 35.0 \cdot J(D_A, D_B)) + 0.50 \cdot (\text{CosSim} \cdot 100.0)$$

### 2.4 Experience Tier Synergy ($S_{exp}$)
- **Peer Learning**: Penalizes large gaps in experience tier to ensure balanced co-discovery.
- **Mentorship Mode**: Rewards a gap of 1–2 tiers where a Senior or Staff engineer mentors an Intermediate or Junior developer.
- **Balanced (Default)**: Ideal for collaboration with mutual respect and rapid delivery ($92.0$ for adjacent tiers).

---

## 3. Explanations & Transparency
DevOn produces human-readable `synergy_reasons` for every computed score so developers understand *why* they were matched and how to start their first pair session effectively.
