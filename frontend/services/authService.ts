const API_PATH = "http://localhost:8000/api";
import { BehaviorSubject } from 'rxjs';

export const userEmail$ = new BehaviorSubject<string | null>(null);

// Inicjalizacja stanu na podstawie ciasteczek
const initializeAuth = () => {
  if (typeof window !== 'undefined') {
    const email = document.cookie
      .split("; ")
      .find((row) => row.startsWith("userEmail="))
      ?.split("=")[1];
    
    if (email) {
      userEmail$.next(decodeURIComponent(email));
    }
  }
};

// Wywołujemy inicjalizację tylko po stronie klienta
if (typeof window !== 'undefined') {
  initializeAuth();
}

export async function getCsrfToken() {
  if (typeof window === 'undefined') {
    return null;
  }

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

  // Zapisz email do ciasteczek i zaktualizuj observable
  document.cookie = `userEmail=${encodeURIComponent(email)}; path=/; max-age=2592000`;
  userEmail$.next(email);

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

  // Usuń ciasteczka i zaktualizuj observable
  document.cookie = "userEmail=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT";
  document.cookie = "sessionid=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT";
  userEmail$.next(null);
}
