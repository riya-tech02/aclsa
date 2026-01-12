export default function MessageBubble({ role, text }) {
  return (
    <div className={`bubble ${role}`}>
      <pre>{text}</pre>
    </div>
  );
}
