// auth.js — interactions basiques + placeholders OAuth
document.addEventListener('DOMContentLoaded', () => {
  const byId = id => document.getElementById(id);

  const signinForm = byId('signin-form');
  const signupForm = byId('signup-form');

  if (signinForm){
    signinForm.addEventListener('submit', (ev)=>{
      ev.preventDefault();
      const email = signinForm.querySelector('input[name="email"]').value.trim();
      if (!email){ alert('Merci de renseigner une adresse email'); return; }
      alert('Connexion simulée — redirection vers le profil');
      window.location.href = '../profile.html';
    });
  }

  if (signupForm){
    signupForm.addEventListener('submit', (ev)=>{
      ev.preventDefault();
      const pass = signupForm.querySelector('input[name="password"]').value;
      const confirm = signupForm.querySelector('#confirm') ? signupForm.querySelector('#confirm').value : '';
      if (pass !== confirm){ alert('Les mots de passe ne correspondent pas'); return; }
      alert('Inscription simulée — redirection vers le profil');
      window.location.href = '../profile.html';
    });
  }

  const bind = (id, provider) => {
    const el = byId(id);
    if (!el) return;
    el.addEventListener('click', () => handleOAuth(provider));
  };

  bind('google-btn','google');
  bind('apple-btn','apple');
  bind('facebook-btn','facebook');
  bind('google-signup','google');
  bind('apple-signup','apple');
  bind('facebook-signup','facebook');
});

// Generic placeholder for OAuth integration
function handleOAuth(provider){
  // Replace with real OAuth integration (backend + redirect)
  alert('Ouverture du flux OAuth : ' + provider);
}
