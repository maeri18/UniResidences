import { useState, useEffect } from "react";

const API = "http://localhost:5000";

// ─── THEME CONFIGURATION ────────────────────────────────────────
const C = {
  bg: "#F7F8FA",
  surface: "#FFFFFF",
  border: "#E4E7EC",
  primary: "#2D5BE3",
  primaryHover: "#1E46C7",
  primaryLight: "#EEF2FF",
  success: "#16A34A",
  successLight: "#DCFCE7",
  error: "#DC2626",
  errorLight: "#FEE2E2",
  text: "#111827",
  textMuted: "#6B7280",
};

const styles = {
  page: { minHeight: "100vh", background: C.bg, fontFamily: "system-ui, sans-serif", color: C.text, paddingBottom: "40px" },
  nav: { background: C.surface, borderBottom: `1px solid ${C.border}`, padding: "0 32px", display: "flex", alignItems: "center", justifyContent: "space-between", height: 56, position: "sticky", top: 0, zIndex: 100 },
  navBrand: { fontWeight: 700, fontSize: 18, color: C.primary },
  card: { background: C.surface, border: `1px solid ${C.border}`, borderRadius: 12, padding: 24, marginBottom: 24, boxShadow: "0 1px 3px rgba(0,0,0,0.05)" },
  cardTitle: { margin: "0 0 16px 0", fontSize: 18, fontWeight: 600 },
  input: { width: "100%", padding: "10px 12px", border: `1px solid ${C.border}`, borderRadius: 6, marginBottom: 16, fontSize: 14, boxSizing: "border-box" },
  button: { background: C.primary, color: "#fff", border: "none", padding: "10px 16px", borderRadius: 6, fontWeight: 500, cursor: "pointer", fontSize: 14 },
  buttonSecondary: { background: "transparent", border: `1px solid ${C.border}`, color: C.textMuted, padding: "8px 14px", borderRadius: 6, cursor: "pointer", fontSize: 13 },
  badge: (type) => ({
    padding: "4px 8px", borderRadius: 4, fontSize: 12, fontWeight: 600,
    background: type === "Accepted" ? C.successLight : type === "Rejected" ? C.errorLight : C.primaryLight,
    color: type === "Accepted" ? C.success : type === "Rejected" ? C.error : C.primary,
  }),
  grid: { display: "grid", gridTemplateColumns: "13fr 11fr", gap: 24, maxWidth: 1200, margin: "24px auto", padding: "0 24px" },
  loginContainer: { maxWidth: 400, margin: "100px auto", padding: "0 16px" },
  tabButton: (active) => ({ flex: 1, padding: "12px", border: "none", background: active ? C.surface : C.bg, fontWeight: 600, color: active ? C.primary : C.textMuted, cursor: "pointer", borderBottom: active ? `2px solid ${C.primary}` : "none" }),
};

export default function App() {
  // Authentication & View Session States
  const [user, setUser] = useState(null); // stores context: { role: 'student'|'admin', id: number }
  const [loginTab, setLoginTab] = useState("student"); // 'student' or 'admin'
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  // Business Operational States
  const [rooms, setRooms] = useState([]);
  const [applications, setApplications] = useState([]);
  const [selectedAppDetails, setSelectedAppDetails] = useState(null);

  // Form Submission States
  const [appMessage, setAppMessage] = useState("");
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const [refusalReason, setRefusalReason] = useState("");
  const [rejectingAppId, setRejectingAppId] = useState(null);

  // Handle Logins
  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    const isStudent = loginTab === "student";
    const endpoint = isStudent ? `${API}/student/login` : `${API}/admin/login`;
    const payload = isStudent 
      ? { student_id: parseInt(userId, 10), student_password: password }
      : { admin_id: parseInt(userId, 10), admin_password: password };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (response.ok) {
        setUser({ role: loginTab, id: parseInt(userId, 10) });
        setUserId("");
        setPassword("");
      } else {
        setErrorMsg(data.message || "Invalid credentials.");
      }
    } catch (err) {
      setErrorMsg("Failed to connect to backend server.");
    }
  };

  const handleLogout = () => {
    setUser(null);
    setRooms([]);
    setApplications([]);
    setSelectedAppDetails(null);
  };

  // Fetch data contextually on successful session login
  useEffect(() => {
    if (!user) return;
    fetchData();
  }, [user]);

  const fetchData = async () => {
    if (user.role === "student") {
      // Get all available rooms for selection
      const resRooms = await fetch(`${API}/student/rooms/available`);
      if (resRooms.ok) setRooms(await resRooms.json());

      // Get student's historical system applications
      const resApps = await fetch(`${API}/student/applications/all?student_id=${user.id}`);
      if (resApps.ok) {
        const data = await resApps.json();
        setApplications(data.applications || []);
      }
    } else if (user.role === "admin") {
      // Get system catalog tracking overview
      const resRooms = await fetch(`${API}/admin/rooms/all`);
      if (resRooms.ok) setRooms(await resRooms.json());

      // Fetch open workload queue
      const resApps = await fetch(`${API}/admin/applications/pending`);
      if (resApps.ok) setApplications(await resApps.json());
    }
  };

  // Student Actions: Apply for Dorm Room
  const handleApply = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API}/student/rooms/apply?room_id=${selectedRoomId}&student_id=${user.id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ application_message: appMessage }),
      });
      const data = await response.json();
      alert(data.message || "Action processed.");
      setSelectedRoomId(null);
      setAppMessage("");
      fetchData();
    } catch (err) {
      alert("Error submitting application.");
    }
  };

  // Admin Actions: Inspect Application Meta Particulars
  const inspectApplication = async (appId) => {
    const res = await fetch(`${API}/admin/applications/details?application_id=${appId}`);
    if (res.ok) setSelectedAppDetails(await res.json());
  };

  // Admin Actions: Accept Lifecycle Request
  const handleAcceptApp = async (appId) => {
    const res = await fetch(`${API}/admin/applications/accept?application_id=${appId}&admin_id=${user.id}`, {
      method: "PUT"
    });
    if (res.ok) {
      alert("Application successfully accepted!");
      setSelectedAppDetails(null);
      fetchData();
    }
  };

  // Admin Actions: Reject Lifecycle Request
  const handleRejectApp = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API}/admin/applications/reject?application_id=${rejectingAppId}&admin_id=${user.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reason_for_refusal: refusalReason }),
    });
    if (res.ok) {
      alert("Application rejected.");
      setRejectingAppId(null);
      setRefusalReason("");
      setSelectedAppDetails(null);
      fetchData();
    }
  };

  return (
    <div style={styles.page}>
      {/* ─── RENDER LOGIN PORTAL ─── */}
      {!user ? (
        <div style={styles.loginContainer}>
          <div style={{ textAlign: "center", marginBottom: 24 }}>
            <h1 style={{ margin: "0 0 8px 0", color: C.primary }}>UniResidences 🏫</h1>
            <p style={{ margin: 0, color: C.textMuted }}>Dormitory Housing Allocations</p>
          </div>
          <div style={{ ...styles.card, padding: 0, overflow: "hidden" }}>
            <div style={{ display: "flex", borderBottom: `1px solid ${C.border}` }}>
              <button style={styles.tabButton(loginTab === "student")} onClick={() => setLoginTab("student")}>Student</button>
              <button style={styles.tabButton(loginTab === "admin")} onClick={() => setLoginTab("admin")}>Admin</button>
            </div>
            <form onSubmit={handleLogin} style={{ padding: 24 }}>
              {errorMsg && <div style={{ color: C.error, background: C.errorLight, padding: 10, borderRadius: 6, marginBottom: 16, fontSize: 13 }}>{errorMsg}</div>}
              <label style={{ display: "block", marginBottom: 6, fontSize: 13, fontWeight: 500 }}>{loginTab === "student" ? "Student ID" : "Admin ID"}</label>
              <input style={styles.input} type="number" required value={userId} onChange={e => setUserId(e.target.value)} placeholder="Enter numeric ID" />
              
              <label style={{ display: "block", marginBottom: 6, fontSize: 13, fontWeight: 500 }}>Password</label>
              <input style={styles.input} type="password" required value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" />
              
              <button style={{ ...styles.button, width: "100%", marginTop: 8 }} type="submit">Sign In as {loginTab === "student" ? "Student" : "Admin"}</button>
            </form>
          </div>
        </div>
      ) : (
        /* ─── RENDER SYSTEM WORKSPACE DASHBOARDS ─── */
        <div>
          <nav style={styles.nav}>
            <span style={styles.navBrand}>UniResidences ({user.role.toUpperCase()} PORTAL)</span>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <span style={{ fontSize: 14, color: C.textMuted }}>ID: <strong>{user.id}</strong></span>
              <button style={styles.buttonSecondary} onClick={handleLogout}>Logout</button>
            </div>
          </nav>

          {/* STUDENT DASHBOARD DESK LAYOUT */}
          {user.role === "student" && (
            <div style={styles.grid}>
              <div>
                <div style={styles.card}>
                  <h2 style={styles.cardTitle}>Available Rooms for Rent</h2>
                  {rooms.length === 0 ? <p style={{ color: C.textMuted, fontSize: 14 }}>No vacant spaces currently available.</p> : (
                    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                      {rooms.map(roomId => (
                        <div key={roomId} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", border: `1px solid ${C.border}`, borderRadius: 8 }}>
                          <span style={{ fontWeight: 500, fontSize: 14 }}>Room Reference Unit #{roomId}</span>
                          <button style={{ ...styles.button, padding: "6px 12px", fontSize: 12 }} onClick={() => setSelectedRoomId(roomId)}>Apply</button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {selectedRoomId && (
                  <div style={styles.card}>
                    <h2 style={styles.cardTitle}>Submit Application for Room #{selectedRoomId}</h2>
                    <form onSubmit={handleApply}>
                      <textarea style={{ ...styles.input, minHeight: 80, fontFamily: "inherit" }} required placeholder="State your reason or application notes here..." value={appMessage} onChange={e => setAppMessage(e.target.value)} />
                      <div style={{ display: "flex", gap: 12 }}>
                        <button style={styles.button} type="submit">Submit Request</button>
                        <button style={styles.buttonSecondary} type="button" onClick={() => setSelectedRoomId(null)}>Cancel</button>
                      </div>
                    </form>
                  </div>
                )}
              </div>

              <div>
                <div style={styles.card}>
                  <h2 style={styles.cardTitle}>My Application History</h2>
                  {applications.length === 0 ? <p style={{ color: C.textMuted, fontSize: 14 }}>You haven't submitted any room requests yet.</p> : (
                    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                      {applications.map(appId => (
                        <div key={appId} style={{ padding: 12, border: `1px solid ${C.border}`, borderRadius: 8, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                          <span style={{ fontSize: 14 }}>Application Reference Ref ID: <strong>{appId}</strong></span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* ADMIN WORKLOAD DESK LAYOUT */}
          {user.role === "admin" && (
            <div style={styles.grid}>
              <div>
                <div style={styles.card}>
                  <h2 style={styles.cardTitle}>Pending Incoming Applications Queue</h2>
                  {applications.length === 0 ? <p style={{ color: C.textMuted, fontSize: 14 }}>Clean queue! No incoming items pending processing.</p> : (
                    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                      {applications.map(appId => (
                        <div key={appId} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 12, border: `1px solid ${C.border}`, borderRadius: 8 }}>
                          <span style={{ fontSize: 14, fontWeight: 500 }}>Application Object ID: #{appId}</span>
                          <button style={{ ...styles.button, padding: "6px 12px", fontSize: 12 }} onClick={() => inspectApplication(appId)}>Inspect Details</button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {selectedAppDetails && (
                  <div style={styles.card}>
                    <h2 style={styles.cardTitle}>Details for Application #{selectedAppDetails.application_Id}</h2>
                    <div style={{ fontSize: 14, display: "flex", flexDirection: "column", gap: 8, marginBottom: 20 }}>
                      <div><span style={{ color: C.textMuted }}>Student Submitter Name:</span> <strong>{selectedAppDetails.student_name}</strong></div>
                      <div><span style={{ color: C.textMuted }}>Requested Target Room ID:</span> <strong>#{selectedAppDetails.room_id}</strong></div>
                      <div><span style={{ color: C.textMuted }}>Submission Date Stamp:</span> {selectedAppDetails.submission_date}</div>
                      <div><span style={{ color: C.textMuted }}>Current Process Status:</span> <span style={styles.badge(selectedAppDetails.status)}>{selectedAppDetails.status}</span></div>
                      <div style={{ background: C.bg, padding: 12, borderRadius: 6, marginTop: 4 }}>
                        <span style={{ display: "block", fontSize: 12, color: C.textMuted, marginBottom: 4 }}>Student Application Message:</span>
                        "{selectedAppDetails.application_message}"
                      </div>
                    </div>
                    {selectedAppDetails.status === "Pending" && !rejectingAppId && (
                      <div style={{ display: "flex", gap: 12 }}>
                        <button style={{ ...styles.button, background: C.success }} onClick={() => handleAcceptApp(selectedAppDetails.application_Id)}>Accept / Allocate</button>
                        <button style={{ ...styles.button, background: C.error }} onClick={() => setRejectingAppId(selectedAppDetails.application_Id)}>Reject Request</button>
                      </div>
                    )}
                  </div>
                )}

                {rejectingAppId && (
                  <div style={styles.card}>
                    <h2 style={{ ...styles.cardTitle, color: C.error }}>Provide Rejection Justification for #{rejectingAppId}</h2>
                    <form onSubmit={handleRejectApp}>
                      <input style={styles.input} type="text" required placeholder="Specify mandatory statement for refusal..." value={refusalReason} onChange={e => setRefusalReason(e.target.value)} />
                      <div style={{ display: "flex", gap: 12 }}>
                        <button style={{ ...styles.button, background: C.error }} type="submit">Confirm Rejection</button>
                        <button style={styles.buttonSecondary} type="button" onClick={() => setRejectingAppId(null)}>Cancel</button>
                      </div>
                    </form>
                  </div>
                )}
              </div>

              <div>
                <div style={styles.card}>
                  <h2 style={styles.cardTitle}>System Dorm Room Catalog Status</h2>
                  <div style={{ display: "flex", flexDirection: "column", gap: 8, maxHeight: "500px", overflowY: "auto" }}>
                    {rooms.map(room => (
                      <div key={room.id} style={{ display: "flex", justifyContent: "space-between", padding: "10px 12px", borderBottom: `1px solid ${C.border}`, fontSize: 13 }}>
                        <span>Room #{room.id} ({room.description.split(".")[0]})</span>
                        <span style={{ fontWeight: 600, color: room.available ? C.success : C.error }}>{room.available ? "Vacant" : "Occupied"}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}