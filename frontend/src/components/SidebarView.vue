<template>
  <v-navigation-drawer app>
    <v-list dense>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            <div class = "sandbox" >
                AI Sandbox
            </div>
            
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

                <v-list-item-group v-model="activeItem">
                    <v-list-item
                    v-for="item in items"
                    :key="item.title"
                    :class="{ 'active-item': isActive(item.route) }"
                    @click="navigate(item.route)"
                    :to="item.route"
                    >
                    <!-- <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item-content> -->

                    <div>    
                        <section  >
                            <img :src="item.icon" alt="icon" class="emoji-icon">
                        
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </section>     
                    </div>
                    </v-list-item>
                </v-list-item-group>
    </v-list>

    <v-divider></v-divider>
    
  </v-navigation-drawer>
</template>

<script>



export default {
  data() {
    return {
      items: [
        { title: 'Home', icon: require('@/assets/icons/home.png'), route: '/' },
        { title: 'AI Tools', icon: require('@/assets/icons/tools.png'), route: '/tools' },
        { title: 'Activities', icon: require('@/assets/icons/activities.png'), route: '/activities' },
        { title: 'Feedback', icon: require('@/assets/icons/feature.png'), route: '/feedback' },
      ],
    };
  },
  methods: {
    navigate(route) {
      this.$router.push(route);
    },
    isActive(route) {
      return this.$route.path === route;
    }
  }
};
</script>

<style scoped>
.logo {
  width: 100px;
  margin: 0 auto;
  display: block;
}
.title{
    margin-top: 20px;
    margin-bottom: 20px;
    
}
.sandbox{
    margin-left: 30px;
    margin-right: 20px; 
    font-size: 35px;
}
section {
  display: flex;
}


.emoji-icon {
  margin-left: 16px;
  margin-right: 14px;
  width: 24px;
  height: 24px;
}
.active-item {
  background-color: #f0f0f0; /* Change to desired active color */
}
</style>