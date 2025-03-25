const API_PATH = "http://localhost:8000/api";

async function getCsrfToken() {
  await fetch(`${API_PATH}/csrf/`, {
    method: "GET",
    credentials: "include",
  });

  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];

  return csrfToken;
}

export async function login(email: string, password: string) {
  let csrfToken = await getCsrfToken();
  const res = await fetch(`${API_PATH}/users/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken || "",
    },
    body: JSON.stringify({ email, password }),
    credentials: "include",
  });

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.error || "Login failed");
  }

  const sessionid = document.cookie
    .split("; ")
    .find((row) => row.startsWith("sessionid="))
    ?.split("=")[1];

  return sessionid;
}

export async function logout() {
  let csrfToken = await getCsrfToken();
  const res = await fetch(`${API_PATH}/users/logout/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken || "",
    },
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Logout failed");
  }
}
