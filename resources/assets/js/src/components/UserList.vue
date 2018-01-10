<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex>
        <v-card>

        </v-card>
      </v-flex>
    </v-layout>
    <v-layout column align-center>
      <img src="../assets/logo.png" alt="Vuetify.js" class="mb-5"/>
      <blockquote>
        &#8220;First, solve the problem. Then, write the code.&#8221;
        <footer>
          <small>
            <em>&mdash;John Johnson</em>
          </small>
        </footer>
      </blockquote>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'hello',
    data () {
      return {
        msg: 'Welcome to Your Vue.js App',
        usersData: {},
        gradesData: {}
      }
    },
    mounted () {
      console.log('mounted')
      axios.get('/api/users/')
        .then((response) => {
          // console.log(response)
          this.usersData = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .hello {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }

  .wrapper {
    padding: 20px 40px;
    border: 1px solid #c0c0c0;
    max-width: 400px;
    margin: 0 auto;
    background: orange;
  }
</style>
