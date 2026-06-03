import { useEffect, useState } from "react";

const BACKEND = "http://localhost:8000";

const COLORS = {
  Hot:  { bg: "#fee2e2", color: "#b91c1c" },
  Warm: { bg: "#fef3c7", color: "#92400e" },
  Cold: { bg: "#dbeafe", color: "#1e40af" },
};

export default function Dashboard() {
  const [leads, setLeads]   = useState([]);
  const [filter, setFilter] = useState("All");
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchLeads(); }, []);

  async function fetchLeads() {
    setLoading(true);
    const res  = await fetch(`${BACKEND}/leads`);
    const data = await res.json();
    setLeads(data);
    setLoading(false);
  }

  async function markContacted(id) {
    await fetch(`${BACKEND}/leads/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: "contacted" }),
    });
    fetchLeads();
  }

  const visible = filter === "All"
    ? leads
    : leads.filter(l => l.classification === filter);

  function short(text, n = 60) {
    return text && text.length > n ? text.slice(0, n) + "…" : text;
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: "24px", background: "#f8fafc", minHeight: "100vh" }}>
      <h1 style={{ fontSize: "26px", fontWeight: "bold", marginBottom: "4px" }}>🎯 Lead Dashboard</h1>
      <p style={{ color: "#64748b", marginBottom: "20px" }}>{leads.length} total leads</p>

      <div style={{ marginBottom: "16px", display: "flex", gap: "12px", alignItems: "center" }}>
        <strong>Filter:</strong>
        <select value={filter} onChange={e => setFilter(e.target.value)}
          style={{ padding: "8px", borderRadius: "8px", border: "1px solid #ccc" }}>
          <option value="All">All</option>
          <option value="Hot">🔥 Hot</option>
          <option value="Warm">🌤 Warm</option>
          <option value="Cold">❄️ Cold</option>
        </select>
        <button onClick={fetchLeads}
          style={{ padding: "8px 14px", borderRadius: "8px", border: "1px solid #ccc", cursor: "pointer" }}>
          ↻ Refresh
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {!loading && (
        <div style={{ overflowX: "auto", background: "white", borderRadius: "12px", boxShadow: "0 1px 4px rgba(0,0,0,0.1)" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#f1f5f9", textAlign: "left" }}>
                {["Name","Email","Phone","Source","Message","Classification","Suggested Reply","Status","Action"].map(h => (
                  <th key={h} style={{ padding: "12px 16px", fontSize: "12px", color: "#64748b", textTransform: "uppercase" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {visible.map(lead => {
                const badge = COLORS[lead.classification] || COLORS.Cold;
                const done  = lead.status === "contacted";
                return (
                  <tr key={lead.id} style={{ borderTop: "1px solid #f1f5f9", opacity: done ? 0.6 : 1 }}>
                    <td style={{ padding: "12px 16px", fontWeight: "600" }}>{lead.name}</td>
                    <td style={{ padding: "12px 16px" }}>{lead.email}</td>
                    <td style={{ padding: "12px 16px" }}>{lead.phone}</td>
                    <td style={{ padding: "12px 16px" }}>
                      <span style={{ background: "#ede9fe", color: "#6d28d9", padding: "2px 8px", borderRadius: "6px", fontSize: "12px" }}>
                        {lead.source}
                      </span>
                    </td>
                    <td style={{ padding: "12px 16px", maxWidth: "180px", fontSize: "13px" }} title={lead.message}>
                      {short(lead.message)}
                    </td>
                    <td style={{ padding: "12px 16px" }}>
                      <span style={{ background: badge.bg, color: badge.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "700" }}>
                        {lead.classification}
                      </span>
                    </td>
                    <td style={{ padding: "12px 16px", maxWidth: "200px", fontSize: "13px", color: "#555" }}>
                      {short(lead.suggested_reply, 80)}
                    </td>
                    <td style={{ padding: "12px 16px" }}>
                      <span style={{ background: done ? "#f3f4f6" : "#dcfce7", color: done ? "#6b7280" : "#166534", padding: "2px 8px", borderRadius: "6px", fontSize: "12px" }}>
                        {lead.status}
                      </span>
                    </td>
                    <td style={{ padding: "12px 16px" }}>
                      {!done && (
                        <button onClick={() => markContacted(lead.id)}
                          style={{ background: "#3b82f6", color: "white", border: "none", padding: "6px 12px", borderRadius: "6px", cursor: "pointer", fontSize: "12px", fontWeight: "600" }}>
                          ✓ Contacted
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}