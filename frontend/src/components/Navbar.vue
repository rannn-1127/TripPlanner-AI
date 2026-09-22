<template>
  <header class="navbar">
    <div class="navbar-container">
      <div class="brand" @click="$router.push('/')">
        <div class="brand-icon">
          🧭
        </div>
        <div class="brand-text">
          <span class="brand-name">TripPlanner</span>
          <span class="brand-ai">AI</span>
        </div>
      </div>

      <nav class="nav-links">
        <router-link to="/" class="nav-item">
          <span class="nav-icon">⌂</span>
          <span>首页</span>
        </router-link>

        <router-link to="/planner" class="nav-item">
          <span class="nav-icon">✈</span>
          <span>开始规划</span>
        </router-link>

        <router-link to="/knowledge" class="nav-item">
          <span class="nav-icon">▤</span>
          <span>知识库</span>
        </router-link>

        <router-link to="/history" class="nav-item">
          <span class="nav-icon">◷</span>
          <span>历史行程</span>
        </router-link>

        <router-link to="/about" class="nav-item">
          <span class="nav-icon">ⓘ</span>
          <span>关于我们</span>
        </router-link>
      </nav>
    </div>
  </header>
</template>

<style>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  height: 68px;
  border-bottom: 1px solid rgba(251,191,36,.18);
  background: rgba(255,250,245,.78);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}
.navbar-container {
  width: min(1240px, calc(100% - 48px));
  height: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}
.brand-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 13px;
  background: linear-gradient(135deg,#fbbf24,#f97316);
  font-size: 21px;
  box-shadow:
    0 8px 20px rgba(249,115,22,.25),
    inset 0 1px rgba(255,255,255,.5);
  transition: .3s ease;
}
.brand:hover .brand-icon {
  transform: translateY(-2px) rotate(8deg);
  box-shadow:
    0 12px 28px rgba(249,115,22,.35);
}
.brand-text {
  display: flex;
  align-items: baseline;
  gap: 5px;
}
.brand-name {
  color:#1f2937;
  font-size:18px;
  font-weight:750;
  letter-spacing:-.4px;
}
.brand-ai {
  color:#f97316;
  font-size:12px;
  font-weight:800;
}
.nav-links {
  display:flex;
  align-items:center;
  gap:8px;
}
.nav-item {
  position:relative;
  display:flex;
  align-items:center;
  gap:7px;
  padding:10px 15px;
  border-radius:12px;
  color:#78716c;
  font-size:13px;
  font-weight:550;
  text-decoration:none;
  transition:.25s ease;
}
.nav-item:hover {
  color:#ea580c;
  background:#fff7ed;
  transform:translateY(-2px);
}
.nav-icon {
  font-size:15px;
  transition:.25s ease;
}
.nav-item:hover .nav-icon {
  transform:scale(1.15);
}
.nav-item.router-link-active {
  color:#ea580c;
  background:linear-gradient(
    135deg,
    #ffedd5,
    #fff7ed
  );
  font-weight:650;
  box-shadow:
    0 4px 12px rgba(249,115,22,.12);
}
.nav-item.router-link-active::after {
  content:"";
  position:absolute;
  left:50%;
  bottom:-6px;
  width:28px;
  height:3px;
  transform:translateX(-50%);
  border-radius:999px;
  background:linear-gradient(
    90deg,
    #fbbf24,
    #f97316
  );
}
.nav-item:active {
  transform:scale(.96);
}
@media(max-width:760px){
  .navbar-container {
    width:calc(100% - 24px);
  }
  .nav-item {
    padding:8px 10px;
  }
  .nav-item span:last-child {
    display:none;
  }
}
@media(max-width:480px){
  .brand-ai {
    display:none;
  }
  .nav-links {
    gap:2px;
  }
  .nav-item {
    padding:8px;
  }
}
</style>