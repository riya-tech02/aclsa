export default function AnalysisPanel({ data }) {
  if (!data) return null;
  return (
    <aside className="analysis-panel">
      <h3>Agent Analysis</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </aside>
  );
}
