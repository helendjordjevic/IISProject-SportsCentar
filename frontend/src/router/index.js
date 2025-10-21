import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import TrainingDetailView from '../views/TrainingDetailView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ProfileView from '../views/ProfileView.vue';
import AddSessionView from '@/views/AddSessionView.vue';
import WeeklyReportView from '@/views/WeeklyReportView.vue';


import { store } from '@/main'; 

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/training/:id',  // ruta za detalje jednog treninga
    name: 'trainingDetail',
    component: TrainingDetailView,
    props: true   // omogućava da parametar id ide u komponentu kao prop
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/trainings/:trainingId/add-session',
    name: 'addSession',
    component: AddSessionView
  },
  {
    path: '/weekly-report',
    name: 'weeklyReport',
    component: WeeklyReportView
  },
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.state.isLoggedIn;

  if ((to.name === 'login' || to.name === 'register') && isLoggedIn) {
    next({ name: 'home' }); // redirect na home ako je već ulogovan
  } else {
    next(); // nastavi normalno
  }
});

export default router;
