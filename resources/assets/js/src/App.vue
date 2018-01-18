<template>
  <v-app :dark="dark">

    <v-dialog v-model="loginDialog" persistent max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">Login</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field v-model="username" label="Username" required/>
              </v-flex>
              <v-flex xs12>
                <v-text-field v-model="password" label="Password" type="password" required/>
              </v-flex>
            </v-layout>
          </v-container>
          <small>{{ loginMessage }}</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn color="blue darken-1" flat @click.native="loginDialog = false">Close</v-btn>
          <v-btn round color="primary" @click.native="loginUser(username, password)">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="logoutDialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Log out</v-card-title>
        <v-card-text>Are you sure you want to log out?</v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn color="green darken-1" flat @click.native="logoutDialog = false">Close</v-btn>
          <v-btn round color="error" @click.native="logoutUser">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <v-navigation-drawer
      fixed
      :mini-variant="miniVariant"
      v-model="drawer"
      app
    >
      <v-toolbar flat class="transparent">
        <v-list class="pa-0">
          <v-list-tile avatar>
            <v-list-tile-avatar @click.stop="drawer = !drawer" class="avatar--tile">
              <img src="./assets/shark_logo_1.png"/>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>NAL LAB Note</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-toolbar>

      <v-list>
        <v-divider/>

        <v-list-tile
          v-if="login"
          value="true"
          v-for="(item, i) in loginItems"
          :key="i"
          @click="item.func"
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"/>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile
          v-if="!login"
          value="true"
          v-for="(item, i) in logoutItems"
          :key="i"
          @click="item.func"
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"/>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider/>
        <v-list-tile @click.stop="changeDark">
          <v-list-tile-action>
            <v-btn icon>
              <v-icon>visibility</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Night mode</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile @click.stop="changeMiniDrawer">
          <v-list-tile-action>
            <v-btn icon>
              <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"/>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Minimize drawer</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>


      </v-list>
    </v-navigation-drawer>

    <v-toolbar fixed app :clipped-left="clipped">
      <v-toolbar-side-icon @click.stop="drawer = !drawer"/>
      <v-toolbar-title>
      </v-toolbar-title>
      <v-layout row justify-space-around align-center style="max-width: 650px">
        <img style="height: 30px" src="./assets/shark_logo_2.png"/>&nbsp;&nbsp;&nbsp;
        <v-text-field
          v-model="keyword"
          placeholder="Search..."
          single-line
          append-icon="search"
          :append-icon-cb="() => {}"
          class="white--text"
          hide-details
        />
      </v-layout>
      <v-spacer/>
      <v-avatar v-if="thumbnailUrl !== null && login" size="40px" style="background-color: rgba(0,0,0,0.2)"><img
        v-bind:src="thumbnailUrl"/></v-avatar>
      <v-btn round color="primary" v-if="login">
        <v-icon>mode_edit</v-icon>
        new
      </v-btn>
      <v-btn icon v-if="!login" @click="loginDialog=true">
        <v-icon>account_circle</v-icon>
      </v-btn>
    </v-toolbar>

    <v-content>
      <v-slide-y-transition mode="out-in">
        <router-view/>
      </v-slide-y-transition>
    </v-content>

    <v-footer :fixed="false" app>
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
  import axios from 'axios'

  export default {
    data () {
      return {
        token: null,
        login: false,
        thumbnailUrl: null,
        dark: false,
        clipped: false,
        drawer: false,
        loginDialog: false,
        logoutDialog: false,
        loginMessage: '*indicates required field',
        username: null,
        password: null,
        keyword: null,
        loginItems: [
          {icon: 'dashboard', title: 'Top', func: function () {}},
          {icon: 'home', title: 'Home', func: function () {}},
          {icon: 'launch', title: 'Log out', func: this.showLogoutDialog},
          {icon: 'rss_feed', title: 'RSS', func: function () {}}
        ],
        logoutItems: [
          {icon: 'dashboard', title: 'Top', func: function () {}},
          {icon: 'exit_to_app', title: 'Log in', func: this.showLoginDialog},
          {icon: 'rss_feed', title: 'RSS', func: function () {}}
        ],
        miniVariant: false
      }
    },
    beforeMount: function () {
      this.$cookie.get('dark')
      this.$cookie.get('miniVariant')
      this.$cookie.get('token')
      this.$cookie.get('thumbnailUrl')
    },
    methods: {
      loginUser: function (username, password) {
        axios.post('/api/auth/login/', {
          username: username,
          password: password
        }).then((res) => {
          this.token = res.data['token']
          this.login = true
          this.$cookie.set('token', this.token, 7)
          this.$cookie.set('login', this.login, 7)
          axios.get('/api/user/' + username + '/')
            .then((res) => {
              this.thumbnailUrl = res.data['thumbnail']
              this.$cookie.set('thumbnailUrl', this.thumbnailUrl, 7)
            })
            .catch((error) => {
              this.loginMessage = error
            })
          this.loginDialog = false
        })
      },
      logoutUser: function () {
        this.login = false
        this.token = null
        this.thumbnailUrl = null
        this.username = null
        this.password = null
        this.logoutDialog = false
      },
      showLoginDialog: function () {
        this.loginDialog = true
      },
      showLogoutDialog: function () {
        this.logoutDialog = true
      },
      changeDark: function () {
        this.dark = !this.dark
        this.$cookie.set('dark', this.dark, 7)
      },
      changeMiniDrawer: function () {
        this.miniVariant = !this.miniVariant
        this.$cookie.set('miniVariant', this.miniVariant, 7)
      }
    }
  }
</script>

