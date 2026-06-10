import { useState } from "react";

const API = "http://localhost:5000";

const C = {
  bg: "#F7F8FA", surface: "#FFFFFF", border: "#E4E7EC",
  primary: "#2D5BE3", primaryLight: "#EEF2FF",
  success: "#16A34A", successLight: "#DCFCE7",
  error: "#DC2626", errorLight: "#FEE2E2",
  warning: "#D97706", warningLight: "#FEF3C7",
  text: "#111827", textMuted: "#6B7280", textLight: "#9CA3AF",
  adminAccent: "#7C3AED", adminLight: "#EDE9FE",
};

const s = {
  page: { minHeight: "100vh", background: C.bg, fontFamily: "'Inter','Segoe UI',sans-serif", color: C.text },
  nav: { background: C.surface, borderBottom: `1px solid ${C.border}`, padding: "0 32px", display: "flex", alignItems: "center", gap: 24, height: 56, position: "sticky", top: 0, zIndex: 100 },
  navBrand: { fontWeight: 700, fontSize: 17, letterSpacing: "-0.3px", marginRight: "auto" },
  navTab: (a) => ({ padding: "0 4px", height: 56, display: "flex", alignItems: "center", borderBottom: a ? `2px solid ${C.primary}` : "2px solid transparent", color: a ? C.primary : C.textMuted, fontWeight: a ? 600 : 400, fontSize: 14, cursor: "pointer", background: "none", border: "none", borderBottom: a ? `2px solid ${C.primary}` : "2px solid transparent" }),
  navRole: (role) => ({ padding: "4px 12px", borderRadius: 99, fontSize: 12, fontWeight: 600, background: role === "admin" ? C.adminLight : C.primaryLight, color: role === "admin" ? C.adminAccent : C.primary }),
  container: { maxWidth: 900, margin: "0 auto", padding: "32px 24px" },
  card: { background: C.surface, border: `1px solid ${C.border}`, borderRadius: 10, padding: 20, marginBottom: 12 },
  row: { display: "flex", gap: 12, alignItems: "flex-end", flexWrap: "wrap", marginBottom: 20 },
  label: { display: "block", fontSize: 13, fontWeight: 500, color: C.textMuted, marginBottom: 5 },
  input: { border: `1px solid ${C.border}`, borderRadius: 7, padding: "9px 12px", fontSize: 14, outline: "none", width: "100%", boxSizing: "border-box", color: C.text, background: C.surface },
  btn: (v = "primary") => ({ padding: "9px 18px", borderRadius: 7, fontSize: 14, fontWeight: 500, cursor: "pointer", transition: "opacity 0.15s", background: v === "primary" ? C.primary : v === "danger" ? C.error : v === "success" ? C.success : v === "admin" ? C.adminAccent : C.surface, color: v === "ghost" ? C.textMuted : "#fff", border: v === "ghost" ? `1px solid ${C.border}` : "none" }),
  badge: (color) => ({ display: "inline-flex", alignItems: "center", padding: "3px 10px", borderRadius: 99, fontSize: 12, fontWeight: 600, background: color === "green" ? C.successLight : color === "red" ? C.errorLight : C.warningLight, color: color === "green" ? C.success : color === "red" ? C.error : C.warning }),
  alert: (t) => ({ padding: "12px 16px", borderRadius: 8, fontSize: 14, marginBottom: 16, background: t === "error" ? C.errorLight : t === "success" ? C.successLight : C.warningLight, color: t === "error" ? C.error : t === "success" ? C.success : C.warning }),
  sectionTitle: { fontSize: 18, fontWeight: 700, marginBottom: 4, letterSpacing: "-0.2px" },
  sectionSub: { fontSize: 14, color: C.textMuted, marginBottom: 20 },
  fieldGroup: { flex: 1, minWidth: 140 },
  textarea: { border: `1px solid ${C.border}`, borderRadius: 7, padding: "9px 12px", fontSize: 14, outline: "none", width: "100%", boxSizing: "border-box", color: C.text, resize: "vertical", minHeight: 80 },
  divider: { border: "none", borderTop: `1px solid ${C.border}`, margin: "20px 0" },
  empty: { textAlign: "center", padding: "48px 24px", color: C.textMuted, fontSize: 14 },
  roomGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))", gap: 12 },
  spinner: { display: "inline-block", width: 16, height: 16, border: `2px solid rgba(255,255,255,0.4)`, borderTop: "2px solid #fff", borderRadius: "50%", animation: "spin 0.7s linear infinite", verticalAlign: "middle" },
};

const Badge = ({ status }) => {
  const color = status === "Accepted" ? "green" : status === "Rejected" ? "red" : "yellow";
  return <span style={s.badge(color)}>{status}</span>;
};
const Alert = ({ msg, type }) => msg ? <div style={s.alert(type)}>{msg}</div> : null;
const Spinner = () => <><style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style><span style={s.spinner} /></>;

// ─── LOGIN PAGE ───────────────────────────────────────────────────
function LoginPage({ onLogin }) {
  const [mode, setMode] = useState(null);
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!id || !password) return setError("Both fields are required.");
    setLoading(true); setError(null);
    try {
      const body = mode === "student"
        ? { student_id: parseInt(id), student_password: password }
        : { admin_id: parseInt(id), admin_password: password };

      const res = await fetch(`${API}/${mode}/login`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        onLogin(mode, parseInt(id));
      } else {
        const data = await res.json();
        setError(data.message || "Invalid credentials.");
      }
    } catch { setError("Network error."); }
    finally { setLoading(false); }
  };

  if (!mode) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: C.bg }}>
        <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
        <div style={{ textAlign: "center", maxWidth: 400, padding: 32 }}>
          <div style={{ fontSize: 28, fontWeight: 800, letterSpacing: "-0.5px", marginBottom: 8 }}>UniResidences</div>
          <p style={{ color: C.textMuted, fontSize: 15, marginBottom: 40 }}>University housing management system</p>
          <div style={{ display: "flex", gap: 16, justifyContent: "center" }}>
            <button style={{ ...s.btn("primary"), padding: "14px 32px", fontSize: 15, borderRadius: 10 }} onClick={() => setMode("student")}>Student Login</button>
            <button style={{ ...s.btn("admin"), padding: "14px 32px", fontSize: 15, borderRadius: 10 }} onClick={() => setMode("admin")}>Admin Login</button>
          </div>
        </div>
      </div>
    );
  }

  const isAdmin = mode === "admin";

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: C.bg }}>
      <div style={{ ...s.card, width: "100%", maxWidth: 380, padding: 32 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 24 }}>
          <button style={{ ...s.btn("ghost"), padding: "4px 10px", fontSize: 12 }} onClick={() => { setMode(null); setError(null); setId(""); setPassword(""); }}>← Back</button>
          <span style={s.navRole(mode)}>{isAdmin ? "Admin" : "Student"}</span>
        </div>
        <p style={{ ...s.sectionTitle, marginBottom: 4 }}>{isAdmin ? "Admin Login" : "Student Login"}</p>
        <p style={{ ...s.sectionSub, marginBottom: 20 }}>{isAdmin ? "Access the administration panel." : "Access your housing portal."}</p>
        <Alert msg={error} type="error" />
        <div style={{ marginBottom: 14 }}>
          <label style={s.label}>{isAdmin ? "Admin ID" : "Student ID"}</label>
          <input style={s.input} type="number" placeholder="e.g. 1" value={id} onChange={e => setId(e.target.value)} onKeyDown={e => e.key === "Enter" && handleLogin()} />
        </div>
        <div style={{ marginBottom: 20 }}>
          <label style={s.label}>Password</label>
          <input style={s.input} type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key === "Enter" && handleLogin()} />
        </div>
        <button style={{ ...s.btn(isAdmin ? "admin" : "primary"), width: "100%", padding: "11px" }} onClick={handleLogin} disabled={loading}>
          {loading ? <Spinner /> : "Sign in"}
        </button>
      </div>
    </div>
  );
}

// ─── STUDENT APP ──────────────────────────────────────────────────
function StudentApp({ studentId, onLogout }) {
  const [tab, setTab] = useState("rooms");
  const tabs = [
    { id: "rooms", label: "Browse Rooms" },
    { id: "apply", label: "Apply" },
    { id: "my-applications", label: "My Applications" },
    { id: "status", label: "Check Status" },
  ];

  const handleLogout = async () => {
    await fetch(`${API}/student/logout`, { method: "POST", credentials: "include" });
    onLogout();
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}>
        <span style={s.navBrand}>UniResidences</span>
        {tabs.map(t => <button key={t.id} style={s.navTab(tab === t.id)} onClick={() => setTab(t.id)}>{t.label}</button>)}
        <span style={s.navRole("student")}>Student #{studentId}</span>
        <button style={{ ...s.btn("ghost"), fontSize: 13 }} onClick={handleLogout}>Sign out</button>
      </nav>
      <div style={s.container}>
        {tab === "rooms" && <BrowseRooms />}
        {tab === "apply" && <ApplyForRoom studentId={studentId} />}
        {tab === "my-applications" && <MyApplications studentId={studentId} />}
        {tab === "status" && <CheckStatus studentId={studentId} />}
      </div>
    </div>
  );
}

function BrowseRooms() {
  const [minBudget, setMinBudget] = useState("");
  const [maxBudget, setMaxBudget] = useState("");
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [detail, setDetail] = useState({});

  const search = async () => {
    setLoading(true); setSearched(true);
    const params = new URLSearchParams();
    if (minBudget) params.append("min_budget", minBudget);
    if (maxBudget) params.append("max_budget", maxBudget);
    try {
      const res = await fetch(`${API}/student/rooms/available?${params}`, { credentials: "include" });
      const ids = await res.json();
      setRooms(Array.isArray(ids) ? ids : []);
    } catch { setRooms([]); } finally { setLoading(false); }
  };

  const fetchDetail = async (id) => {
    if (detail[id]) return;
    try {
      const res = await fetch(`${API}/student/rooms/description?room_id=${id}`, { credentials: "include" });
      const data = await res.json();
      setDetail(d => ({ ...d, [id]: data.description }));
    } catch {}
  };

  return (
    <div>
      <p style={s.sectionTitle}>Available Rooms</p>
      <p style={s.sectionSub}>Filter by rent budget to find matching rooms.</p>
      <div style={s.row}>
        <div style={s.fieldGroup}><label style={s.label}>Min rent (€)</label><input style={s.input} type="number" placeholder="0" value={minBudget} onChange={e => setMinBudget(e.target.value)} /></div>
        <div style={s.fieldGroup}><label style={s.label}>Max rent (€)</label><input style={s.input} type="number" placeholder="No limit" value={maxBudget} onChange={e => setMaxBudget(e.target.value)} /></div>
        <button style={s.btn("primary")} onClick={search}>Search</button>
      </div>
      {loading && <div style={{ textAlign: "center", padding: 32 }}><span style={{ ...s.spinner, borderTopColor: C.primary, borderColor: C.border }} /></div>}
      {!loading && searched && rooms.length === 0 && <div style={s.empty}>No rooms found for this budget range.</div>}
      {!loading && rooms.length > 0 && (
        <div style={s.roomGrid}>
          {rooms.map(id => (
            <div key={id} style={s.card}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <span style={{ fontWeight: 600 }}>Room {id}</span>
                <span style={s.badge("green")}>Available</span>
              </div>
              <p>ID for application : <strong>{id}</strong></p>
              {detail[id]
                ? <p style={{ fontSize: 13, color: C.textMuted, margin: 0 }}>{detail[id]}</p>
                : <button style={{ ...s.btn("ghost"), fontSize: 12, padding: "5px 10px" }} onClick={() => fetchDetail(id)}>View description</button>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function ApplyForRoom({ studentId }) {
  const [roomId, setRoomId] = useState("");
  const [message, setMessage] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!roomId) return setFeedback({ type: "error", msg: "Room ID is required." });
    if (!message) return setFeedback({ type: "error", msg: "Application message is required." });
    setLoading(true); setFeedback(null);
    try {
      const res = await fetch(`${API}/student/rooms/apply?room_id=${roomId}&student_id=${studentId}`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ application_message: message }),
      });
      const data = await res.json();
      setFeedback({ type: res.ok ? "success" : "error", msg: data.message });
      if (res.ok) { setRoomId(""); setMessage(""); }
    } catch (error) { setFeedback({ type: "error", msg: error.message }); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ maxWidth: 480 }}>
      <p style={s.sectionTitle}>Apply for a Room</p>
      <p style={s.sectionSub}>Submit an application for an available room.</p>
      <Alert msg={feedback?.msg} type={feedback?.type} />
      <div style={{ marginBottom: 14 }}><label style={s.label}>Room ID</label><input style={s.input} type="number" placeholder="e.g. 3" value={roomId} onChange={e => setRoomId(e.target.value)} /></div>
      <div style={{ marginBottom: 16 }}><label style={s.label}>Message</label><textarea style={s.textarea} placeholder="Briefly explain why you'd like this room..." value={message} onChange={e => setMessage(e.target.value)} /></div>
      <button style={s.btn("primary")} onClick={submit} disabled={loading}>{loading ? <Spinner /> : "Submit Application"}</button>
    </div>
  );
}

function MyApplications({ studentId }) {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true); setError(null); setFetched(true);
    try {
      const res = await fetch(`${API}/student/applications/all?student_id=${studentId}`, { credentials: "include" });
      const data = await res.json();
      if (!res.ok) return setError(data.message);
      setApps(data.applicationDetails || []);
    } catch { setError("Network error."); } finally { setLoading(false); }
  };

  return (
    <div>
      <p style={s.sectionTitle}>My Applications</p>
      <p style={s.sectionSub}>All your submitted applications, newest first.</p>
      <Alert msg={error} type="error" />
      <button style={{ ...s.btn("primary"), marginBottom: 16 }} onClick={load}>Load Applications</button>
      {loading && <div style={{ textAlign: "center", padding: 32 }}><span style={{ ...s.spinner, borderTopColor: C.primary, borderColor: C.border }} /></div>}
      {!loading && fetched && apps.length === 0 && !error && <div style={s.empty}>No applications found.</div>}
      {!loading && apps.map(([submission_date, id, room_description, roomId]) => (
  <div 
    key={id} 
    style={{ 
      ...s.card, 
      display: "flex", 
      flexDirection: "column", // Changed to column so details stack nicely
      gap: "4px",
      marginBottom: "12px" 
    }}
  >
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <span style={{ fontWeight: 600 }}>Application #{id}</span>
      
    </div>
    
    <div style={{ fontSize: 14, color: C.textDim, marginTop: 4 }}>
      <p style={{ margin: 0}}> <strong>/Application Id:</strong> {id}</p>
      <p style={{ margin: 0}}> <strong>Room Id:</strong> {roomId}</p>
      <p style={{ margin: 0 }}><strong>Room description:</strong> {room_description}</p>
      <p style={{ margin: 0 }}><strong>Submission date:</strong> {submission_date}</p>
    </div>
  </div>
))}
    </div>
  );
}

function CheckStatus({ studentId }) {
  const [applicationId, setApplicationId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const check = async () => {
    if (!applicationId) return setError("Application ID is required.");
    setLoading(true); setError(null); setResult(null);
    try {
      const res = await fetch(`${API}/student/application/status?student_id=${studentId}&application_id=${applicationId}`, { credentials: "include" });
      const data = await res.json();
      if (!res.ok) return setError(data.message);
      setResult(data.status);
    } catch { setError("Network error."); } finally { setLoading(false); }
  };

  return (
    <div style={{ maxWidth: 400 }}>
      <p style={s.sectionTitle}>Application Status</p>
      <p style={s.sectionSub}>Check the current status of a specific application.</p>
      <Alert msg={error} type="error" />
      <div style={{ marginBottom: 14 }}><label style={s.label}>Application ID</label><input style={s.input} type="number" placeholder="e.g. 1" value={applicationId} onChange={e => setApplicationId(e.target.value)} /></div>
      <button style={s.btn("primary")} onClick={check} disabled={loading}>{loading ? <Spinner /> : "Check Status"}</button>
      {result && (
        <div style={{ ...s.card, marginTop: 16, display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontSize: 14, color: C.textMuted }}>Status:</span>
          <Badge status={result} />
        </div>
      )}
    </div>
  );
}

// ─── ADMIN APP ────────────────────────────────────────────────────
function AdminApp({ adminId, onLogout }) {
  const [tab, setTab] = useState("rooms");
  const tabs = [
    { id: "rooms", label: "All Rooms" },
    { id: "pending", label: "Pending Applications" },
    { id: "details", label: "Application Details" },
  ];

  const handleLogout = async () => {
    await fetch(`${API}/admin/logout`, { method: "POST", credentials: "include" });
    onLogout();
  };

  return (
    <div style={s.page}>
      <nav style={s.nav}>
        <span style={s.navBrand}>UniResidences</span>
        {tabs.map(t => <button key={t.id} style={s.navTab(tab === t.id)} onClick={() => setTab(t.id)}>{t.label}</button>)}
        <span style={s.navRole("admin")}>Admin #{adminId}</span>
        <button style={{ ...s.btn("ghost"), fontSize: 13 }} onClick={handleLogout}>Sign out</button>
      </nav>
      <div style={s.container}>
        {tab === "rooms" && <AdminRooms />}
        {tab === "pending" && <PendingApplications adminId={adminId} />}
        {tab === "details" && <ApplicationDetails />}
      </div>
    </div>
  );
}

function AdminRooms() {
  const [availability, setAvailability] = useState("");
  const [minBudget, setMinBudget] = useState("");
  const [maxBudget, setMaxBudget] = useState("");
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const search = async () => {
    setLoading(true); setSearched(true);
    const params = new URLSearchParams();
    if (availability !== "") params.append("availability", availability);
    if (minBudget) params.append("min_budget", minBudget);
    if (maxBudget) params.append("max_budget", maxBudget);
    try {
      const res = await fetch(`${API}/admin/rooms/all?${params}`, { credentials: "include" });
      const ids = await res.json();
      setRooms(Array.isArray(ids) ? ids : []);
    } catch { setRooms([]); } finally { setLoading(false); }
  };

  return (
    <div>
      <p style={s.sectionTitle}>Room Overview</p>
      <p style={s.sectionSub}>Filter rooms by availability and rent.</p>
      <div style={s.row}>
        <div style={s.fieldGroup}><label style={s.label}>Availability</label>
          <select style={s.input} value={availability} onChange={e => setAvailability(e.target.value)}>
            <option value="">All</option><option value="true">Available</option><option value="false">Occupied</option>
          </select>
        </div>
        <div style={s.fieldGroup}><label style={s.label}>Min rent (€)</label><input style={s.input} type="number" placeholder="0" value={minBudget} onChange={e => setMinBudget(e.target.value)} /></div>
        <div style={s.fieldGroup}><label style={s.label}>Max rent (€)</label><input style={s.input} type="number" placeholder="No limit" value={maxBudget} onChange={e => setMaxBudget(e.target.value)} /></div>
        <button style={s.btn("primary")} onClick={search}>Search</button>
      </div>
      {loading && <div style={{ textAlign: "center", padding: 32 }}><span style={{ ...s.spinner, borderTopColor: C.primary, borderColor: C.border }} /></div>}
      {!loading && searched && rooms.length === 0 && <div style={s.empty}>No rooms match these filters.</div>}
      {!loading && rooms.length > 0 && <div style={s.roomGrid}>{rooms.map(id => <div key={id} style={s.card}><span style={{ fontWeight: 600 }}>Room #{id}</span></div>)}</div>}
    </div>
  );
}

function PendingApplications({ adminId }) {
  const [pending, setPending] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);
  const [feedback, setFeedback] = useState({});
  const [rejectMsg, setRejectMsg] = useState({});
  const [rejectOpen, setRejectOpen] = useState({});

  const load = async () => {
    setLoading(true); setFetched(true);
    try {
      const res = await fetch(`${API}/admin/applications/pending`, { credentials: "include" });
      const ids = await res.json();
      setPending(Array.isArray(ids) ? ids : []);
    } catch {} finally { setLoading(false); }
  };

  const accept = async (id) => {
    try {
      const res = await fetch(`${API}/admin/applications/accept?application_id=${id}&admin_id=${adminId}`, { method: "PUT", credentials: "include" });
      const data = await res.json();
      setFeedback(f => ({ ...f, [id]: { type: res.ok ? "success" : "error", msg: res.ok ? "Accepted." : data.message } }));
      if (res.ok) setPending(p => p.filter(x => x !== id));
    } catch { setFeedback(f => ({ ...f, [id]: { type: "error", msg: "Network error." } })); }
  };

  const reject = async (id) => {
    if (!rejectMsg[id]) return setFeedback(f => ({ ...f, [id]: { type: "error", msg: "Reason is required." } }));
    try {
      const res = await fetch(`${API}/admin/applications/reject?application_id=${id}&admin_id=${adminId}`, {
        method: "PUT", credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reason_for_refusal: rejectMsg[id] }),
      });
      const data = await res.json();
      setFeedback(f => ({ ...f, [id]: { type: res.ok ? "success" : "error", msg: res.ok ? "Rejected." : data.message } }));
      if (res.ok) { setPending(p => p.filter(x => x !== id)); setRejectOpen(r => ({ ...r, [id]: false })); }
    } catch { setFeedback(f => ({ ...f, [id]: { type: "error", msg: "Network error." } })); }
  };

  return (
    <div>
      <p style={s.sectionTitle}>Pending Applications</p>
      <p style={s.sectionSub}>Review and process outstanding student applications.</p>
      <button style={{ ...s.btn("primary"), marginBottom: 16 }} onClick={load}>Load Pending</button>
      {loading && <div style={{ textAlign: "center", padding: 32 }}><span style={{ ...s.spinner, borderTopColor: C.primary, borderColor: C.border }} /></div>}
      {!loading && fetched && pending.length === 0 && <div style={s.empty}>No pending applications.</div>}
      {!loading && pending.map(id => (
        <div key={id} style={{ ...s.card, marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ fontWeight: 600 }}>Application #{id}</span>
              <Badge status="Pending" />
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button style={s.btn("success")} onClick={() => accept(id)}>Accept</button>
              <button style={s.btn("danger")} onClick={() => setRejectOpen(r => ({ ...r, [id]: !r[id] }))}>Reject</button>
            </div>
          </div>
          {feedback[id] && <div style={{ ...s.alert(feedback[id].type), marginTop: 10, marginBottom: 0 }}>{feedback[id].msg}</div>}
          {rejectOpen[id] && (
            <div style={{ marginTop: 12, paddingTop: 12, borderTop: `1px solid ${C.border}` }}>
              <label style={s.label}>Reason for rejection</label>
              <textarea style={{ ...s.textarea, marginBottom: 8 }} placeholder="Explain the reason..." value={rejectMsg[id] || ""} onChange={e => setRejectMsg(r => ({ ...r, [id]: e.target.value }))} />
              <button style={s.btn("danger")} onClick={() => reject(id)}>Confirm Rejection</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function ApplicationDetails() {
  const [applicationId, setApplicationId] = useState("");
  const [details, setDetails] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const lookup = async () => {
    if (!applicationId) return setError("Application ID is required.");
    setLoading(true); setError(null); setDetails(null);
    try {
      const res = await fetch(`${API}/admin/applications/details?application_id=${applicationId}`, { credentials: "include" });
      const data = await res.json();
      if (!res.ok) return setError(data.message);
      setDetails(data);
    } catch { setError("Network error."); } finally { setLoading(false); }
  };

  return (
    <div style={{ maxWidth: 520 }}>
      <p style={s.sectionTitle}>Application Details</p>
      <p style={s.sectionSub}>Look up the full details of any application by ID.</p>
      <Alert msg={error} type="error" />
      <div style={s.row}>
        <div style={s.fieldGroup}><label style={s.label}>Application ID</label><input style={s.input} type="number" placeholder="e.g. 1" value={applicationId} onChange={e => setApplicationId(e.target.value)} /></div>
        <button style={s.btn("primary")} onClick={lookup} disabled={loading}>{loading ? <Spinner /> : "Look up"}</button>
      </div>
      {details && (
        <div style={s.card}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <span style={{ fontWeight: 700, fontSize: 16 }}>Application #{details.application_Id}</span>
            <Badge status={details.status} />
          </div>
          <hr style={s.divider} />
          {[
            ["Student", details.student_name],
            ["Room", `#${details.room_id}`],
            ["Submitted", details.submission_date],
            ["Message", details.application_message],
            details.handled_by != null ? ["Handled by Admin", `#${details.handled_by}`] : null,
            details.reason_for_refusal ? ["Rejection reason", details.reason_for_refusal] : null,
          ].filter(Boolean).map(([k, v]) => (
            <div key={k} style={{ display: "flex", gap: 12, marginBottom: 8, fontSize: 14 }}>
              <span style={{ color: C.textMuted, minWidth: 140 }}>{k}</span>
              <span style={{ fontWeight: 500 }}>{v}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── ROOT ─────────────────────────────────────────────────────────
export default function App() {
  const [auth, setAuth] = useState(null);

  if (!auth) return <LoginPage onLogin={(role, id) => setAuth({ role, id })} />;
  if (auth.role === "student") return <StudentApp studentId={auth.id} onLogout={() => setAuth(null)} />;
  if (auth.role === "admin") return <AdminApp adminId={auth.id} onLogout={() => setAuth(null)} />;
}
