/* ==========================================================================
   CAMPUS CIRCLE AI — CLIENT CONTROLLER & ML VISUALIZATION ENGINE
   Reactive State Management, REST API Interfacing, Chart.js Integrations
   ========================================================================== */

let currentUser = {};
let activeChannel = "Aarav Sharma (Python Mentor)";
let currentSelectedItem = null;
let xaiChartInstance = null;
let modelChartInstance = null;

// ----------------- DOM READY ENTRY POINT -----------------
document.addEventListener("DOMContentLoaded", async () => {
  setupNavigation();
  setupRangeSliders();
  setupModals();

  // Load Initial API Data
  await loadUserProfile();
  await loadMarketplaceItems();
  await loadMentorsAndBarter();
  await loadBookings();
  await loadChatChannels();
  await loadReviews();
  await runPricePrediction();
  renderModelPerformanceChart();
  updateFinancialSimulator();
});

// ----------------- NAVIGATION & VIEW SWITCHING -----------------
function setupNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetView = item.getAttribute("data-view");
      switchView(targetView);
    });
  });
}

function switchView(viewId) {
  // Update sidebar active class
  document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
  const activeNav = document.querySelector(`.nav-item[data-view="${viewId}"]`);
  if (activeNav) activeNav.classList.add("active");

  // Update views
  document.querySelectorAll(".view-section").forEach(sec => sec.classList.remove("active"));
  const targetSec = document.getElementById(viewId);
  if (targetSec) targetSec.classList.add("active");

  // Re-render charts if entering ML views
  if (viewId === "view-sell" && xaiChartInstance) {
    xaiChartInstance.resize();
  }
  if (viewId === "view-ml" && modelChartInstance) {
    modelChartInstance.resize();
  }
}

// ----------------- USER PROFILE & VERIFICATION -----------------
async function loadUserProfile() {
  try {
    const res = await fetch("/api/user");
    currentUser = await res.json();
    renderUserWidgets();
  } catch (err) {
    console.error("Failed to load user profile:", err);
  }
}

function renderUserWidgets() {
  document.getElementById("widget-user-name").textContent = currentUser.name;
  document.getElementById("widget-user-branch").textContent = `${currentUser.branch} (Sem ${currentUser.semester})`;
  document.getElementById("widget-karma-badge").textContent = `🌱 ${currentUser.eco_credits} Karma`;
  
  const verifyBadge = document.getElementById("widget-verify-badge");
  const proBadge = document.getElementById("widget-pro-badge");

  if (currentUser.verified) {
    verifyBadge.textContent = "✅ ID Verified";
    verifyBadge.className = "badge badge-verified";
  } else {
    verifyBadge.textContent = "⚠️ Unverified";
    verifyBadge.className = "badge badge-karma";
  }

  proBadge.style.display = currentUser.is_pro ? "inline-flex" : "none";

  // Card inside View 2
  const cardName = document.getElementById("card-name");
  if (cardName) {
    cardName.textContent = currentUser.name;
    document.getElementById("card-email").textContent = currentUser.email;
    document.getElementById("card-roll").textContent = currentUser.roll_no;
    document.getElementById("card-branch").textContent = currentUser.branch;
    document.getElementById("card-sem").textContent = `Semester ${currentUser.semester}`;
    document.getElementById("card-badge-karma").textContent = `🌱 ${currentUser.eco_credits} Eco-Credits`;
    document.getElementById("card-badge-status").textContent = currentUser.verified ? "✅ Institutional Email Verified" : "⚠️ Email Verification Pending";
  }

  // Revenue Pro status box
  const proBox = document.getElementById("pro-status-box");
  if (proBox) {
    if (currentUser.is_pro) {
      proBox.innerHTML = `
        <div style="font-size:1.1rem; font-weight:800; color:#f59e0b; margin-bottom:4px;">🏆 CAMPUS PRO ACTIVE</div>
        <p style="font-size:0.86rem; color:#cbd5e1; margin:0;">Zero fees on all transactions, golden verified badge, and priority mentor placement.</p>
      `;
      document.getElementById("btn-toggle-pro").textContent = "Downgrade to Basic Student Tier";
    } else {
      proBox.innerHTML = `
        <div style="font-size:1.1rem; font-weight:800; color:#fff; margin-bottom:4px;">FREE BASIC STUDENT TIER</div>
        <p style="font-size:0.86rem; color:#94a3b8; margin:0;">Standard resource exchange and free skill barters. Upgrade for priority search visibility.</p>
      `;
      document.getElementById("btn-toggle-pro").textContent = "⚡ Upgrade to Campus Pro (₹49/sem)";
    }
  }
}

// Form edit user
document.getElementById("form-edit-user").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    name: document.getElementById("edit-name").value,
    email: document.getElementById("edit-email").value,
    roll_no: document.getElementById("edit-roll").value,
    branch: currentUser.branch,
    semester: parseInt(document.getElementById("edit-sem").value)
  };

  const res = await fetch("/api/user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  currentUser = data.user;
  renderUserWidgets();
  alert("✅ Profile updated successfully!");
});

// Verify OTP
document.getElementById("btn-verify-otp").addEventListener("click", async () => {
  const otpVal = document.getElementById("otp-input").value.trim();
  try {
    const res = await fetch("/api/user/verify-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ otp: otpVal })
    });
    if (!res.ok) {
      const err = await res.json();
      alert("❌ " + err.detail);
      return;
    }
    const data = await res.json();
    currentUser = data.user;
    renderUserWidgets();
    alert("🎉 " + data.message);
  } catch (e) {
    alert("Network error verifying OTP");
  }
});

// ----------------- MARKETPLACE MODULE -----------------
async function loadMarketplaceItems() {
  const search = document.getElementById("market-search").value;
  const category = document.getElementById("market-cat").value;
  const swapOnly = document.getElementById("market-swap-only").checked;

  const url = new URL("/api/items", window.location.origin);
  if (category && category !== "All Categories") url.searchParams.set("category", category);
  if (search) url.searchParams.set("search", search);
  if (swapOnly) url.searchParams.set("swap_only", "true");

  try {
    const res = await fetch(url);
    const items = await res.json();
    renderMarketplaceGrid(items);
  } catch (err) {
    console.error("Error loading marketplace items:", err);
  }
}

document.getElementById("market-search").addEventListener("input", debounce(loadMarketplaceItems, 300));
document.getElementById("market-cat").addEventListener("change", loadMarketplaceItems);
document.getElementById("market-swap-only").addEventListener("change", loadMarketplaceItems);

function renderMarketplaceGrid(items) {
  const container = document.getElementById("market-items-grid");
  container.innerHTML = "";

  if (items.length === 0) {
    container.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:40px; color:#64748b;">No campus items match your search filters. Try listing one!</div>`;
    return;
  }

  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div>
        <div class="item-header">
          <div class="item-title">${item.name}</div>
          <div class="item-price">₹${Math.round(item.fair_price)}</div>
        </div>
        <div class="item-meta">
          <span class="badge badge-karma">${item.category}</span>
          <span class="badge" style="background:rgba(245,158,11,0.15); color:#fbbf24;">⭐ ${item.condition}/5 Condition</span>
          <span class="badge" style="background:rgba(255,255,255,0.06); color:#cbd5e1;">Used ${item.age_sem} Sem</span>
          ${item.allow_swap ? '<span class="badge badge-verified">🔄 Swap Eligible</span>' : ''}
        </div>
        <div class="item-desc">${item.description}</div>
      </div>
      <div>
        <div class="item-seller">
          <strong>Seller:</strong> ${item.seller_name} (${item.seller_branch}) • MRP: <del>₹${Math.round(item.mrp)}</del>
        </div>
        <div class="item-actions">
          <button class="btn btn-emerald btn-sm" onclick="openBuyModal('${item.id}')" style="flex:1;">🛒 Buy Now</button>
          ${item.allow_swap ? `<button class="btn btn-secondary btn-sm" onclick="openSwapModal('${item.id}')" style="flex:1;">🔄 Swap</button>` : ''}
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// ----------------- FAIR PRICE REGRESSION & EXPLAINABLE AI -----------------
function setupRangeSliders() {
  const ageSlider = document.getElementById("sell-age");
  const condSlider = document.getElementById("sell-cond");
  const demandSlider = document.getElementById("sell-demand");

  ageSlider.addEventListener("input", (e) => {
    document.getElementById("sell-age-val").textContent = e.target.value;
    runPricePrediction();
  });
  condSlider.addEventListener("input", (e) => {
    document.getElementById("sell-cond-val").textContent = e.target.value;
    runPricePrediction();
  });
  demandSlider.addEventListener("input", (e) => {
    document.getElementById("sell-demand-val").textContent = e.target.value;
    runPricePrediction();
  });

  document.getElementById("sell-mrp").addEventListener("input", debounce(runPricePrediction, 400));
  document.getElementById("sell-cat").addEventListener("change", runPricePrediction);
  document.getElementById("btn-recalculate-ml").addEventListener("click", runPricePrediction);
}

async function runPricePrediction() {
  const category = document.getElementById("sell-cat").value;
  const mrp = parseFloat(document.getElementById("sell-mrp").value) || 1200;
  const age = parseInt(document.getElementById("sell-age").value) || 2;
  const cond = parseInt(document.getElementById("sell-cond").value) || 4;
  const demand = parseFloat(document.getElementById("sell-demand").value) || 0.85;

  try {
    const res = await fetch("/api/predict-price", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: category,
        original_mrp: mrp,
        age_semesters: age,
        condition_rating: cond,
        demand_index: demand
      })
    });
    const data = await res.json();
    const pred = data.prediction;
    const breakdown = data.attribution_breakdown;

    document.getElementById("val-fair-price").textContent = `₹${pred.suggested_fair_price}`;
    document.getElementById("val-deprec").textContent = `-${pred.depreciation_percent}% Deprec`;
    document.getElementById("val-savings").textContent = `₹${pred.student_saving_inr}`;
    document.getElementById("val-dt-baseline").textContent = `₹${pred.decision_tree_estimate}`;

    renderXaiChart(breakdown);
  } catch (err) {
    console.error("Error in ML price prediction:", err);
  }
}

function renderXaiChart(breakdown) {
  const ctx = document.getElementById("chart-xai");
  if (!ctx) return;

  const labels = Object.keys(breakdown);
  const values = Object.values(breakdown);
  const colors = values.map(v => v >= 0 ? "#10b981" : "#ef4444");

  if (xaiChartInstance) {
    xaiChartInstance.destroy();
  }

  xaiChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Attribution Impact (₹)",
        data: values,
        backgroundColor: colors,
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` Impact: ₹${ctx.raw}`
          }
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "#94a3b8" }
        },
        y: {
          grid: { display: false },
          ticks: { color: "#cbd5e1", font: { weight: "600", size: 11 } }
        }
      }
    }
  });
}

// Form publish item
document.getElementById("form-sell-item").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    name: document.getElementById("sell-title").value,
    category: document.getElementById("sell-cat").value,
    mrp: parseFloat(document.getElementById("sell-mrp").value),
    age_sem: parseInt(document.getElementById("sell-age").value),
    condition: parseInt(document.getElementById("sell-cond").value),
    demand_index: parseFloat(document.getElementById("sell-demand").value),
    allow_swap: document.getElementById("sell-swap").checked,
    description: document.getElementById("sell-desc").value
  };

  const res = await fetch("/api/items", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  await loadUserProfile();
  await loadMarketplaceItems();
  alert(`🎉 Item '${data.item.name}' published at fair valuation of ₹${data.item.fair_price}! +30 Eco-Credits awarded.`);
  switchView("view-marketplace");
});

// ----------------- SKILL HUB & 2-WAY BARTER -----------------
async function loadMentorsAndBarter() {
  const learn = document.getElementById("barter-learn-query").value;
  const teach = document.getElementById("barter-teach-query").value;

  try {
    const res = await fetch("/api/discover-skills", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ learn_query: learn, teach_query: teach, top_k: 4 })
    });
    const data = await res.json();
    renderMentorsFeed(data.matches);
  } catch (err) {
    console.error("Error discovering skills:", err);
  }
}

document.getElementById("btn-run-barter").addEventListener("click", loadMentorsAndBarter);

function renderMentorsFeed(mentors) {
  const container = document.getElementById("mentors-feed");
  container.innerHTML = "";

  mentors.forEach(m => {
    const card = document.createElement("div");
    card.className = "card-box";
    card.style.borderLeft = m.is_mutual_barter ? "5px solid #10b981" : "1px solid var(--border-subtle)";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <h4 style="color:#fff; margin-bottom:4px;">${m.name} <span style="font-size:0.8rem; color:#94a3b8;">(${m.mentor_id})</span></h4>
          <p style="font-size:0.82rem; color:#94a3b8; margin:0;">${m.branch} • Semester ${m.semester} • ⭐ ${m.rating}/5.0 (${m.total_sessions} sessions)</p>
        </div>
        <div style="display:flex; gap:6px; align-items:center;">
          ${m.is_mutual_barter ? '<span class="badge" style="background:#ecfdf5; color:#047857; font-weight:800;">🎉 2-Way Barter Match</span>' : ''}
          <span class="badge badge-karma" style="font-size:0.82rem; padding:4px 10px;">⚡ ${m.match_score_pct}% Match</span>
        </div>
      </div>
      <div style="margin:12px 0; font-size:0.9rem;">
        <div><strong>Offers:</strong> <span style="color:#38bdf8;">${m.skills_offered}</span></div>
        <div style="margin-top:4px;"><strong>Seeking:</strong> <span style="color:#f59e0b;">${m.skills_wanted}</span></div>
      </div>
      <p style="font-size:0.85rem; color:#cbd5e1; font-style:italic; margin-bottom:12px;">"${m.bio}"</p>
      <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-subtle); padding-top:10px;">
        <span style="font-weight:700; color:#fbbf24;">
          ${m.hourly_fee_inr === 0 || m.is_mutual_barter ? "FREE (Mutual Skill Barter 🔄)" : `₹${m.hourly_fee_inr}/hr`}
        </span>
        <button class="btn btn-primary btn-sm" onclick="quickBookMentor('${m.name}')">Book Session 📅</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function quickBookMentor(mentorName) {
  switchView("view-booking");
  const select = document.getElementById("book-mentor-select");
  for (let opt of select.options) {
    if (opt.value.includes(mentorName)) {
      opt.selected = true;
      break;
    }
  }
}

// Form register mentor
document.getElementById("form-register-mentor").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    skills_offered: document.getElementById("reg-skills-offered").value,
    skills_wanted: document.getElementById("reg-skills-wanted").value,
    hourly_fee_inr: parseFloat(document.getElementById("reg-hourly-fee").value) || 0,
    experience_years: parseFloat(document.getElementById("reg-exp-years").value) || 1.5,
    bio: document.getElementById("reg-bio").value
  };

  const res = await fetch("/api/mentors", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  await loadUserProfile();
  await loadMentorsAndBarter();
  alert(`🎉 Registered as peer mentor! +40 Eco-Credits awarded.`);
});

// ----------------- SESSION BOOKING MODULE -----------------
async function loadBookings() {
  try {
    const res = await fetch("/api/bookings");
    const bookings = await res.json();
    renderBookingsList(bookings);
  } catch (err) {
    console.error("Error loading bookings:", err);
  }
}

function renderBookingsList(bookings) {
  const container = document.getElementById("bookings-list");
  container.innerHTML = "";

  bookings.forEach(b => {
    const item = document.createElement("div");
    item.className = "card-box";
    item.style.padding = "16px";
    item.style.borderLeft = "4px solid #10b981";
    item.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4 style="color:#fff; margin:0;">${b.topic}</h4>
        <span class="badge badge-verified">${b.status}</span>
      </div>
      <div style="font-size:0.85rem; color:#94a3b8; margin:6px 0;">
        Mentor: <strong>${b.mentor_name}</strong> • ${b.date} • ${b.time_slot}
      </div>
      <div style="font-size:0.82rem; color:#cbd5e1;">📍 ${b.mode}</div>
      <div style="font-size:0.75rem; color:#64748b; margin-top:6px;">Booking Code: <code>${b.booking_id}</code> • Fee: ${b.fee}</div>
    `;
    container.appendChild(item);
  });
}

document.getElementById("form-book-session").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    mentor_name: document.getElementById("book-mentor-select").value.split(" (")[0],
    topic: document.getElementById("book-topic").value,
    date: document.getElementById("book-date").value,
    time_slot: document.getElementById("book-slot").value,
    mode: document.getElementById("book-mode").value,
    notes: document.getElementById("book-notes").value
  };

  const res = await fetch("/api/bookings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  await loadUserProfile();
  await loadBookings();
  alert(`🎉 Session booked with ${data.booking.mentor_name}! Booking Ref: ${data.booking.booking_id}. +25 Eco-Credits awarded.`);
});

// Set default date for booking
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
document.getElementById("book-date").value = tomorrow.toISOString().split("T")[0];

// ----------------- IN-APP CAMPUS CHAT -----------------
async function loadChatChannels() {
  try {
    const res = await fetch("/api/chat");
    const channels = await res.json();
    renderChatChannelsList(channels);
    renderActiveChannelMessages(channels[activeChannel] || []);
  } catch (err) {
    console.error("Error loading chat:", err);
  }
}

function renderChatChannelsList(channels) {
  const container = document.getElementById("chat-channels-list");
  container.innerHTML = "";

  Object.keys(channels).forEach(name => {
    const li = document.createElement("li");
    li.className = `chat-channel-item ${name === activeChannel ? "active" : ""}`;
    const msgs = channels[name];
    const lastMsg = msgs.length > 0 ? msgs[msgs.length - 1].text : "No messages yet";

    li.innerHTML = `
      <div class="chat-channel-name">${name}</div>
      <div class="chat-channel-preview">${lastMsg}</div>
    `;
    li.addEventListener("click", () => {
      activeChannel = name;
      document.querySelectorAll(".chat-channel-item").forEach(el => el.classList.remove("active"));
      li.classList.add("active");
      document.getElementById("active-channel-name").textContent = `💬 ${name}`;
      renderActiveChannelMessages(channels[name]);
    });
    container.appendChild(li);
  });
}

function renderActiveChannelMessages(messages) {
  const container = document.getElementById("chat-messages-container");
  container.innerHTML = "";

  messages.forEach(m => {
    const bubble = document.createElement("div");
    bubble.className = `bubble ${m.sender === "user" ? "bubble-user" : "bubble-other"}`;
    bubble.innerHTML = m.text.replace(/\n/g, "<br>");
    container.appendChild(bubble);
  });
  container.scrollTop = container.scrollHeight;
}

document.getElementById("form-chat-send").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("chat-text-input");
  const msgText = input.value.trim();
  if (!msgText) return;
  input.value = "";

  try {
    const res = await fetch("/api/chat/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ channel: activeChannel, message: msgText })
    });
    const data = await res.json();
    renderActiveChannelMessages(data.messages);
    loadChatChannels();
  } catch (err) {
    console.error("Error sending message:", err);
  }
});

// ----------------- RATINGS & REVIEWS -----------------
async function loadReviews() {
  try {
    const res = await fetch("/api/reviews");
    const reviews = await res.json();
    renderReviewsFeed(reviews);
  } catch (err) {
    console.error("Error loading reviews:", err);
  }
}

function renderReviewsFeed(reviews) {
  const container = document.getElementById("reviews-feed");
  container.innerHTML = "";

  reviews.forEach(r => {
    const card = document.createElement("div");
    card.className = "card-box";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4 style="color:#fff; margin:0;">${r.target}</h4>
        <span style="color:#fbbf24; font-weight:700;">${"⭐".repeat(r.rating)} (${r.rating}/5)</span>
      </div>
      <div style="font-size:0.78rem; color:#94a3b8; margin:4px 0;">
        <span class="badge badge-verified">Verified Transaction</span> • ${r.category} • by <strong>${r.reviewer}</strong> on ${r.date}
      </div>
      <p style="font-size:0.88rem; color:#cbd5e1; margin-top:8px;"><em>"${r.comment}"</em></p>
    `;
    container.appendChild(card);
  });
}

document.getElementById("form-submit-review").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    target: document.getElementById("review-target").value,
    category: document.getElementById("review-cat").value,
    rating: parseInt(document.getElementById("review-stars").value),
    comment: document.getElementById("review-comment").value
  };

  const res = await fetch("/api/reviews", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  await loadUserProfile();
  await loadReviews();
  document.getElementById("review-comment").value = "";
  alert("🎉 Thank you! Verified review posted! +15 Eco-Credits awarded.");
});

// ----------------- REVENUE MODEL & SIMULATOR -----------------
document.getElementById("btn-toggle-pro").addEventListener("click", async () => {
  const res = await fetch("/api/upgrade-pro", { method: "POST" });
  const data = await res.json();
  currentUser.is_pro = data.is_pro;
  renderUserWidgets();
});

function updateFinancialSimulator() {
  const stu = parseInt(document.getElementById("sim-stu").value);
  const proRate = parseInt(document.getElementById("sim-pro").value);
  const swaps = parseInt(document.getElementById("sim-swaps").value);

  document.getElementById("sim-stu-val").textContent = stu;
  document.getElementById("sim-pro-val").textContent = proRate;
  document.getElementById("sim-swaps-val").textContent = swaps;

  const proSubscribers = Math.round(stu * (proRate / 100));
  const proRev = proSubscribers * 49 * 2; // 2 semesters
  const totalTrades = stu * swaps;
  const commRev = Math.round(totalTrades * 0.4 * 600 * 0.02);
  const totalRev = proRev + commRev;
  const totalSavings = totalTrades * 480;
  const wasteKg = Math.round(totalTrades * 1.85);

  document.getElementById("sim-rev-val").textContent = `₹${totalRev.toLocaleString()}`;
  document.getElementById("sim-sav-val").textContent = `₹${totalSavings.toLocaleString()}`;
  document.getElementById("sim-waste-val").textContent = `${wasteKg.toLocaleString()} kg`;
}

document.getElementById("sim-stu").addEventListener("input", updateFinancialSimulator);
document.getElementById("sim-pro").addEventListener("input", updateFinancialSimulator);
document.getElementById("sim-swaps").addEventListener("input", updateFinancialSimulator);

// ----------------- ML PERFORMANCE CHART -----------------
function renderModelPerformanceChart() {
  const ctx = document.getElementById("chart-models");
  if (!ctx) return;

  modelChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Decision Tree Baseline", "Random Forest Regressor"],
      datasets: [{
        label: "R² Goodness of Fit",
        data: [0.9133, 0.9527],
        backgroundColor: ["#f59e0b", "#10b981"],
        borderRadius: 8,
        barThickness: 34
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          min: 0.85,
          max: 1.0,
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "#94a3b8" }
        },
        y: {
          grid: { display: false },
          ticks: { color: "#fff", font: { weight: "700", size: 12 } }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` R² Score: ${(ctx.raw * 100).toFixed(2)}%`
          }
        }
      }
    }
  });
}

// ----------------- MODALS -----------------
function setupModals() {
  document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("active");
      }
    });
  });
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

function openBuyModal(itemId) {
  fetch(`/api/items?search=${itemId}`)
    .then(res => res.json())
    .then(items => {
      const item = items[0];
      if (!item) return;
      currentSelectedItem = item;
      document.getElementById("buy-modal-details").innerHTML = `
        <div style="background:rgba(255,255,255,0.04); padding:14px; border-radius:8px; border:1px solid var(--border-subtle);">
          <div style="font-weight:700; color:#fff; font-size:1.05rem;">${item.name}</div>
          <div style="color:#34d399; font-weight:800; font-size:1.3rem; margin:6px 0;">₹${Math.round(item.fair_price)}</div>
          <div style="font-size:0.84rem; color:#94a3b8;">Seller: ${item.seller_name} (${item.seller_email})</div>
        </div>
      `;
      openModal("modal-buy");
    });
}

document.getElementById("btn-confirm-buy").addEventListener("click", async () => {
  if (!currentSelectedItem) return;
  const pickup = document.getElementById("buy-pickup-select").value;
  const res = await fetch(`/api/items/${currentSelectedItem.id}/buy`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pickup_point: pickup })
  });
  const data = await res.json();
  closeModal("modal-buy");
  await loadUserProfile();
  alert(`🎉 ${data.message} Reference: ${data.order_reference}`);
});

function openSwapModal(itemId) {
  fetch(`/api/items?search=${itemId}`)
    .then(res => res.json())
    .then(items => {
      const item = items[0];
      if (!item) return;
      currentSelectedItem = item;
      document.getElementById("swap-modal-details").innerHTML = `
        <div style="background:rgba(255,255,255,0.04); padding:12px; border-radius:8px;">
          <div style="font-weight:700; color:#fff;">Target Item: ${item.name}</div>
          <div style="font-size:0.85rem; color:#94a3b8;">Owner: ${item.seller_name}</div>
        </div>
      `;
      openModal("modal-swap");
    });
}

document.getElementById("btn-confirm-swap").addEventListener("click", async () => {
  if (!currentSelectedItem) return;
  const offer = document.getElementById("swap-offer-input").value;
  const res = await fetch(`/api/items/${currentSelectedItem.id}/swap`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ swap_offer: offer })
  });
  const data = await res.json();
  closeModal("modal-swap");
  alert(`📩 ${data.message}`);
});

// Helper debounce
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
