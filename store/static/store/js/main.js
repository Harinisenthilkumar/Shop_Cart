// Toast notification
function showToast(msg, icon = '✓') {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.className = 'toast';
    document.body.appendChild(t);
  }
  t.innerHTML = `<span class="toast-icon">${icon}</span><span>${msg}</span>`;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 2800);
}

// CSRF helper
function getCsrf() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
    document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || '';
}

// Add to cart (AJAX)
document.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-add-cart]');
  if (!btn) return;
  e.preventDefault();
  const pid = btn.dataset.addCart;
  const size = btn.closest('form')?.querySelector('[name=size]')?.value || '';
  const form = new FormData();
  form.append('csrfmiddlewaretoken', getCsrf());
  form.append('size', size);
  fetch(`/cart/add/${pid}/`, {
    method: 'POST',
    body: form,
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(r => r.json())
  .then(data => {
    showToast(data.message || 'Added to cart!', '🛍️');
    const badge = document.querySelector('.cart-badge');
    if (badge && data.count !== undefined) badge.textContent = data.count;
  })
  .catch(() => showToast('Added to cart!', '🛍️'));
});

// Wishlist toggle (AJAX)
document.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-wishlist]');
  if (!btn) return;
  e.preventDefault();
  const pid = btn.dataset.wishlist;
  const form = new FormData();
  form.append('csrfmiddlewaretoken', getCsrf());
  fetch(`/wishlist/toggle/${pid}/`, {
    method: 'POST',
    body: form,
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(r => {
    if (r.status === 401) { window.location = '/login/'; return null; }
    return r.json();
  })
  .then(data => {
    if (!data) return;
    if (data.action === 'added') {
      btn.classList.add('active');
      btn.textContent = '♥';
      showToast('Added to wishlist!', '♥');
    } else {
      btn.classList.remove('active');
      btn.textContent = '♡';
      showToast('Removed from wishlist', '♡');
    }
  });
});

// Size selection
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.size-btn');
  if (!btn) return;
  btn.closest('.size-options')?.querySelectorAll('.size-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  const input = document.querySelector('input[name=size]');
  if (input) input.value = btn.dataset.size;
});

// Star rating selector
document.addEventListener('click', function(e) {
  const label = e.target.closest('.star-label');
  if (!label) return;
  const val = label.dataset.val;
  const input = document.querySelector('input[name=rating]');
  if (input) input.value = val;
  label.closest('.star-select')?.querySelectorAll('.star-label').forEach((l, i) => {
    l.style.color = i < val ? 'var(--gold)' : 'var(--border)';
  });
});

// Scroll reveal
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('fade-up'); observer.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.product-card').forEach(el => observer.observe(el));
