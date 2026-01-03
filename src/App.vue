<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <h1>雙北防災資源分析系統</h1>
        <p>Taipei & New Taipei Disaster Resource Analysis Dashboard</p>
        <nav class="nav-tabs">
          <router-link to="/" class="nav-tab" active-class="active">總覽 Overview</router-link>
          <router-link to="/aed" class="nav-tab" active-class="active">AED 分析</router-link>
          <router-link to="/shelter" class="nav-tab" active-class="active">避難收容處所</router-link>
          <router-link to="/air-raid" class="nav-tab" active-class="active">防空疏散設施</router-link>
          <router-link to="/tourist" class="nav-tab" active-class="active">景點周邊資源</router-link>
          <router-link to="/comparison" class="nav-tab" active-class="active">雙北比較</router-link>
        </nav>
      </div>
    </header>

    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
