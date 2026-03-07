const AUTH_KEY = "sprs_auth";

export function setSession(session) {
  localStorage.setItem(AUTH_KEY, JSON.stringify(session));
}

export function getSession() {
  const raw = localStorage.getItem(AUTH_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearSession() {
  localStorage.removeItem(AUTH_KEY);
}

export function logoutUser() {
  clearSession();
}

export function isAuthenticated() {
  const session = getSession();
  return Boolean(session?.access_token);
}

export function getToken() {
  return getSession()?.access_token || "";
}

export function getUserRole() {
  return getSession()?.user?.role || "";
}

export function hasRole(allowedRoles = []) {
  if (!allowedRoles.length) return true;
  const role = getUserRole();
  return allowedRoles.includes(role);
}
