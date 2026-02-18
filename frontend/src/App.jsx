import { useState, useEffect } from "react";

const MATCH_COLORS = {
  high: { bg: "#1e3a2f", text: "#a6e3a1", label: "High Match" },
  mid: { bg: "#3a3520", text: "#f9e2af", label: "Mid Match" },
  low: { bg: "#3a1f1f", text: "#f38ba8", label: "Low Match" },
};

function getMatchLevel(pct) {
  if (pct >= 80) return "high";
  if (pct >= 50) return "mid";
  return "low";
}

function JobCard({ job, index }) {
  const level = getMatchLevel(job.match_percentage);
  const colors = MATCH_COLORS[level];

  return (
    <div style={{
      background: colors.bg,
      border: `1px solid ${colors.text}33`,
      borderRadius: "10px",
      padding: "16px 20px",
      marginBottom: "12px",
      display: "flex",
      alignItems: "center",
      gap: "16px",
    }}>
      <div style={{ fontSize: "14px", color: "#888", minWidth: "28px" }}>#{index}</div>

      <div style={{ flex: 1 }}>
        <a href={job.link} target="_blank" rel="noreferrer" style={{
          color: "#89dceb", fontWeight: "bold", fontSize: "16px",
          textDecoration: "none"
        }}>
          {job.title}
        </a>
        <div style={{ color: "#cdd6f4", fontSize: "14px", marginTop: "4px" }}>
          {job.company} · {job.location}
        </div>
        <div style={{ color: "#888", fontSize: "13px", marginTop: "4px" }}>
          {job.reason}
        </div>
      </div>

      <div style={{
        background: colors.text + "22",
        color: colors.text,
        fontWeight: "bold",
        fontSize: "18px",
        padding: "8px 14px",
        borderRadius: "8px",
        minWidth: "60px",
        textAlign: "center",
      }}>
        {job.match_percentage}%
      </div>
    </div>
  );
}

function FilterBar({ filter, setFilter, search, setSearch }) {
  return (
    <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap" }}>
      <input
        placeholder="Search job or company..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        style={{
          flex: 1, minWidth: "200px", padding: "10px 14px",
          background: "#313244", border: "1px solid #45475a",
          borderRadius: "8px", color: "#cdd6f4", fontSize: "14px"
        }}
      />
      {["all", "high", "mid", "low"].map(f => (
        <button key={f} onClick={() => setFilter(f)} style={{
          padding: "10px 18px", borderRadius: "8px", border: "none",
          cursor: "pointer", fontWeight: "bold", fontSize: "14px",
          background: filter === f ? "#4472C4" : "#313244",
          color: filter === f ? "white" : "#888",
        }}>
          {f === "all" ? "All" : MATCH_COLORS[f].label}
        </button>
      ))}
    </div>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/jobs.json")
      .then(r => r.json())
      .then(setData)
      .catch(() => setError("Could not load jobs.json – run main.py first!"));
  }, []);

  const filtered = data?.jobs?.filter(job => {
    const matchFilter = filter === "all" || getMatchLevel(job.match_percentage) === filter;
    const matchSearch = search === "" ||
      job.title.toLowerCase().includes(search.toLowerCase()) ||
      job.company.toLowerCase().includes(search.toLowerCase());
    return matchFilter && matchSearch;
  }) ?? [];

  if (error) return (
    <div style={{ background: "#1e1e2e", minHeight: "100vh", display: "flex",
      alignItems: "center", justifyContent: "center", color: "#f38ba8", fontSize: "18px" }}>
      {error}
    </div>
  );

  if (!data) return (
    <div style={{ background: "#1e1e2e", minHeight: "100vh", display: "flex",
      alignItems: "center", justifyContent: "center", color: "#cdd6f4", fontSize: "18px" }}>
      Loading...
    </div>
  );

  return (
    <div style={{ background: "#1e1e2e", minHeight: "100vh", color: "#cdd6f4",
      fontFamily: "'Segoe UI', Arial, sans-serif", padding: "30px" }}>

      <div style={{ maxWidth: "900px", margin: "0 auto" }}>

        {/* Header */}
        <div style={{ marginBottom: "30px" }}>
          <h1 style={{ color: "#89b4fa", margin: 0, fontSize: "28px" }}>
            Job Agent Dashboard
          </h1>
          <p style={{ color: "#888", marginTop: "6px" }}>
            Last run: {data.generated_at} · {data.total_jobs_found} unique jobs found
          </p>
        </div>

        {/* Cost Summary */}
        <div style={{ background: "#313244", borderRadius: "10px", padding: "16px 20px",
          marginBottom: "24px", display: "flex", gap: "30px", flexWrap: "wrap" }}>
          <div>
            <div style={{ color: "#888", fontSize: "12px" }}>INPUT TOKENS</div>
            <div style={{ color: "#f9e2af", fontWeight: "bold" }}>{data.cost.input_tokens.toLocaleString()}</div>
          </div>
          <div>
            <div style={{ color: "#888", fontSize: "12px" }}>OUTPUT TOKENS</div>
            <div style={{ color: "#f9e2af", fontWeight: "bold" }}>{data.cost.output_tokens.toLocaleString()}</div>
          </div>
          <div>
            <div style={{ color: "#888", fontSize: "12px" }}>TOTAL COST</div>
            <div style={{ color: "#a6e3a1", fontWeight: "bold" }}>${data.cost.total_cost_usd}</div>
          </div>
          <div>
            <div style={{ color: "#888", fontSize: "12px" }}>SHOWING</div>
            <div style={{ color: "#cdd6f4", fontWeight: "bold" }}>{filtered.length} jobs</div>
          </div>
        </div>

        {/* Filters */}
        <FilterBar filter={filter} setFilter={setFilter} search={search} setSearch={setSearch} />

        {/* Jobs */}
        {filtered.length === 0 ? (
          <div style={{ color: "#888", textAlign: "center", marginTop: "40px" }}>
            No jobs match your filter.
          </div>
        ) : (
          filtered.map((job, i) => (
            <JobCard key={i} job={job} index={i + 1} />
          ))
        )}
      </div>
    </div>
  );
}