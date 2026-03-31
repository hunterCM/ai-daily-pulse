const API_BASE = "/api";

async function request(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  subscribe: (email, name) =>
    request("/subscribers/", {
      method: "POST",
      body: JSON.stringify({ email, name }),
    }),

  unsubscribe: (email) =>
    request(`/subscribers/${encodeURIComponent(email)}`, { method: "DELETE" }),

  getSubscriberCount: () => request("/subscribers/count"),

  getBriefs: (skip = 0, limit = 30) =>
    request(`/briefs/?skip=${skip}&limit=${limit}`),

  getLatestBrief: () => request("/briefs/latest"),

  getBrief: (id) => request(`/briefs/${id}`),

  getArticles: (skip = 0, limit = 50, source, category) => {
    let url = `/articles?skip=${skip}&limit=${limit}`;
    if (source) url += `&source=${encodeURIComponent(source)}`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    return request(url);
  },

  getStats: () => request("/stats"),

  getSources: () => request("/sources"),

  getCategories: () => request("/categories"),

  triggerBrief: () => request("/trigger-brief", { method: "POST" }),

  healthCheck: () => request("/health"),
};
