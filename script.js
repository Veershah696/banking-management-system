const API_BASE = (window.location.origin.includes('file') || window.location.origin === "null") 
    ? "http://127.0.0.1:5000" 
    : window.location.origin;

// 1. Health Check
async function checkHealth() {
    const indicator = document.getElementById("health-indicator");
    if (!indicator) return;
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        const data = await res.json();
        indicator.innerText = data.success ? "✅ Connected" : "❌ " + data.message;
        indicator.style.color = data.success ? "white" : "#ff4444";
    } catch (e) {
        indicator.innerText = "❌ Backend NOT Running";
        indicator.style.color = "#ff4444";
    }
}

if (document.getElementById("health-indicator")) setInterval(checkHealth, 3000);

// 2. Login
async function login() {
    const u = document.getElementById("username").value;
    const p = document.getElementById("password").value;
    const err = document.getElementById("error");

    try {
        const res = await fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: u, password: p })
        });
        
        if (!res.ok) {
            const data = await res.json();
            err.innerText = data.message || "Database Error";
            return;
        }

        const data = await res.json();
        if (data.success) window.location.href = "dashboard.html";
        else err.innerText = data.message;
    } catch (e) {
        console.error(e);
        err.innerText = "Connection Error: Is 'python app.py' running at " + API_BASE + "?";
    }
}

// 3. Register
async function register() {
    const u = document.getElementById("reg-username").value;
    const p = document.getElementById("reg-password").value;
    const msg = document.getElementById("reg-message");

    try {
        const res = await fetch(`${API_BASE}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: u, password: p })
        });
        const data = await res.json();
        msg.innerText = data.message;
        msg.style.color = data.success ? "green" : "red";
        if (data.success) setTimeout(() => window.location.href = "login.html", 1500);
    } catch (e) {
        msg.innerText = "Connection Error: Is 'python app.py' running?";
        msg.style.color = "red";
    }
}

// 4. Load Accounts
async function loadData() {
    const table = document.getElementById("tableBody");
    try {
        const res = await fetch(`${API_BASE}/api/accounts`);
        const data = await res.json();
        if (data.success) {
            table.innerHTML = data.accounts.map(acc => `
                <tr>
                    <td>${acc.name}</td>
                    <td>${acc.acc_no}</td>
                    <td>₹${acc.balance}</td>
                    <td>
                        <button class="btn-edit" onclick="showModal('edit', '${acc.acc_no}', '${acc.name}', '${acc.balance}')">Edit</button>
                        <button class="btn-delete" onclick="deleteAccount('${acc.acc_no}')">Delete</button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (e) {
        table.innerHTML = "<tr><td colspan='4'>Error: Backend not reachable.</td></tr>";
    }
}

// 5. Add/Edit Modal
function showModal(type, accNo = '', name = '', balance = '') {
    const modal = document.getElementById("accountModal");
    document.getElementById("modalTitle").innerText = type === 'add' ? "Add New Account" : "Edit Account";
    document.getElementById("accNo").value = accNo;
    document.getElementById("accNo").disabled = type === 'edit';
    document.getElementById("accName").value = name;
    document.getElementById("accBalance").value = balance;
    document.getElementById("saveBtn").onclick = () => saveAccount(type);
    modal.style.display = "block";
}

function closeModal() { document.getElementById("accountModal").style.display = "none"; }

async function saveAccount(type) {
    const url = type === 'add' ? '/api/accounts/add' : '/api/accounts/update';
    const payload = {
        acc_no: document.getElementById("accNo").value,
        name: document.getElementById("accName").value,
        balance: document.getElementById("accBalance").value
    };

    try {
        const res = await fetch(API_BASE + url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        alert(data.message);
        if (data.success) { closeModal(); loadData(); }
    } catch (e) { alert("Server Error"); }
}

async function deleteAccount(accNo) {
    if (!confirm("Are you sure?")) return;
    try {
        const res = await fetch(`${API_BASE}/api/accounts/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ acc_no: accNo })
        });
        const data = await res.json();
        alert(data.message);
        if (data.success) loadData();
    } catch (e) { alert("Server Error"); }
}

function searchData() {
    let input = document.getElementById("search").value.toLowerCase();
    let rows = document.querySelectorAll("tbody tr");
    rows.forEach(row => {
        let name = row.children[0].innerText.toLowerCase();
        row.style.display = name.includes(input) ? "" : "none";
    });
}
function logout() { window.location.href = "login.html"; }
