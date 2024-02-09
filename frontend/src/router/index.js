/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Početna stranica',
      component: () => import('../pages/index.vue')
    },
    {
      path: '/login',
      name: 'Prijava',
      component: () => import('../pages/login.vue')
    },
    {
      path: '/register',
      name: 'Registracija',
      component: () => import('../pages/register.vue')
    },
    {
      path: '/dashboard',
      name: 'Korisnički panel',
      component: () => import('../pages/dashboard.vue')
    },
    {
      path: '/patient',
      name: 'Profil pacijenta',
      component: () => import('../pages/patient/index.vue'),
      children: [
        {
          path: '/create',
          name: 'Kreiraj profil',
          component: () => import('../pages/patient/create.vue')
        },
        {
          path: '/update',
          name: 'Ažuriraj profil',
            component: () => import('../pages/patient/update/index.vue'),
          children: [
            {
              path: '/email',
              name: 'Ažuriraj email',
              component: () => import('../pages/patient/update/email.vue')
            },
            {
              path: '/password',
              name: 'Ažuriraj lozinku',
              component: () => import('../pages/patient/update/password.vue')
            }
          ]
        }
      ]
    },
    {
      path: '/doctor',
      name: 'Profil doktora',
      component: () => import('../pages/doctor/index.vue'),
      children: [
        {
            path: '/create',
            name: 'Kreiraj profil',
            component: () => import('../pages/doctor/create.vue')
        },
        {
          path: '/update',
          name: 'Ažuriraj profil',
          component: () => import('../pages/doctor/update/index.vue'),
          children: [
            {
              path: '/email',
              name: 'Ažuriraj email',
              component: () => import('../pages/doctor/update/email.vue')
            },
            {
              path: '/password',
              name: 'Ažuriraj lozinku',
              component: () => import('../pages/doctor/update/password.vue')
            }
          ]
        }
      ]
    },
    {
      path: '/patients',
      name: 'Pacijenti',
      component: () => import('../pages/patients.vue')
    },
    {
      path: '/doctors',
      name: 'Doktori',
      component: () => import('../pages/doctors.vue')
    },
    {
      path: '/appointments',
      name: 'Pregledi',
      component: () => import('../pages/appointments/index.vue'),
      children: [
        {
          path: '/create',
          name: 'Zakaži pregled',
          component: () => import('../pages/appointments/create.vue')
        }
      ]
    },
  ]
})

router.onError((error, to) => {
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    window.location = to.fullPath
  }
})

export default router
