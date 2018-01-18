import Vue from 'vue'
import Router from 'vue-router'
import UserList from '../components/UserList'
import UserHome from '../components/UserHome'
import NoteDetail from '../components/NoteDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'UserList',
      component: UserList
    },
    {
      path: '/note/user/:username/',
      name: 'user',
      component: UserHome
    },
    {
      path: '/note/:noteId/',
      name: 'note',
      component: NoteDetail
    }
  ]
})
