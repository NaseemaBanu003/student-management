const state = {
  token: localStorage.getItem('access_token') || '',
  user: JSON.parse(localStorage.getItem('user') || 'null'),
};

const authCard = document.getElementById('authCard');
const dashboardSection = document.getElementById('dashboardSection');
const sidebar = document.getElementById('sidebar');
const userChip = document.getElementById('userChip');
const loginForm = document.getElementById('loginForm');
const logoutButton = document.getElementById('logoutButton');
const statsGrid = document.getElementById('statsGrid');
const activityTableBody = document.getElementById('activityTableBody');
const toast = document.getElementById('toast');

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2400);
}

function setAuthVisibility() {
  const loggedIn = !!state.token;
  authCard.classList.toggle('hidden', loggedIn);
  dashboardSection.classList.toggle('hidden', !loggedIn);
  sidebar.classList.toggle('hidden', !loggedIn);
  userChip.textContent = state.user ? `${state.user.first_name || 'User'} ${state.user.last_name || ''}`.trim() : 'Guest';
}

async function apiRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }

  const response = await fetch(`/api${path}`, {
    ...options,
    headers,
  });

  const result = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(result.message || 'Request failed');
  }
  return result;
}

async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const result = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    state.token = result.data.access_token;
    state.user = result.data.user;
    localStorage.setItem('access_token', state.token);
    localStorage.setItem('user', JSON.stringify(state.user));
    setAuthVisibility();
    await loadDashboard();
    showToast('Login successful');
  } catch (error) {
    showToast(error.message);
  }
}

async function loadDashboard() {
  try {
    const response = await apiRequest('/dashboard/admin');
    const data = response.data || {};
    const stats = [
      { label: 'Students', value: data.total_students || 0 },
      { label: 'Active Students', value: data.active_students || 0 },
      { label: 'Faculty', value: data.total_faculty || 0 },
      { label: 'Departments', value: data.departments || 0 },
      { label: 'Courses', value: data.courses || 0 },
      { label: 'Pending Fees', value: data.pending_fees || 0 },
    ];

    statsGrid.innerHTML = stats.map((item) => `
      <div class="stat-card">
        <div class="stat-label">${item.label}</div>
        <div class="stat-value">${item.value}</div>
      </div>
    `).join('');

    const activityItems = [{ action: 'System updated', user: 'Admin', timestamp: 'Today' }, { action: 'Attendance synced', user: 'Faculty', timestamp: 'Today' }];
    activityTableBody.innerHTML = activityItems.map((item) => `
      <tr>
        <td>${item.action}</td>
        <td>${item.user}</td>
        <td>${item.timestamp}</td>
      </tr>
    `).join('');
  } catch (error) {
    showToast(error.message);
  }
}

async function handleLogout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
  state.token = '';
  state.user = null;
  setAuthVisibility();
  showToast('Logged out');
}

loginForm.addEventListener('submit', handleLogin);
logoutButton.addEventListener('click', handleLogout);
document.getElementById('menuToggle').addEventListener('click', () => {
  sidebar.classList.toggle('visible');
});
setAuthVisibility();
if (state.token) {
  loadDashboard();
}
