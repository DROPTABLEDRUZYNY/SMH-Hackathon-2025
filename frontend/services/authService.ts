async function getCsrfToken() {
    await fetch("http://localhost:8000/api/csrf/", {
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
  const res = await fetch("http://localhost:8000/api/users/login/", {
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
  const res = await fetch("http://localhost:8000/api/users/logout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",   // TODO: Add X-CSRFToken header (?)
    },
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Logout failed");
  }
}