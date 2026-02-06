const navDesktop = document.getElementById('navDesktop');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const header = document.getElementById('header');
const mobileNav = document.getElementById('mobileNav');

// Header effect
 window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Mobile menu
mobileMenuBtn.addEventListener('click', () => {
    mobileNav.classList.toggle('active');
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
            mobileNav.classList.remove('active');
        }
        async function loginAdmin() {
    const senha = document.getElementById('senhaAdmin').value;

    const res = await fetch('/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ senha })
    });

    const data = await res.json();

    if (data.ok) {
        alert('Acesso liberado');
        document.getElementById('adminPanel').style.display = 'block';
    } else {
        alert('Senha incorreta');
    }
}
async function loginAdmin() {
  const senha = document.getElementById('senhaAdmin').value;

  const res = await fetch('/admin/login', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({senha})
  });

  const data = await res.json();

  if (data.ok) {
    document.getElementById('adminPanel').style.display = 'block';
    carregarAdmin();
  } else {
    alert('Senha incorreta');
  }
}

async function carregarAdmin() {
  const res = await fetch('/api/motos');
  const motos = await res.json();

  const div = document.getElementById('adminMotos');
  div.innerHTML = '';

  motos.forEach(m => {
    div.innerHTML += `
      <div>
        <b>${m.nome}</b>
        <button onclick="removerMoto(${m.id})">Excluir</button>
      </div>
    `;
  });
}

async function removerMoto(id) {
  await fetch('/api/motos/' + id, { method:'DELETE' });
  carregarAdmin();
}

document.getElementById('formMoto')?.addEventListener('submit', async e => {
  e.preventDefault();
  const form = new FormData(e.target);

  await fetch('/api/motos', {
    method:'POST',
    body: form
  });

  e.target.reset();
  carregarAdmin();
  
});

    });
});