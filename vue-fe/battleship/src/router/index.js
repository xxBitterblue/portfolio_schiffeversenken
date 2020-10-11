import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home'
import Game from '../components/Game/Game'
import Lobby from '../components/Lobby'
import EndScreen from '../components/Game/EndScreen'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/game',
    name: 'Game',
    component: Game
  },
  {
    path: '/lobby',
    name: 'Lobby',
    component: Lobby
  },
  {
    path: '/endscreen/:winnerId',
    name: 'EndScreen',
    component: EndScreen,
    props: true
  } 
]

const routerHistory = createWebHistory()

const router = createRouter({
  history: routerHistory,
  routes
})

export default router