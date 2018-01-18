<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex xs9npm install vue-quill-editor --save>
        <v-data-table
          v-bind:headers="headers"
          :items="getTableData"
          hide-actions
          disable-initial-sort
          class="elevation-1"
        >
          <template slot="items" slot-scope="props">
            <td>{{ props.item.year }}</td>
            <td class="text-xs-left">
              <ul>
                <li v-for="user in props.item.b4">
                  <v-avatar size="20px" style="background-color: rgba(0,0,0,0.2)">
                    <img v-if="user.thumbnail !== null" v-bind:src="user.thumbnail"/>
                    <v-icon v-else>account_circle</v-icon>
                  </v-avatar>&nbsp;
                  <router-link :to="{ name: 'user', params: { username: user.username }}">
                    {{ user.last_name + user.first_name }}
                  </router-link>
                </li>
              </ul>
            </td>
            <td class="text-xs-left">
              <li v-for="user in props.item.m1">
                <v-avatar size="20px" style="background-color: rgba(0,0,0,0.2)">
                  <img v-if="user.thumbnail !== null" v-bind:src="user.thumbnail"/>
                  <v-icon v-else>account_circle</v-icon>
                </v-avatar>&nbsp;
                <router-link :to="{ name: 'user', params: { username: user.username }}">
                  {{ user.last_name + user.first_name }}
                </router-link>
              </li>
            </td>
            <td class="text-xs-left">
              <ul>
                <li v-for="user in props.item.m2">
                  <v-avatar size="20px" style="background-color: rgba(0,0,0,0.2)">
                    <img v-if="user.thumbnail !== null" v-bind:src="user.thumbnail"/>
                    <v-icon v-else>account_circle</v-icon>
                  </v-avatar>&nbsp;
                  <router-link :to="{ name: 'user', params: { username: user.username }}">
                    {{ user.last_name + user.first_name }}
                  </router-link>
                </li>
              </ul>
            </td>
            <td class="text-xs-left">
              <ul>
                <li v-for="user in props.item.teacher">
                  <v-avatar size="20px" style="background-color: rgba(0,0,0,0.2)">
                    <img v-if="user.thumbnail !== null" v-bind:src="user.thumbnail"/>
                    <v-icon v-else>account_circle</v-icon>
                  </v-avatar>&nbsp;
                  <router-link :to="{ name: 'user', params: { username: user.username }}">
                    {{ user.last_name + user.first_name }}
                  </router-link>
                </li>
              </ul>
            </td>
            <td class="text-xs-left">
              <ul>
                <li v-for="user in props.item.other">
                  <v-avatar size="20px" style="background-color: rgba(0,0,0,0.2)">
                    <img v-if="user.thumbnail !== null" v-bind:src="user.thumbnail"/>
                    <v-icon v-else>account_circle</v-icon>
                  </v-avatar>
                  <router-link :to="{ name: 'user', params: { username: user.username }}">
                    {{ user.last_name + user.first_name }}
                  </router-link>
                </li>
              </ul>
            </td>
          </template>
        </v-data-table>
      </v-flex>

      <v-flex xs3>
        <v-card>
          <v-card-title>
            <span class="headline">Tags</span>
          </v-card-title>
          <v-card-actions>
            <v-layout row wrap align-center>
              <v-chip outline v-for="(tag, i) in tagsData" :key="i">
                {{ tag.name }}
              </v-chip>
            </v-layout>
          </v-card-actions>
        </v-card>
      </v-flex>

    </v-layout>

  </v-container>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'user-list',
    data () {
      return {
        belongsData: [],
        tagsData: {},
        headers: [
          {text: 'Users', align: 'left', sortable: false, value: 'name'},
          {text: '学部4年次', align: 'center', sortable: false, value: 'b4'},
          {text: '修士1年次', align: 'center', sortable: false, value: 'm1'},
          {text: '修士2年次', align: 'center', sortable: false, value: 'm2'},
          {text: '教員', align: 'center', sortable: false, value: 'teacher'},
          {text: 'その他', align: 'center', sortable: false, value: 'other'}
        ]
      }
    },
    mounted: function () {
      console.log('mounted')
      axios.get('/api/tags/')
        .then((response) => {
          this.tagsData = response.data
        })
        .catch((error) => {
          console.log(error)
        })
      axios.get('/api/belongs/')
        .then((response) => {
          this.belongsData = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },
    computed: {
      getTableData: function () {
        let data = []
        let addedList = []
        let belongs = this.belongsData
        for (let belong of belongs) {
          let user = belong.user
          let year = new Date(belong.start).getFullYear()
          let key
          if (addedList.indexOf(year) >= 0) {
            for (let j in data) {
              if (data[j].year === year) {
                key = j
              }
            }
          } else {
            data.push({year: year, b4: [], m1: [], m2: [], teacher: [], other: []})
            addedList.push(year)
            key = data.length - 1
          }
          if (belong.grade.name === 'B4') {
            data[key].b4.push(user)
          } else if (belong.grade.name === 'M1') {
            data[key].m1.push(user)
          } else if (belong.grade.name === 'M2') {
            data[key].m2.push(user)
          } else if (belong.grade.name === 'Teacher') {
            data[key].teacher.push(user)
          } else {
            data[key].other.push(user)
          }
        }
        data.sort((a, b) => b.year - a.year)
        return data
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  ul {
    list-style-type: none;
    padding-top: 5px;
  }

  li {
    list-style: none;
    vertical-align: middle;
    padding-bottom: 5px;
  }

  a {
    color: #42b983;
  }

  a:visited {
    color: #8e8c84;
  }

  a:hover {
    color: #fff;
    background-color: #0c3;
  }
</style>
