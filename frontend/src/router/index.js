import { createRouter, createWebHistory } from "vue-router"

import Home from "../views/Home.vue"
import Planner from "../views/Planner.vue"
import History from "../views/History.vue"
import Knowledge from "../views/Knowledge.vue"
import About from "../views/About.vue"


const router = createRouter({

  history: createWebHistory(),

  routes: [

    {
      path: "/",
      component: Home
    },

    {
      path: "/planner",
      component: Planner
    },

    {
      path: "/history",
      component: History
    },

    {
      path: "/knowledge",
      component: Knowledge
    },

    {
      path: "/about",
      component: About
    }

  ]

})


export default router