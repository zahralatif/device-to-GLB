export const API_URL = import.meta.env.VITE_API_URL;

export async function healthCheck() {
  const response = await fetch(`${API_URL}/api/v1/health`);
  return response.json();
}