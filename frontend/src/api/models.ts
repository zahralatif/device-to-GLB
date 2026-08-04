import { API_URL } from "./client";

export async function getModels() {
  const response = await fetch(`${API_URL}/api/v1/models/`);

  if (!response.ok) {
    throw new Error("Failed to load models");
  }

  return response.json();
}