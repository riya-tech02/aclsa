const API_URL = "https://aclsa-agent.onrender.com";

export async function sendMessage(userId, text) {
  const res = await fetch(`${API_URL}/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, text })
  });
  if (!res.ok) throw new Error("Agent error");
  return res.json();
}
