// oauth.js — module central pour déclencher l'auth sociale (Google, Apple, Facebook)
export function initOAuth() {
  document.querySelectorAll(".social-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const provider = btn.classList.contains("google")
        ? "Google"
        : btn.classList.contains("apple")
        ? "Apple"
        : "Facebook";
      alert(`Authentification via ${provider} — à connecter à ton backend`);
    });
  });
}
