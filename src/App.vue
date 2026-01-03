<template>
  <div id="app">
    <header class="header">
      <div class="container">
        <h1>雙北防災資源分析系統</h1>
        <p>Taipei & New Taipei Disaster Resource Analysis Dashboard</p>
        <nav class="nav-tabs">
          <router-link to="/" class="nav-tab" active-class="active">總覽 Overview</router-link>
          <router-link to="/topic1" class="nav-tab" active-class="active">Topic 1: 區域人口與防災資源比</router-link>
          <router-link to="/topic2" class="nav-tab" active-class="active">Topic 2: 避難所人均面積</router-link>
          <router-link to="/topic3" class="nav-tab" active-class="active">Topic 3: 景點周遭距離</router-link>
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
