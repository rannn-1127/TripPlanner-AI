<template>
  <header class="navbar">
    <div class="navbar-container">

      <!-- Logo -->
      <div
        class="brand"
        @click="$router.push('/')"
      >
        <div class="brand-icon">
          ✦
        </div>

        <div class="brand-text">
          <span class="brand-name">
            TripPlanner
          </span>

          <span class="brand-ai">
            AI
          </span>
        </div>
      </div>


      <!-- Navigation -->
      <nav class="nav-links">


        <!-- 首页 -->
        <router-link
          to="/"
          class="nav-item"
        >
          <span class="nav-icon">⌂</span>
          <span>首页</span>
        </router-link>


        <!-- 新增：开始规划 -->
        <router-link
          to="/planner"
          class="nav-item"
        >
          <span class="nav-icon">✦</span>
          <span>开始规划</span>
        </router-link>


        <!-- 知识库 -->
        <router-link
          to="/knowledge"
          class="nav-item"
        >
          <span class="nav-icon">▤</span>
          <span>知识库</span>
        </router-link>


        <!-- 历史行程 -->
        <router-link
          to="/history"
          class="nav-item"
        >
          <span class="nav-icon">◷</span>
          <span>历史行程</span>
        </router-link>


        <!-- 关于 -->
        <router-link
          to="/about"
          class="nav-item"
        >
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
  height: 64px;
  border-bottom: 1px solid #e9ebf0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.navbar-container {
  width: min(1200px, calc(100% - 40px));
  height: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}



/* Logo */

.brand {
  display: flex;
  align-items: center;
  gap: 9px;
  cursor: pointer;
  user-select: none;
}

.brand-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  background: #6366f1;
  color: #ffffff;
  font-size: 16px;
  box-shadow:
    0 5px 14px rgba(99, 102, 241, 0.22);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.brand:hover .brand-icon {
  transform:
    rotate(10deg)
    scale(1.08);
  box-shadow:
    0 8px 20px rgba(99, 102, 241, 0.32);
}

.brand-text {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.brand-name {
  color: #252932;
  font-size: 17px;
  font-weight: 700;
}

.brand-ai {
  color: #6366f1;
  font-size: 11px;
  font-weight: 700;
}

/* Navigation */
.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 13px;
  border-radius: 9px;
  color: #737987;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;

  transition:
    color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}



.nav-item:hover {
  color: #4f46e5;
  background: #f5f6ff;
  transform: translateY(-1px);
}

.nav-icon {
  font-size: 14px;

  transition:
      transform 0.2s ease;
}

.nav-item:hover .nav-icon {
  transform: scale(1.15);
}

.nav-item.router-link-active {
  color: #4f46e5;
  background: #f0f1ff;
  font-weight: 600;
}

.nav-item.router-link-active::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -1px;
  width: 20px;
  height: 2px;
  transform: translateX(-50%);

  border-radius: 999px;

  background: #6366f1;

  box-shadow:
    0 0 8px rgba(99, 102, 241, 0.5);
}

@media (max-width: 760px) {

  .navbar-container {
    width: calc(100% - 24px);
  }

  .nav-item {
    padding: 8px 9px;
  }

  .nav-item span:last-child {
    display: none;
  }

  .nav-icon {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .brand-ai {
    display: none;
  }

  .nav-links {
    gap: 1px;
  }

  .nav-item {
    padding: 8px;
  }
}

</style>